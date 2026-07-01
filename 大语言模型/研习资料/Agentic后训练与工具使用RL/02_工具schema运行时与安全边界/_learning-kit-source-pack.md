# Source Pack: 工具 schema、运行时与安全边界

## Source Boundary

- Course: Agentic 后训练与工具使用 RL
- Unit: 工具 schema、运行时与安全边界
- Snapshot: access date 2026-06-21

## Source-To-Unit Notes

- `index.html` 给出这门课的路线：01 先拆能力层级，02 进一步把接口、运行时和安全边界拆开，后面才进入 ReAct、Toolformer、ToolBench / API-Bank、OpenEnv 和沙盒上线。
- 现有 `学习页.html` 已经包含可复用的教学主线：schema、运行时、guardrail、handoff、tracing、伪代码、状态账本、例题和练习。
- 公共资料边界建议以这些材料为主：
  - OpenAI Agents SDK 的 tools / handoffs / guardrails / tracing 文档
  - Hugging Face TRL 的 OpenEnv 资料
  - ReAct、Toolformer、ToolBench / ToolLLM、API-Bank 论文
  - verl 与推理训练资料，用来对照可验证奖励和交互式奖励

## Unit Boundary

- 重点讲清：schema 约束、运行时职责、权限与副作用边界、trace 和观察的作用。
- 暂不展开：具体 agent 训练算法、ReAct 轨迹格式、OpenEnv 的完整实现、沙盒上线流程。

## Gaps

- 目前没有绑定某个私有仓库或作业仓库；本页只写到公开文档和论文层面的通用理解。
- 课程索引已经给出后续单元的学习顺序；本页只负责把“接口 / 运行时 / 边界”这一层讲透。
