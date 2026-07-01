# 06 追踪与运行记录｜Source Pack

## Source Boundary

- Course root: `30_研究/Agent/研习资料/AgentHarnessEngineering`
- Unit: `06_追踪与运行记录`
- Snapshot: 2026-06-21。本次只使用当前课程地图、旧学习页和页内已经列出的公开资料线索，不重新联网抓取文档原文。

## Source-To-Unit Notes

- `index.html`
  - 说明课程共有 7 个单元，06 位于 05 之后，职责是把外部协议之后的运行证据链讲清楚。
  - 用来锁定本单元的职责：trace、span、checkpoint、恢复排查与运行记录。
- `06_追踪与运行记录/学习页.html`
  - 是本次收尾的主要内容来源。
  - 旧页中的章节已经覆盖：概念图、术语误区、讲解链、案例、常见错误、练习、导出和参考资料。
  - 这些内容足够重构成共享壳下的教学链、追踪图、术语对照、恢复案例和练习导出。
- 旧页中已经出现的公开参考名称
  - OpenAI Agents SDK Tracing
  - LangGraph Durable Execution / Persistence
  - 这些名字只作为当前页面的资料边界与术语锚点，不在本次生成里重新联网核验。

## Working Claims

- 本单元讲的是：trace 负责解释过程，span 负责切分动作，checkpoint 负责保存恢复坐标。
- 学完本单元，读者应能从运行证据判断问题来源，并把 trace_id、group_id、thread_id、checkpoint_id 关联起来。
- 本单元不展开版本迁移的全部动作；它只为后续迁移判断提供可读证据。

## Gaps And Follow-Ups

- 本次没有重新抓取官方文档、release note 或规范原文；如果后续要补更细的 API 参数，应回到对应公开来源重新核对。
- 旧页里已有内容较完整，但还需要在 shared shell 下补足导出上下文和可检视失败案例。
- 后续单元应继续按课程地图展开：版本更新与迁移策略。
