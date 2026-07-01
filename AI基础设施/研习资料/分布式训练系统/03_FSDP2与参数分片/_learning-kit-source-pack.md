# FSDP2 与参数分片 source pack

## Source Boundary

- Course: `分布式训练系统`
- Unit: `03_FSDP2与参数分片`
- Access date: `2026-06-21`
- Source types:
  - 课程根目录 `index.html`
  - `01_训练循环与扩展目标/学习页.html`
  - `02_数据并行梯度同步与通信/学习页.html`
  - PyTorch `DistributedDataParallel` 官方文档
  - PyTorch `torch.distributed.fsdp.fully_shard` 官方文档
  - PyTorch `torch.distributed.tensor` 官方文档
  - Megatron Core User Guide / Parallelism Strategies Guide
- Scope: 只用当前 course root 内已有课程材料与上述官方文档，不额外扩展到别的仓库、课程或私有代码。

## Source To Unit Notes

- 课程地图把 03 放在 02 之后、04 之前：先理解 DDP 的梯度同步，再进入 FSDP2 的参数分片，最后才去看张量并行和流水线并行。
- 01 单元已经给出训练 step 的状态账本：参数、激活、梯度、优化器状态。03 只改写这张账本里“长期常驻”的那几项。
- 02 单元已经把 `rank`、`world size`、`process group`、collective 和 `all-reduce` 说清。03 继续沿着这条线，把 `all-gather`、`reduce-scatter`、`reshard_after_forward` 和 `fully_shard` 放回训练时序里。
- PyTorch `DistributedDataParallel` 文档支持“每个模型副本同步梯度”的边界。
- PyTorch `torch.distributed.fsdp.fully_shard` 文档支持 FSDP2 / `fully_shard` 的 DTensor 表示、hook 生命周期、分片/聚合时序、包装顺序和 `reshard_after_forward` 的取舍。
- PyTorch `torch.distributed.tensor` 文档支持 DTensor / SPMD 的术语边界。
- Megatron Core 文档支持“多种并行策略可组合，但它们不等于 FSDP2”这一对照边界。

## Operational Facts

- DDP 通常保留完整模型副本；它同步的是梯度。
- FSDP2 主要沿数据并行维度分片参数、梯度和优化器状态；它仍然是数据并行训练，不是在做张量并行。
- `fully_shard(module)` 之后再创建优化器，能避免优化器抓住旧的参数引用。
- `model(x)` 会走模块调用路径；直接调用 `model.forward(x)` 容易绕开默认 hook。
- `reshard_after_forward=True` 往往更省显存，但需要更多聚合通信。
- FSDP2 省的是常驻状态，不会自动解决激活峰值。
- Megatron Core 提供的是更宽的训练栈视角，包含 TP、PP、DP、EP、CP、分布式优化器和分布式检查点；本页只用它做边界参照。

## Gaps

- 当前课程没有独立的公开 assignment repo 可桥接，所以本单元先做概念与操作桥接，不写成 API 教程。
- 本页不展开 Megatron Core 的张量并行、流水线并行、上下文并行或专家并行细节，这些会在后续单元返回。
- 若未来 PyTorch 文档改版，需重新核对 `fully_shard`、DDP、DTensor 和 Megatron Core 的页面标题与行为描述。
