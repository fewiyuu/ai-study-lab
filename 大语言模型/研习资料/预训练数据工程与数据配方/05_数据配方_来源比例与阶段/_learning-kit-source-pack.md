# Source Pack: 数据配方、来源比例与阶段

## Source Boundary

- Course: 预训练数据工程与数据配方
- Unit: 05_数据配方_来源比例与阶段
- Snapshot: access date 2026-06-21
- Source types: existing course index, neighboring unit pages, and the public sources listed below.

## Source-To-Unit Notes

- This unit sits after 04_去重去污染与泄漏控制 and before 06_小模型消融与数据验证.
- The learner should already understand data ingestion, filtering, deduplication, contamination control, and leakage boundaries.
- The page should separate four related but different decisions:
  - source selection: which data pools exist and what capability each pool contributes
  - source weighting: how much each pool should be sampled during training
  - stage scheduling: when a pool should be emphasized or reduced during pretraining
  - validation feedback: which metrics or ablations should change the next recipe
- The teaching emphasis should be:
  - inventory size is not the same as training share
  - sampling weight is a decision, not a fact about the data itself
  - stage coefficients can change the same source's role over time
  - recipe quality is judged by downstream effects, not by a prettier ratio table

## Source Facts

- Meta Llama 3 documents that the models were pretrained on over 15T public tokens, with over 5% non-English data, four times more code than Llama 2, and filtering pipelines that include heuristic filters, NSFW filters, semantic deduplication, and text classifiers. It also states that extensive experiments were used to choose the best mix of data sources, and that scaling laws helped select an optimal data mix.
- The Llama 3 blog also notes that the models were trained on 8,192-token sequences with a mask so self-attention does not cross document boundaries.
- DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining argues that mixture proportions across domains materially affect LM performance. It uses a small proxy model with Group DRO to infer domain weights, then resamples a dataset with those weights before training a larger model.
- DoReMi reports that the reweighted mixture improves downstream accuracy and reaches baseline performance with fewer training steps.
- FineWeb is described as cleaned and deduplicated English web data from CommonCrawl. The dataset page says the pipeline used DataTrove, and the processing steps include URL filtering, Trafilatura extraction, FastText language filtering, quality filtering, MinHash deduplication per crawl, and PII formatting.
- FineWeb also reports that deduplicating each crawl individually outperformed deduplicating the whole dataset as one unit in its ablations.
- DataTrove describes a platform-agnostic pipeline with `Document` objects (`text`, `id`, `metadata`), plus readers, writers, extractors, filters, stats, token blocks, and dedup blocks.
- DataTrove also emphasizes logging directories, completion markers, and skipping completed tasks, which are useful for making a recipe reproducible and resumable.
- OLMo 2 states that a new specialized data mix, Dolmino Mix 1124, was introduced via late-stage curriculum training during the annealing phase of pretraining.
- OLMo 2 also emphasizes fully released artifacts, training logs, checkpoints, and recipes, which makes the recipe auditable rather than opaque.

## Public Source Context

- Meta Llama 3 blog:
  https://ai.meta.com/blog/meta-llama-3/
- DoReMi paper:
  https://arxiv.org/abs/2305.10429
- OLMo 2 paper:
  https://arxiv.org/abs/2501.00656
- FineWeb dataset page:
  https://huggingface.co/datasets/HuggingFaceFW/fineweb
- DataTrove repository:
  https://github.com/huggingface/datatrove

## Gaps

- No upstream unit handout is available in this workspace for this page.
- Treat the exact percentages in examples as teaching examples unless a cited source states them directly.
- Treat source mix recommendations as editorial synthesis when they combine multiple public sources.
- The page should not claim that a single recipe is universally optimal; it should explain how to justify and test a recipe under a specific model goal.
