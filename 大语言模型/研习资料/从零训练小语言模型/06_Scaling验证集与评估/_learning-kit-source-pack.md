# Source Pack: Scaling、验证集与评估

## Source Boundary

- Course: 从零训练小语言模型
- Unit: 06 Scaling、验证集与评估
- Snapshot: 2026-06-21
- Access date: 2026-06-21
- Local inputs: course-root `index.html` and the existing unit page `学习页.html` for the same unit.

## Source-To-Unit Notes

- The course index places this unit after GPU systems and before open training recipes, so this page should focus on reading training signals and protecting evaluation conclusions, not on systems tuning.
- Stanford CS336 Spring 2025 establishes the broader course path from training mechanics into scaling, evaluation, and data concerns. Use it for unit placement and for the fact that scaling and evaluation are part of the main path, not a side topic.
- Public references already visible in the existing page copy include `Scaling Laws for Neural Language Models`, `Training Compute-Optimal Large Language Models`, `Holistic Evaluation of Language Models`, `Language Models are Few-Shot Learners`, the contamination report, and Paloma. Keep them as source labels only; do not expand beyond what the existing page already supports.
- This rewrite should keep the unit at the evaluation-judgment level: loss curves, validation design, scaling intuition, benchmark protocol, contamination, and report boundaries.

## Unit Boundary

- This page covers: training vs validation loss, perplexity, held-out design, domain splits, scaling-law intuition, evaluation protocol, contamination/leakage, and how to write a cautious model-evaluation conclusion.
- This page does not cover: full benchmark implementation, dataset curation pipelines, or detailed scaling-law fitting methodology. Those belong to neighboring or later units.
- Keep the anchor examples at the level of a small loss calculation, a validation-split checklist, a scaling comparison, and an evaluation-pitfall diagnosis. Do not stretch this page into a paper-by-paper survey.

## Gaps

- No local training transcript, benchmark log, or repository snapshot was provided for a private implementation, so do not claim repository-specific filenames or performance numbers beyond the public source labels above.
- Avoid inventing exact benchmark scores, scaling-fit constants, or contamination rates unless the page shows them as examples only.
- If later unit pages need repository-specific operational details, create a new source pack for that unit instead of stretching this one.
