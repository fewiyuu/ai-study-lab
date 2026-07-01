# RAG 论文精读 04｜解码与任务适配：从 QA 到分类

## Source Boundary

- 课程根索引：`../index.html`
- 论文本体：`../../../../../50_资源/论文/2005.11401v4.pdf`
- 本地抽取文本：`../../../../../50_资源/论文/2005.11401v4.txt`
- 相邻单元参考：`../03_组件与训练_DPR_BART_MIPS/学习页.html`
- 后续单元参考：`../05_实验结果与消融_主结论怎么读/学习页.html`

## Snapshot

- 论文：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- arXiv：2005.11401
- 本地 PDF / TXT：仓库内已有副本，文件时间为 2026-06-06
- 访问日期：2026-06-21

## Source-To-Unit Notes

- 本页承接第 03 节的 retriever / generator / index 结构，专讲论文 2.5 Decoding 与 3 Experiments 里和任务适配有关的部分。
- 2.5 说明测试时的两种近似：RAG-Token 可以像标准自回归模型一样解码；RAG-Sequence 不能直接单次 beam search，需要先按文档分别 beam，再做跨文档重计分。论文把两种做法称为 Thorough Decoding 和 Fast Decoding。
- 3.1 QA 结果对应 Open-domain QA 的 EM；2.5 的解码设置和 Appendix A 的实现细节共同说明为什么 QA 使用 50 retrieved documents、Thorough Decoding、而且 greedy decoding 已足够。
- 3.2 / 3.3 讲生成任务：Open MS-MARCO 关注 BLEU-1、Rouge-L；Jeopardy question generation 关注 BLEU-1、Q-BLEU-1 和人评。这里最值得读的是“RAG-Token 在 Jeopardy 上更好”的原因分析。
- 3.4 讲 FEVER：把 supports / refutes / not enough info 映射成单 token 直接训练，输出长度为 1，因此 RAG-Sequence 与 RAG-Token 在这个任务上等价。Appendix E 再补一句：论文主要覆盖分类，不展开证据句抽取子任务。
- Table 1 / Table 2 / Table 6 / Figure 2 是本页的实验依据；Appendix A 给出 QA、MS-MARCO、Jeopardy 的检索文档数、beam size、Fast / Thorough Decoding 取舍；Appendix E 给出 FEVER 分类的实现说明。

## This Unit Covers

- RAG-Token 和 RAG-Sequence 在测试时为什么需要不同解码策略。
- Thorough Decoding 与 Fast Decoding 的差别。
- QA、MS-MARCO、Jeopardy、FEVER 四类任务各自怎么写成文本输出。
- 为什么 FEVER 的分类可以被写成长度为 1 的生成任务。
- 哪些指标适合自动评估，哪些地方必须看人评或任务边界。

## Gaps

- 本页不再回讲第 02 节的概率公式和 latent document 细节，只在解码处引用它。
- 本页不展开第 03 节的 retriever 训练，只把它当成本页解码与任务适配的前提。
- 本页不把 FEVER 的证据句抽取当作主讲内容，那里留给更专门的任务页或后续复盘。
