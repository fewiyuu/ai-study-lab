---
title: 11_Agent团队与消息总线
aliases:
  - Agent团队与消息总线
  - 团队协作让Agent更强大
  - Learn Claude Code 11
tags:
  - LearnClaudeCode
  - Agent
  - multi-agent
  - message-bus
  - course-forge
source: https://www.bilibili.com/video/BV1YcQSB4EZ7
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. Agent team 的最小底座是什么？
> 2. `.teams/config.json` 和 `.teams/inbox/*.jsonl` 分别保存什么？
> 3. `spawn_teammate` 如何创建队员？
> 4. lead loop 和 teammate loop 有哪些相同点和不同点？
> 5. 为什么 teammate 的工具集要裁剪？
> 6. `/tm` 和 `/inbox` 为什么不需要进入 LLM loop？

> [!abstract] 核心主线
> Agent team 的底座由成员管理和消息总线组成。TeammateManager 负责 `.teams/config.json`，记录 team name、members、角色和状态；MessageBus 负责 `.teams/inbox/{name}.jsonl`，用 JSONL 文件当每个 Agent 的收件箱。lead Agent 可以调用 `spawn_teammate(name, role, prompt)` 创建队员，并启动独立 teammate loop。每个 loop 开始时都会读取自己的 inbox，把消息注入 messages 后再请求模型。lead 和 teammate 的主要区别是 system prompt、工具集和循环上限；teammate 工具集必须裁剪，避免无限生成新队员。

## 概念精讲

### Agent team 不是多开几个模型

多 Agent 协作至少需要两个基础设施：

- 成员状态：谁在团队里，角色是什么，状态是什么。
- 通信通道：成员之间如何发送和读取消息。

本节用文件系统实现：

```text
.teams/
  config.json
  inbox/
    lead.jsonl
    alice.jsonl
```

### MessageBus：文件邮箱

每个 Agent 有自己的 inbox 文件。发给 lead 的消息写入 `lead.jsonl`；发给 Alice 的消息写入 `alice.jsonl`。

消息是一行 JSON：

```json
{"type":"message","from":"alice","content":"Hi, I am Alice, a coder.","timestamp":"2026-03-25T...Z"}
```

读取 inbox 后会清空文件。这和后台任务的 drain notification 类似：取出消息并清空，避免重复注入。

### TeammateManager：成员配置

`.teams/config.json` 保存团队成员：

```json
{
  "team_name": "default",
  "members": [
    {"name": "alice", "role": "coder", "status": "idle"}
  ]
}
```

`spawn_teammate` 接收三个参数：

| 参数 | 含义 |
|---|---|
| `name` | 队员名字，例如 Alice |
| `role` | 队员角色，例如 coder |
| `prompt` | 队员自己的任务说明 |

创建队员时，状态先设为 working；队员 loop 结束后，状态改为 idle 并保存回 config。

## 双 loop 对比

lead loop 和 teammate loop 很像：

1. 读取自己的 inbox。
2. 把 inbox 消息注入 messages。
3. 请求模型。
4. 执行 tool use。
5. 把工具结果写回 messages。

关键差异：

| 维度 | lead loop | teammate loop |
|---|---|---|
| system prompt | team leader | 角色专属 prompt |
| inbox | `lead.jsonl` | `alice.jsonl` 等 |
| 工具集 | 更完整，可 spawn/list/send/read | 裁剪后的 teammate tools |
| 循环 | 主交互循环可持续 | 有限轮，例如 50 轮 |
| 状态 | 主控 | working → idle |

> [!warning] 工具裁剪很关键
> teammate 不应该拥有和 lead 完全相同的工具。如果 Alice 也能 `spawn_teammate`，就可能继续生成更多队员，形成无限外包。

## 消息流示例

用户让 lead 生成 Alice，并让 Alice 给 lead 发消息：

1. lead 调用 `spawn_teammate`。
2. TeammateManager 把 Alice 写入 `config.json`，状态 working。
3. 系统启动 Alice 的 teammate loop 线程。
4. Alice 根据自己的 prompt 调用 `send_message`。
5. MessageBus 把消息写入 `.teams/inbox/lead.jsonl`。
6. lead 下一轮 loop 开头读取 `lead.jsonl`。
7. 消息被注入 lead 的 messages，然后文件被清空。
8. Alice loop 结束，状态改为 idle。

## Slash 命令

`/tm` 和 `/inbox` 是直接命令，不走 LLM：

- `/tm`：读取 config，显示团队成员和状态。
- `/inbox`：读取 lead inbox，显示消息并清空。

这样做更快、更稳定。查看系统状态不一定需要模型参与。

## 判断与行动清单

> [!todo] 设计 Agent team 前先检查
> - [ ] 是否有团队成员配置。
> - [ ] 是否有每个成员自己的 inbox。
> - [ ] 消息是否包含 type/from/content/timestamp。
> - [ ] 读取 inbox 后是否清空。
> - [ ] spawn 是否检查重复成员。
> - [ ] teammate 是否有独立 prompt。
> - [ ] teammate tools 是否被裁剪。
> - [ ] teammate loop 是否有轮数上限。
> - [ ] 成员状态是否保存回 config。

## 应用与迁移问答

> [!question] 为什么 inbox 用 JSONL？
> JSONL 适合一行一条消息，便于追加、读取和逐条解析。纯文本缺少结构，后续难以区分类型、发送者和内容。

> [!question] 为什么读取 inbox 后要清空？
> 否则同一条消息会在每轮都被读出来，反复注入 messages。

> [!question] Agent team 和子 Agent 有什么关系？
> 二者都涉及独立 loop 和工具裁剪。区别是子 Agent 更像一次任务委托，teammate 更像团队成员，有名称、状态和 inbox。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 以为 Agent team 只是多开几个模型。
> - 忘记成员状态要保存到 config。
> - 读取 inbox 后没有清空。
> - teammate 使用和 lead 完全相同的工具。
> - teammate loop 没有轮数上限。
> - 把 `/tm`、`/inbox` 误认为必须走 LLM。
> - 文件 inbox 并发写入没有保护。

## 费曼解释润色版

> [!quote]
> Agent team 的最小实现不是直接让多个模型聊天，而是先建立成员管理和消息总线。TeammateManager 负责 `.teams/config.json`，保存团队名、成员、角色和状态。MessageBus 负责 `.teams/inbox/{name}.jsonl`，每个 Agent 都有自己的文件邮箱。lead Agent 可以调用 `spawn_teammate` 创建 Alice，把她写入 config，并启动一个独立 teammate loop。Alice 的 loop 每轮也会读取自己的 inbox，再请求模型和执行工具。Alice 如果要给 lead 发消息，就调用 `send_message`，把一行 JSON 写到 `lead.jsonl`。lead 下一轮开始时读取自己的 inbox，把消息加入 messages，并清空文件。lead 和 teammate 的区别在于 prompt、工具集和循环边界；teammate 的工具集要裁剪，避免它继续无限生成新队员。

## 易错卡片

> [!warning] 误区：teammate 可以拥有 lead 的所有工具
> 正确说法：teammate tools 应该裁剪，尤其不应默认允许继续 spawn。

> [!warning] 误区：读取 inbox 不需要清空
> 正确说法：读取后清空才能避免消息重复进入上下文。

> [!warning] 误区：成员状态只在内存里改就行
> 正确说法：需要保存回 config，`/tm` 才能看到真实状态。

> [!warning] 误区：slash 命令也要走模型
> 正确说法：`/tm` 和 `/inbox` 是系统状态查询，直接处理更合适。
