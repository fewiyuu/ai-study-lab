# Source Pack: Continuous batching 与调度循环

## Source Boundary

- Course: 现代 LLM 推理引擎内核
- Unit: Continuous batching 与调度循环
- Snapshot: 2026-06-21（access date; public docs may drift）

## Sources And What They Support

- [vLLM - Optimization and Tuning](https://docs.vllm.ai/en/stable/configuration/optimization/)
  - 支撑 chunked prefill、decode 优先、`max_num_batched_tokens` 的吞吐/ITL/TTFT 取舍。
- [vLLM - SchedulerConfig](https://docs.vllm.ai/en/latest/api/vllm/config/scheduler/)
  - 支撑 `scheduler_reserve_full_isl`、`watermark`、`async_scheduling`、`stream_interval` 等调度参数的语义。
- [vLLM - Engine Arguments](https://docs.vllm.ai/en/stable/configuration/engine_args/)
  - 支撑 `--max-num-seqs`、`--max-num-partial-prefills`、`--max-long-partial-prefills`、`--long-prefill-token-threshold`、`--scheduling-policy`、`--enable-chunked-prefill` 的解释。
- [vLLM - Scheduler API](https://docs.vllm.ai/en/stable/api/vllm/v1/core/sched/scheduler/)
  - 支撑 `_schedule_prefills`、`PREEMPTED_FOR_RECOMPUTE`、token budget、cached block / remote cache 这类调度细节。
- [SGLang - Welcome](https://docs.sglang.ai/)
  - 支撑 SGLang 作为生产级 serving framework、低延迟与高吞吐的定位。
- [SGLang - Benchmark and Profiling](https://docs.sglang.ai/developer_guide/benchmark_and_profiling.html)
  - 支撑 scheduler 负责 batching and execution、离线吞吐测试的运行方式。
- [SGLang - HiCache System Design and Optimization](https://docs.sglang.ai/advanced_features/hicache_design.html)
  - 支撑 HiCache 的系统架构、workflow、local match / prefetch / write-back、以及 page_size / layout 参数。
- [SGLang - HiCache Best Practices](https://docs.sglang.ai/advanced_features/hicache_best_practices.html)
  - 支撑 HiCache 的三层缓存定位，以及它更适合长上下文和多轮对话的结论。

## Source-To-Unit Notes

- 这节课先把 “一轮迭代里谁先走、谁后走、谁被切块、谁被抢占” 讲清楚，再去看更下游的引擎架构。
- 只要看到 `max_num_batched_tokens`、`max_num_seqs`、`max_num_partial_prefills`、`max_long_partial_prefills`、`long_prefill_token_threshold`、`watermark`、`scheduler_reserve_full_isl` 这些词，先回到 vLLM 的 optimization、engine args 和 scheduler config 文档。
- 只要看到“decode 优先”“chunked prefill 自动切块”“重复 preemption”“preempted request 被当成重新 prefill”“迭代调度”和“token budget”，先回到 vLLM 的 scheduler 文档。
- 只要看到“scheduler handles batching and execution”“offline throughput”“三层 KV cache”“long-context / multi-turn”，先回到 SGLang 的 welcome、benchmark 和 HiCache 文档。
- 这节课停在调度循环和参数取舍，不展开网络网关、路由器、RPC、分布式服务发现，也不替代后面的引擎对比单元。

## Operational Facts

- vLLM V1 在可能时默认启用 chunked prefill；开启后，调度会优先安排 decode 请求，再在 `max_num_batched_tokens` 预算内塞入 prefill。
- `max_num_batched_tokens` 控制单轮可处理的 token 上限。小一些通常更利于 ITL，大一些通常更利于 TTFT 和吞吐。
- `max_num_seqs` 控制单轮可处理的序列数；它不是 token 预算的替代品。
- `max_num_partial_prefills`、`max_long_partial_prefills` 和 `long_prefill_token_threshold` 一起决定长 prompt 以多大粒度进入队列。
- `scheduler_reserve_full_isl=True` 会先检查完整输入长度是否能进 KV cache，避免只看第一块导致过度准入和 KV thrashing。
- `watermark` 会给 KV cache 留出一部分空位，降低 GPU 内存紧张时反复 eviction 和 repeated preemption 的概率。
- vLLM 文档明确提到，`PREEMPTED_FOR_RECOMPUTE` 会被当成从头重新 prefill 的请求来处理。
- SGLang 的 scheduler 负责 batching 和 execution；HiCache 则把 KV cache 扩到 GPU / host / distributed storage 的层级。

## Gaps

- 这页不冻结任何具体 benchmark 数字；它教的是调度语义、状态迁移和参数取舍。
- 这页不展开完整的服务网关、路由层和多机部署；那些会在后面的系统单元里继续。
- 这页不替代源码逐行阅读，只给公开文档对应的阅读入口和调参边界。
