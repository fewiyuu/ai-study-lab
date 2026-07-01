# 训练系统选型与实验阅读 source pack

## Source Boundary

- Course: `分布式训练系统`
- Unit: `08_训练系统选型与实验阅读`
- Access date: `2026-06-21`
- Source types:
  - 课程根目录 `index.html`
  - `06_激活检查点混合精度与优化器状态/学习页.html`
  - `07_检查点容错与集群运行/学习页.html`
  - PyTorch `torch.distributed.checkpoint` 官方文档
  - PyTorch `Getting Started with Distributed Checkpoint` 教程
  - PyTorch `Asynchronous Saving with Distributed Checkpoint` 教程
  - PyTorch `Getting Started with Fully Sharded Data Parallel (FSDP2)` 教程
  - PyTorch `torch.distributed.fsdp.fully_shard` 官方文档
  - NVIDIA Megatron Core `User Guide`
  - NVIDIA Megatron Core `Parallelism Strategies Guide`
  - NVIDIA Megatron Core `Distributed Optimizer`
  - NVIDIA Megatron Core `core.dist_checkpointing`
  - NVIDIA Megatron Core `core.dist_checkpointing.core`
  - NVIDIA Megatron Core `core.dist_checkpointing.strategies.state_dict_saver`
  - NVIDIA Megatron Core `core.dist_checkpointing.strategies.filesystem_async`
  - NVIDIA/Megatron-LM 仓库与 `megatron/core/QuickStart.md`
- Scope: 只使用当前 course root 内已有课程材料和上述公开官方资料，不扩展到其他仓库、课程或私有代码。

## Source To Unit Notes

- 06 单元已经把激活检查点、混合精度和优化器状态讲清楚；这一页不再追数值细节，而是把这些状态放到“选什么训练栈、拿什么实验读法验证”的框架里。
- 07 单元已经讲了 checkpoint、恢复和容错；这一页继续向上收束到系统选型，重点不再是保存链路，而是“什么时候该选 FSDP2，什么时候该选 Megatron Core，实验该怎么看”。
- PyTorch DCP 官方文档用来说明：分布式 checkpoint 支持并行保存和加载，支持 load-time resharding，并且在分布式 `state_dict` 语义下工作，而不是只认单文件权重。
- PyTorch DCP 教程用来说明：`state_dict` 的生成和加载会处理模型与优化器的 FQN 映射，异步保存有自己的内存与发布限制。
- FSDP2 文档用来说明：`fully_shard(model)` 把参数、梯度和优化器状态都放进分片语义里，适合保留 PyTorch 迭代体验同时缓解状态驻留显存。
- Megatron Core `User Guide` 和 `Parallelism Strategies Guide` 用来说明：DP、TP、PP、CP、EP 是可组合的并行构件，选型不该只盯一个框架名字。
- Megatron Core `Distributed Optimizer` 用来说明：优化器状态的分布式组织会影响训练栈的保存和恢复方式，不能按普通单卡 `torch.save` 处理。
- Megatron Core `core.dist_checkpointing`、`core.dist_checkpointing.core`、`state_dict_saver` 和 `filesystem_async` 用来说明：Megatron Core 的 checkpoint 不是单文件权重，而是带元数据、策略和异步写入流程的分布式 checkpoint。
- Megatron-LM 仓库和 `QuickStart.md` 用来说明：`examples/run_simple_mcore_train_loop.py` 适合作为最小入口，`pretrain_gpt.py` 适合作为更完整的公开训练入口与实验阅读对象。

## Operational Facts

- DCP 解决的是分布式语义，不是单纯的文件打包；它支持保存和加载分布式 `state_dict`，并允许在恢复时按新 world size 重新装配。
- DCP 异步保存有内存限制：它会先把模型状态复制到内部 CPU buffer，再进行后续保存流程，所以“异步”不等于“零代价”。
- FSDP2 的 `fully_shard` 把参数从普通 tensor 变成分片语义的一部分，因此 checkpoint 也要能理解分片布局、模块边界和恢复时的重分片。
- Megatron Core 的并行策略选择不是二选一，而是 DP / TP / PP / CP / EP 的组合问题；实验阅读时要看清楚作者用了哪几种并行维度。
- Megatron Core `state_dict_saver` 把异步保存拆成 planning / actual saving / finalization 三段，实际写入必须放在异步阶段。
- Megatron Core `filesystem_async` 说明 checkpoint 写盘策略可以和对象存储、异步执行、发布流程一起设计。
- `examples/run_simple_mcore_train_loop.py` 和 `pretrain_gpt.py` 是这页的公开代码桥接入口；后续要落到具体实验时，应先回到这两个入口再核对版本和参数。
- 本页只做训练系统选型和实验阅读，不展开具体 repo 适配、私有集群流程或版本迁移命令；需要落地时，必须重新核对上游版本。

## Gaps

- 本页不把训练系统选型写成固定答案；它给的是可解释的起点和验证框架。
- 本页不覆盖私有仓库、内部调度器或企业存储后端，只用公开资料说明可迁移的判断方式。
- 任何 `--save`、`--load`、`--save-interval` 之类参数都可能随版本变化；正式落地前需要回到对应版本文档再次核对。
