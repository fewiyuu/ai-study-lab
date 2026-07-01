# 张量并行与流水线并行 source pack

## Source Boundary

- Course: `分布式训练系统`
- Unit: `04_张量并行与流水线并行`
- Access date: `2026-06-21`
- Source types:
  - 课程根目录 `index.html`
  - `03_FSDP2与参数分片/学习页.html`
  - PyTorch `torch.distributed.tensor.parallel` 官方文档
  - PyTorch `torch.distributed.pipelining` 官方文档
  - PyTorch `torch.distributed.tensor` 官方文档
  - Megatron Core `User Guide` 与 `Parallelism Strategies Guide`
- Scope: 只用当前 course root 内已有课程材料与上述官方文档，不额外扩展到别的仓库、课程或私有代码。

## Source To Unit Notes

- 03 单元已经把数据并行和参数分片的主线讲清：这页开始转向模型内部并行，不再把重点放在“常驻状态怎么省”，而是放在“层内矩阵怎么切、层序怎么排、micro-batch 怎么跑”。
- 课程地图把 04 放在 03 之后、05 之前：先用 PyTorch 的 TP/PP 原语建立直觉，再在 05 单元看 Megatron Core 如何把这些原语组合进更完整的训练栈。
- PyTorch `torch.distributed.tensor.parallel` 文档支持 TP 的入口、`parallelize_module()`、`ColwiseParallel`、`RowwiseParallel`、`SequenceParallel`、`PrepareModuleInput` 和 `PrepareModuleOutput`。
- PyTorch `torch.distributed.pipelining` 文档支持模型分区、micro-batch、调度和梯度传播；它明确把 runtime 的职责放在 micro-batch splitting、scheduling、communication 和 gradient propagation 上。
- PyTorch `torch.distributed.tensor` 文档支持 DTensor / 设备网格 / shard 的边界语义。
- Megatron Core 的并行策略指南支持“TP 切单层、PP 切模型深度、DP 切 batch 维”的对照边界，也支持把这些策略组合起来看。

## Operational Facts

- Tensor Parallelism (TP) 建立在 DTensor 上，核心是把单层里的矩阵、激活或序列维度分给多个 rank。
- `ColwiseParallel` 适合把线性层的输出维切开；`RowwiseParallel` 适合把输入维切开，并在另一侧恢复或规约。
- `parallelize_module()` 只接受 1-D `DeviceMesh`，所以 TP 先要明确用哪条并行轴。
- Pipeline Parallelism (PP) 把模型按深度切成 stage，再把输入拆成 micro-batch 送进调度器。
- PP 的空转来自依赖和 stage 数，不来自“框架没把 GPU 用满”；micro-batch 太少时，bubble 很快变大。
- TP 和 PP 都不是 DP 的替代品；它们通常与 DP 组合使用，但各自通信边界不同。
- 这页先不展开 Sequence Parallel、Context Parallel、Expert Parallel、zero-bubble schedule 或 Megatron Core 的分布式优化器细节，这些会在后续单元或更晚的边界里再回来。

## Gaps

- 当前课程没有独立的公开 assignment repo 可桥接，所以本单元先做概念与操作桥接，不写成 API 教程。
- 若未来 PyTorch 文档改版，需重新核对 `parallelize_module()`、`ColwiseParallel`、`RowwiseParallel` 和 `pipelining` 的页面标题与行为描述。
