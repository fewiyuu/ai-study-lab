---
title: 12_团队关机协议与FSM
aliases:
  - 团队关机协议与FSM
  - 团队协议上关机
  - Learn Claude Code 12
tags:
  - LearnClaudeCode
  - Agent
  - team-protocol
  - FSM
  - learning-kit
source: https://www.bilibili.com/video/BV1NVXMBwEJt
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. 关机协议解决什么问题？
> 2. `shutdown_request` 如何创建请求并发送给 teammate？
> 3. `shutdown_response` 为什么需要 request_id？
> 4. pending、approved、rejected、shutdown 分别是什么状态？
> 5. `should_exit` 如何让 teammate loop 自然退出？
> 6. lead 如何确认 Alice 已经关机？

> [!abstract] 核心主线
> 关机协议是在 Agent team 消息总线之上定义的可确认流程。lead 调用 `shutdown_request(alice)`，生成 request_id，把请求记录到 `shutdown_requests` 字典，状态为 pending，并把 shutdown_request 消息写入 `alice.jsonl`。Alice 的 teammate loop 读到消息后调用 `shutdown_response(request_id, approve, reason)`。如果 approve=true，请求状态变 approved，`should_exit` 设为 true，Alice 退出 loop，config 中成员状态从 working 变为 shutdown，并给 lead inbox 发确认消息。这个过程可以看成一个有限状态机 FSM。

## 概念精讲

### 协议让团队动作可确认

只发一句“请关机”是不够的。lead 需要知道：

- 请求是否已创建。
- 请求发给了谁。
- 对方是否批准。
- 对方是否真的退出。
- 最终状态是否写入 config。

关机协议把这些步骤变成可追踪状态，而不是散乱聊天。

### FSM 是有限状态机

FSM 全称是 finite state machine，中文可叫有限状态机。它表示系统只能处在有限几个状态里，并按规则跳转。

关机请求状态：

```text
pending → approved
pending → rejected
```

成员状态：

```text
working → shutdown
```

注意：请求状态和成员状态不是同一件事。request approved 表示 Alice 同意关机；member shutdown 表示 Alice 的 loop 已经退出并保存了最终成员状态。

## 请求：`shutdown_request`

lead 发起关机请求时：

1. 生成 request_id。
2. 在 `shutdown_requests` 中登记目标和 pending 状态。
3. 通过 MessageBus 写入 Alice 的 inbox。
4. 返回“request sent”。

```python
def shutdown_request(teammate):
    request_id = str(uuid.uuid4())[:8]

    with lock:
        shutdown_requests[request_id] = {
            "target": teammate,
            "status": "pending",
        }

    bus.send(
        to=teammate,
        sender="lead",
        message_type="shutdown_request",
        content="Please shutdown gracefully.",
        extra={"request_id": request_id},
    )
```

Alice inbox 中会出现：

```json
{"type":"shutdown_request","from":"lead","content":"Please shutdown gracefully.","request_id":"a13f29c0"}
```

request_id 用于把后续响应和这次请求对上。没有 request_id，多请求并发时会混乱。

## 响应：`shutdown_response`

Alice 读到自己的 inbox 后，模型会调用 `shutdown_response`：

```json
{
  "request_id": "a13f29c0",
  "approve": true,
  "reason": "Acknowledged. I will shut down gracefully."
}
```

处理逻辑：

- 找到 request_id 对应请求。
- approve=true：状态改为 approved。
- approve=false：状态改为 rejected。
- 给 lead 发一条响应消息。
- 如果 approved，则 teammate loop 设置 `should_exit = True`。

`should_exit` 让 loop 自然退出，而不是粗暴杀线程。

## 退出与确认

Alice 批准关机后：

1. `shutdown_response` 把请求状态改为 approved。
2. 向 lead inbox 写入确认消息。
3. `should_exit` 变 true。
4. teammate loop 在下一处检查时 break。
5. final member 状态从 working 改为 shutdown。
6. 保存 `.teams/config.json`。

lead 下一轮 loop 读取 `lead.jsonl` 时，就能知道 Alice 已确认关机。

## 关键区分

| 项目 | 保存位置 | 含义 |
|---|---|---|
| `shutdown_requests[request_id].status` | 内存字典 | 这次关机请求的状态 |
| `member.status` | `.teams/config.json` | 队员当前生命周期状态 |
| `alice.jsonl` | Alice inbox | lead 发给 Alice 的请求 |
| `lead.jsonl` | lead inbox | Alice 发给 lead 的确认 |
| `should_exit` | teammate loop 局部控制 | 是否退出当前 teammate loop |

## 判断与行动清单

> [!todo] 实现关机协议前先检查
> - [ ] 是否生成唯一 request_id。
> - [ ] 请求是否登记为 pending。
> - [ ] 请求是否写入目标 teammate inbox。
> - [ ] teammate 是否读取自己的 inbox。
> - [ ] response 是否带 request_id。
> - [ ] approve/reject 是否更新请求状态。
> - [ ] approved 是否设置 `should_exit`。
> - [ ] loop 退出后是否把成员状态保存为 shutdown。
> - [ ] 是否给 lead 发确认消息。

## 应用与迁移问答

> [!question] 为什么不直接 kill teammate 线程？
> 直接 kill 没有确认，也可能丢掉收尾动作。graceful shutdown 让 teammate 自己响应、退出并保存状态。

> [!question] lead 查询请求还是 pending，可能是什么原因？
> Alice 线程没运行、Alice 还没读 inbox、Alice 没调用 response、response 没更新字典，或 debug 时主线程和子线程被人为暂停。

> [!question] approved 和 shutdown 有什么区别？
> approved 是请求状态，表示 Alice 同意；shutdown 是成员状态，表示 Alice 已退出并保存结果。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 把 request 状态和 member 状态混为一谈。
> - 创建请求但不写入 teammate inbox。
> - response 不带 request_id。
> - Alice approved 后没有给 lead 回信。
> - 设置 `should_exit` 后没有保存 shutdown 状态。
> - 拒绝请求时不记录 rejected。
> - 以为主线程创建请求后，Alice 一定已经关机。

## 费曼解释润色版

> [!quote]
> 关机协议把“让队员停止”变成一个可确认的状态流程。lead 调用 `shutdown_request` 时，会生成 request_id，把请求放进 `shutdown_requests`，状态设为 pending，并通过 MessageBus 写入 Alice 的 inbox。Alice 的 teammate loop 开头读取自己的 inbox，看到 shutdown_request 后，模型调用 `shutdown_response`，带上 request_id、approve 和 reason。如果 approve 为 true，请求状态从 pending 变成 approved，并设置 `should_exit`。Alice 还会向 lead inbox 发确认消息。随后 teammate loop 看到 `should_exit`，自然 break，最后把 config 中 Alice 的状态从 working 保存为 shutdown。如果 Alice 拒绝，请求状态应变成 rejected，loop 不退出。这个过程就是一个小型 FSM，用明确状态替代含糊的自然语言判断。

## 易错卡片

> [!warning] 误区：approved 就等于成员已经 shutdown
> 正确说法：approved 是请求状态；shutdown 是 loop 退出后保存的成员状态。

> [!warning] 误区：关机就是直接杀线程
> 正确说法：本节是 graceful shutdown，要请求、响应、退出和确认。

> [!warning] 误区：只要发给 Alice 一句话就够了
> 正确说法：需要 request_id 和状态记录，否则无法追踪请求。

> [!warning] 误区：pending 表示协议失败
> 正确说法：pending 只表示还未收到有效响应，需要检查 Alice 是否读到并处理请求。
