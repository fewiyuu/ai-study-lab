# 激活检查点、混合精度与优化器状态 source pack

## Source Boundary

- Course: `分布式训练系统`
- Unit: `06_激活检查点混合精度与优化器状态`
- Access date: `2026-06-21`
- Source types:
  - 课程根目录 `index.html`
  - `05_Megatron_Core训练栈/学习页.html`
  - `07_检查点容错与集群运行/学习页.html`
  - PyTorch `torch.utils.checkpoint` 官方文档
  - PyTorch `torch.amp` / automatic mixed precision 官方文档
  - NVIDIA Megatron Core `Overview`、`Training Examples`、`Distributed Optimizer`
  - NVIDIA Megatron Core custom FSDP / distributed checkpointing 相关文档
  - NVIDIA Megatron Core `dist_checkpointing` 与 optimizer / strategies API 文档
- Scope: 只使用当前 course root 内已有课程材料和上述公开官方资料，不扩展到其他仓库、课程或私有代码。

## Source To Unit Notes

- 05 单元已经把 Megatron Core 的训练栈、并行组、调度器和分布式 optimizer 串起来；这一页要继续往下看三个直接影响显存和稳定性的开关：激活检查点、混合精度和优化器状态布局。
- 07 单元会继续讲 durable checkpoint、容错和恢复，所以这一页只讲 activation checkpointing 这一类“重算型节省”，不把训练恢复流程展开到故障演练。
- PyTorch `torch.utils.checkpoint` 用来说明激活检查点如何在 backward 时重算 forward 片段，以计算换显存。
- PyTorch automatic mixed precision 文档用来说明 `autocast` 和 `GradScaler` 是可拆分的模块；低精度计算、缩放和稳定性不能混成一件事。
- Megatron Core `Overview` 和 `Training Examples` 用来确认它支持 FP16 / BF16 / FP8、分布式优化器和训练示例入口。
- custom FSDP / distributed checkpointing 文档用来确认：分布式状态保存与分片优化器状态是联动的，不只是“保存权重”。

## Operational Facts

- activation checkpointing 会丢弃一部分 forward 激活，在 backward 时按需重算，以显存换计算。
- 如果 checkpoint 包裹了随机层，`preserve_rng_state` 之类的机制会影响 dropout / augmentation 的一致性和重现性。
- `autocast` 影响算子执行 dtype，`GradScaler` 负责低精度训练中的缩放；二者是模块化关系，不是同一个开关。
- BF16 场景通常更看重数值稳定性和框架支持，而不是一味依赖梯度缩放；FP16 更常和 scaler 一起讨论。
- Megatron Core 明确提供 FP16、BF16、FP8 的混合精度能力，以及 distributed optimizer 和 distributed checkpointing。
- custom FSDP 的公开文档说明它需要配合 distributed optimizer，因为分布式 checkpoint 是状态恢复的一部分。
- Megatron Core 的 distributed optimizer 会把 Adam 的 `exp_avg` 和 `exp_avg_sq` 等状态做 shard 化处理，并通过 `dist_checkpointing` 的策略和 planner 读写。
- `dist_checkpointing` 的策略层负责 save / load 算法和形状校验，避免“文件能读，语义却错位”。
- `examples/run_simple_mcore_train_loop.py` 可以作为最小训练烟测入口；`pretrain_gpt.py` 是更完整的公开代码桥接入口。

## Gaps

- 本课程当前没有独立的公开 assignment repo 可桥接，所以这一页先做概念与操作桥接，不写成仓库教程。
- 当前页不展开 07 的 durable checkpoint、容错重启和作业恢复策略。
- 具体命令参数名和示例写法可能随 Megatron Core 版本变化，正式抄写前需要重新核对官方文档和仓库帮助信息。
