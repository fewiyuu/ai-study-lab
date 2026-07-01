# RAG 论文精读 06｜记忆更新与边界：热替换空文档与检索坍塌

## Source Boundary

- 课程根索引：`../index.html`
- 论文本体：`../../../../../50_资源/论文/2005.11401v4.pdf`
- 本地抽取文本：`../../../../../50_资源/论文/2005.11401v4.txt`
- 前一单元：`../05_实验结果与消融_主结论怎么读/学习页.html`
- 后一单元：`后续课程页，不在本页展开`

## Snapshot

- 论文：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- arXiv：2005.11401
- 本地 PDF / TXT：仓库内已有副本，文件时间为 2026-06-06
- 访问日期：2026-06-21

## Source-To-Unit Notes

- 本页主读论文第 4.5 节 Additional Results，以及 Appendix F / G / H 中和边界有关的部分。
- Table 6 负责回答“学到的检索是否真有用”：freeze retriever、换 BM25、保留 learned retrieval，三种设置分别在测什么。
- “Index hot-swapping” 用 2016 / 2018 两个 Wikipedia 索引回答世界领导人问题，说明外部记忆版本可以直接影响答案。
- “Effect of Retrieving more documents” 说明测试时调 K 会改变效果和代价，RAG-Sequence 和 RAG-Token 的趋势不完全一致。
- Appendix F 讨论 null document：给空证据一个显式位置，但几种做法都没有带来收益，所以主模型省略。
- Appendix G 负责参数规模对照，用来压住“只靠参数记忆就够了”的过度外推。
- Appendix H 说明 retrieval collapse：某些任务里检索器会学成总取同一批文档，生成器随后忽略文档，系统退化到近似 BART。
- Broader Impact 段落把收益和风险一起说清：更事实的系统也可能放大偏见、错误和滥用。

## This Unit Covers

- 先把“外部记忆可编辑”讲明白，再讲“编辑以后为什么还会失效”。
- 用状态账本把索引版本、检索器、生成器、空文档和 K 值放在一张表里看。
- 用 Table 6、Figure 3、Appendix F/H 读出论文的边界，而不是只记结论。
- 把热替换、无答案处理、检索坍塌和风险控制区分开。

## Gaps

- 本页不重讲第 02 节概率公式，也不重复第 03 节训练目标。
- 本页不展开 FEVER 证据句抽取的实现细节。
- 本页不把本论文的结论直接外推成所有 RAG 系统的统一答案。
