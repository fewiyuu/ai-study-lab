---
title: 02_消息历史与Agent循环
aliases:
  - 消息历史与 Agent 循环
  - Learn Claude Code 02
tags:
  - LearnClaudeCode
  - Agent
  - messages
  - course-forge
source: https://www.bilibili.com/video/BV1zTPszbEup
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. `history` 为什么是列表，而不是一段字符串？
> 2. 外层 `while True` 和 `agent_loop` 里的 `while True` 有什么区别？
> 3. 用户输入 `hello` 后，消息如何被包装？
> 4. `stop_reason=end_turn` 表示什么？
> 5. 为什么 `response.content` 要按 block 遍历？
> 6. 为什么本节暂时不讲 `tool_use`？

> [!abstract] 核心主线
> 本节只看一次不触发工具的 `hello` 对话。外层循环等待用户输入，把输入包装成 `role=user` 的消息并追加进 `history`；`agent_loop` 把整个 messages 发给模型，拿到 response 后追加 assistant 消息；当 `stop_reason` 是 `end_turn` 时，内层循环结束，外层循环从最后一条 assistant 消息的 content blocks 中找到 text 并打印。

## 概念精讲

### 两层循环

外层循环负责“多次用户输入”。只要用户不退出，程序就会继续等待下一条 prompt。

内层 `agent_loop` 负责“完成当前用户任务”。如果当前任务只需要模型回复文本，它一轮就结束；如果需要工具调用，后续章节会让它继续跑更多轮。

判断句：外层循环的单位是“下一条用户输入”，内层循环的单位是“当前任务完成前的模型轮次”。

### history 是消息列表

`history` 保存整个会话的消息。用户输入 `hello` 后，代码追加：

```python
{"role": "user", "content": "hello"}
```

`agent_loop` 返回后，`history` 通常会多出一条 assistant 消息。此时 `history[-1]` 指向最后一条消息，也就是模型刚刚返回的响应。

### assistant content 是 block 列表

模型响应的 `content` 不一定是普通字符串。本节调试时能看到 thinking block 和 text block。代码遍历 blocks，只打印有 `text` 属性的块。

```python
response_content = history[-1]["content"]

for block in response_content:
    if hasattr(block, "text"):
        print(block.text)
```

判断句：如果你直接把 `response.content` 当字符串打印，你还没有进入消息协议层。

## 最小可操作样例

```python
history = []

while True:
    query = input("> ")
    if query in ("q", "exit"):
        break

    history.append({"role": "user", "content": query})
    agent_loop(history)

    response_content = history[-1]["content"]
    for block in response_content:
        if hasattr(block, "text"):
            print(block.text)
```

`agent_loop` 的核心动作：

```python
response = client.messages.create(
    model=model,
    messages=messages,
    tools=tools,
)

messages.append({"role": "assistant", "content": response.content})

if response.stop_reason == "end_turn":
    return
```

## 关键术语

| 术语 | 含义 | 容易混淆点 |
|---|---|---|
| `history` | 会话消息列表 | 不是一段拼接后的聊天文本 |
| 外层循环 | 等待下一次用户输入 | 不负责处理工具链路 |
| `agent_loop` | 完成当前任务的内层循环 | 不等于整个程序循环 |
| `stop_reason` | 模型这一轮停止的原因 | `end_turn` 和 `tool_use` 后果不同 |
| content block | assistant 内容里的结构化块 | 不能一律当字符串 |

## 判断与行动清单

> [!todo] 调试一次 hello 对话
> - [ ] 在 `history = []` 附近确认初始列表。
> - [ ] 输入 `hello` 后观察 `query`。
> - [ ] 追加 user 后确认 `history` 有一条消息。
> - [ ] 进入 `agent_loop` 后观察模型 response。
> - [ ] 确认 `stop_reason` 是 `end_turn`。
> - [ ] 查看 `history[-1]["content"]` 里的 block 类型。
> - [ ] 找到 text block 并打印。

## 应用与迁移问答

> [!question] 第二次输入时，模型为什么能看到上一轮？
> 因为外层循环维护的是同一个 `history` 列表。上一轮的 user 和 assistant 消息没有被丢掉，第二次调用模型时会继续作为 messages 传入。

> [!question] 为什么 response 要先 append 再判断 `stop_reason`？
> 因为无论当前轮是否结束，模型刚才返回的内容都是会话历史的一部分。后续打印、工具处理或下一轮请求都依赖这条 assistant 消息。

> [!question] 为什么本节避开 `tool_use`？
> 先把无工具调用的一轮消息流看清楚，下一节再加入工具调用。如果一开始把 messages、blocks、stop_reason 和工具执行混在一起，调试时很容易分不清是谁改变了 history。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 把外层循环和 `agent_loop` 混成一个循环。
> - 忘记 `agent_loop` 修改的是传入的同一个 messages 列表。
> - 以为 assistant 的 content 是字符串。
> - 没有把 response 追加进 messages，就想从 `history[-1]` 读取回复。
> - 看到 thinking block 就想直接打印，而不是找 text block。

## 费曼解释润色版

> [!quote]
> 输入 `hello` 后，外层循环先拿到这段用户输入，并把它包装成一条 `role=user` 的消息追加进 `history`。然后程序把同一个 `history` 传给 `agent_loop`。`agent_loop` 把 messages 发给模型，拿到 response 后，把模型回复作为 assistant 消息追加回这个列表。因为这次只是普通问候，模型的 `stop_reason` 是 `end_turn`，说明当前轮不用工具，内层循环可以返回。回到外层后，代码取 `history[-1]["content"]`，遍历里面的 blocks，找到带 `text` 的块并打印。这样一次 hello 对话就完整走完了。

## 易错卡片

> [!warning] 误区：`history` 是字符串
> 正确说法：`history` 是消息列表，里面每条消息有 role 和 content。

> [!warning] 误区：两个 `while True` 是同一个东西
> 正确说法：外层等用户输入，内层完成当前任务。

> [!warning] 误区：`content` 可以直接打印
> 正确说法：assistant 的 content 可能是 block 列表，要找 text block。

> [!warning] 误区：`end_turn` 表示程序结束
> 正确说法：`end_turn` 只表示当前 assistant 轮结束，外层循环仍可继续等待输入。
