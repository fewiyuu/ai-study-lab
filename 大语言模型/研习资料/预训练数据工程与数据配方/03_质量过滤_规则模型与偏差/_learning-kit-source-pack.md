# Source Pack: 质量过滤、规则模型与偏差

## Source Boundary

- Course: 预训练数据工程与数据配方
- Unit: 03_质量过滤_规则模型与偏差
- Snapshot: access date 2026-06-21
- Source types: existing course index, neighboring unit pages, and the public sources already cited by the course index plus the official sources below.

## Source-To-Unit Notes

- This unit sits after 02_获取解析与标准化 and before 04_去重去污染与泄漏控制.
- The page should assume the learner already has a stable `document` and now needs to decide what to keep, delete, downweight, or quarantine.
- The teaching emphasis should be:
  - 过滤先看信号，不先看结论
  - 规则过滤解决可解释、可快速统计的问题
  - 分类器过滤解决语义型质量判断，但会继承标注偏差
  - 阈值是价值选择，不是纯技术参数
  - 偏差审计要看分桶删除率、来源覆盖和被删样本上下文

## Source Facts

- FineWeb is a large cleaned and deduplicated web dataset derived from Common Crawl snapshots.
- FineWeb-Edu is the educationally filtered branch of that line and uses a classifier trained from Llama3-style annotations; the public collection page describes a 0-5 scale and a threshold of 3 for retaining some high-level educational pages.
- C4 documentation shows that blocklist-style filtering can disproportionately remove text from and about minority individuals.
- NeMo Curator describes a scalable data curation platform with text curation workflows for filtering, deduplication, and formatting.
- DataTrove describes a platform-agnostic pipeline library for processing, filtering, and deduplicating large text data.

## Public Source Context

- Stanford CS336 Spring 2025 data materials support the course-wide data lifecycle.
- FineWeb paper and blog support the scale and the data-quality/validation loop.
- FineWeb-Edu collection and dataset pages support the classifier threshold and educational-quality example.
- C4 case study supports the bias and blocklist discussion.
- NeMo Curator and DataTrove support the operational pipeline and the distinction between rule filters, model filters, and quarantine/review steps.

## Gaps

- No upstream lecture handout or assignment bundle is available in this workspace for this unit.
- Keep implementation guidance at the teaching level supported by the current sources.
- Treat any deeper operational recipe as a recommendation, not as a direct source claim.
