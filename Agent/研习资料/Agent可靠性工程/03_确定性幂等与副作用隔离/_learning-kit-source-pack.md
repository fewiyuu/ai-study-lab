# Agent 可靠性工程 / 03 确定性、幂等与副作用隔离

## Source Boundary

- 课程地图：`../index.html`
- 前一单元：`../02_持久执行与检查点/学习页.html`
- 当前单元原始页快照：`学习页.html`
- 快照：2026-06-21，基于本地 Vault 现状与公开文档页面

## Source-To-Unit Notes

| 来源 | 支持什么 | 在本页怎么用 |
| --- | --- | --- |
| `../index.html` | 课程位置、单元顺序、前后关系 | 用来确认本单元承接 02 的恢复语义，继续往 04 / 05 / 06 收束 |
| `../02_持久执行与检查点/学习页.html` | 长任务恢复、checkpoint、事件历史、Workflow / Activity 分工、报告生成与人工确认锚点 | 作为本页的前置背景，不重复讲恢复实现，只在恢复之后进入确定性、幂等与副作用隔离 |
| `学习页.html` | 旧页里的退款、订单、发短信、trace、错误表、幂等存储、冲突处理等锚点 | 作为本页的事实边界与案例来源，保留“重复外部动作”“证据链不足”这条主线 |
| Temporal Workflow Definition | Workflow 必须确定性、外部交互应放到 Activities | 用来支撑“为什么可重放逻辑不能直接碰外部世界” |
| Temporal Workflow Execution / Events and Event History | replay、事件历史、恢复继续的位置 | 用来支撑“为什么恢复和重放依赖历史” |
| Temporal Activity Definition / Retry Policy | Activity 的幂等建议、自动重试语义、外部副作用边界 | 用来支撑“为什么 Activity 要能安全重复执行” |
| Temporal Side Effects 文档 | 非确定性值记录到历史、Side Effect 不应修改 Workflow 状态 | 用来支撑“少量非确定性值如何被隔离，而不是直接混入 Workflow 决策” |
| OpenAI Agents SDK Tracing / Spans / Tools | trace、span、tool execution、agent run、model generation、handoff 边界 | 用来支撑“如何把一次重复调用和它的证据链记录下来” |
| OpenTelemetry semantic conventions / GenAI events / GenAI metrics | `gen_ai.*` 语义、model/tool/event 字段、统一观测语言 | 用来支撑“trace 字段怎么统一，工具调用、模型调用和事件怎么对齐” |

## Lesson Boundary

- 本单元只讲确定性、幂等和副作用隔离的边界，不展开完整工作流框架、重试策略、结构化输出、追踪后端接入或上线验收清单。
- 主锚点建议固定为“退款 / 发信 / 写库这类外部动作在重放或重试时不能重复伤害外部世界”。
- 下一步自然连接：
  - 04 工具失败、超时与重试策略
  - 05 结构化输出与防漂移边界
  - 06 追踪指标与事件语义

## Gaps And Guardrails

- 不补新的网络考据；只使用课程地图、旧单元页和上面列出的公开资料名。
- 如果某个动作还分不清是可重放逻辑还是外部副作用，先标成“边界未定”，不要硬塞进幂等或确定性一侧。
- 本页要写成“怎么把重复到达挡在边界外”，不是“把所有可靠性术语一次讲完”。
