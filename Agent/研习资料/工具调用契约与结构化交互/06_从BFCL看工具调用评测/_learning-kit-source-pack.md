# 06｜从 BFCL 看工具调用评测 本地 source pack

## Source Boundary

- Course: 工具调用契约与结构化交互
- Unit: `06_从BFCL看工具调用评测/学习页.html`
- Snapshot date: 2026-06-21
- 访问日期: 2026-06-21
- Local reading base: 课程首页 `index.html`、当前单元旧版 `学习页.html`
- Public source families used in this pass:
  - OpenAI Function Calling guide: https://developers.openai.com/api/docs/guides/function-calling
  - OpenAI Structured Outputs guide: https://developers.openai.com/api/docs/guides/structured-outputs
  - MCP Tools spec 2025-11-25: https://modelcontextprotocol.io/specification/2025-11-25/server/tools
  - MCP Schema Reference: https://modelcontextprotocol.io/specification/2025-11-25/schema
  - BFCL leaderboard: https://gorilla.cs.berkeley.edu/leaderboard.html
  - BFCL V3 multi-turn / multi-step: https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html
  - BFCL V4 agentic / memory / format sensitivity: https://gorilla.cs.berkeley.edu/blogs/15_bfcl_v4_web_search.html, https://gorilla.cs.berkeley.edu/blogs/16_bfcl_v4_memory.html, https://gorilla.cs.berkeley.edu/blogs/17_bfcl_v4_prompt_variation.html
- No additional web crawl was used to fill in the local lesson draft beyond the public docs above.

## What The Course Index Establishes

课程首页把这门课排成一条连贯路线：

1. 先讲工具调用的契约思维
2. 再讲函数调用基础、描述选择与分发
3. 接着讲结构化输出与 JSON Schema
4. 然后进入 MCP 工具规范与协议边界
5. 再处理错误、拒绝、取消与回退
6. 本单元继续把“能调用”拆成可测能力
7. 后面再到可维护工具面的设计准则

对本单元最重要的约束是：

- 不把 BFCL 写成一个排行榜介绍
- 不把评测只写成“看模型有没有成功调用一次”
- 不把 AST、执行验证、relevance、multi-turn、parallel 混成一层
- 不把 schema 正确等同于任务正确

## What The Old Page Already Covers

旧页已经有一条可用的教学骨架，方向是对的：

- 单轮、并行、多轮、拒调和 agentic 评测维度已经分开
- Structured Outputs 和 MCP outputSchema 已经接到评测思路里
- 课程里已经有案例切换、评测维度表、错误清单和练习区
- 当前页的主线是“把工具调用能力拆成可验证对象”，不是单纯讲概念

## Source-To-Unit Mapping

### 1. 课程首页

支持内容：

- 本单元在整门课里的位置
- 这页前后应该接什么
- 课程范围到哪里为止

### 2. OpenAI Function Calling

支持内容：

- 工具定义、参数 schema、调用选择和执行回填
- 工具调用是模型和外部系统协作，不是模型自己完成动作

### 3. OpenAI Structured Outputs

支持内容：

- JSON Schema 约束和 strict 输出
- 结构可校验不等于语义自动正确

### 4. MCP Tools + Schema Reference

支持内容：

- inputSchema / outputSchema
- structuredContent 与下一步工具的衔接
- 结果结构为什么会影响可测性

### 5. BFCL Leaderboard / V3 / V4

支持内容：

- single-turn、multiple、parallel、relevance、multi-turn、agentic、format sensitivity
- 评测从“单次成功”扩展到“任务链路和失败归因”
- 不调用、晚调用、错工具、错参数、并行遗漏都应进入评测

## What To Keep

重构时要保留的不是旧 HTML 壳，而是旧页的教学主线：

1. 先说明 BFCL 想测什么
2. 再拆开常见评测维度
3. 把 OpenAI Structured Outputs 和 MCP 契约接进评测对象
4. 最后把这些维度收束到业务回归集

## What To Sharpen

- 给出更清楚的评测分流表：先看结构、再看执行、再看状态和拒调
- 补一张“工具调用失败层次”的表，让读者知道错在模型、schema、执行还是任务状态
- 给“业务评测集”一个可执行的最小样例，而不是只给方向
- 把练习里“选项题”做成可本地检查的版本，减少空白大题占比
- 给页面补上课程返回入口和更清楚的参考边界

## Gaps And Boundaries

- 这份 source pack 只依赖本地已有页面和公开文档家族，没有重新爬取整套站点
- 本页不要扩成 OpenAI Function Calling 或 Structured Outputs 的总览；那是前置单元
- 本页不要扩成 MCP 协议总览；这里只讲它如何进入评测
- 本页不要扩成 BFCL 论文史或 leaderboard 排行分析；这里只借用它的任务拆法
- 本页不要把“评测好看”写成目标；目标是可复现、可回归、可归因
