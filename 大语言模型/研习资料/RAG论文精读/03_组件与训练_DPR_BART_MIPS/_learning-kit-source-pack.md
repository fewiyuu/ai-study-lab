# RAG 论文精读 03｜组件与训练：DPR、BART、MIPS

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

- 本页承接第 02 节的 latent document 与 marginalization，聚焦论文 2.2 Retriever、2.3 Generator、2.4 Training，以及实验里的 retrieval ablations。
- 核心来源是：retriever 采用 DPR bi-encoder；`d(z)=BERT_d(z)`、`q(x)=BERT_q(x)`；top-K 检索是 MIPS 问题；generator 采用 BART-large，把输入 `x` 与 retrieved content `z` 直接拼接；训练目标是最小化 target 的 negative marginal log-likelihood；优化使用 Adam。
- 论文明确说训练时固定 document encoder 与文档索引，只 fine-tune query encoder `BERT_q` 和 BART generator。
- Appendix C 的训练设置只作为工程背景：December 2018 Wikipedia、21M 个 100-word chunks、FAISS 的 HNSW 近似、CPU 上约 100GB 索引内存、压缩后约 36GB、8 张 32GB V100、mixed precision、Fairseq。
- Appendix D 的多答案处理只作为边界例子：NQ/WQ 多个 `(q, a)` 对；TriviaQA 过滤不在 top 1000 文档中的候选答案；CuratedTrec 从 top 1000 文档里挑 regex 匹配最多的监督目标。

## This Unit Covers

- DPR 的 query encoder / document encoder 分工。
- MIPS 为什么是检索核心，FAISS 在这里扮演什么角色。
- BART 在 RAG 里为什么叫 parametric memory。
- 训练时哪些参数更新，哪些对象固定。
- learned retrieval、frozen retriever、BM25 消融分别说明什么。
- 工程上为什么固定索引、以及这会带来什么代价。

## Gaps

- 本页不展开 DPR 的预训练细节，只用它作为 retriever 初始化和索引构建的起点。
- 本页不讲解码主流程，相关差异放回第 02 节和后续任务适配单元。
- 本页不复述主结果表的全部数值，只抽出和训练信号、检索更新有关的证据。
