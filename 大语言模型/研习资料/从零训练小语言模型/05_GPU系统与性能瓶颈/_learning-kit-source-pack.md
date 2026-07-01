# Source Pack: GPU 系统与性能瓶颈

## Source Boundary

- Course: 从零训练小语言模型
- Unit: 05 GPU 系统与性能瓶颈
- Snapshot: 2026-06-21
- Access date: 2026-06-21
- Local inputs: course-root `index.html` and the existing unit page `学习页.html` for the same unit.

## Source-To-Unit Notes

- The course index places this unit after training loop / optimizer / checkpoint and before scaling / evaluation, so this page should focus on system bottlenecks rather than training semantics.
- Stanford CS336 Spring 2025 establishes the broader course path from language modeling foundations into implementation-heavy training topics. Use it for unit placement and for the fact that GPU/system reasoning is part of the core path, not an appendix.
- Public references already visible in the existing page copy include NVIDIA / PyTorch / Triton / FlashAttention / NCCL concepts, plus `llm.c`-style training implementation language. Keep them as source labels only; do not expand beyond what the existing page already supports.
- This rewrite should keep the unit at the system-performance level: memory accounting, throughput, kernel behavior, mixed precision, communication bottlenecks, profiling, and diagnosis order.

## Unit Boundary

- This page covers: memory ledger, throughput ledger, kernel granularity, roofline intuition, mixed precision, attention cost, multi-GPU communication, profiler reading, and diagnosis flow.
- This page does not cover: full CUDA programming, distributed training engineering, optimizer state recovery, or scaling-law analysis. Those belong to neighboring units.
- Keep the anchor examples at the level of a small memory calculation, a throughput calculation, a trace table, and a bottleneck diagnosis checklist. Do not stretch this page into a CUDA tutorial.

## Gaps

- No local training transcript, hardware benchmark log, or repository snapshot was provided for a private implementation, so do not claim repository-specific filenames or performance numbers beyond the public source labels above.
- Avoid inventing exact profiler traces or benchmark figures unless the page shows them as examples only.
- If later unit pages need repository-specific operational details, create a new source pack for that unit instead of stretching this one.
