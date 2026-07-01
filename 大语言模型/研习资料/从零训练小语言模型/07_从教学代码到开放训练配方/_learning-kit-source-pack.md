# Source Pack: 从教学代码到开放训练配方

## Source Boundary

- Course: 从零训练小语言模型
- Unit: 07 从教学代码到开放训练配方
- Snapshot: 2026-06-21
- Access date: 2026-06-21
- Local inputs: course-root `index.html`, the current unit page `学习页.html`, and the course shell / runtime assets already installed in this course root.

## Source-To-Unit Notes

- The course index places this unit after `Scaling、验证集与评估` and before `小规模复现实验设计`, so the page should bridge from evaluation judgment into a publicly auditable training recipe.
- The existing unit page already frames the right learning target: distinguish a toy run from a public training report, then read data, hyperparameters, evaluation protocol, stage logs, and artifact traceability as evidence.
- Public source labels already visible in the existing page copy are `Stanford CS336: Language Modeling from Scratch`, `karpathy/llm.c`, `OLMo 2` paper, and the `OLMo` project page. Keep those labels as source references and do not invent extra paper claims or numbers.
- This unit should stay at the recipe-and-report level: what a training report must disclose, how to tell open weights from fully open training, and how to write a cautious boundary statement.

## Unit Boundary

- This page covers: toy-run versus recipe distinction, data provenance, token mix, filtering and deduplication, hyperparameter bookkeeping, evaluation protocol, stage or checkpoint lineage, artifact traceability, and reproducibility boundaries.
- This page does not cover: benchmark implementation details, dataset curation pipelines, or full open-training scaling recipes. Those belong to adjacent or later units.
- Keep the anchor examples at the level of a small report table, a traceable evidence chain, a stage note, and a boundary statement. Do not turn this page into a paper-by-paper survey or a model-release press note.

## Gaps

- No local repository snapshot, benchmark log, or private implementation transcript is provided, so do not claim specific repository filenames, code paths, scores, or training numbers beyond the public labels above.
- Avoid inventing exact benchmark results, dataset sizes, or checkpoint counts unless the page shows them as teaching examples only.
- If later unit pages need repository-specific operational details, create a new source pack for that unit rather than stretching this one.
