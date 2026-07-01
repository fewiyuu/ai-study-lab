# 检查点、容错与集群运行 source pack

## Source Boundary

- Course: `分布式训练系统`
- Unit: `07_检查点容错与集群运行`
- Access date: `2026-06-21`
- Source types:
  - 课程根目录 `index.html`
  - `06_激活检查点混合精度与优化器状态/学习页.html`
  - PyTorch `torch.distributed.checkpoint` 官方文档
  - PyTorch `Getting Started with Distributed Checkpoint` 教程
  - PyTorch `Asynchronous Saving with Distributed Checkpoint` 教程
  - PyTorch `torch.distributed.fsdp.fully_shard` / FSDP2 官方文档
  - Megatron Core `Overview`、`Quick Start`、`Training Examples`
  - Megatron Core `Distributed Optimizer`
  - Megatron Core `dist_checkpointing`、`core.dist_checkpointing.core`
  - Megatron Core `filesystem_async` strategy 和 `MSC Integration`
- Scope: 只使用当前 course root 内已有课程材料和上述公开官方资料，不扩展到其他仓库、课程或私有代码。

## Source To Unit Notes

- 06 单元已经把激活检查点、混合精度和优化器状态讲清楚；这一页接着讲“这些状态如何被可靠保存、恢复和迁移”，重点是 checkpoint 的原子性、恢复验证和集群级容错。
- 08 单元会继续做训练系统选型与实验阅读，所以这一页只讲 checkpoint / resume / fault tolerance 的操作边界，不把系统选型展开。
- PyTorch DCP 教程用来说明：分布式 state_dict 会在 `save/load` 时调用对象的 `state_dict` / `load_state_dict`，并支持 FSDP 之后的分片加载与不同 world size 的恢复。
- PyTorch DCP 异步保存教程用来说明：`async_save` 可以减少阻塞，但保存流程要按“写临时结果、确认完成、再发布最新指针”的思路设计。
- FSDP2 `fully_shard` 文档用来说明：参数、梯度和优化器状态都可能是分片的，所以 checkpoint 也要接受分布式语义，而不是只认单文件权重。
- Megatron Core `dist_checkpointing` 用来说明：它的 checkpoint 不是单纯的 `torch.save`，而是 `torch_dist` 风格的分布式 checkpoint，带有元数据、策略和分片语义。
- Megatron Core `Distributed Optimizer` 用来说明：优化器状态会按 data parallel rank 分布保存，恢复时要校验 shard 映射与策略。
- Megatron Core `MSC Integration` 用来说明：保存路径可以指向 object storage，checkpoint 运营会延伸到存储后端，而不只是本地磁盘。

## Operational Facts

- PyTorch DCP 会按分布式 `state_dict` 读写训练状态，加载时会在预分配的 state_dict 上原地填充，并利用模型已有的分片信息支持重新分片。
- DCP 教程显示：`AppState` 这类包装可以把 model / optimizer 一起交给 `save` 和 `load`，`load_state_dict` 会负责把恢复的状态放回模型和优化器。
- FSDP2 教程说明：`fully_shard` 适合在子模块和根模型上逐层应用；恢复时可以在相同或不同 world size 下加载分片 state_dict。
- FSDP2 的分片语义意味着：如果只保存模型权重，不保存优化器、scheduler、step、数据游标和 RNG，恢复后的训练轨迹会变。
- PyTorch DCP 的异步保存可以减少前台停顿，但如果没有完成标记和原子发布，`latest` 指针可能会指向半成品。
- Megatron Core 的 distributed optimizer 目标是把 optimizer state 平均分摊到 data parallel ranks，减少冗余驻留内存。
- Megatron Core `dist_checkpointing` 包含 `common.pt` 这类 common state 文件，以及分片状态和策略层；它强调的不是单一文件格式，而是完整的 checkpoint 组织方式。
- `examples/run_simple_mcore_train_loop.py` 可以作为最小烟测入口；`pretrain_gpt.py` 是更完整的公开训练入口。
- `--save` / `--load` / `--save-interval` 这类运行参数会随版本变化；本页只讲它们的角色，正式抄写命令前需要再核对文档。

## Gaps

- 本页不展开 08 的训练系统选型、成本对比和实验阅读。
- 本页不做私有仓库或内部集群流程教程，只把公开文档中的 checkpoint / resume 语义和可执行检查方式串起来。
- 若你要落到真实环境，存储后端、对象存储、调度器和版本差异都要重新核对；本页只给出可迁移的判断框架。
