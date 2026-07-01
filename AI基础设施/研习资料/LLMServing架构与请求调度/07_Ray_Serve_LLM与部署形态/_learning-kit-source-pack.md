# LLM Serving 架构与请求调度｜单元 07 来源包

## Source Boundary

- Course root: `LLMServing架构与请求调度`
- Unit: `Ray Serve LLM 与部署形态`
- Snapshot / 访问日期: 2026-06-22
- This rebuild uses the course index, the legacy page in this folder, the
  adjacent unit pages in the same course, and the public documentation links
  already listed in the course index. No new remote crawl was needed during
  page production.

## Source-To-Unit Notes

- `../index.html` fixes the course route. It places this unit after SLO,
  observability, and capacity planning, and before production fault handling.
  That means the page should explain how Ray Serve LLM packages serving
  behavior into a deployable shape, but it should not turn into a pure
  incident-response page.
- `./学习页.html` is the legacy teaching page in this folder. It already carries
  the unit boundary the rewrite should preserve: Ray Serve LLM as a service
  layer, OpenAI-compatible entry points, deployment choices, routing,
  autoscaling, observability, and backend trade-offs.
- `01_Serving边界与请求生命周期/学习页.html`,
  `03_队列Admission_Control与背压/学习页.html`,
  `04_模型副本路由与多租户/学习页.html`,
  `05_自动伸缩批处理与资源隔离/学习页.html`, and
  `06_SLO观测与容量规划/学习页.html` supply the surrounding vocabulary:
  request path, queueing, replica routing, scaling, and SLO/metrics terms.
- The public reference set named by the course index supports the stable
  vocabulary used in this unit:
  - Ray Serve and Ray Serve LLM docs for deployment, replicas, autoscaling,
    routing, metrics, and the OpenAI-compatible serving surface.
  - vLLM docs for OpenAI-compatible online serving, engine kwargs, and the
    common server-side vocabulary used in production LLM deployments.
  - SGLang docs for OpenAI-compatible APIs and structured generation/runtime
    vocabulary.
  - TensorRT-LLM docs for high-performance serving, OpenAI-compatible server
    shape, and hardware-bound deployment trade-offs.
  - Ray Service / KubeRay docs for the Kubernetes deployment form when the
    lesson needs a portable cluster-level shape.

## Gaps And Editorial Decisions

- The exact wording of Ray Serve LLM docs and backend docs changes quickly.
  The lesson therefore teaches durable deployment patterns and inspection
  habits instead of freezing one vendor snapshot as if it were permanent.
- The page treats "deployment shape" as a comparison problem: which layer owns
  the entry point, which layer owns the engine, which layer owns routing, and
  which layer owns scaling. That synthesis is editorial, not a single source
  claim.
- The lesson stops before production incident handling. Those scenarios belong
  to the next unit and should stay out of this page's main teaching chain.
