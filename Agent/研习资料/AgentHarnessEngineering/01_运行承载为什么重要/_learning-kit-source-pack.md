# 01 运行承载为什么重要｜Source Pack

## Source Boundary

- Course root: `30_研究/Agent/研习资料/AgentHarnessEngineering`
- Unit: `01_运行承载为什么重要`
- Snapshot: 2026-06-21，本次仅使用当前课程地图与旧学习页，不进行联网爬取

## Source-To-Unit Notes

- `index.html`
  - 说明课程名、7 个单元的顺序、前置关系和后续方向。
  - 用来确定本单元在整门课中的位置：它是第一单元，职责是先定义运行承载层的边界。
- `01_运行承载为什么重要/学习页.html`
  - 是本次重构的主要内容来源。
  - 其中已有章节可直接转成新页的教学主线：课程位置、概念导图、术语与误区、为什么需要运行承载层、运行循环、工具与权限、状态与会话、可恢复执行、运行记录、更新信号、工程案例、常见错误、练习、导出、参考来源。
  - 这些内容支持新页的机制说明、例子、误区、案例诊断和练习设计。
- 旧页中已经出现的公开参考名称
  - OpenAI Agents SDK
  - Agents SDK release notes
  - LangGraph Durable Execution
  - Temporal
  - MCP specification
  - OpenTelemetry GenAI semantic conventions
  - 这些名称只作为现有稿件里的来源线索保留，不在本次生成里重新联网核验。

## Working Claims

- 本单元讲的是智能体外层的运行承载层：循环、工具、权限、状态、恢复、追踪和版本边界。
- 学完这一单元，读者应能把“模型能力问题”和“运行系统边界问题”分开看。
- 这一单元不展开模型训练、提示词大全、完整框架 API 教程或跨框架优劣比较。

## Gaps And Follow-Ups

- 本次没有重新抓取官方文档、release note 或规范原文；如果后续要补更细的 API 细节，应回到官方来源重新核对。
- 这份 source pack 只覆盖单元 01 的讲义重构，不替后续单元写具体内容。
- 后续单元应继续围绕课程地图里的顺序展开：运行循环、工具面与工作空间、状态与可恢复执行、外部协议、追踪、版本迁移。
