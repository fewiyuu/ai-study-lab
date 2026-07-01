# LoRA 论文精读 · 第 3 块 source pack

## 资料边界

本页只使用课程根目录里的本地材料，不在页面生产阶段重新爬网：

- `../index.html`
- `../课程拆解.md`
- `./学习页.html`（旧版学习页，作为内容母版）

Snapshot: access date 2026-06-21.

## 这节课要解决什么

第 3 块的任务很具体：把 LoRA 放回 Transformer block 里，说明它通常落在哪些 dense layer 上，为什么论文和实践常先看 `W_q`、`W_v`，以及这些选择怎样影响显存、checkpoint、吞吐和任务切换。

读完这一节，学习者应该能解释：

- LoRA 原则上可以放到任意 dense layer，但论文主要研究 attention 权重
- `q_proj / k_proj / v_proj / o_proj` 和 `W_q / W_k / W_v / W_o` 的对应关系
- `W_q`、`W_v` 常被优先选择的工程原因，以及 merge / unmerge 的状态边界

## 来源如何支持这节课

| 来源 | 支持内容 |
|---|---|
| `../index.html` | 课程顺序、每块角色、先后依赖、整门课的学习路径 |
| `../课程拆解.md` | 术语表、知识骨架、可练习点、资料边界、`W_q/W_v` 的课程定位 |
| `./学习页.html` | 旧版第 3 块的具体论述、例子、对照表、练习题和边界提醒 |
| `LoRA: Low-Rank Adaptation of Large Language Models`（arXiv:2106.09685） | Applying LoRA to Transformer、Practical Benefits and Limitations 等论文段落对应的概念依据 |

## 旧页里已经有的关键材料

旧页已经覆盖了这条主线，重构时要保留并整理成更稳的教学链：

1. LoRA 原则上可用于任意 dense layer，但论文主要研究 attention 权重。
2. 论文实验和实现里常先看 `W_q` 与 `W_v`，把它们作为最典型的 target modules。
3. 工程收益不只来自参数少，还来自显存、checkpoint、吞吐和任务切换方式。
4. merge / unmerge、混合任务 batch 和重复 merge 是这节里最容易混淆的状态问题。

## 这页应该怎样改写

重构时不要只把旧页换成新壳，而要把它整理成一条可检查的教学链：

- 先用一个 Transformer block 的小例子把 `q / k / v / o` 的位置钉住
- 再说明为什么论文和工程上常先看 `W_q`、`W_v`
- 再用状态表讲清训练态、merge 态和混合任务态的差别
- 最后把“显存更省”拆成参数、梯度、checkpoint 和任务切换四笔账

## 后续单元衔接

这一节只负责 LoRA 在 Transformer 里的落点和工程含义，不展开 rank 解释和实验表格：

- 第 4 块：实验设计与结果解读
- 第 5 块：rank 与低秩解释
- 第 6 块：实践验收与论文复述

## 公开边界

- 不把 QLoRA、DoRA、AdaLoRA、rsLoRA 扩成新综述
- 不把 `W_q / W_v` 写成所有模型和所有任务的唯一最优选择
- 不把 merge 说成训练时必须执行的步骤
- 不把参数少直接写成推理一定更快
- 不暴露本地生成流程、临时任务文件或私人路径

