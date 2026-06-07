---
title: 20_Hook系统
aliases:
  - Hook系统
  - 钩子系统
  - Learn Claude Code 20
tags:
  - LearnClaudeCode
  - Agent
  - hook
  - extensibility
  - course-forge
source: https://www.bilibili.com/video/BV1rEQpBFELa
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. Hook 是什么？
> 2. Hook 和生命周期、中间件、模板方法有什么共同点？
> 3. 本节代码提供了哪三个 Hook event？
> 4. `run_hooks` 的基本流程是什么？
> 5. 为什么运行 Hook 前要检查 workspace trust？
> 6. matcher 如何决定 Hook 是否运行？
> 7. `blocked` 和 `messages` 在 Hook 输出里有什么作用？

> [!abstract] 核心主线
> Hook 是固定主流程中的扩展口：不修改 Agent loop 主体，也能在关键时机插入自定义逻辑。本节实现了三个 Hook：`session_start` 在会话开始时触发，`pre_tool_use` 在工具执行前触发，`post_tool_use` 在工具执行后触发。配置来自 `.hooks.json`。`run_hooks` 会先检查 workspace trust，再根据 event 找到对应 Hook 列表，用 matcher 判断是否匹配当前工具，把 event、tool name、tool input、tool output 注入环境变量，然后执行 command。Hook 输出可以用于日志、上下文补充，也可以在 pre hook 中设置 `blocked=true` 阻止工具执行。

## 概念精讲

### Hook 的直觉

Hook 就是主流程中的预留扩展点。

框架把整体流程固定下来，但在关键节点留下口子，让你插入自定义逻辑，而不用修改主流程源码。

常见类比：

- Vue / React 生命周期。
- Android Activity 生命周期。
- 测试框架的 setup / teardown。
- Web 框架 middleware。
- 模板方法模式里的抽象步骤。

> [!abstract] 一句话
> Hook = 固定主流程 + 关键节点扩展口。

## 本节三个 Hook event

| Hook | 触发时机 | 典型用途 |
|---|---|---|
| `session_start` | 会话开始时 | 加载配置、记录启动、注入初始上下文 |
| `pre_tool_use` | 工具执行前 | 检查、阻止、改写、记录即将执行的操作 |
| `post_tool_use` | 工具执行后 | 记录结果、上报可观测性、补充上下文 |

示例配置：

```json
{
  "session_start": [
    {"command": "echo session start ok"}
  ],
  "pre_tool_use": [
    {"matcher": "bash", "command": "echo before bash"}
  ],
  "post_tool_use": [
    {"matcher": "*", "command": "echo post tool use ok"}
  ]
}
```

## `run_hooks` 运行流程

1. 创建默认结果：

```python
result = {"blocked": False, "messages": []}
```

2. 检查 workspace trust。
3. 根据 event 取出 hooks。
4. 用 matcher 判断是否匹配当前工具。
5. 把 context 注入环境变量。
6. 执行 hook command。
7. 解析输出并合并到 result。

## workspace trust

Hook 可以执行本地命令，所以必须检查工作区是否可信。

视频调试里，如果缺少类似 `.claude/.claude_trusted` 的标记文件，Hook 不会运行。

> [!warning] Hook 能执行命令
> 不可信项目里的 `.hooks.json` 如果能直接运行命令，会产生安全风险。

## matcher

matcher 决定 Hook 是否适用于当前工具：

- `matcher="bash"`：只匹配 Bash。
- `matcher="read_file"`：只匹配读文件。
- `matcher="*"`：匹配所有工具。

不匹配就 continue，不执行该 Hook。

## 环境变量上下文

Hook command 可以通过环境变量拿到上下文：

```text
HOOK_EVENT
HOOK_TOOL_NAME
HOOK_TOOL_INPUT
HOOK_TOOL_OUTPUT
```

`HOOK_TOOL_OUTPUT` 通常会截断，例如只取前 10000 字符，避免输出过大。

## Hook 输出

如果 Hook 输出普通文本，可以作为日志或消息。

如果 Hook 输出结构化 JSON，可以包含：

```json
{
  "blocked": true,
  "messages": [
    "This command was blocked by pre_tool_use hook."
  ]
}
```

含义：

- `blocked=true`：阻止后续工具执行，通常用于 `pre_tool_use`。
- `messages`：补充信息，可注入到模型上下文或工具结果。

## Hook 的工程价值

Hook 体现开闭原则：

- 对主循环修改关闭。
- 对扩展逻辑开放。

可以用来做：

- 日志记录。
- 安全检查。
- 可观测性上报。
- 会话开始加载配置。
- 工具执行后写入记忆。
- 工具执行前阻止敏感路径。
- 会话结束时压缩上下文。

## 判断与行动清单

> [!todo] 设计 Hook 系统前先检查
> - [ ] 主流程中是否明确预留 event。
> - [ ] Hook 配置是否独立于主循环。
> - [ ] 是否检查 workspace trust。
> - [ ] 是否支持 matcher。
> - [ ] 是否把上下文传给 Hook。
> - [ ] 是否限制输出大小。
> - [ ] 是否支持 `blocked`。
> - [ ] 是否支持补充 `messages`。
> - [ ] Hook 执行失败是否不会破坏主流程。
> - [ ] 是否记录 Hook 执行日志。

## 应用与迁移问答

> [!question] Hook 和权限系统有什么关系？
> 权限系统是内置安全决策；Hook 可以在工具前后额外插入检查、阻断或记录。两者都属于执行前后的治理层。

> [!question] Hook 是否应该修改主循环？
> 不应该。Hook 的价值就是在不改主循环的情况下扩展行为。

> [!question] post_tool_use 为什么适合做记忆？
> 因为它能拿到工具执行结果，可以把重要结果摘要写入长期记忆或审计日志。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 把 Hook 理解成随便插代码。
> - 忘记 Hook 是主流程预留的扩展点。
> - 不检查 workspace trust 就执行命令。
> - matcher 不匹配时还运行 Hook。
> - pre hook blocked 后仍然执行工具。
> - post hook 输出没有回填到模型上下文。
> - 每个新需求都改主循环，而不是挂 Hook。

## 费曼解释润色版

> [!quote]
> Hook 系统的核心是：主流程保持稳定，在关键节点留下扩展口。Learn Claude Code 这一节有三个 Hook：`session_start` 在会话开始时运行，`pre_tool_use` 在工具执行前运行，`post_tool_use` 在工具执行后运行。配置写在 `.hooks.json` 里。系统调用 `run_hooks` 时，先检查 workspace trust，避免不可信项目直接执行本地命令；然后根据 event 找到 Hook 列表，用 matcher 判断是否匹配当前工具；匹配后把 event、tool name、tool input、tool output 写入环境变量，再执行 Hook command。Hook 输出可以是普通日志，也可以是 JSON。如果 pre hook 返回 `blocked=true`，工具就不执行；如果返回 messages，系统可以把这些信息补进模型上下文。这样不用改 Agent loop，也能扩展日志、安全检查、可观测性、记忆写入和上下文增强。

## 易错卡片

> [!warning] 误区：Hook 就是往主循环里继续加代码
> 正确说法：Hook 是为了少改主循环，把扩展逻辑放到预留事件上。

> [!warning] 误区：Hook 配置可以在任何目录无条件运行
> 正确说法：应该先检查 workspace trust。

> [!warning] 误区：post hook 只能打印日志
> 正确说法：post hook 还能补充上下文、写入记忆、上报结果。

> [!warning] 误区：pre hook 不能影响工具执行
> 正确说法：pre hook 可以通过 `blocked=true` 阻止工具执行。
