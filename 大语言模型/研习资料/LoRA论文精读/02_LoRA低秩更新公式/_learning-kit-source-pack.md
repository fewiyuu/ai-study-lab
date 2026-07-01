# LoRA 论文精读 · 第 2 块 source pack

## 资料边界

本页只使用课程根目录中的本地材料，不在页面生产阶段重新爬网：

- `../index.html`
- `../课程拆解.md`
- `./学习页.html`（旧版学习页，作为内容母版）

这些材料共同对应论文 **LoRA: Low-Rank Adaptation of Large Language Models** 的方法部分，尤其是 `Low-Rank-Parametrized Update Matrices`。课程拆解中列出的公共来源包括：

- https://arxiv.org/abs/2106.09685
- `原始资料/source/iclr2022_conference.tex`
- `原始资料/source/expt.tex`

Snapshot: access date 2026-06-21.

## 这节课要解决什么

第 2 块只处理 LoRA 的核心公式，不展开 Transformer 放置位置和实验表格。学习者读完后应该能做四件事：

1. 写出 `h = W_0 x + BAx` 和带缩放的 `h = W_0 x + (alpha / r) BAx`。
2. 解释 `W_0 in R^{d x k}`、`A in R^{r x k}`、`B in R^{d x r}`、`r << min(d,k)` 的形状关系。
3. 根据 `d`、`k`、`r`、层数和目标矩阵数估算 LoRA 的可训练参数量。
4. 说明初始化、`alpha / r` 缩放、merge/unmerge 和重复 merge 的诊断方法。

## 来源如何支持这节课

| 来源 | 支持内容 |
|---|---|
| `../index.html` | 第 2 块在课程中的角色：承接 PEFT 动机，进入低秩更新公式，为 Transformer 放置和实验解读做准备 |
| `../课程拆解.md` | 术语表、知识骨架、公式边界、可练习点、资料边界 |
| `./学习页.html` | 旧版第 2 块的公式、矩阵形状图、参数量计算器、初始化解释、merge 示例、练习题 |

## 旧页里已经有的关键材料

旧页的主线可以保留，但需要迁入 shared shell 并补足反馈：

1. LoRA 冻结预训练权重 `W_0`，只训练低秩分支 `A` 和 `B`，让 `Delta W = BA`。
2. 形状检查是第一道验收：`BA` 必须和 `W_0` 一样是 `d x k`，才能和原权重相加。
3. 参数量从 full fine-tuning 的 `d*k` 变成 LoRA 的 `r(d+k)`；对方阵投影可近似为 `2*d_model*r`。
4. 初始化使用 `A` 随机、`B=0`，使训练第 0 步仍等同于预训练模型输出。
5. `alpha/r` 控制 LoRA 分支进入主分支的尺度，不是优化器学习率。
6. merge 后可以把 `W_0 + scaling * BA` 视作普通线性层；但混合任务 batch 和重复 merge 需要单独诊断。

## 这页应该怎样改写

重构目标不是换壳，而是把公式讲成可检查的机制链：

- 先用一个线性层的 forward 例子锚定 `x -> A -> B -> h`。
- 用形状追踪和读写表说明每一步读什么、写什么、错了会出现什么症状。
- 用小数字矩阵和 4096 维投影两个例子连接“公式”和“参数量”。
- 用代码片段说明训练态、merge 态、unmerge 态的状态边界。
- 练习区要混合选择、填空、匹配、诊断和短答；开放题必须有参考答案或评分要点。

## 后续单元衔接

这一节只负责公式和状态账本。后续概念不在本页展开：

- 第 3 块：LoRA 放进 Transformer 的具体位置，尤其是 `W_q`、`W_v` 等线性层。
- 第 4 块：实验设计与结果读法。
- 第 5 块：rank 扫描、低秩现象和子空间解释。
- 第 6 块：实践验收、target modules、保存、加载和论文复述。

## 公开边界

- 不把 QLoRA、DoRA、AdaLoRA、rsLoRA 扩成新综述。
- 不把 `alpha/r` 写成学习率，也不把 merge 说成训练时必须执行的步骤。
- 不宣称 rank 越大指标一定更好；本页只说明 rank 改变表达自由度和参数量。
- 不暴露本地生成流程、临时任务文件或私人路径。
