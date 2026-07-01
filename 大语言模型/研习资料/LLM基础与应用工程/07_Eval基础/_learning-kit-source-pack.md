# Source Pack: 07_Eval基础

## Unit

- Course: LLM 基础与应用工程
- Unit: 07_Eval基础
- Output: `07_Eval基础/学习页.html`
- Snapshot / 访问日期: `2026-06-21`

## Source Boundary

本页重构的是课程里已经存在的本地学习页。它的职责是把“Eval 基础”收进 learning-kit 1.0 的共享壳，并把上一页的结构化输出接到下一页的样本集、指标、基线和回归检查。没有上游作业仓库或具体命令入口可桥接，因此本页只做通用工程讲解，不写具体文件名、函数名或测试命令。

## Sources Used

| Source | URL / Path | Supports |
| --- | --- | --- |
| Course index | `../index.html` | 确认本页位于 06 和 08 之间，承担“把感觉变成可复查证据”的位置。 |
| Old unit page | `学习页.html` before reconstruction | 主教学骨架：Eval 闭环、样本分层、指标与判分、基线和回归、误区诊断、练习结构。 |
| Course shell config | `../course-shell.json` | 统一上一节 / 下一节 / 锚点导航。 |
| OpenAI Prompt engineering guide | https://developers.openai.com/api/docs/guides/prompt-engineering | 支持“先把任务、输入、约束和输出拆开，再看程序如何接住结果”。 |
| OpenAI Structured Outputs | https://developers.openai.com/api/docs/guides/structured-outputs | 支持“输出形状需要稳定，程序才能解析、校验和重试”。 |
| OpenAI Function calling | https://developers.openai.com/api/docs/guides/function-calling | 支持“参数、返回值和调用边界要结构化描述”。 |
| OpenAI API docs overview | https://developers.openai.com/api/docs | 支持“结构化数据和工具调用是常见工程场景”。 |
| OpenAI Cookbook structured outputs intro | https://developers.openai.com/cookbook/examples/structured_outputs_intro | 支持“结构化输出适合更稳的生产流程和复查流程”。 |

## Source-To-Unit Notes

- 本页把 Eval 讲成“固定样本 + 规则/指标 + 错误分析 + 基线对比”的闭环，不把它写成抽象口号。
- 样本集要先覆盖普通样本、边界样本、高风险样本和历史坏例，再追数量。
- 指标要按任务分层：确定性任务优先硬指标，开放文本任务用 rubric 或 LLM-as-judge，再抽样人工复核。
- 平均分只能给方向，坏样本列表才告诉你该修哪一层。
- 这页会把 06 页的结构化输出接到 Eval：字段、枚举、缺失值和错误分支都会变成可评测材料。
- 这页也会把 08 页的 RAG 预热好：检索是否命中、答案是否被材料支持、资料缺失时是否拒答，都会在后面继续展开。

## Gaps And Notes

- 没有公开仓库、课后作业或具体 SDK 版本可桥接，因此本页不写具体仓库路径、测试名或接口代码。
- 例子是教学例子，来自课程旧页和官方文档的通用做法，不是对某个产品实现的逐字复述。
- 如果以后要绑定到具体 SDK、特定基线或某个评测平台，需重新核对当时的官方文档版本和访问日期。
