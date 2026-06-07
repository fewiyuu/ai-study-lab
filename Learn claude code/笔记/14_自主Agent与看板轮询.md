---
title: 14_自主Agent与看板轮询
aliases:
  - 自主Agent与看板轮询
  - 从被动到主动自主Agent
  - Learn Claude Code 14
tags:
  - LearnClaudeCode
  - Agent
  - autonomous-agent
  - task-board
  - course-forge
source: https://www.bilibili.com/video/BV111XLBHEhb
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. 自主 Agent 和被动 teammate 的根本差别是什么？
> 2. `.tasks` 目录为什么可以看作任务看板？
> 3. `claim_task` 为什么必须检查 `owner`、`status`、`blocked_by`？
> 4. lock 在认领任务时解决什么问题？
> 5. A 依赖 B 时，为什么不能先 claim A？
> 6. 任务完成后为什么进入 `idle`，而不是马上 `shutdown`？
> 7. 依赖解除为什么最好交给系统规则维护？

> [!abstract] 核心主线
> 自主 Agent 的自主性不是“随便行动”，而是能自己扫描任务源、判断可执行任务、原子化认领并持续轮询。lead 先把任务写入 `.tasks/task_N.json`，再启动 Alice。Alice 的 autonomous loop 会读取任务看板，优先 claim `owner` 为空、`status` 为 `pending`、`blocked_by` 为空的任务；claim 成功后写入 `owner=alice` 和 `status=in_progress`，完成后改为 `completed`。当暂时没有可做任务时，Alice 调用 `idle`，状态变为 `idle`，继续按间隔检查 inbox 和 `.tasks`。如果约定时间内仍无新任务，才进入 `shutdown`。

## 概念精讲

### 从等指令到自己拉任务

被动 teammate 的工作方式是：lead 发消息，teammate 读 inbox，然后执行这条指令。自主 Agent 的变化是：它不只看 inbox，还会主动扫描 `.tasks` 目录，自己发现任务。

关键区别不在于是否运行在后台，而在于任务选择权从“lead 逐条推送”变成“Agent 从共享看板拉取”。这让系统可以持续投放任务，也让多个 Agent 有机会围绕同一个任务池协作。

### `.tasks` 是结构化任务看板

`.tasks/task_N.json` 保存任务状态。每个 JSON 至少包含任务编号、主题、状态、认领者和依赖信息。

```json
{
  "id": 3,
  "subject": "A",
  "status": "pending",
  "owner": "",
  "blocked_by": [1]
}
```

这些字段让模型不用靠记忆猜测任务进度，而是读取当前状态后再行动。状态写在文件里，也方便 lead、其他 Agent 或调试工具查看。

### `claim_task` 的三重检查

`claim_task` 不应只是“把 owner 改成自己”。它必须先确认任务真的可以拿：

| 检查项 | 通过条件 | 失败含义 |
|---|---|---|
| `owner` | 为空 | 已被其他 Agent 认领 |
| `status` | `pending` | 任务不在待领取状态 |
| `blocked_by` | 为空 | 前置依赖尚未解除 |

三项都通过后，系统才写入：

```json
{
  "owner": "alice",
  "status": "in_progress"
}
```

这一步是自主 Agent 进入执行阶段的边界：claim 前只是候选任务，claim 后才是 Alice 当前负责的工作。

### lock 防止并发抢任务

如果 Alice 和 Bob 同时扫描 `.tasks`，它们可能同时看到同一个任务还没人认领。没有 lock 时，两边都可能写入自己的 owner，导致任务重复执行。

lock 的作用是把“读取任务、检查字段、写入 owner/status”包成一个不可打断的小事务。同一时间只有一个 Agent 能完成这组检查和写入。

> [!warning] lock 保护的是认领临界区
> 临界区是指一段不能被多个执行者同时进入的关键代码。这里的关键代码就是“判断能不能 claim，并把任务改成 in_progress”。

### B/C/A 依赖例子

示例中有三个任务：B、C、A。其中 B 和 C 没有依赖，可以先做；A 的 `blocked_by` 包含 B 的 id，所以一开始不能 claim。

合理顺序是：

1. Alice 扫描 `.tasks`。
2. 看到 B/C 可做，先 claim 并完成。
3. A 因 `blocked_by` 不为空，第一次 claim 失败。
4. B 完成后，依赖应被解除。
5. A 重新变成可领取任务，再被 claim 和完成。

视频调试里，模型第一次 claim A 失败，是因为 A 仍然写着 `blocked_by: [1]`。后续模型用 `write_file` 清空依赖后才认领成功。

### 依赖解除应系统化

让模型手动修改 JSON 可以跑通 demo，但长期看不稳。更好的做法是系统在任务完成时自动检查依赖关系：如果 task1 completed，就把所有 `blocked_by` 中引用 task1 的任务更新为可执行状态。

这样做的好处是：依赖规则由系统保证，模型只负责选择和执行任务，不需要记住每次都要手动清理依赖字段。

### idle polling 与 shutdown timeout

所有当前任务完成后，Agent 不应立刻退出。它会调用 `idle`，把状态写成 `idle`，然后继续轮询 inbox 和 `.tasks`。

常见策略是每 5 秒检查一次，持续约 60 秒。如果期间有新消息或新任务，就重新工作；如果超时仍没有新任务，再把状态改为 `shutdown` 并 return。

> [!abstract] 状态直觉
> `idle` 表示“我暂时没活，但还在线”；`shutdown` 表示“我确认一段时间没活，准备结束”。两者不能混用。

## 判断与行动清单

> [!todo] 实现自主 Agent 前先检查
> - [ ] 是否有结构化任务源，例如 `.tasks/task_N.json`。
> - [ ] Agent loop 是否主动扫描任务源，而不是只等 inbox。
> - [ ] 认领任务前是否检查 `owner`。
> - [ ] 认领任务前是否检查 `status == pending`。
> - [ ] 认领任务前是否检查 `blocked_by` 为空。
> - [ ] claim 的检查和写入是否在 lock 中完成。
> - [ ] claim 成功后是否写入 owner 和 in_progress。
> - [ ] 完成后是否写入 completed。
> - [ ] 没有可做任务时是否进入 idle polling。
> - [ ] idle 超时后是否再 shutdown。

## 应用与迁移问答

> [!question] 自主 Agent 是不是不需要 lead？
> 不是。lead 仍然可以创建任务、设定目标和投放任务。自主 Agent 只是从任务池中主动拉取可做任务。

> [!question] 为什么 `blocked_by` 不为空时不能 claim？
> 因为任务的前置条件还没满足。提前 claim 会让执行顺序错乱，甚至产出依赖未完成的结果。

> [!question] 为什么任务完成后不马上 shutdown？
> 因为系统可能很快投放新任务。idle polling 给 Agent 一个等待窗口，让它能接住后续工作。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 把自主性理解成“模型自己乱想任务”。
> - 忘记自主 Agent 需要可扫描的任务源。
> - 只检查 owner，不检查 status 和 blocked_by。
> - 没有 lock，导致多个 Agent 抢同一个任务。
> - A 依赖 B 时仍然先 claim A。
> - 任务完成后忘记把状态写成 completed。
> - 把 idle 当成 shutdown。
> - 依赖解除全靠模型手动改 JSON，没有系统规则兜底。

## 费曼解释润色版

> [!quote]
> 自主 Agent 的关键不是“没人指挥”，而是它能自己从任务看板拉活。lead 先把任务写进 `.tasks/task_N.json`，每个任务都有 owner、status 和 blocked_by。Alice 启动后进入 autonomous loop，扫描 `.tasks`，读取任务状态，只认领 owner 为空、status 是 pending、blocked_by 为空的任务。认领时要在 lock 里完成检查和写入，避免多个 Agent 同时抢同一个任务。claim 成功后，Alice 把任务 owner 写成自己、status 写成 in_progress，做完后改成 completed。如果没有任务可做，Alice 进入 idle，而不是直接退出；它继续每隔几秒检查 inbox 和 `.tasks`，一段时间都没有新任务后才 shutdown。依赖关系最好由系统在任务完成时自动解除，不要完全依赖模型手动修改 JSON。

## 易错卡片

> [!warning] 误区：自主 Agent 等于自己发明任务
> 正确说法：自主 Agent 是从明确的任务源中主动发现和认领任务。

> [!warning] 误区：claim 只要写 owner 就行
> 正确说法：还要检查 status 和 blocked_by，并且在 lock 里原子完成。

> [!warning] 误区：任务都做完就应该立刻退出
> 正确说法：先进入 idle，继续轮询一段时间；超时无任务再 shutdown。

> [!warning] 误区：依赖解除交给模型临场处理就够了
> 正确说法：依赖解除最好系统化，否则容易漏改、错改或提前执行。
