# 03｜结构化输出与 JSON Schema 本地 source pack

## Source Boundary

- Course: 工具调用契约与结构化交互
- Unit: `03_结构化输出与JSON_Schema/学习页.html`
- Snapshot date: 2026-06-20
- Local inputs only: 课程首页 `index.html` 和当前单元旧页 `学习页.html`
- No web crawl was used in this pass

## What The Course Index Establishes

课程首页把这门课排成一条清晰路线：先是契约思维，再到函数调用基础，然后进入本单元的结构化输出与 JSON Schema，后面接 MCP 工具规范、错误与回退、BFCL 评测、可维护工具面设计。

对本单元最重要的是这几条约束：

- 本单元要区分“结构化回答”“工具参数”“协议级工具声明”
- 本单元只讲结构约束，不把主题扩到错误处理、取消、评测或完整 MCP 协议
- 本单元的下一跳是 `04_MCP工具规范与协议边界`，但那一层现在只作为课程路由，不在这里展开

## What The Old Page Already Covers

旧页已经有一条可用的教学骨架，核心内容没有问题：

- JSON Schema 描述 JSON 数据结构和约束
- JSON mode 或“能吐出 JSON”并不等于 schema 级保证
- 工具参数比普通结构化回答风险更高，因为它可能触发真实执行
- 一个弱 schema 的反例：只有 `result` 和 `extra`，没有足够的必填、值域和额外字段约束
- 一个业务例子：用会议纪要输出风险对象，字段包括 `risk_found`、`risk_type`、`owner`、`evidence`
- 一个协议迁移例子：把 `search` 工具从“搜索东西”改成更清楚的命名、输入 schema 和结构化输出

## Source-To-Unit Mapping

### 1. 课程首页

支持内容：

- 课程位置
- 单元顺序
- 公开来源边界
- 与前后单元的关系

### 2. 旧学习页

支持内容：

- 本单元的 anchor example
- JSON / schema / structured outputs 的区别
- schema 反例、诊断题和迁移题
- 适合继续打磨的练习方向

## What To Keep

本单元重构时要保留的不是旧 HTML 壳，而是旧页的教学顺序：

1. 先把概念边界分清
2. 再看 schema 怎么约束结构
3. 然后用一个小对象例子把字段、枚举、必填和额外字段串起来
4. 最后把这套思路迁到工具参数和协议工具声明上

## What To Sharpen

- 把“看起来像 JSON”与“能稳定被消费”拆开讲
- 补一个可手工跟踪的状态/结构表，让读者看见从需求到 schema 再到消费结果的变化
- 把练习区做成诊断闭环，而不是只让人填空
- 在导出记录里保留可复查的代码片段、表格和失败信号

## Gaps And Boundaries

- 这份 source pack 只依赖本地已有页面，没有重新爬取公开网页
- 课程首页列出的公开来源家族仍然成立，但这次没有重新核对外部文档版本
- 本页不要扩成 MCP 协议总览；那属于下一单元
- 本页不要扩成错误、拒绝、取消或评测设计；那属于后面的单元

