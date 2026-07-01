# Source Pack: PagedAttention 与块管理

## Source Boundary

- Course: 现代 LLM 推理引擎内核
- Unit: PagedAttention 与块管理
- Snapshot: 2026-06-21（access date; public docs may drift）

## Sources And What They Support

- [vLLM - Paged Attention](https://docs.vllm.ai/en/latest/design/paged_attention/)
  - 支撑 PagedAttention 的基本块概念、`BLOCK_SIZE`、按块读取 KV cache 的解释。
- [vLLM - Automatic Prefix Caching](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/)
  - 支撑 prefix cache 只在前缀完全一致时复用 KV、只省 prefill 不省 decode 的边界。
- [vLLM - block_pool API](https://docs.vllm.ai/en/latest/api/vllm/v1/core/block_pool/)
  - 支撑 block hash、prefix caching、append-only block tables、cache miss / cache hit 的实现语义。
- [vLLM - Engine Arguments](https://docs.vllm.ai/en/latest/configuration/engine_args/)
  - 支撑 `--block-size`、`--enable-prefix-caching`、`--kv-cache-dtype` 这些配置词汇。
- [PagedAttention paper](https://arxiv.org/abs/2309.06180)
  - 支撑 PagedAttention 解决 fragmentation、redundant duplication、near-zero waste 的核心论断。
- [SGLang - HiCache System Design and Optimization](https://docs.sglang.ai/advanced_features/hicache_design.html)
  - 支撑 RadixTree / HiRadixTree、三层缓存、local match / prefetch / write-back 的系统边界。
- [SGLang - HiCache Best Practices](https://docs.sglang.ai/advanced_features/hicache_best_practices.html)
  - 支撑 HiCache 适合长上下文、多轮会话、共享前缀高的负载，以及 page-first / layer-first / heterogeneous TP 这类工程取舍。

## Source-To-Unit Notes

- 这节课先把 KV cache 从“显存账”转成“块表 + 复用规则 + 尾部浪费”的问题，再解释 PagedAttention 为什么能把逻辑连续和物理连续拆开。
- 只要看到“共享前缀能不能复用”“block size 怎么影响尾部浪费”“为什么 block table 要 append-only”，优先回到 vLLM 的 Paged Attention、block_pool 和 Engine Arguments 文档。
- 只要看到“同一前缀复用到多层缓存”“长上下文 / 多轮 / 共享前缀场景下值得不值得上层次化缓存”，优先回到 SGLang 的 HiCache 两篇文档。
- 这节课要停在块管理和复用边界，不继续讲 continuous batching、调度循环、speculative decoding、chunked prefill 或 kernel 级 attention 优化。

## Operational Facts

- vLLM 的 Paged Attention 文档明确把 KV cache 切成固定大小的 blocks；每个 block 存一个 head 上固定 token 数。
- vLLM 的 Automatic Prefix Caching 只在 prefix 完全一致时复用 KV，省的是 prefilling 阶段，不省 decoding 阶段。
- vLLM 的 block_pool 文档明确说 cached block 带有 block hash，可用于 prefix caching，并保持 block tables append-only。
- SGLang 的 HiCache 文档把缓存层级组织成 GPU / host / external storage 三层，适合长上下文和多轮对话。

## Gaps

- 这页不冻结任何具体 benchmark 数字；它教的是块管理的机制、诊断和边界。
- 这页不展开整个 vLLM / SGLang 源码树，只在需要理解 block table、prefix caching 和层次化缓存时引用公开文档。
- 这页的下一步是第 04 单元的 continuous batching 与调度循环。
