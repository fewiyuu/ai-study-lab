# Source Pack: 数据工程全景：从网页到token

## Source Boundary

- Course: 预训练数据工程与数据配方
- Unit: 01_数据工程全景_从网页到token
- Snapshot: access date 2026-06-20
- Source types: existing course index, existing unit page, public source links already cited by the course index.

## Source-To-Unit Notes

- Course index maps this unit as the foundation for the data lifecycle: raw data -> document -> sample -> token -> shard.
- Existing unit page provides the main teaching spine: object chain, pipeline steps, tool view, worked cases, and diagnostic exercises.
- Course index sources support the broader course context:
  - Stanford CS336 spring 2025 data materials for the end-to-end data pipeline.
  - NeMo Curator and DataTrove for filtering, deduping, and pipeline design.
  - FineWeb papers/blog for data validation and recipe experiments.
  - OLMo 2 for source transparency and training record conventions.

## Source Facts

- raw data refers to source material before document extraction.
- document is the治理对象 after正文抽取 and metadata retention.
- sample is the training input unit after packing or windowing.
- token is the tokenizer output used by the loss.
- shard is the storage/read unit for distributed training.
- The first-stage distinction that matters most is document vs sample.
- Another distinction that matters is token vs shard.

## Gaps

- No additional upstream lecture note or repository snapshot is available in this workspace.
- The page should stay within the public course index and existing page boundary, and not claim stronger source specificity than the current material supports.
- Operational details beyond the current course page and index should be treated as unit-level teaching recommendations, not source claims.
