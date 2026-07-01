# 03 并行化与专业化 - Source Pack

## Source Boundary

- Course: 多智能体系统
- Unit: 03 并行化与专业化
- Snapshot date: 2026-06-21
- Local source types used:
  - Claude 官方文章《Building multi-agent systems: When and how to use them》
  - 仓内整理笔记《资料熔炼》
  - 课程索引 `index.html`
  - 现有课程草稿 `03_并行化与专业化/学习页.html`

## Source-To-Unit Notes

- 官方文章中的 `Parallelization` 章节支撑本单元的并行化判断：只有在多个方向彼此独立时，才适合并行探索。
- 官方文章中的 `Specialization`、`Tool specialization`、`System prompt specialization`、`Domain specialization` 章节支撑本单元的专业化判断：专业化的前提是工具、提示词或领域边界真的分离。
- 官方文章中的 `Tool search` 思路支撑本单元的工具多场景判断：工具很多不必然意味着要拆智能体，按需发现可能更轻。
- 官方文章中的 `The verification subagent pattern` 只作为边界提示，不作为本单元主线；它会在下一单元展开。
- 《资料熔炼》补足了课程拆块顺序、术语表和来源对应关系，可用于把原文术语转成可教的单元结构。
- 现有 03 草稿保留了并行/专业化/路由/工具的典型例子，可作为重构素材，但最终页面要迁移到共享学习页壳里。

## Operation Facts

- 本单元讲的是工程判断，不是固定公式。
- 并行化主要换来覆盖度，不保证更省 token；成本通常来自上下文复制、协调消息和合成。
- 专业化主要换来更清晰的工具和任务边界；一旦边界不清，路由成本会吞掉收益。
- 工具很多时，可以先考虑工具搜索、按需加载或工具分组，再决定是否拆智能体。
- 本单元不绑定具体框架实现，也不引入新库。

## Gaps And Inferences

- 原文没有给出“多少工具必须拆智能体”的固定阈值，因此本页只能写成经验判断和试点建议。
- 原文没有给出通用路由算法，因此本页会用结构判断和返回格式来说明路由，而不是宣称某个固定公式。
- 验证子智能体与落地边界是下一单元内容，本单元只在边界段落里点到为止。
