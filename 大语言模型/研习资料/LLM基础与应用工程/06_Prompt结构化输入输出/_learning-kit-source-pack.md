# Source Pack: 06_Prompt结构化输入输出

## Unit

- Course: LLM 基础与应用工程
- Unit: 06_Prompt结构化输入输出
- Output: `06_Prompt结构化输入输出/学习页.html`
- Snapshot / 访问日期: `2026-06-21`

## Source Boundary

本页重构已有的本地学习页，目标是把“Prompt 结构化输入输出”收进 learning-kit 1.0 的共享壳。没有附带上游作业仓库或公开课程任务；本页的事实边界来自课程目录、旧版本地页面、课程壳配置，以及下面列出的官方文档。

## Sources Used

| Source | URL / Path | Supports |
| --- | --- | --- |
| Course index | `../index.html` | 确认本页位于 05 和 07 之间，承担“把自然语言需求写成可检查接口”的位置。 |
| Old unit page | `学习页.html` before reconstruction | 主教学骨架：prompt 契约、结构化输入、结构化输出、判分与校验、常见误区、练习结构。 |
| Course shell config | `../course-shell.json` | 课程内上一节 / 下一节 / 锚点导航的统一来源。 |
| OpenAI Prompt engineering guide | https://developers.openai.com/api/docs/guides/prompt-engineering | 支持“prompt 是输入模型的说明，效果依赖提示是否清楚、具体、可复用”。 |
| OpenAI Structured Outputs | https://developers.openai.com/api/docs/guides/structured-outputs | 支持“输出应遵循 JSON Schema，程序可据此解析和校验”。 |
| OpenAI Function calling | https://developers.openai.com/api/docs/guides/function-calling | 支持“函数/工具参数需要结构化描述，输出和调用之间要有稳定契约”。 |
| OpenAI API overview / structured data | https://developers.openai.com/api/docs | 支持“从模型获取结构化数据是 API 的常见用法之一”。 |
| OpenAI structured outputs intro | https://developers.openai.com/cookbook/examples/structured_outputs_intro | 支持“结构化输出可用于更稳的生产流程、函数调用和预定义结构”。 |

## Source-To-Unit Notes

- 本页要把 prompt 讲成接口契约，而不是只讲“怎么把话说得像样”。
- 结构化输入要拆出任务、上下文、约束和缺失时的处理方式。
- 结构化输出要写清字段、类型、枚举、错误字段和失败分流。
- 程序侧要负责 parse、validate、retry 和降级，prompt 不能替代权限控制或业务校验。
- 练习题要能把错误定位到任务、上下文、格式、校验或重试中的某一层。
- 第 07 页会继续把这种接口思路接到 Eval：先看基线，再看坏样本和回归。

## Gaps And Notes

- 没有公开仓库或上游作业可桥接，因此本页只做通用工程讲解，不写具体文件名、函数名或命令入口。
- 例子是基于官方文档和本地旧页整理出来的教学例子，不是对某一特定产品实现的逐字复述。
- 如果后续要绑定到某个具体 SDK 或版本，需要重新检查官方文档的当前页和访问日期。
