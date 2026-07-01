---
title: 17_HarnessEngineering总览
aliases:
  - Harness Engineering总览
  - Agent等于LLM加Harness
  - Learn Claude Code 17
tags:
  - LearnClaudeCode
  - Agent
  - HarnessEngineering
  - architecture
  - learning-kit
source: https://www.bilibili.com/video/BV1gRDeB3ETN
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. 为什么说 Agent = LLM + Harness？
> 2. Harness 是什么？
> 3. Learn Claude Code 系列可以归纳成哪几类关注点？
> 4. 工具、上下文、权限、任务、隔离分别解决什么问题？
> 5. 为什么不能只把 Agent 能力归因于模型？
> 6. Skill 在 Harness 中扮演什么角色？
> 7. 以后看 OpenCode、Codex、Claude Code 源码时应优先找哪些模块？

> [!abstract] 核心主线
> Learn Claude Code 第一阶段的收束观点是：Agent = LLM + Harness。LLM 负责理解、生成、推理和选择工具；Harness 是模型之外的工程结构，负责工具管理、上下文管理、权限审批、任务持久化、团队协作、工作区隔离和审计追踪。前面各节不是零散功能，而是在搭建一个让模型稳定做事的 Harness：从最小 loop 到工具调用，从 Skill 和上下文压缩到任务系统，从子 Agent、消息总线和团队协议到自主领任务、Git Worktree 和审计日志。以后阅读其他 Agent 项目时，应先识别这些 Harness 部件，而不是只盯模型调用。

## 概念精讲

### Agent = LLM + Harness

LLM 是语言模型，负责：

- 理解用户意图。
- 生成自然语言。
- 选择工具调用。
- 根据工具结果继续推理。

Harness 是模型之外的工程结构，负责：

- 提供工具。
- 管理上下文。
- 控制权限。
- 持久化任务。
- 调度子 Agent。
- 隔离执行环境。
- 记录审计日志。

> [!abstract] 直觉
> 模型像动力源，Harness 像外部控制系统。没有 Harness，模型可以输出文字，但很难稳定、安全、可追踪地完成工程任务。

## 五类 Harness 关注点

| 关注点 | 对应章节 | 解决的问题 |
|---|---|---|
| 工具管理 | tool use、多工具分发、专用工具 | 模型如何从“说话”变成“行动” |
| 上下文管理 | 消息历史、Skill、上下文压缩 | 模型如何知道任务、规则和历史 |
| 权限与审批 | 计划审批、操作审批、安全路径 | 高风险动作如何被约束 |
| 任务与协作 | todo、`.tasks`、子 Agent、消息总线 | 复杂任务如何拆分、委托、同步 |
| 隔离与审计 | Git Worktree、index、events.jsonl | 多任务如何互不干扰并可追踪 |

这些关注点相对正交，可以分别设计，但组合后才形成完整 Agent Harness。

## 系列能力路线

### 从零到可用

1. 本地启动最小 Agent。
2. 消息历史和 Agent loop。
3. 工具调用让 Agent 做事。
4. 多工具分发和专用工具。
5. 行动前先规划。

这条线让模型从“一次性回答”变成“能循环、能用工具、能规划行动”的最小 Agent。

### 从可用到可靠

1. 子 Agent 和任务委托。
2. Skill 渐进式披露。
3. 上下文压缩和无限会话。
4. 任务持久化和计划看板。
5. 后台任务和通知队列。

这条线解决持续工作、复杂任务拆分和上下文治理问题。

### 从单体到团队

1. Agent 团队和消息总线。
2. 团队关机协议。
3. 计划审批协议。
4. 自主 Agent 和看板轮询。
5. Git Worktree 任务隔离。
6. 可审计任务追踪。

这条线解决多个 Agent 如何通信、治理、领任务、隔离执行和留下证据。

## Skill 的位置

Skill 是 Harness 中“可复用知识与动作包”。

它把一类任务的做法沉淀成：

- 说明文件。
- 工作流程。
- 模板。
- 脚本。
- 检查规则。

模型仍然负责理解当前任务，但 Skill 提供稳定方法论，减少每次都靠临时 prompt 解释规则。

> [!question] 什么时候该写 Skill？
> 当一类任务会重复出现，并且需要稳定流程、模板、工具或检查规则时，就适合沉淀成 Skill。

## 以后看 Agent 源码的阅读清单

> [!todo] 先找 Harness 部件
> - [ ] Agent loop 在哪里。
> - [ ] 消息历史如何保存。
> - [ ] 工具 schema 如何定义。
> - [ ] tool use block 如何解析。
> - [ ] 工具结果如何回填给模型。
> - [ ] 上下文如何压缩或裁剪。
> - [ ] 权限和审批在哪里。
> - [ ] 任务状态如何持久化。
> - [ ] 子 Agent 如何创建和通信。
> - [ ] 后台任务如何通知主 Agent。
> - [ ] 工作目录如何隔离。
> - [ ] 审计日志如何记录。

## 应用与迁移问答

> [!question] 为什么不能只研究模型调用？
> 因为真实 Agent 的稳定性主要来自模型之外的工具协议、上下文、权限、任务、隔离和审计。模型调用只是入口。

> [!question] Harness 是否会限制模型？
> 会，但这是有意的。限制危险路径、规范工具调用和提供上下文，都是为了让模型更可靠地完成任务。

> [!question] OpenCode、Codex、Claude Code 是否都会有类似 Harness？
> 实现细节会不同，但大概率都会有 loop、工具、上下文、权限、任务、隔离、审计等类似结构。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 把 Agent 等同于模型本身。
> - 只记章节名，不理解背后的工程关注点。
> - 以为工具调用就是全部 Harness。
> - 忽略权限、审批和审计。
> - 把 Skill 当成普通 prompt，而不是可复用能力包。
> - 看其他源码时只搜 model API，不看任务和工具系统。

## 费曼解释润色版

> [!quote]
> Harness Engineering 讲的是模型之外那套让模型稳定做事的工程系统。一个 Agent 不是只有 LLM，而是 LLM 加 Harness。LLM 负责理解用户意图、生成回答、选择工具和根据结果继续推理；Harness 负责提供工具、管理上下文、控制权限、保存任务、调度子 Agent、隔离工作目录和记录审计日志。Learn Claude Code 系列从最小 loop 开始，逐步加入工具调用、规划、Skill、上下文压缩、任务系统、后台任务、消息总线、团队协议、自主领任务和 Git Worktree。把这些放在一起看，它们不是零散功能，而是在约束和放大模型能力。以后看 OpenCode、Codex 或 Claude Code 源码，不应该只看模型 API，而要问：工具怎么定义，任务怎么保存，权限怎么审批，工作区怎么隔离，失败后怎么追踪。Skill 也是 Harness 的一部分，因为它把一类任务的流程、模板和规则沉淀成可复用能力。

## 易错卡片

> [!warning] 误区：Agent 就是 LLM
> 正确说法：Agent = LLM + Harness。

> [!warning] 误区：Harness 只是外围小工具
> 正确说法：Harness 是让模型能安全、稳定、可追踪做事的核心工程。

> [!warning] 误区：Skill 只是更长的 prompt
> 正确说法：Skill 是可复用的任务流程、模板、工具和检查规则集合。

> [!warning] 误区：看 Agent 源码只需要看模型调用
> 正确说法：更重要的是看 loop、工具、上下文、权限、任务、隔离和审计。
