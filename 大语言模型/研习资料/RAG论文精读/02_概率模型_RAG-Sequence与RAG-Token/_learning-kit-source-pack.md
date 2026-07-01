# RAG 论文精读 02｜概率模型：RAG-Sequence 与 RAG-Token

## Source Boundary

- 课程根索引：`../index.html`
- 旧学习页：`./学习页.html`
- 论文本体：`../../../../50_资源/论文/2005.11401v4.pdf`
- 本地抽取文本：`../../../../50_资源/论文/2005.11401v4.txt`

## Snapshot

- 论文：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- arXiv：2005.11401
- 本地 PDF / TXT：仓库内已有副本，文件时间为 2026-06-06
- 访问日期：2026-06-21

## Source-To-Unit Notes

- 课程索引负责说明 6 个单元的顺序和分工；本单元承接第 01 节的动机，进入论文 2.1 Models 和 2.5 Decoding。
- 本页的主线来自 Figure 1、2.1 Models、2.5 Decoding，以及“sequence classification length 1 时两种模型等价”的一句话。
- 旧学习页已经把符号、公式和解码差异展开；这次重构把重点收紧到“求和位置、递推对象、解码方式、分类退化”四个判断上。
- 手算例子和故障排查表是教学补充，不是论文原文数值。

## This Unit Covers

- `p_\eta(z|x)`、`p_\theta(y|x,z)`、top-K 截断和边际化的关系。
- RAG-Sequence：同一篇文档负责整段输出。
- RAG-Token：每个 token 都可以对文档边际化。
- 这两种形式在解码和分类任务上的差别。

## Gaps

- 本页不讲 DPR 训练、BART 结构、MIPS 索引和实验主表；这些放到第 03-05 节。
- 如果后续单元要引用 Table 1/2/3 的具体数字，继续回到本地 PDF / TXT 复核。
