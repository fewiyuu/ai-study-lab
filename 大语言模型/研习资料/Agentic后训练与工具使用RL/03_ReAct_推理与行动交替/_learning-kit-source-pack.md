# Source Pack: ReAct：推理与行动交替

## Source Boundary

- Course: Agentic 后训练与工具使用 RL
- Unit: ReAct：推理与行动交替
- Snapshot: access date 2026-06-21

## Source-To-Unit Notes

- 课程地图把 03 放在工具 schema / 运行时之后、Toolformer / ToolBench / API-Bank 之前。这个位置很关键：先把 ReAct 看成轨迹组织方式，再去看自监督工具学习、任务评测和环境训练。
- 本页的主来源是 ReAct 论文：它强调 reasoning traces 和 task-specific actions 交替出现，并用观察更新后续计划。
- 作为对照和桥接，本页还参考这些公开材料：
  - OpenAI Agents SDK 的 tools / handoffs / guardrails / tracing 文档
  - ToolLLM / ToolBench 论文
  - API-Bank 论文
  - TRL OpenEnv 资料

## Unit Boundary

- 重点讲清：Thought / Action / Observation 的循环、轨迹如何被阅读和诊断、为什么它能进入后训练和评测。
- 暂不展开：完整 ReAct prompt 模板、Toolformer 的数据生成细节、ToolBench 的 evaluator 细节、OpenEnv 的实现和完整环境 RL。

## Gaps

- 目前没有绑定私有仓库、作业仓库或内部实验日志；本页只写公开文档和论文层面的通用理解。
- 课程后续单元会继续把轨迹问题拆到数据构造、评测和环境闭环里；本页只负责把 ReAct 的中间层讲透。
