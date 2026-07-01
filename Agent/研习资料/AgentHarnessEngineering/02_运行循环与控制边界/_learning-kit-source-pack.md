# 02 运行循环与控制边界｜Source Pack

## Source Boundary

- Course root: `30_研究/Agent/研习资料/AgentHarnessEngineering`
- Unit: `02_运行循环与控制边界`
- Snapshot: 2026-06-21，本次重构只使用当前课程地图、目标旧学习页和页内已列公开资料线索，不进行联网爬取。

## Source-To-Unit Notes

- `index.html`
  - 说明课程名、7 个单元的顺序、前置关系和后续方向。
  - 用来确定本单元在整门课中的位置：它承接 01 的运行承载概念，负责把连续任务拆成运行循环、工具边界、终止条件和人工介入点。
- `02_运行循环与控制边界/学习页.html`
  - 是本次重构的主要内容来源。
  - 旧页中的课程位置、概念导图、术语与误区、核心讲解、运行循环案例、常见错误、练习区和参考资料，支持新页的教学结构、机制表、故障回溯、练习反馈和导出记录。
- 旧页中已经出现的公开参考名称
  - OpenAI Agents SDK: Running agents
  - OpenAI Agents SDK: Tools
  - OpenAI Agents SDK release notes
  - LangGraph Durable Execution
  - 这些来源用于约束 run、turn、tool call、tool result、final output、max turns、checkpoint、resume、replay 和副作用隔离等概念。

## Working Claims

- 本单元讲的是智能体运行循环：从任务输入、模型回合、工具请求、宿主程序检查、结果回填，到继续、交接、终止或人工介入。
- 学完本单元，读者应能把模型意图、工具执行、运行层控制和人工审批分开，并能为常见故障定位循环边界。
- 本单元不展开完整工具目录、工作空间隔离、外部协议连接、完整追踪系统或版本迁移策略；这些内容放到后续单元。

## Gaps And Follow-Ups

- 本次没有重新抓取官方文档或 release note 原文；如果后续补具体 SDK API 参数，应回到官方来源重新核对。
- 这份 source pack 只覆盖单元 02 的学习页重构，不替其他单元写具体内容。
- 后续单元应继续沿课程地图展开：工具面与工作空间、状态会话与可恢复执行、外部协议与连接器、追踪与运行记录、版本更新与迁移策略。
