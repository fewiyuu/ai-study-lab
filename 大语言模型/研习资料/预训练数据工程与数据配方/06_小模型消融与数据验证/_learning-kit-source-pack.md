# Source Pack: 小模型消融与数据验证

## Source Boundary

- Course: 预训练数据工程与数据配方
- Unit: 06_小模型消融与数据验证
- Snapshot: access date 2026-06-21
- Source types: existing course index, neighboring unit pages, and the public sources listed below.

## Source-To-Unit Notes

- This unit sits after 05_数据配方_来源比例与阶段 and before 07_可复现流水线与运行记录.
- The learner should already understand parsing, filtering, deduplication, contamination control, and source mixing.
- The page should separate four related but different decisions:
  - proxy-model ablation: whether a data change helps under a controlled small training budget
  - unified evaluation: which benchmark protocol makes two runs comparable
  - validation of a rule: whether a filter or threshold removes noise without over-pruning useful data
  - evidence lifecycle: when a short-run signal is enough, when to inspect samples, and when to ask for a longer run
- The teaching emphasis should be:
  - small-model results are an early signal, not the final recipe
  - a fair comparison fixes model, budget, tokenizer, sampling, and evaluation protocol
  - validation must inspect kept, removed, and borderline samples
  - logging and checkpoints matter because recipe decisions must be reproducible later

## Source Facts

- Meta Llama 3 says the models were pretrained on over 15T public tokens, with over 5% non-English data and four times more code than Llama 2. It also describes heuristic filters, NSFW filters, semantic deduplication, text classifiers, extensive data-mix experiments, and scaling laws that helped choose the final mix.
- The Llama 3 blog also notes that the models were trained on 8,192-token sequences with a mask so self-attention does not cross document boundaries.
- FineWeb is described as more than 18.5T tokens of cleaned and deduplicated English web data from CommonCrawl, originally 15T tokens. Its pipeline ran on DataTrove and includes URL filtering, Trafilatura extraction, FastText language filtering, quality filtering, MinHash deduplication per crawl, and PII formatting.
- FineWeb reports that deduplicating each crawl individually outperformed deduplicating the whole dataset as one unit in its ablations.
- DataTrove describes a platform-agnostic pipeline built around `Document` objects with `text`, `id`, and `metadata`, plus readers, writers, extractors, filters, stats, token blocks, and dedup blocks.
- DataTrove also documents logging directories, completion markers, and skipped tasks for resumable runs, which are useful when a recipe has to be audited later.
- DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining argues that mixture proportions across domains materially affect LM performance. It trains a small proxy model with Group DRO to produce domain weights, then resamples the dataset with those weights before training a larger model.
- DoReMi reports that the reweighted mixture improves downstream accuracy and reaches baseline performance with fewer training steps.
- OLMo 2 introduces a specialized data mix, Dolmino Mix 1124, via late-stage curriculum training during the annealing phase of pretraining.
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
- Treat the exact thresholds, benchmark lists, and example percentages as teaching examples unless a cited source states them directly.
- Treat recipe recommendations as editorial synthesis when they combine multiple public sources.
- The page should not claim that one validation protocol is universally optimal; it should explain how to justify and test a recipe for a specific model goal.
