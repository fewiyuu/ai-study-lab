# Source Pack: 可复现流水线与运行记录

## Source Boundary

- Course: 预训练数据工程与数据配方
- Unit: 07_可复现流水线与运行记录
- Snapshot: access date 2026-06-22
- Source types: existing course index, neighboring unit pages, and the public sources listed below.

## Source-To-Unit Notes

- This unit sits after 06_小模型消融与数据验证 and before 08_许可隐私与发布边界.
- The learner should already understand filtering, deduplication, source mixing, and small-model validation.
- The page should separate four related but different decisions:
  - pipeline spec: what stages, dependencies, and parameters define a run
  - run record: what evidence is needed to explain a specific execution
  - replay boundary: what must stay fixed for a rerun to be comparable
  - handoff note: what the next operator needs to continue safely
- The teaching emphasis should be:
  - code version alone is not enough for reproducibility
  - input snapshots, tokenizer versions, filter versions, seeds, and checkpoints all matter
  - a manifest is useful only when it records content hashes, sizes, counts, and stage context
  - replayability is judged by whether the next person can continue or explain the same run

## Source Facts

- DataTrove describes a platform-agnostic pipeline built around `Document` objects with `text`, `id`, and `metadata`, plus readers, writers, extractors, filters, stats, token blocks, dedup blocks, logging directories, completion markers, and skipping completed tasks.
- Meta Llama 3 states that its pretraining used 8,192-token sequences and a mask so self-attention does not cross document boundaries.
- OLMo 2 emphasizes fully released artifacts, training logs, checkpoints, and recipes, which makes the recipe auditable rather than opaque.
- FineWeb reports that its pipeline used DataTrove and that crawl-level deduplication choices changed the result, which makes run records and replay boundaries part of the lesson rather than admin overhead.

## Public Source Context

- DataTrove repository:
  https://github.com/huggingface/datatrove
- Meta Llama 3 blog:
  https://ai.meta.com/blog/meta-llama-3/
- OLMo 2 paper:
  https://arxiv.org/abs/2501.00656
- FineWeb dataset page:
  https://huggingface.co/datasets/HuggingFaceFW/fineweb

## Gaps

- No upstream unit handout is available in this workspace for this page.
- Treat the exact field list, checkpoint names, and example YAML blocks as teaching examples unless a cited source states them directly.
- Treat replay and handoff recommendations as editorial synthesis when they combine multiple public sources.
- The page should not claim that a single logging format is universally optimal; it should explain how to record enough evidence for the specific run you need to continue or audit.
