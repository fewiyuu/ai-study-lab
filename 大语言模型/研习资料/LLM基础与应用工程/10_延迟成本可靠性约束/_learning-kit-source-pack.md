# Source Pack: 10_延迟、成本、可靠性约束

## Unit

- Course: LLM 基础与应用工程
- Unit: 10_延迟成本可靠性约束
- Output: `10_延迟成本可靠性约束/学习页.html`
- Snapshot / 访问日期: `2026-06-22`

## Source Boundary

这一页承接 09 页的最小 Agent 循环，把“模型可以在受控边界内决定下一步”收束到上线时最常见的三笔账：延迟、成本、可靠性。它只讲单次请求的预算、路由、回退、日志和告警，不展开完整 SRE、分布式 tracing、容量规划、A/B 实验或自动扩缩容。

## Sources Used

| Source | URL / Path | Supports |
| --- | --- | --- |
| Course index | `../index.html` | 确认本页位于 09 之后、课程结束前，承担“把 Agent 链路收束到生产约束”的位置。 |
| Previous unit page | `../09_Agent最小流程/学习页.html` | 承接工具循环、状态写回和停止条件，说明这些动作一旦上线就会变成延迟、成本和可靠性问题。 |
| Current page before reconstruction | `学习页.html` before reconstruction | 主教学骨架：三角约束、延迟拆解、成本估算、可靠性回退、场景比较、故障诊断、练习结构。 |
| OpenAI Pricing | https://developers.openai.com/api/docs/pricing | 支持“tokens 按输入和输出计费，成本要按请求结构来算，而不是只看模型回答是否正确”。 |
| OpenAI Rate limits | https://developers.openai.com/api/docs/guides/rate-limits | 支持“请求速率、token 量和 429 需要进入回退与重试设计”。 |
| OpenAI Streaming API responses | https://developers.openai.com/api/docs/guides/streaming-responses | 支持“流式输出能更早显示结果，减少等待感，但不等于减少总计算量”。 |
| OpenAI Flex processing | https://developers.openai.com/api/docs/guides/flex-processing | 支持“长请求、复杂任务和默认超时要按流程重新看待”。 |
| OpenAI Error codes | https://developers.openai.com/api/docs/guides/error-codes | 支持“429、5xx 和其他错误码需要区分处理，不能一律盲重试”。 |
| OpenAI Production best practices | https://developers.openai.com/api/docs/guides/production-best-practices | 支持“上线时需要计划监控、超时、重试和回退，而不是只盯着离线结果”。 |

## Source-To-Unit Notes

- 本页把延迟写成一条请求链上的分段：排队、路由、拼上下文、模型生成、工具调用、后验检查和重试。它先教你找最重的一段，再决定是否流式输出、压缩上下文、缓存、限流或改回退。
- 本页把成本写成可估算的结构：输入 token、输出 token、工具调用、重试和人工复核都会改账单。这里用的是比较方向的工程估算，不是某个模型的固定报价表。
- 本页把可靠性写成可控失败：错误码、超时、权限拒绝、旧缓存和 schema 错误都应该落到清楚的下一步，而不是只写一行“失败”。
- `streaming`、`backoff`、`cache`、`handoff`、`timeout` 这些动作都来自同一条请求链，只是分别解决“先看到结果”“别把失败放大”“别重复花钱”“高风险先停”“别挂住”。
- 练习要诊断真实故障：平均值很好看但尾部很慢、重试越多越贵、缓存把旧政策发给用户、日志没有错误码、退款类动作没有转人工。

## Gaps And Notes

- 本页不写具体供应商价格、账户额度或某个项目的部署参数；它只教估算方法和决策顺序。
- 这里的 streaming、rate limit、timeout 和 fallback 规则来自官方通用文档，不对应某个私有系统的唯一实现。
- 如果以后要落到具体产品或 SDK，需重新核对当时的官方文档版本、访问日期和实际价格页。
