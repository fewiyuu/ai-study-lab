# LLM Serving 架构与请求调度｜单元 02 来源包

## Source Boundary

- Course root: `LLMServing架构与请求调度`
- Unit: `OpenAI 兼容接口与流式返回`
- Snapshot / 访问日期: 2026-06-21
- This rebuild uses the course map, the legacy unit page, and the public
  reference set already listed in the course index. No new network crawl was
  needed for the local reconstruction pass.

## Source-To-Unit Notes

- `../index.html` fixes the course sequence. It shows that this unit sits after
  Serving 边界与请求生命周期 and before queueing、路由、伸缩和 SLO。
  That placement determines the lesson boundary: the page should explain API
  合同、SSE 流式返回、chunk 解析、错误处理和框架差异，但不展开
  admission control、replica routing or autoscaling in full.
- `./学习页.html` is the legacy teaching page in this folder. It provides the
  original lesson chain: contract boundary, stream walkthrough, metrics
  split, common mistakes, and practice pattern. The 1.0 rebuild keeps that
  chain, but moves it into the shared study-page shell and export workflow.
- The course index points to public references for the broader topic set:
  OpenAI API docs, MDN SSE semantics, vLLM docs, Ray Serve docs, TensorRT-LLM
  docs, and SGLang docs. Those references support terminology and public
  framing, especially for compatibility boundaries and streaming behavior.

## Gaps And Editorial Decisions

- The exact upstream API surface for OpenAI-compatible serving frameworks can
  drift. The page therefore teaches stable behavior and inspection habits
  instead of locking onto a vendor-specific implementation detail that may age
  quickly.
- The lesson is intentionally framed as a production-interface unit, not a
  general networking lesson and not a full serving-system design unit.
- The later course units handle queueing、routing、multitenancy、autoscaling and
  SLO; this page stops at the boundary where those topics start to matter.

