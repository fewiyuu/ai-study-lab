# Source Pack: 推理生命周期 prefill 与 decode

## Source Boundary

- Course: 现代 LLM 推理引擎内核
- Unit: 推理生命周期 prefill 与 decode
- Snapshot: 2026-06-21（access date; public docs may drift）

## Sources And What They Support

- [vLLM - Optimization and Tuning](https://docs.vllm.ai/en/stable/configuration/optimization/)
  - 支撑 chunked prefill、decode 优先、`max_num_batched_tokens` 对 TTFT / ITL / 吞吐的取舍。
- [vLLM - Engine Arguments](https://docs.vllm.ai/en/stable/configuration/engine_args/)
  - 支撑 `--max-num-batched-tokens`、`--max-num-seqs`、`--max-num-partial-prefills`、`--max-long-partial-prefills`、`--long-prefill-token-threshold`、`--scheduler-reserve-full-isl` 的语义。
- [vLLM - Scheduler API](https://docs.vllm.ai/en/stable/api/vllm/v1/core/sched/scheduler/)
  - 支撑 preempted request 回到 waiting queue、`PREEMPTED_FOR_RECOMPUTE`、token budget、blocked waiting request 这些调度状态。
- [SGLang - Benchmark and Profiling](https://docs.sglang.ai/developer_guide/benchmark_and_profiling.html)
  - 支撑 TTFT、ITL、TPOT、throughput 这些在线 serving 指标，以及 benchmark 工具的选择。
- [SGLang - Welcome](https://docs.sglang.ai/)
  - 支撑 SGLang 作为 serving framework 的定位，以及它与低延迟 / 高吞吐推理服务的关系。

## Source-To-Unit Notes

- 这一页只讲一次请求的生命周期：prompt 如何进入 prefill，为什么 prefill 会写入 KV cache，decode 为什么是一轮一 token，以及为什么 TTFT 和 ITL 要分开看。
- 看到 chunked prefill、`max_num_batched_tokens`、`max_num_seqs`、`max_num_partial_prefills`、`scheduler_reserve_full_isl` 这些词时，优先回到 vLLM 的 optimization 和 engine args 文档。
- 看到 preempted request、waiting / running 状态、`PREEMPTED_FOR_RECOMPUTE`、request 回队这些词时，优先回到 vLLM 的 scheduler API。
- 看到 TTFT、ITL、TPOT、throughput 或 benchmark 选择时，优先回到 SGLang 的 benchmark 文档。
- 这一页只负责生命周期和指标读法，不展开 KV cache 账本、PagedAttention 块管理、continuous batching 细节或 kernel 级优化。

## Operational Facts

- vLLM 文档把 prefill 解释为处理完整 prompt 的阶段，把 decode 解释为逐 token 生成的阶段。
- vLLM 的 chunked prefill 会优先安排 decode，再在剩余 `max_num_batched_tokens` 预算里塞 prefill；如果 prefill 太大，还会自动切块。
- 小一些的 `max_num_batched_tokens` 通常更利于 ITL；更大的值通常更利于 TTFT。
- `max_num_seqs` 控制一轮能处理多少条序列，不等于 token budget。
- `scheduler_reserve_full_isl=True` 会先检查完整输入长度是否能进入 KV cache，避免只看第一块造成过度准入。
- SGLang 的 benchmark 文档把 TTFT、ITL、TPOT 和吞吐区分开，强调在线 serving 应优先看 `bench_serving` 一类更接近真实负载的测试。

## Gaps

- 这页不冻结任何具体模型架构、tokenizer 或 benchmark 数字；它教的是生命周期、指标和调度语义。
- 这页不展开完整源码树，只在需要理解请求状态迁移和队列行为时引用公开 API 文档。
- 这页的下一步是第 02 单元：KV cache 与显存账本。
