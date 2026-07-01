---
title: 03_工具调用让Agent做事
aliases:
  - 工具调用让 Agent 做事
  - Learn Claude Code 03
tags:
  - LearnClaudeCode
  - Agent
  - tool-use
  - learning-kit
source: https://www.bilibili.com/video/BV1zGNGzhEKk
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. `tools` 列表到底告诉模型什么？
> 2. `stop_reason=tool_use` 和 `end_turn` 有什么区别？
> 3. 模型返回 `tool_use` 后，本地程序做了什么？
> 4. 为什么工具执行结果必须写回 messages？
> 5. 命令失败、无输出、被拦截时还要不要回写？
> 6. 为什么工具 schema 不能代替本地安全检查？

> [!abstract] 核心主线
> 工具调用让 Agent 从“只会聊天”变成“能做事”。请求模型时，本地程序把 `tools` 列表一起发过去；模型如果需要本地动作，会返回 `tool_use` block；本地代码读取 block 里的参数，调用对应 handler，例如 `run_bash(command)`；执行后的成功、失败或无输出结果会被包装成 `tool_result`，追加到 messages，再次发给模型。模型正是靠这些执行反馈决定下一步。

## 概念精讲

### tools 是能力说明

`tools` 列表告诉模型本地有哪些工具可以请求。它通常包含工具名、用途和输入参数结构。模型看到这个列表后，才可能返回 `tool_use`。

判断句：`tools` 不是执行结果，也不是本地函数本身，而是给模型看的能力说明。

### tool_use 是请求，不是执行

当 `response.stop_reason == "tool_use"` 时，模型在说：“我需要你调用某个工具。”这时本地程序要遍历 `response.content`，找到 `type == "tool_use"` 的 block，再读取它的 `input`。

```python
for block in response.content:
    if block.type == "tool_use":
        command = block.input["command"]
        output = run_bash(command)
```

模型没有直接执行 Bash。真正执行命令的是 `run_bash` 这样的本地 handler。

### tool_result 必须回写

工具执行结果必须作为新消息追加到 messages。下一次请求模型时，模型才能看到刚才发生了什么。

```python
messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": block.id,
        "content": output,
    }]
})
```

如果不回写结果，模型只知道自己请求过工具，却不知道工具成功、失败、无输出还是被安全拦截。

## 最小可操作样例

```python
response = client.messages.create(
    model=model,
    messages=messages,
    tools=tools,
)

messages.append({
    "role": "assistant",
    "content": response.content,
})

if response.stop_reason == "tool_use":
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            output = run_bash(block.input["command"])
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": output,
            })
    messages.append({"role": "user", "content": tool_results})
```

## 关键术语

| 术语 | 含义 | 容易混淆点 |
|---|---|---|
| `tools` | 给模型看的工具能力清单 | 不等于已经执行 |
| `tool_use` | 模型请求调用工具的 block | 请求不等于结果 |
| `tool_result` | 本地工具执行后的反馈 | 成功失败都要写回 |
| `run_bash` | 本地 Bash handler | 模型不直接执行 Bash |
| `tool_use_id` | 匹配请求和结果的 id | 丢失后模型难以对应 |

## 判断与行动清单

> [!todo] 处理一次 tool_use
> - [ ] 确认请求模型时传入了 `tools`。
> - [ ] 检查 `response.stop_reason` 是否为 `tool_use`。
> - [ ] 遍历 `response.content`，找到 `tool_use` block。
> - [ ] 读取工具名和 input 参数。
> - [ ] 在本地 handler 中做必要安全检查。
> - [ ] 执行工具并收集 stdout、stderr 或拦截原因。
> - [ ] 用 `tool_use_id` 包装成 `tool_result`。
> - [ ] 把 `tool_result` 追加进 messages。
> - [ ] 带着更新后的 messages 再次请求模型。

## 应用与迁移问答

> [!question] 为什么失败输出也要写回？
> 失败输出是环境反馈。模型看到“找不到文件”或“权限不足”后，才知道下一步要换路径、换命令或解释限制。

> [!question] messages 为什么会越来越长？
> 每次用户请求、assistant 响应、tool_result 都会进入 messages。连续工具调用会让 messages 依次变成 user、assistant tool_use、tool_result、assistant tool_use、tool_result。

> [!question] 简单危险命令拦截够安全吗？
> 不够。它只说明执行前应该有安全检查。生产级 Agent 还需要更完整的权限规则、路径限制、审批模式和审计记录。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 把 `tool_use` 当成已经执行完成。
> - 执行了命令，但忘记把结果追加到 messages。
> - 只回写成功输出，不回写失败输出。
> - 没有保存 `tool_use_id`，导致请求和结果对应不清。
> - 相信工具 schema 足够安全，没有在本地 handler 做检查。

## 费曼解释润色版

> [!quote]
> Agent 能做事，是因为请求模型时把可用工具列表发了过去。模型看到工具说明后，如果判断需要本地动作，就会返回 `tool_use` block，比如请求执行 Bash 命令。这个命令不是模型自己执行，而是本地程序取出参数后调用 `run_bash`。执行结果可能成功、失败、无输出或被安全拦截，这些都要包装成 `tool_result` 写回 messages。下一次模型请求会带着这些结果，所以模型才能知道刚才发生了什么，并决定继续调用工具还是结束回答。没有 `tool_result`，Agent 就会失去执行反馈，只能继续猜。

## 易错卡片

> [!warning] 误区：`tools` 会自动执行工具
> 正确说法：`tools` 只是告诉模型可请求哪些工具。

> [!warning] 误区：`tool_use` 就是工具结果
> 正确说法：`tool_use` 是请求，`tool_result` 才是执行反馈。

> [!warning] 误区：失败输出没必要回写
> 正确说法：失败输出能帮助模型调整下一步。

> [!warning] 误区：模型在执行 Bash
> 正确说法：本地 handler 执行 Bash，模型只提出请求。
