# Source Pack: 工具使用的能力层级

## Source Boundary

- Course: Agentic 后训练与工具使用 RL
- Unit: 工具使用的能力层级
- Snapshot: access date 2026-06-21

## Source-To-Unit Notes

- `index.html` 说明整门课的路线：先工具接口，再轨迹数据，再环境强化学习；本单元是第一块，负责把“会调用工具”拆成可诊断的能力层级。
- 旧页 `学习页.html` 提供了可复用的教学主线：工具接口、行动/观察、环境、奖励、五层分层、例题、误区和练习。
- 公开资料边界建议以这些材料为主：
  - OpenAI Agents SDK 的 tools / handoffs / guardrails / tracing 文档
  - Hugging Face TRL 的 OpenEnv 相关资料
  - ReAct、Toolformer、ToolBench / ToolLLM、API-Bank 论文
  - verl 与推理训练资料，用来对照环境奖励和可验证奖励
- 本单元要补的不是新知识点，而是把能力层级、失败症状和修复路径讲得更清楚，方便后续单元接上 schema、轨迹和环境训练。

## Unit Boundary

- 重点讲清：L0-L4 的分层、每层的失败信号、怎样从失败定位到修法。
- 暂不展开：具体 schema 设计、ReAct 轨迹格式、Toolformer 数据生成细节、OpenEnv 的完整实现、沙盒上线流程。

## Gaps

- 目前没有单独的外部课程讲义或仓库命令可直接桥接；因此本页只写到公开论文和文档层面的通用理解，不声称绑定某个私有实验仓库。
- 课程索引给出了后续单元的学习顺序；本页只负责把“能力层级”这一层讲透。
