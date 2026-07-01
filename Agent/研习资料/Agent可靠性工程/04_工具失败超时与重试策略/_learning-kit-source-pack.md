# Agent 可靠性工程 / 04 工具失败、超时与重试策略

## Source Boundary

- 课程地图：`../index.html`
- 前一单元：`../03_确定性幂等与副作用隔离/学习页.html`
- 当前单元原始页快照：`学习页.html`
- 快照：2026-06-21，基于本地 Vault 现状与公开文档页面

## Source-To-Unit Notes

| 来源 | 支持什么 | 在本页怎么用 |
| --- | --- | --- |
| `../index.html` | 课程位置、单元顺序、前后关系 | 用来确认本单元承接 03 的幂等边界，再往 05 / 06 收束 |
| `../03_确定性幂等与副作用隔离/学习页.html` | Workflow / Activity 边界、幂等键、外部副作用、trace 证据链 | 作为本页前置背景，不重复讲重复副作用本身，只继续往“失败怎么处理”走 |
| `学习页.html` | 旧页里的超时、重试、限流、熔断、人工接管、追踪字段、案例和练习 | 作为本页的事实边界与案例来源，保留“失败分类先于重试策略”这条主线 |
| Temporal Failure Detection / Activity Timeouts | Start-To-Close、Schedule-To-Close、Schedule-To-Start、Heartbeat Timeout、Activity 失败语义 | 用来支撑“超时是时间预算，不是一个数字” |
| Temporal Retry Policies | initial interval、backoff coefficient、maximum interval、maximum attempts、non-retryable error types | 用来支撑“重试策略必须有上限和错误边界” |
| OpenAI Agents SDK Tracing | trace、span、tool、handoff、generation、事件与敏感数据控制 | 用来支撑“每次尝试都要能被串回同一条证据链” |
| OpenTelemetry GenAI semantic conventions | `gen_ai.*` 语义、工具调用、模型调用、事件字段 | 用来支撑“trace 字段怎么统一，工具调用与模型调用怎么对齐” |

## Lesson Boundary

- 本单元只讲工具失败、超时、重试、熔断和人工接管的边界，不展开完整工作流框架、结构化输出、防漂移、评测体系或上线验收清单。
- 主锚点建议固定为“读取失败、超时、限流、权限失败、业务冲突和写操作不确定成功时，下一步怎么选”。
- 下一步自然连接：
  - 05 结构化输出与防漂移边界
  - 06 追踪指标与事件语义
  - 07 评测回放与回归测试

## Gaps And Guardrails

- 不补新的网络考据；只使用课程地图、前一单元页、当前页快照和上面列出的公开资料名。
- 如果一个错误到底是临时失败、终态失败还是重复副作用暂时分不清，先标成“边界未定”，不要硬塞进可重试一侧。
- 本页要写成“怎么把失败分流”，不是“把所有可靠性术语一次讲完”。
