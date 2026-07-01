# Source Pack: 08_RAG最小流程

## Unit

- Course: LLM 基础与应用工程
- Unit: 08_RAG最小流程
- Output: `08_RAG最小流程/学习页.html`
- Snapshot / 访问日期: `2026-06-21`

## Source Boundary

这一页承接 07 页的评测意识，继续往下讲“怎么把外部证据接进回答”。它要把 RAG 讲成一条可排查的链路：文档处理、切分、向量化、索引、检索、上下文拼接、生成、引用和失败归因。页面内容仍然是课程内部教学例子，不绑定某个私有仓库或特定业务系统。

## Sources Used

| Source | URL / Path | Supports |
| --- | --- | --- |
| Course index | `../index.html` | 确认本页位于 07 和 09 之间，承担“把评测接到检索与生成”的位置。 |
| Previous unit page | `../07_Eval基础/学习页.html` | 让本页承接“样本、指标、基线、回归”的评测思路，把它延伸到检索证据和引用。 |
| Old unit page | `学习页.html` before reconstruction | 主教学骨架：RAG 最小流程、离线/在线两段、chunk 与 metadata、检索与重排、上下文拼接、错误诊断、场景迁移。 |
| OpenAI Prompt engineering guide | https://developers.openai.com/api/docs/guides/prompt-engineering | 支持“任务、输入、约束、输出要分开写”的提示词边界。 |
| OpenAI Retrieval guide | https://developers.openai.com/api/docs/guides/retrieval | 支持“向量库作为索引、语义检索返回相关 chunk、结果可带来源文件”的检索链路。 |
| OpenAI Vector embeddings guide | https://developers.openai.com/api/docs/guides/embeddings | 支持“文本转成向量后可做搜索、聚类和相似度排序”的向量表示理解。 |
| OpenAI File search guide | https://developers.openai.com/api/docs/guides/tools-file-search | 支持“文件搜索是托管工具，能对上传文件做语义和关键词检索”的工具边界。 |
| OpenAI File inputs guide | https://developers.openai.com/api/docs/guides/file-inputs | 支持“长文件更适合走 File Search，而不是直接整份塞进输入”的选型判断。 |
| OpenAI Using tools guide | https://developers.openai.com/api/docs/guides/tools | 支持“文件检索、web search、function calling 属于不同工具边界”的工具分工。 |

## Source-To-Unit Notes

- 本页先把 RAG 定位成“先找证据，再让模型基于证据回答”，而不是“向量库 + 生成模型”的简单拼接。
- 离线段要讲清楚：抽取正文、切块、保留 metadata、建立索引。chunk 粒度和 metadata 直接影响后面的召回、引用和排错。
- 在线段要讲清楚：问题向量化、检索候选、可选重排、上下文拼接、生成约束。每一步都要能打印中间结果。
- 这页会把“答案是否被资料支持”“资料缺失时是否拒答”“引用能否回指原文”当成最小验收条件。
- 08 页结束后，下一页 09 会继续把这条链路接进 Agent 的规划、工具和执行流程。

## Gaps And Notes

- 没有绑定某个私有知识库、客服系统或项目仓库，所以页面例子使用教学用的报销制度、API 文档和课程笔记场景。
- 目前不引入特定 SDK 版本、向量库产品或评测平台；如果以后要落到具体产品，需要再核对当时的官方文档版本。
- 例子中的检索、重排和引用格式是教学结构，不等同于某个托管服务的唯一实现。
