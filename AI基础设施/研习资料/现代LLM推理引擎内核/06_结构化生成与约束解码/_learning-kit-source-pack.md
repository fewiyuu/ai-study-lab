# Source Pack: 结构化生成与约束解码

## Source Boundary

- Course: 现代 LLM 推理引擎内核
- Unit: 结构化生成与约束解码
- Snapshot: 2026-06-21（access date; public docs may drift）

## Sources And What They Support

- [vLLM Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/)
  - 支撑 choice、regex、json、grammar、guided decoding backend 和结构化输出入口的公开说明。
- [vLLM Structured Outputs examples](https://docs.vllm.ai/en/v0.8.4/getting_started/examples/structured_outputs.html)
  - 支撑 guided decoding 示例、Choice、Regex、JSON schema、Grammar 的小例子。
- [SGLang Structured Outputs](https://docs.sglang.ai/advanced_features/structured_outputs.html)
  - 支撑 json_schema、regex、EBNF 和 grammar backend 的公开说明。
- [SGLang Frontend Language](https://docs.sglang.ai/references/frontend/frontend_tutorial.html)
  - 支撑前端语言里结构化输出、regex schema 和工具相关示例。
- [vLLM GitHub repository](https://github.com/vllm-project/vllm)
  - 支撑项目定位、源码入口和实现范围。
- [SGLang GitHub repository](https://github.com/sgl-project/sglang)
  - 支撑项目定位、源码入口和实现范围。

## Source-To-Unit Notes

- 这一页只讲 decode 时的约束怎么生效：约束来源、token 过滤、状态推进、结束条件和 backend 回退。
- 看到 JSON schema、regex、EBNF、grammar、choice 这些词时，先回到公开文档里的结构化输出说明，再看页面里的伪代码和状态表。
- 看到 reasoning_content 和 final answer 分开时，重点是判断约束应该落在哪一段，而不是把它当成单纯的格式清洗问题。
- 这一页不展开应用层校验、schema 自动修复、agent 编排或长链路工具调用；那些内容留给后面的单元和实际工程。

## Operational Facts

- 结构化生成和 guided decoding 发生在采样前后，不是把输出生成完以后再补格式。
- backend 的差异会同时影响兼容矩阵、性能和错误形态，所以日志里要先看是约束对象、状态推进还是 backend 支持范围出了问题。
- 如果约束太严、状态机推进不通或 backend 不匹配，最常见的表面症状是输出变慢、回退、卡在闭合符号附近，或者模型开始吐自然语言补丁。

## Gaps

- 这一页不冻结具体 benchmark 数字，也不冻结某个 backend 的全部兼容矩阵。
- 这一页不替代官方文档里的实现细节，只负责把公开接口和 decode 过程连起来。
- 下一步是第 07 单元：引擎对比与源码阅读路线。
