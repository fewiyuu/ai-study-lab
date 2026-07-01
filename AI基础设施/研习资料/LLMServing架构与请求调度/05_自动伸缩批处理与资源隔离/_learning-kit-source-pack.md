# LLM Serving 架构与请求调度｜单元 05 来源包

## Source Boundary

- Course root: `LLMServing架构与请求调度`
- Unit: `自动伸缩、批处理与资源隔离`
- Snapshot / access date: 2026-06-22
- This rebuild uses the existing course index, the legacy unit page in the same
  folder, and the public reference set already listed in the course index. No
  new remote crawl was needed during page production.

## Source-To-Unit Notes

- `../index.html` fixes the course sequence. It places this unit after
  routing and multitenancy, and before SLO / observability / capacity
  planning. That placement sets the lesson boundary: the page should explain
  replica count, batching, and resource isolation after requests have already
  been admitted and routed.
- `./学习页.html` is the legacy teaching page in this folder. It provides the
  local lesson chain: scaling object, batching tradeoff, isolation policy,
  route/state ledger, diagnostic loop, worked cases, and practice structure.
- Ray Serve and Ray Serve LLM documentation support the service-layer concepts:
  autoscaling targets, replica state, queue visibility, and deployment
  vocabulary.
- vLLM documentation supports the engine-facing boundary: scheduler behavior,
  batch token budgets, and runtime pressure around prompt length and output
  length.
- TensorRT-LLM documentation supports the production inference vocabulary
  around in-flight batching, chunked input handling, and backend constraints.
- SGLang documentation is used as an additional public serving/runtime
  reference for queue, batching, and capacity tuning vocabulary.

## Unit Boundary

This unit teaches three linked decisions after admission and routing:

- how many replicas to keep warm, and when to scale them
- how large a batch budget to allow before TTFT and tail latency bend upward
- how to split long-context, short-interactive, and batch-style traffic so they
  do not compete in one shared pool

It intentionally does not teach replica routing, SLO math, Kubernetes
placement, or full incident response. Those topics are handled by neighboring
course units.

## Gaps And Editorial Decisions

- Metric names, counters, and defaults drift across releases. The page teaches
  stable inspection habits instead of freezing one vendor-specific snapshot as
  if it were permanent.
- The capacity formula in the lesson is an operating estimate, not a public
  promise from any single framework. It is useful for first-pass planning and
  should be corrected by actual traffic and length distributions.
- The page uses a state ledger to keep replica state, queue depth, batch
  budget, and route reasoning separate during diagnosis. That is a teaching
  choice, not a claim that any single runtime exposes those fields with the
  same names.

## Public References

- Ray Serve autoscaling guide: https://docs.ray.io/en/latest/serve/autoscaling-guide.html
- Ray Serve LLM documentation: https://docs.ray.io/en/latest/serve/llm/index.html
- Ray Serve documentation: https://docs.ray.io/en/latest/serve/index.html
- vLLM documentation: https://docs.vllm.ai/en/latest/
- TensorRT-LLM documentation: https://nvidia.github.io/TensorRT-LLM/
- SGLang documentation: https://docs.sglang.ai/
