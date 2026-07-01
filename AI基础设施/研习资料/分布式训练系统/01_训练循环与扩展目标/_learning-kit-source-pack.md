# 训练循环与扩展目标 source pack

## Source Boundary

- Course: `分布式训练系统`
- Unit: `01_训练循环与扩展目标`
- Local snapshot: `2026-06-21`
- Source types: 课程根目录的 `index.html` + 现有旧学习页 `学习页.html`
- Scope: 只使用当前 course root 内的材料；不爬网，不补外部资料。

## Source To Unit Notes

- `index.html` 提供课程地图、单元顺序、前后单元关系和课程边界。
- 旧学习页提供当前单元的主体材料：训练 step 的状态账本、rank/world size/process group、数据并行与梯度同步、FSDP2 与参数分片、Megatron Core 的并行维度、检查点与恢复、常见误区、练习和导出。
- 本单元的教学主线应保持为：先看单卡训练循环里的状态流，再解释多卡扩展为什么需要同步、分片和恢复能力。
- 推荐保留的锚点例子：一个训练 step，从 forward 读参数、写激活，到 backward 读激活、写梯度，再到 optimizer step 读梯度和优化器状态、写回参数。

## Course Map Cues

- 01 之后的 02 重点是数据并行、梯度同步与通信。
- 03 接 FSDP2 与参数分片。
- 04 和 05 再进入张量并行、流水线并行和 Megatron Core 训练栈。
- 06-08 处理激活检查点、混合精度、检查点、容错和选型。

## Gaps

- 没有外部官方 source pack，因此本次重构不引入新的公开来源边界。
- 本单元应保持为概念与操作桥接，不扩成框架 API 教程。
- 若课程地图或单元命名以后变化，先回看 `index.html` 再改学习页。
