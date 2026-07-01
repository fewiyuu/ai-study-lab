# 数据并行、梯度同步与通信 source pack

## Source Boundary

- Course: `分布式训练系统`
- Unit: `02_数据并行梯度同步与通信`
- Local snapshot: `2026-06-21`
- Source types:
  - 课程根目录 `index.html`
  - `01_训练循环与扩展目标/学习页.html`
  - PyTorch Distributed 官方文档
  - PyTorch `DistributedDataParallel` 官方文档
  - PyTorch FSDP2 / `fully_shard` 官方文档与教程
  - Megatron Core 官方文档
- Scope: 只用当前 course root 内已有课程材料与上述官方文档，不额外爬网其他资料。

## Source To Unit Notes

- 课程地图定义了单元顺序：01 先把训练 step 的读写顺序讲清，02 再把这条 step 放到数据并行和通信里看，03 才进入 FSDP2 的分片。
- 01 单元提供锚点：同一个训练 step 会读参数、写激活、写梯度、再由 optimizer step 写回参数。02 直接复用这个锚点，只是把它复制到多个 rank 上。
- PyTorch Distributed 官方文档支持本单元对 `rank`、`world size`、`process group`、collective 和 `all-reduce` 的解释。
- `DistributedDataParallel` 官方文档支持“多个模型副本之间同步梯度”的核心语义。
- FSDP2 / `fully_shard` 官方文档和教程支持“DDP 复制完整模型副本，FSDP2 通过分片参数、梯度和优化器状态改变内存布局与通信模式”的边界说明。
- Megatron Core 官方文档支持“多种并行策略可以组合使用，数据并行只是其中一条维度”的后续衔接。

## Operational Facts

- `rank` 是通信组里的进程编号，`world size` 是参与协作的进程总数，`process group` 是能彼此做 collective 的那组进程。
- DDP 语义是同步每个模型副本的梯度；`all-reduce` 可以是求和，也可以是平均，平均是训练代码层面的约定，不是这个词本身自动保证的。
- 如果每个 rank 读到同一份数据，数据并行就只是在重复计算。
- 如果不同 rank 进入 collective 的顺序不一致，常见表现是挂住而不是立刻报清楚的 Python 异常。
- DDP 通常保留完整模型副本；显存压力主要靠 FSDP2 / 分片策略解决，不靠单纯增加数据并行 rank。

## Gaps

- 这门课当前没有独立的公开代码仓库或 assignment repo 可桥接，所以本单元先做概念与操作桥接，不写成 API 教程。
- 如果以后官方文档版本变化，需重新核对 doc title、页面结构和 `fully_shard` / DDP 的当前描述。
