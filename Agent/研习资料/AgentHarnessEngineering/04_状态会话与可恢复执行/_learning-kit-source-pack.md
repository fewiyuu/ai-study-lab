# 04 状态、会话与可恢复执行｜Source Pack

## Source Boundary

- Course root: `30_研究/Agent/研习资料/AgentHarnessEngineering`
- Unit: `04_状态会话与可恢复执行`
- Snapshot: 2026-06-21。本次只使用当前课程地图、旧学习页和页内已经列出的公开资料线索，不重新联网抓取文档原文。

## Source-To-Unit Notes

- `index.html`
  - 说明课程共有 7 个单元，04 位于 03 之后，负责把前面讲过的工具面和运行循环继续推进到状态、会话和恢复语义。
  - 用来锁定本单元的职责：它要回答“长任务中断后怎么继续”“哪类状态该保存在哪里”“重复运行如何不写坏外部系统”。
- `04_状态会话与可恢复执行/学习页.html`
  - 是本次重构的主要内容来源。
  - 旧页中的章节已经覆盖：会话与恢复的区别、四类状态、LangGraph 的 thread/checkpoint/super-step/interrupt/resume、OpenAI Agents SDK sessions 与 tracing、退款审批案例、常见错误、设计检查表、练习和导出。
  - 这些内容足够重构成共享壳下的教学链、状态账本、恢复表、失败实验和练习区。
- 旧页中已经出现的公开参考名称
  - OpenAI Agents SDK Sessions
  - OpenAI Agents SDK Tracing
  - LangGraph Durable Execution
  - LangGraph Persistence
  - LangGraph Interrupts
  - Temporal
  - 这些名字只作为当前页面的资料边界与术语锚点，不在本次生成里重新联网核验。

## Working Claims

- 本单元讲的是长任务里的四条线：会话历史、执行检查点、业务副作用和追踪记录。
- 学完本单元，读者应能看懂一个可恢复流程里哪些信息给模型、哪些信息给运行时、哪些信息必须在业务系统里幂等保存。
- 本单元不展开外部协议接入、完整可观测性平台、版本迁移策略或跨框架对比；这些内容留给后续单元。

## Gaps And Follow-Ups

- 本次没有重新抓取官方文档、release note 或规范原文；如果后续要补更细的 API 参数，应回到对应公开来源重新核对。
- 旧页里已有内容较完整，但还需要在 shared shell 下补足导出上下文、状态账本和可检视失败案例。
- 后续单元应继续按课程地图展开：外部协议与连接器、追踪与运行记录、版本更新与迁移策略。
