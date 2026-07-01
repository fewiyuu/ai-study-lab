# RAG 论文精读 01｜论文导读：参数记忆与非参数记忆

## Source Boundary

- 课程根索引：`../index.html`
- 旧学习页：`./学习页.html`
- 论文本体：`../../../../50_资源/论文/2005.11401v4.pdf`
- 本地抽取文本：`../../../../50_资源/论文/2005.11401v4.txt`

## Snapshot

- 论文：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- arXiv：2005.11401
- 本地 PDF / TXT：仓库内已有副本，文件时间为 2026-06-06
- 复核时间：2026-06-21

## Source-To-Unit Notes

- 课程索引负责说明这 6 个单元的顺序和分工；本单元是第一块，先讲为什么 RAG 要把检索接到生成前面。
- 旧学习页已经覆盖了 Abstract、Introduction、Figure 1、三类任务例子、参数记忆 / 非参数记忆、以及练习闭环；重构时保留这些事实骨架，但把表达收紧成更清楚的教学链。
- 本地 PDF / TXT 用来核对术语、Figure 1 的链路、RAG-Sequence / RAG-Token 的文字语义，以及后续单元要引用的实验与边界位置。

## This Unit Covers

- 语言模型为什么会遇到“记得住，但难更新、难引用、难检查”的问题。
- 参数记忆和非参数记忆的分工。
- Figure 1 里“查询 -> 检索 -> 条件生成 -> 文档边际化”的链路。
- 论文把 RAG 讲成通用 seq2seq 配方时，真正依赖的前提是什么。

## Gaps

- 这一页只负责开场和机制入门，不展开实验表、消融结论和更新边界。
- 如果后续单元要引用具体图表编号、实验设置或结果数值，继续回到本地 PDF / TXT 复核。
