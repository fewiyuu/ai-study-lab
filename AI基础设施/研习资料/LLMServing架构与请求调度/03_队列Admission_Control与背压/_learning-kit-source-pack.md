# LLM Serving 架构与请求调度｜单元 03 来源包

## Source Boundary

- Course root: `LLMServing架构与请求调度`
- Unit: `队列、Admission Control 与背压`
- Snapshot / 访问日期: 2026-06-21
- This rebuild uses the course map, the legacy unit page in the same folder,
  and the public reference set already listed in the course index. No new
  network crawl was needed for the local reconstruction pass beyond verifying
  official docs names and stable behavior.

## Source-To-Unit Notes

- `../index.html` fixes the course scope and the neighboring units. It places
  this unit after OpenAI-compatible API and stream semantics, and before model
  replica routing, autoscaling, SLO, Ray Serve LLM, and production issues.
- `学习页.html` in this folder provides the original teaching material:
  queueing, admission control, backpressure, load patterns, error mapping,
  metrics, and practice structure.
- Public references already listed in the course index support the stable
  terminology used in this unit:
  - Ray Serve docs for replica concurrency, queue limits, backpressure, and
    503 rejection behavior.
  - vLLM docs for continuous batching, chunked prefill, prefix caching, and
    scheduler behavior.
  - SGLang docs for model routing, server arguments, queue depth signals, and
    gateway behavior.
  - TensorRT-LLM docs for in-flight batching, chunked context, KV cache, and
    request scheduling.

## Gaps And Editorial Decisions

- Queue limits, scheduler defaults, and performance counters can drift across
  releases. The page therefore teaches stable patterns and names concrete
  config points as version-sensitive rather than freezing one exact runtime
  snapshot.
- The unit stops before replica routing and autoscaling. Those topics belong to
  the next units and should not be folded into this page.
- The legacy page used a monolithic shell and only a few diagnostic questions.
  The 1.0 rebuild expands the practice loop, adds explicit state traces and
  control-path tables, and moves the page into the shared study-page shell.
