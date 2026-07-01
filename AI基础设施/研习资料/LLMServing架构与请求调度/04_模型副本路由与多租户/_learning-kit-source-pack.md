# LLM Serving 架构与请求调度｜单元 04 来源包

## Source Boundary

- Course root: `30_研究/AI基础设施/研习资料/LLMServing架构与请求调度`
- Unit: `04_模型副本路由与多租户`
- Snapshot / access date: 2026-06-21
- This rebuild uses the existing course index, the legacy unit page, and the public reference set listed in the course index. It does not crawl new remote material during page production.

## Source-To-Unit Notes

- The course index places this unit after queue / Admission Control / backpressure and before autoscaling / batching / resource isolation. The page should therefore assume a request has already been admitted, then explain where it is routed.
- The legacy page gives the local unit scope: model replicas, routing policies, multi-tenant isolation, cache-aware routing, route logs, common incidents, and diagnostic practice.
- Ray Serve and Ray Serve LLM documentation support the service-layer concepts: deployment, replica, router, OpenAI-compatible service, autoscaling surface, and metrics.
- vLLM documentation supports the engine-facing boundary: OpenAI-compatible serving, scheduler behavior, prefix cache / cache-aware considerations, and request-level runtime pressure.
- SGLang documentation is used as an additional public serving/runtime reference for router and server concepts.
- TensorRT-LLM documentation supports the production inference vocabulary around high-performance serving, batching, scheduling, and backend constraints.

## Unit Boundary

This unit teaches routing and tenancy decisions after admission:

- route from public model name to model family, version, tenant policy, resource pool, and replica
- read routing state and record route decisions for later diagnosis
- balance fairness, cache locality, latency, and rollout safety
- explain common incidents such as hot tenants, cache-unfriendly routing, stale replicas, and version drift

It intentionally does not teach full autoscaling policy, GPU resource isolation internals, Kubernetes scheduling, or SLO capacity planning. Those are handled by later units in the course.

## Public References

- Ray Serve LLM documentation: https://docs.ray.io/en/latest/serve/llm/index.html
- Ray Serve documentation: https://docs.ray.io/en/latest/serve/index.html
- vLLM documentation: https://docs.vllm.ai/en/latest/
- TensorRT-LLM documentation: https://nvidia.github.io/TensorRT-LLM/
- SGLang documentation: https://docs.sglang.ai/
