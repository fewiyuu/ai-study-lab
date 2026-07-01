# 07｜可维护工具面的设计准则 本地 source pack

## Source Boundary

- Course: 工具调用契约与结构化交互
- Unit: `07_可维护工具面的设计准则/学习页.html`
- Snapshot date: 2026-06-21
- 访问日期: 2026-06-21
- Local reading base: 课程首页 `index.html`、当前单元旧版 `学习页.html`
- Public source families used in this pass:
  - OpenAI Function Calling guide: https://developers.openai.com/api/docs/guides/function-calling
  - OpenAI Structured Outputs guide: https://developers.openai.com/api/docs/guides/structured-outputs
  - MCP Tools spec 2025-11-25: https://modelcontextprotocol.io/specification/2025-11-25/server/tools
  - MCP Schema Reference: https://modelcontextprotocol.io/specification/2025-11-25/schema
  - BFCL leaderboard: https://gorilla.cs.berkeley.edu/leaderboard.html
- No additional web crawl was used in this pass beyond the public source families above.

## What The Course Index Establishes

课程首页把这门课排成一条连贯路线：

1. 先讲工具调用的契约思维
2. 再讲函数调用基础、描述选择与分发
3. 接着讲结构化输出与 JSON Schema
4. 然后进入 MCP 工具规范与协议边界
5. 再处理错误、拒绝、取消与回退
6. 再用 BFCL 把调用能力拆成可测维度
7. 最后落到可维护工具面的设计准则

对本单元最重要的约束是：

- 不把“工具越多越强”写成默认结论
- 不把 schema 正确等同于业务正确
- 不把返回结构、权限注解、版本策略和评测样本分开看
- 不把 BFCL 当成排行榜介绍，而是把它当成失败维度的拆解器

## What The Old Page Already Covers

旧页已经有一条可用的教学骨架，方向是对的：

- 工具面和后端函数全集要分开
- schema 和业务规则要分开
- 结构化输出和工具调用要分开
- MCP 工具和任意远程接口要分开
- BFCL 分数和业务上线质量要分开
- 工具描述和提示词补丁要分开
- 练习里已经开始写工具去重、schema 收敛、负例评测和风险分级

## Source-To-Unit Mapping

### 1. 课程首页

支持内容：

- 本单元在整门课里的位置
- 前后单元怎么衔接
- 这门课为什么要先讲契约、再讲评测、最后讲治理

### 2. OpenAI Function Calling

支持内容：

- 工具定义、参数 schema、调用选择和执行回填
- 工具调用是模型与外部系统协作，不是模型自己完成动作

### 3. OpenAI Structured Outputs

支持内容：

- JSON Schema 约束和 strict 输出
- 结构可校验不等于语义自动正确

### 4. MCP Tools + Schema Reference

支持内容：

- inputSchema / outputSchema
- structuredContent 与后续工具消费
- 工具行为注解和返回结构为什么会影响可测性

### 5. BFCL Leaderboard

支持内容：

- tool selection、multiple tools、parallel、relevance、multi-turn、agentic、format sensitivity
- 把“能调用一次”拆成“选对、填对、并行对、拒调对、版本对、回归对”

## What To Keep

重构时要保留的不是旧 HTML 壳，而是旧页的教学主线：

1. 先说明工具面为什么必须可维护
2. 再拆开命名、schema、返回、权限、版本和评测
3. 用一个最小工具例子把这些点串起来
4. 最后把这套思路收束到自己的工具注册表和回归集

## What To Sharpen

- 给出一张读写表，让读者看见 name、description、schema、返回和权限各自负责什么
- 补一张版本迁移台账，让读者知道哪些改动是兼容的，哪些会打断旧调用
- 把练习做成诊断闭环，而不是单纯背定义
- 给页面补上课程返回入口和更清楚的边界说明

## Gaps And Boundaries

- 这份 source pack 只依赖本地已有页面和公开文档家族，没有重新爬取整套站点
- 本页不要扩成 OpenAI Function Calling 或 Structured Outputs 的总览；那是前置单元
- 本页不要扩成 MCP 协议总览；这里只讲它如何进入工具面设计
- 本页不要扩成 BFCL 论文史或 leaderboard 排名分析；这里只借用它的维度拆法
- 本页不要把“评测好看”写成目标；目标是可复现、可回归、可归因
