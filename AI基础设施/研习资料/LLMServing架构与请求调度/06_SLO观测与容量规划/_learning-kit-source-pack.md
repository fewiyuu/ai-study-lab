# LLM Serving 架构与请求调度｜单元 06 来源包

## Source Boundary

- Course root: `LLMServing架构与请求调度`
- Unit: `SLO、观测与容量规划`
- Snapshot / access date: 2026-06-22
- This rebuild uses the course index, the legacy unit page in the same folder,
  and the public reference set already listed in the course index. No new
  remote crawl was needed during page production.

## Source-To-Unit Notes

- `../index.html` fixes the course sequence. It places this unit after
  batching, autoscaling, and resource isolation, and before Ray Serve LLM and
  production fault handling. That placement sets the lesson boundary: the page
  should explain SLOs, observability signals, and capacity planning, but not
  expand deployment topologies or incident response in full.
- `./学习页.html` is the legacy teaching page in this folder. It provides the
  original lesson chain: SLO definitions, metric decomposition, worked
  capacity estimates, common mistakes, and diagnostic practice structure.
- The public reference set named by the course index supports the stable
  vocabulary used in this unit:
  - Ray Serve and Ray Serve LLM docs for service-layer metrics, replica state,
    autoscaling surface, and deployment vocabulary.
  - vLLM docs for serving throughput, batching, scheduler behavior, and
    latency/throughput vocabulary.
  - TensorRT-LLM docs for high-performance serving, KV cache, batching, and
    backend constraints.
  - SGLang docs for serving/runtime concepts that overlap with routing and
    server telemetry.
  - OpenTelemetry docs for traces, metrics, and logs as the surrounding
    observability stack.

## Gaps And Editorial Decisions

- Metric names, counters, and defaults can drift across releases. The page
  therefore teaches stable patterns and inspection habits instead of freezing
  one vendor-specific snapshot as if it were permanent.
- The capacity formula in the lesson is an operating estimate, not a public
  promise from any single framework. It is useful for first-pass planning and
  should be corrected by actual traffic and length distributions.
- The page stops before deployment shape, route selection, and production
  incidents. Those topics belong to later course units and should not be folded
  into this one.
