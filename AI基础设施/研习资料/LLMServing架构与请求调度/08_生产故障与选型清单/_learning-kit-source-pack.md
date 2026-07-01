# LLM Serving 架构与请求调度｜单元 08 来源包

## Source Boundary

- Course root: `LLMServing架构与请求调度`
- Unit: `生产故障与选型清单`
- Snapshot / access date: 2026-06-22
- This rebuild uses the course index, the legacy unit page in the same folder,
  and the public reference set already listed in the course index. No new
  remote crawl is needed during page production.

## Source-To-Unit Notes

- `../index.html` fixes the course order. This unit closes the course by
  turning the earlier layers into an operational checklist: fault signals,
  failure diagnosis, framework boundary, and rollout/rollback decision.
- `./学习页.html` is the legacy teaching page in this folder. It already
  contains the production fault stories, framework selection table, and
  preflight checklist that should remain the lesson spine.
- The public reference set named by the course index supports the stable
  vocabulary used in this unit:
  - Ray Serve LLM and Ray Serve docs for service-layer deployment,
    autoscaling, replica, router, and metrics vocabulary.
  - vLLM docs for OpenAI-compatible serving, batching, scheduler behavior,
    and serving metrics.
  - SGLang docs for runtime, structured generation, router, and production
    deployment vocabulary.
  - TensorRT-LLM docs for high-performance serving, batching, KV cache, and
    backend deployment vocabulary.
  - OpenTelemetry docs for traces, metrics, and logs in the surrounding
    observability stack.

## Gaps And Editorial Decisions

- Framework names and defaults drift across releases. The page therefore
  teaches stable operating patterns instead of freezing one vendor snapshot as
  if it were permanent.
- The selection table should explain which layer each framework owns: ingress,
  service orchestration, engine/runtime, or GPU backend. That keeps the page
  from collapsing into a generic benchmark comparison.
- The unit stops before Kubernetes platform design, cross-cluster routing, and
  model kernel tuning. Those belong to other notes or later operational work.
