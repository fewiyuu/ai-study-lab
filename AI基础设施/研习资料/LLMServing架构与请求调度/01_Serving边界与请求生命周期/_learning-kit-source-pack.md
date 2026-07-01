# LLM Serving 架构与请求调度｜单元 01 来源包

## Source Boundary

- Course root: `LLMServing架构与请求调度`
- Unit: `Serving 边界与请求生命周期`
- Snapshot / 访问日期: 2026-06-21
- This rebuild uses only the existing course `index.html` and the legacy unit
  page in the same folder. No network crawl was used.

## Source-To-Unit Notes

- `../index.html` fixes the course scope, the unit order, and the neighboring
  topics. It shows that this unit sits before OpenAI-compatible API details,
  queueing, routing, autoscaling, SLO, Ray Serve LLM, and production issues.
- `学习页.html` in this folder provides the original teaching material:
  boundary, request lifecycle, example walkthrough, metrics, mistakes, and
  practice pattern.
- The rewritten page keeps the same learning contract but moves it into the
  shared learning-kit shell and practice/export workflow.

## Gaps And Editorial Decisions

- There was no local source pack, so this file becomes the internal source
  boundary for the rebuild.
- The later section order is editorial synthesis from the course map and the
  old page, not a separate public syllabus.
- Public source URLs already listed in the course index remain references for
  the broader course, but they were not re-crawled during this pass.
