# Megatron Core 训练栈 source pack

## Source Boundary

- Course: `分布式训练系统`
- Unit: `05_Megatron_Core训练栈`
- Access date: `2026-06-21`
- Source types:
  - 课程根目录 `index.html`
  - `04_张量并行与流水线并行/学习页.html`
  - `06_激活检查点混合精度与优化器状态/学习页.html`
  - `07_检查点容错与集群运行/学习页.html`
  - NVIDIA Megatron Core developer guide: Overview / Parallelism Strategies / Training Examples / Distributed Optimizer
  - NVIDIA/Megatron-LM GitHub repository README and `pretrain_gpt.py`
- Scope: 只使用当前 course root 内已有课程材料与上述公开官方资料，不再扩展到其他仓库、课程或私有代码。

## Source To Unit Notes

- 04 单元已经把 TP / PP 的基本切分讲清，这一页要把它们放回 Megatron Core 的训练栈里：先看组件层级，再看并行组、调度器、优化器和 checkpoint 如何接起来。
- 06 单元会继续拆激活检查点、混合精度和优化器状态，所以这一页只讲这些能力在 Megatron Core 训练路径里的位置，不展开数值稳定性和显存优化细节。
- 07 单元会继续拆 checkpoint 恢复与容错，所以这一页只把“保存什么、谁来读、何时会错位”讲清。
- Megatron Core 官方文档用于训练栈总览、并行策略分类、训练示例入口和分布式优化器边界。
- NVIDIA/Megatron-LM 仓库用于确认 `pretrain_gpt.py` 是公开的训练入口与参考实现，适合作为从文档走向代码的下一步。

## Operational Facts

- Megatron Core 是可组合库；Megatron-LM 是带预配置训练脚本的 reference example。
- `parallel_state` 负责并行组初始化与查询，是判断 rank 归属、通信组和 collective 范围的第一站。
- 一次训练路径通常可以读成：解析配置 -> 初始化并行组 -> 构建模型块 -> 组织数据与调度 -> forward/backward -> optimizer step -> checkpoint。
- `forward_backward_func` 把 micro-batch、pipeline stage 和梯度传播串进同一条训练循环。
- `dist_checkpointing` 和 distributed optimizer 改写的不只是显存账本，也改写了恢复时需要保存和加载的状态边界。
- `pretrain_gpt.py` 是公开的代码桥接入口，适合作为这页后的第一段代码阅读。

## Gaps

- 本课程当前没有独立的公开 assignment repo 可桥接，所以这一页先做概念与操作桥接，不写成仓库教程。
- 若后续把本页升级成更操作化的阅读页，需要重新核对当前版本 `pretrain_gpt.py --help` 的参数名和训练示例写法。
- 本页不展开 zero-bubble schedule、TransformerEngine 内核优化、FSDP2 细节或更晚的容错机制。
