# 01 先单智能体与决策框架 - Source Pack

## Source Boundary

- Course: 多智能体系统
- Unit: 01 先单智能体与决策框架
- Snapshot date: 2026-06-21
- Local source types used:
  - Claude 官方文章《Building multi-agent systems: When and how to use them》
  - 仓内整理笔记《资料熔炼》
  - 现有课程草稿 `01_先单智能体与决策框架/学习页.html`
  - 课程索引草稿 `课程索引.html`

## Source-To-Unit Notes

- 文章中的 `The case for starting with a single agent` 支持本单元的起点判断：先跑单智能体基线，再决定要不要拆分。
- 文章中的 `A decision framework` 支持本单元的三类约束：上下文保护、并行化、专业化。
- 文章中的 `Outgrowing single-agent architectures` 支持本单元的决策边界：只有在明确约束和收益足够时，才进入多智能体方案。
- 仓内整理笔记补足了术语表、课程拆块和后续单元映射。
- 现有草稿页提供了原始例子、练习类型和页面节奏，可作为重构素材，但不直接沿用旧 shell。

## Operation Facts

- 本页使用的是工程判断框架，不是形式化算法。
- 本页保留“单智能体基线 -> 识别约束 -> 估算协调成本 -> 小范围实验 -> 决定是否拆分”的顺序。
- 本页不爬网，不补充新的外部资料。

## Gaps And Inferences

- 原文没有给出固定阈值，因此页面中的“是否值得拆分”只能写成可验证的经验判断，而不是绝对公式。
- 原文没有把多智能体框架细化到某个具体实现，因此后续单元只讲分拆思路，不绑定某个库名。
- 课程索引中后续单元的排序沿用现有课程结构，属于课程编排推断。
