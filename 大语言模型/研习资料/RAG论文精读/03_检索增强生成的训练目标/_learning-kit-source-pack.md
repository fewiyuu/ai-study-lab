# RAG 论文精读 03｜检索增强生成的训练目标

## Source Boundary

- 课程根索引：`../index.html`
- 论文本体：`../../../../../50_资源/论文/2005.11401v4.pdf`
- 本地抽取文本：`../../../../../50_资源/论文/2005.11401v4.txt`
- 相邻单元参考：`../02_概率模型_RAG-Sequence与RAG-Token/学习页.html`

## Snapshot

- 论文：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- arXiv：2005.11401
- 本地 PDF / TXT：仓库内已有副本，文件时间为 2026-06-06
- 访问日期：2026-06-21

## Source-To-Unit Notes

- 本页承接第 02 节的 latent document 与 marginalization，聚焦论文 2.4 Training。
- 核心来源是：训练语料为输入/输出对 `(x_j, y_j)`；训练目标是最小化目标的 negative marginal log-likelihood；优化使用 Adam；论文联合训练 query encoder `BERT_q` 和 BART generator，但固定 document encoder `BERT_d` 与文档索引。
- 本页也使用 Retrieval Ablations 中 learned retrieval / fixed retriever / BM25 的比较，说明训练目标为什么能给检索器提供任务信号。
- Appendix C 的训练设置只作为工程背景：Fairseq、mixed precision、8 张 32GB V100、FAISS CPU MIPS、Wikipedia 索引约 100GB，后续压缩到 36GB。
- Appendix D 的多答案处理只作为边界例子：NQ/WQ 用多个 `(q, a)` 对训练；TriviaQA 过滤不在 top 1000 文档中的候选答案；CuratedTrec 会从 top 1000 文档里挑 regex 匹配最多的监督目标。

## This Unit Covers

- negative marginal log-likelihood 在 RAG 训练里的含义。
- 为什么“没有文档标签”仍然能训练 retriever。
- 哪些参数更新：`BERT_q` 与 BART generator。
- 哪些对象固定：`BERT_d` 与 Wikipedia vector index。
- 固定索引的工程原因和代价。
- learned retrieval、fixed retriever、BM25 消融怎样帮助理解训练目标。

## Gaps

- 本页不展开 DPR bi-encoder、BART 架构、MIPS/FAISS 的完整实现；那些属于旧第 03 或后续组件页。
- 本页不读实验主表的具体数值排名，只用消融结论解释训练信号。
- 本页不讲解码细节；解码差异在第 02 节已有铺垫，后续任务适配单元再展开。
