---
title: 06_子Agent与任务委托
aliases:
  - 子Agent与任务委托
  - Learn Claude Code 06
tags:
  - LearnClaudeCode
  - Agent
  - sub-agent
  - delegation
  - learning-kit
source: https://www.bilibili.com/video/BV1R6crzFERf
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. 子 Agent 为什么可以理解成 `task` 工具？
> 2. `description` 和 `prompt` 分别承担什么作用？
> 3. `run_sub_agent` 为什么要创建新的 `sub_messages`？
> 4. 为什么子 Agent 最多只跑有限轮，例如 30 轮？
> 5. 为什么父 Agent 只接收最终 text，而不是完整子上下文？
> 6. 为什么 `child_tools` 里通常不包含 `task`？

> [!abstract] 核心主线
> 子 Agent 的工程本质是任务委托。父 Agent 的工具列表里有 `task`，模型按 schema 生成 `description` 和 `prompt`，本地代码把这次工具调用交给 `run_sub_agent`。子 Agent 会创建独立的 `sub_messages`，用受限的 `child_tools` 在最多 30 轮内完成任务。结束时，父 Agent 只收到最终文本结果，子 Agent 的中间上下文被丢弃。这样既能减少父上下文压力，也能通过工具集限制子 Agent 的权限。

## 概念精讲

### 子 Agent 是一种工具化委托

本节里的子 Agent 不是独立的新应用，也不是模型隐藏思考。父 Agent 看到的是一个普通工具：`task`。模型选择调用 `task`，就像选择调用 `read_file` 或 `bash` 一样。

区别在于，`task` 的执行不是一次简单函数，而是开启一个新的 Agent 循环。这个循环在本地实现中由 `run_sub_agent` 管理。

判断句：子 Agent 在父级视角里是工具调用，在本地实现里是一段独立 Agent loop。

### `description` 和 `prompt`

`task` 工具通常有两个关键参数：

| 字段 | 含义 | 写作要求 |
|---|---|---|
| `description` | 委托任务短标签 | 简短说明任务类型 |
| `prompt` | 真正交给子 Agent 的任务说明 | 写清目标、范围、限制、输出格式 |

```json
{
  "name": "task",
  "input": {
    "description": "Summarize Python files",
    "prompt": "读取当前项目中的所有 Python 文件，按文件名列出每个文件的核心职责。只总结职责，不要修改文件。"
  }
}
```

如果 `prompt` 只写“帮我看看项目”，子 Agent 很难知道要看什么、输出什么、能不能修改文件。

### `run_sub_agent` 创建独立上下文

子 Agent 的第一步是创建新的 `sub_messages`。它不是父 Agent 的 `messages` 原地复用，而是子任务自己的工作台。

```python
def run_sub_agent(prompt: str) -> str:
    sub_messages = [{"role": "user", "content": prompt}]

    for _ in range(30):
        response = call_model(
            messages=sub_messages,
            tools=child_tools,
        )
        sub_messages.append(response)

        if response_has_tool_use(response):
            result = execute_child_tool(response)
            sub_messages.append(result)
            continue

        return final_text(response)
```

这个循环和主 Agent loop 很像，但边界更清楚：它使用 `child_tools`，并且最多只跑有限轮。

## 关键机制

### 只返回最终 text

视频里强调：子 Agent 可能已经与模型交互七八次，但父 Agent 不需要知道完整过程。`run_sub_agent` 最终只返回最后一次 response 里的文本内容。

父 Agent 的 messages 大致只看到：

1. 用户原始任务。
2. 父模型调用 `task`。
3. `task` 工具返回的最终结果。

这样主上下文保持短，父 Agent 后续只需要理解压缩后的结果，而不是被子任务的所有中间探索淹没。

### 子上下文会被丢弃

这里的 context 可以粗略理解为 `sub_messages`。它包含子 Agent 的中间工具调用、读取结果、失败尝试和修正路径。

这些内容不整段追加回父 Agent。否则子 Agent 的意义会被抵消：父上下文仍然会变得很重。

> [!warning] 误区
> 子 Agent 不是把父 Agent 的上下文扩大一圈，而是把一段子任务的探索隔离出去，再把结果压缩回来。

### `child_tools` 是权限收缩

父 Agent 可以有 `task`，但子 Agent 通常不应该有 `task`。如果子 Agent 也能继续调用 `task`，任务委托就可能无限递归，变成难以审计的层层外包。

更一般地，子 Agent 应该只拿完成任务所需的最小工具集：

- 只读总结任务：给 read/search，通常不给 write/edit。
- 修复代码任务：可给 edit，但仍要限制范围。
- 外部系统任务：谨慎给权限，避免误操作。

## 判断与行动清单

> [!todo] 设计子 Agent 前先检查
> - [ ] 这个任务是否足够独立，值得委托。
> - [ ] `description` 是否能概括任务。
> - [ ] `prompt` 是否写清目标、范围、限制和输出格式。
> - [ ] 子 Agent 是否使用独立 `sub_messages`。
> - [ ] 子循环是否有轮数上限。
> - [ ] `child_tools` 是否只包含必要工具。
> - [ ] `child_tools` 是否避免包含 `task`。
> - [ ] 父 Agent 是否只接收最终 text。

## 应用与迁移问答

> [!question] 什么时候适合委托给子 Agent？
> 当任务相对独立、可能消耗多轮工具调用、但父 Agent 只需要最终结论时，适合委托。比如扫描一批文件、整理某类资料、做局部排查。

> [!question] 什么时候主 Agent 直接做更好？
> 如果任务很短，只需要一两次工具调用，或者必须与当前父级推理紧密交错，直接做更简单。

> [!question] 为什么子 Agent 不能无限运行？
> 子 Agent 可能陷入循环、反复调用工具或始终找不到答案。轮数上限让它有明确边界，避免子任务失控。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 把子 Agent 当成另一个永久在线的主 Agent。
> - 忘记 `task` 是父 Agent 的工具调用。
> - 把 `sub_messages` 误认为父 `messages`。
> - 把子 Agent 的完整上下文追加回父级。
> - 给子 Agent 和父 Agent 完全一样的工具。
> - 让子 Agent 也拥有 `task`，导致递归委托风险。
> - 委托 prompt 写得太空，导致结果不可用。

## 费曼解释润色版

> [!quote]
> 子 Agent 可以理解成父 Agent 的一种任务委托工具。父 Agent 通过 `task` 发起委托，参数里用 `description` 简短标记任务，用 `prompt` 写清真正要做什么。本地代码收到 `task` 后进入 `run_sub_agent`，创建一个新的 `sub_messages`，让子 Agent 在自己的上下文里调用工具完成任务。这个子循环不会无限运行，通常会有 30 轮之类的上限。子 Agent 使用的是 `child_tools`，权限可以比父 Agent 更小，并且通常不包含 `task`，避免无限递归委托。任务结束后，父 Agent 只收到最终 text，而不是完整子上下文。这样父上下文保持短，后续推理更集中，同时子任务的权限也更容易控制。

## 易错卡片

> [!warning] 误区：子 Agent 会把所有中间消息并入父上下文
> 正确说法：父 Agent 只接收最终文本结果，子上下文会被丢弃。

> [!warning] 误区：子 Agent 的工具应该和父 Agent 一样
> 正确说法：子 Agent 应该使用最小必要工具集。

> [!warning] 误区：子 Agent 也能继续调用 `task`
> 正确说法：通常不应给子 Agent `task`，否则有递归委托风险。

> [!warning] 误区：`description` 和 `prompt` 随便写都行
> 正确说法：`prompt` 决定子 Agent 的任务边界和输出质量。
