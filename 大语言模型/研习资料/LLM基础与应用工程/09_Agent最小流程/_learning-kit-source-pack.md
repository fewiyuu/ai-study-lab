# Source Pack: 09_Agent最小流程

## Unit

- Course: LLM 基础与应用工程
- Unit: 09_Agent最小流程
- Output: `09_Agent最小流程/学习页.html`
- Snapshot / 访问日期: `2026-06-21`

## Source Boundary

这一页承接 08 页的 RAG 链路，把“先找证据再回答”推进到“模型可以在受控边界内决定下一步”。本页只讲最小 Agent 流程：目标、状态、动作、工具执行、观察、停止条件、权限和日志。它不追多 Agent 协作、复杂记忆、长期规划框架或某个私有业务系统。

## Sources Used

| Source | URL / Path | Supports |
| --- | --- | --- |
| Course index | `../index.html` | 确认本页位于 08 RAG 和 10 生产约束之间，承担“从检索链路进入可控工具循环”的位置。 |
| Previous unit page | `../08_RAG最小流程/学习页.html` | 承接“证据进入上下文后再生成”的链路，把检索步骤扩展为可选择、可观察、可停止的工具动作。 |
| Next unit page | `../10_延迟成本可靠性约束/学习页.html` | 提醒本页的工具循环会带来延迟、成本和可靠性问题，下一页专门收束这些生产约束。 |
| Old unit page | `学习页.html` before reconstruction | 主教学骨架：Agent 边界、最小循环、工具规格、状态、停止条件、错误诊断、练习题。 |
| OpenAI Using tools guide | https://developers.openai.com/api/docs/guides/tools | 支持“构建 agent 时可以通过内置工具、function calling、tool search、remote MCP 等扩展模型能力”的工具边界。 |
| OpenAI Function calling guide | https://developers.openai.com/api/docs/guides/function-calling | 支持“function/tool calling 让模型生成工具参数，由应用代码执行工具并返回结果”的最小工具调用闭环。 |
| OpenAI Agents SDK guide | https://developers.openai.com/api/docs/guides/agents | 支持“当服务器负责编排、工具执行、状态和审批时，SDK 路径适合构建 agent”的工程分工。 |
| OpenAI Agents SDK: Agents | https://openai.github.io/openai-agents-python/agents/ | 支持“agent 是带 instructions、tools，以及可选 handoffs、guardrails、structured outputs 的 LLM 配置”的定义边界。 |
| OpenAI Agents SDK: Tools | https://openai.github.io/openai-agents-python/tools/ | 支持“工具可以是托管工具、本地函数工具、MCP、agent-as-tool 等，工具面要按场景选择”的工具分类。 |
| OpenAI Agents SDK: Guardrails | https://openai.github.io/openai-agents-python/guardrails/ | 支持“guardrails 与 human review 用于在风险动作前阻断或暂停”的护栏思路。 |

## Source-To-Unit Notes

- 本页把 Agent 定义成受控执行循环，不把“回答很长”“用了 prompt”“固定 RAG 链路”都叫 Agent。
- 核心对象是 `state -> model decides action -> app validates/executes tool -> observation -> state -> stop/continue`。模型提出动作请求，应用代码负责权限、参数校验、工具执行和日志。
- 工具描述要包含用途、参数、返回、限制、失败类型和权限；“什么时候不用”比“能做什么”更能降低误调用。
- 状态只保留当前任务决策需要的信息：目标、已知事实、已调用工具、观察、剩余步数、预算、待确认事项和风险标记。
- 停止条件不是失败，而是工程控制：信息足够、缺输入、达到步数/预算、工具连续失败、权限不满足、需要人工确认。
- 练习要诊断路径问题：循环不停、重复提问、工具误选、越权查询、高风险动作未确认、只看最终答案不看过程。

## Gaps And Notes

- 本页不绑定某个 Agent 框架或 SDK 版本；代码示例是教学伪代码，用于说明控制边界。
- 不引入多 Agent handoff、长期记忆、复杂 planner、浏览器控制或自动代码修改，这些会让最小流程失焦。
- 高风险动作例子只讲护栏原则，不提供真实外部系统的执行脚本。
