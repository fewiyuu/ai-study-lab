# Source Pack: 获取、解析与标准化

## Source Boundary

- Course: 预训练数据工程与数据配方
- Unit: 02_获取解析与标准化
- Snapshot: access date 2026-06-20
- Source types: existing course index, existing unit page, and the public sources already cited by the course index.

## Source-To-Unit Notes

- Course index places this unit immediately after the object-chain overview.
- This unit fills the gap between raw ingestion and later quality filtering.
- The teaching emphasis is on three stable steps:
  - 先获取到原始网页或记录
  - 再抽取正文和保留元数据
  - 最后做编码标准化、记录 schema、分片准备
- The unit should help the learner distinguish:
  - document vs sample
  - extraction vs filtering
  - encoding normalization vs quality judgment
  - metadata for traceability vs text content for training

## Source Facts

- raw data refers to source material before document extraction.
- document is the治理对象 after正文抽取 and metadata retention.
- sample is the training input unit after packing or windowing.
- token is the tokenizer output used by the loss.
- shard is the storage/read unit for distributed training.
- The most important distinction for this unit is document vs raw page.
- The next most important distinction is extraction vs normalization.

## Public Source Context

- Stanford CS336 Spring 2025 data materials support the course-wide data lifecycle.
- NeMo Curator and DataTrove support the idea of extraction, cleaning, and pipeline organization.
- FineWeb materials support the transition from curated documents to validation and data recipe work.
- OLMo 2 supports source transparency and training-record conventions.

## Gaps

- No extra upstream lecture note, repo snapshot, or assignment handout is available in this workspace.
- Keep concrete operational guidance at the level supported by the current course index and page boundary.
- Treat any deeper implementation advice as a teaching recommendation, not as a direct source claim.
