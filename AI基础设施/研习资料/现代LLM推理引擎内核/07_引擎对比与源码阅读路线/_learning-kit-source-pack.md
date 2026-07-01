# Source Pack: 引擎对比与源码阅读路线

## Source Boundary

- Course: 现代 LLM 推理引擎内核
- Unit: 引擎对比与源码阅读路线
- Snapshot: 2026-06-21（access date; public docs may drift）

## Sources And What They Support

- [vLLM Features](https://docs.vllm.ai/en/latest/features/)
  - 支撑 vLLM 的功能入口、Structured Outputs、Tool Calling、Quantization 与相关特性总览。
- [vLLM Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/)
  - 支撑 choice、regex、json、grammar 与 guided decoding backend 的公开说明。
- [vLLM Automatic Prefix Caching](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/)
  - 支撑 prefix cache、KV cache 复用和共享前缀的公开说明。
- [SGLang Welcome](https://docs.sglang.ai/)
  - 支撑 SGLang 作为 high-performance serving framework 的定位。
- [SGLang Structured Outputs](https://docs.sglang.ai/advanced_features/structured_outputs.html)
  - 支撑 json_schema、regex 和 EBNF 的公开说明。
- [SGLang Benchmark and Profiling](https://docs.sglang.ai/developer_guide/benchmark_and_profiling.html)
  - 支撑 TTFT、TPOT、ITL、吞吐等观测语义。
- [vLLM GitHub repository](https://github.com/vllm-project/vllm)
  - 支撑项目定位、源码入口和实现范围。
- [SGLang GitHub repository](https://github.com/sgl-project/sglang)
  - 支撑项目定位、源码入口和实现范围。

## Source-To-Unit Notes

- 这一页只负责把 vLLM、SGLang 和 PagedAttention 放到同一张工程地图里，帮助读者区分 serving framework、runtime、cache 技术和 backend。
- 源码阅读路线以“入口 -> 调度 -> 缓存 -> 执行 -> 指标”为主线；先找角色，再找文件名。
- benchmark 只在补齐模型、硬件、长度分布、并发和 prefix cache 语境后才有可比性。
- 这一页把 PagedAttention 当作缓存层的技术参照，不把它误写成完整 serving 框架。

## Operational Facts

- vLLM 的公开文档同时覆盖 features、structured outputs 和 automatic prefix caching，所以它适合拿来串起功能入口、约束生成和缓存复用。
- SGLang 的公开文档同时覆盖 structured outputs 和 benchmark / profiling，所以它适合拿来串起前端表达、运行时和观测指标。
- 读源码时先找 request entry、scheduler / engine step、cache manager、model runner 和 metrics / tracing，通常比直接钻 kernel 更稳。

## Gaps

- 这一页不冻结某一版 benchmark 数字，也不替代仓库里的实现细节说明。
- 这一页不比较所有推理引擎，只保留足够做源码阅读和选型起点的维度。
- 下一步如果继续往下学，更适合去看更靠近部署、路由或内核实现的专题。
