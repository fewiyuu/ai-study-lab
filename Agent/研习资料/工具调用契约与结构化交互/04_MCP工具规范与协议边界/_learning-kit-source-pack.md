# 04｜MCP 工具规范与协议边界 本地 source pack

## Source Boundary

- Course: 工具调用契约与结构化交互
- Unit: `04_MCP工具规范与协议边界/学习页.html`
- Snapshot date: 2026-06-21
- Local inputs: 课程首页 `index.html`、当前单元旧版 `学习页.html`
- Public sources used for factual grounding:
  - MCP Tools specification 2025-06-18
  - OpenAI Function Calling guide
  - OpenAI Structured Outputs guide
  - Berkeley Function Calling Leaderboard v4
- No extra web crawl was used during the local draft pass beyond the public docs above.

## What The Course Index Establishes

课程首页把这门课排成一条清晰路线：先是契约思维，再到函数调用基础，接着进入结构化输出与 JSON Schema，然后轮到本单元的 MCP 工具规范与协议边界，后面还有错误与回退、BFCL 评测和可维护工具面设计。

对本单元最重要的是这几条约束：

- 这一页要把 MCP 的工具层、协议层、结果层和评测层分开
- 这一页要说明工具结果里的 `content`、`structuredContent`、`isError` 和 `outputSchema` 各自做什么
- 这一页要和上一单元的结构化输出衔接，但不要把它们混成一层
- 这一页只讲协议边界和可观测后果，不扩成完整 MCP 架构总览

## What The Public Sources Support

### 1. MCP Tools specification 2025-06-18

支持内容：

- `tools/list` 和 `tools/call` 的基本消息流
- tool 定义里的 `name`、`title`、`description`、`inputSchema`、`outputSchema`
- tool result 里的 `content`、`structuredContent`、`isError`
- 协议错误和工具执行错误的区分
- `listChanged` 通知和工具列表变化

### 2. OpenAI Function Calling guide

支持内容：

- function / tool calling 的五步流程
- `tool_choice` 的常见模式：`auto`、`required`、强制某个函数、限制可用工具集
- function 定义中的 `name`、`description`、`parameters`、`strict`
- 工具描述和参数 schema 对模型选择的重要性

### 3. OpenAI Structured Outputs guide

支持内容：

- Structured Outputs 和 JSON mode 的边界
- `response_format: { type: "json_schema", strict: true }`
- JSON Schema 仍然是结构约束，不是事实正确性的保证
- 何时用结构化回答，何时用 function calling

### 4. BFCL leaderboard v4

支持内容：

- 工具调用评测不是只看一次成功演示
- 评测要覆盖工具选择、参数准确、多工具、多步、无关工具拒绝和异常场景
- BFCL 适合当作评测设计的参照，不适合当作你业务系统的全部验收

## Source-To-Unit Mapping

### 1. 课程首页

支持内容：

- 本单元在整门课里的位置
- 单元之间的顺序
- 前后单元的边界

### 2. MCP Tools specification 2025-06-18

支持内容：

- 工具列表、工具调用和工具结果
- `inputSchema` / `outputSchema`
- 协议错误与工具执行错误
- 工具 result 的结构化返回语义

### 3. OpenAI Function Calling guide

支持内容：

- 模型提出调用候选、宿主程序执行、回填结果的链路
- `tool_choice` 的选择空间
- function 描述与参数约束

### 4. OpenAI Structured Outputs guide

支持内容：

- JSON Schema 和合法 JSON 的区别
- `json_schema` 模式的结构约束
- 与 function calling 的分工

### 5. BFCL leaderboard v4

支持内容：

- 工具调用评测维度
- 业务评测和基准榜单之间的差别
- 评测设计时的参考维度

## What To Keep

本单元重构时要保留的不是旧 HTML 壳，而是旧页里已经可用的教学顺序：

1. 先看 MCP 解决什么边界问题
2. 再把 host、client、server、tool、resource、prompt 分清
3. 然后用一个最小工具定义把 `inputSchema`、`structuredContent` 和 `outputSchema` 串起来
4. 接着用协议错误、工具执行错误和 stdout 污染三个例子拆开边界
5. 最后把评测放回 BFCL 和业务验收

## What To Sharpen

- 把“能调用工具”与“协议、执行、返回都对齐”拆开讲
- 给出一张角色账本，让读者看见 host / client / server / tool / result 的读写关系
- 用一个最小工具定义和一个工具结果样例，让结构化内容、输出 schema 和错误语义都能直接看见
- 把练习做成诊断闭环，而不是单纯判断名词
- 在导出记录里保留可复查的请求、响应、结果和失败信号

## Gaps And Boundaries

- 这份 source pack 不重新展开 MCP 的 prompts、resources、authorization 和全套 lifecycle
- 这份 source pack 不把 OpenAI SDK 封装细节当成课程事实
- 这份 source pack 不把 BFCL 的具体分数当成课程重点；重点是维度和设计方法
- 课程内容只使用公开文档的版本边界和本地旧页骨架，不把其他课程单元混进来
