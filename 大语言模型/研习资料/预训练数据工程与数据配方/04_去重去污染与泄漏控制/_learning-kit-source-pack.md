# Source Pack: 去重、去污染与泄漏控制

## Source Boundary

- Course: 预训练数据工程与数据配方
- Unit: 04_去重去污染与泄漏控制
- Snapshot: access date 2026-06-21
- Source types: existing course index, neighboring unit pages, and the public sources listed below.

## Source-To-Unit Notes

- This unit sits after 03_质量过滤_规则模型与偏差 and before 05_数据配方_来源比例与阶段.
- The learner should already understand raw document ingestion, quality filtering, and basic thresholding.
- This page should separate three related but different problems:
  - exact / fuzzy deduplication inside the training corpus
  - benchmark contamination between training data and evaluation data
  - leakage across split, version, logging, tuning, and review workflows
- The teaching emphasis should be:
  - deduplication is about repeated training mass
  - contamination is about benchmark independence
  - leakage is about information crossing a boundary too early
  - logs and manifests matter because they make the decision reversible

## Source Facts

- NeMo Curator documents exact deduplication with hashing, fuzzy deduplication with MinHash + LSH, and semantic matching with embeddings.
- NeMo Curator task decontamination docs show task preparation plus `find_matching_ngrams` and `remove_matching_ngrams` as a practical contamination workflow.
- DataTrove describes a platform-agnostic pipeline for processing, filtering, and deduplicating large text data.
- FineWeb is a cleaned and deduplicated English web dataset derived from Common Crawl and built with DataTrove.
- FineWeb documentation and blog materials are useful for explaining large-scale cleaning and the deduplication / validation loop.
- The benchmark contamination survey frames contamination as a reliability problem for evaluation rather than a simple string-match problem.
- The rephrased-samples paper is useful for explaining why exact matches are not the whole story and why reformulations still matter.

## Public Source Context

- Official NeMo Curator deduplication docs:
  https://docs.nvidia.com/nemo/curator/curate-text/process-data/deduplication
- Official NeMo Curator task decontamination docs:
  https://docs.nvidia.com/nemo-framework/user-guide/24.07/datacuration/taskdecontamination.html
- Official NeMo Curator text processing concepts:
  https://docs.nvidia.com/nemo/curator/about/concepts/text/data/processing
- DataTrove repository:
  https://github.com/huggingface/datatrove
- FineWeb dataset page and README:
  https://huggingface.co/datasets/HuggingFaceFW/fineweb
  https://huggingface.co/datasets/HuggingFaceFW/fineweb/blob/main/README.md
- Benchmark contamination survey:
  https://arxiv.org/abs/2406.04244
- Rethinking Benchmark and Contamination with Rephrased Samples:
  https://arxiv.org/abs/2311.04850
- Investigating Data Contamination in Modern Benchmarks:
  https://arxiv.org/html/2311.09783v2

## Gaps

- No upstream unit handout is available in this workspace for this page.
- Treat thresholds, signatures, and split rules as teaching examples unless a cited source states them directly.
- Keep implementation guidance at the level supported by the current sources and the neighboring course units.
