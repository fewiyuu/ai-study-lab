# RAG 论文精读 05｜实验结果与消融：主结论怎么读

## Source Boundary

- 课程根索引：`../index.html`
- 论文本体：`../../../../../50_资源/论文/2005.11401v4.pdf`
- 本地抽取文本：`../../../../../50_资源/论文/2005.11401v4.txt`
- 前一单元参考：`../04_解码与任务适配_从QA到分类/学习页.html`
- 后一单元参考：`../06_记忆更新与边界_热替换空文档与检索坍塌/学习页.html`

## Snapshot

- 论文：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- arXiv：2005.11401
- 本地 PDF / TXT：仓库内已有副本，文件时间为 2026-06-06
- 访问日期：2026-06-21

## Source-To-Unit Notes

- 本页主读论文第 4 节 Results、4.5 Additional Results，以及 Appendix A / E / F / G 中和结果解读有关的部分。
- Table 1 是开放域 QA 的主结果：RAG-Sequence 在 NQ、WebQuestions、CuratedTrec、TriviaQA 等任务上对比 closed-book 和 extractive baseline 的位置。
- Table 2 / Table 3 / Table 4 负责生成与人工评估：Open MS-MARCO、Jeopardy question generation、factuality、specificity。
- FEVER 小节和 Table 2 负责分类任务边界：把 claim label 写成单 token 后，RAG-Sequence 与 RAG-Token 在这个任务上等价；Appendix E 说明主文只讲分类，不展开证据句抽取。
- Table 6 是 ablation 核心：freeze retriever、换 BM25、看 learned retrieval 是否真的有用。
- Figure 3 负责 K 值变化：更多文档不一定总是更好，收益和噪声一起变。
- Appendix A 负责实现层面的检索文档数和解码选择；Appendix F 说明 null document 没带来收益；Appendix G 负责参数规模和 closed-book 对照，用来压住“只靠参数就够了”这种过度外推。

## This Unit Covers

- 结果表该怎么读，先看任务、指标，再看 baseline 和结论。
- QA、生成、分类三类任务为什么不能用同一把尺子量到底。
- 人评在生成任务里补的是什么。
- Frozen retriever、BM25、K 值变化分别在检验什么。
- 哪些结论能收进论文主张，哪些只能算条件成立。

## Gaps

- 本页不重讲第 02 节的概率公式，也不重做第 03 节的训练目标。
- 本页不把 FEVER 的证据句抽取当主任务，只把它作为边界提醒。
- 本页不展开 Appendix C 的所有工程细节，只取和结果解释直接相关的片段。
