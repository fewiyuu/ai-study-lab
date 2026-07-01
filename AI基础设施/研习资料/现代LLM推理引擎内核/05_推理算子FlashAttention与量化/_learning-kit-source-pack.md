# Source Pack: 推理算子、FlashAttention 与量化

## Source Boundary

- Course: 现代 LLM 推理引擎内核
- Unit: 推理算子、FlashAttention 与量化
- Snapshot: 2026-06-21（access date; public docs may drift）

## Sources And What They Support

- [FlashAttention GitHub](https://github.com/Dao-AILab/flash-attention)
  - 支撑 FlashAttention 的 IO-aware exact attention、分块、online softmax、重计算和支持范围。
- [vLLM - Optimization and Tuning](https://docs.vllm.ai/en/stable/configuration/optimization/)
  - 支撑 attention 相关优化、chunked prefill、性能与显存取舍的解释。
- [vLLM - Quantization](https://docs.vllm.ai/en/stable/features/quantization/)
  - 支撑量化目标、常见格式、内存 footprint 和硬件支持的基础说法。
- [vLLM - Quantized KV Cache](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/)
  - 支撑 FP8 KV cache、压缩缓存和上下文显存的说法。
- [vLLM - Engine Arguments](https://docs.vllm.ai/en/stable/configuration/engine_args/)
  - 支撑 `--max-num-seqs`、`--enable-chunked-prefill`、`--preemption-mode`、`--scheduler-reserve-full-isl`、`--max-num-partial-prefills`、`--max-long-partial-prefills`、`--long-prefill-token-threshold` 的语义。
- [vLLM - Scheduler API](https://docs.vllm.ai/en/stable/api/vllm/v1/core/sched/scheduler/)
  - 支撑 `PREEMPTED_FOR_RECOMPUTE`、token budget、抢占和重算这类调度细节。
- [SGLang - Benchmark and Profiling](https://docs.sglang.ai/developer_guide/benchmark_and_profiling.html)
  - 支撑 `bench_serving`、TTFT、TPOT、ITL、吞吐等在线/离线观测语义。
- [SGLang - Welcome](https://docs.sglang.ai/)
  - 支撑 SGLang 作为 serving framework 的定位，以及 attention backend、KV cache、量化相关的公开叙述。

## Source-To-Unit Notes

- 这页先把 “FlashAttention 为什么重要” 和 “量化到底省哪一笔账” 讲清楚，再把它放回 prefill / decode、backend 兼容性和缓存对象里看。
- 只要看到 `FlashAttention`、`attention backend`、`FP8 KV cache`、`权重量化`、`反量化`、`TTFT`、`TPOT`、`ITL`，先回到这组公开资料。
- 这页停在算子层和表示层，不展开网络网关、路由器、分布式 RPC、MoE expert parallelism，也不替代后面的结构化生成单元。

## Operational Facts

- FlashAttention 的核心是减少 attention 中间结果在 HBM 里的往返，而不是把 attention 变成近似算法。
- vLLM 的量化文档把量化视为内存 footprint 和吞吐的权衡；Quantized KV Cache 文档把 FP8 cache 和更长上下文、更高吞吐联系起来。
- vLLM 和 SGLang 都会根据硬件、dtype、head size、序列长度、量化配置和缓存布局选择或回退 attention backend。
- `max_num_seqs`、`max_num_partial_prefills`、`max_long_partial_prefills`、`long_prefill_token_threshold` 和 `scheduler_reserve_full_isl` 影响的是准入和并发边界，不是单个 kernel 的数学形式。
- KV cache 量化省的是上下文和并发带来的 cache 显存；权重量化省的是模型常驻权重显存。
- 只看单 kernel benchmark 不够，线上判断要回到 TTFT、TPOT、ITL、吞吐、显存峰值和输出质量一起看。

## Gaps

- 这页不冻结任何单一硬件平台上的性能数字。
- 这页不承诺某个 backend 在所有模型和 GPU 上都最优。
- 这页不替代源码逐行阅读，只给后续阅读和排障的公开入口。
