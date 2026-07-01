# Source Pack: 02_Transformer与Attention直观理解

## Source Boundary

- Course root: `LLM基础与应用工程`
- Unit: `02_Transformer与Attention直观理解`
- Snapshot / 访问日期: `2026-06-21`
- Source material used in this run:
  - course-root `index.html`
  - current unit page `学习页.html`
  - course-root `course-shell.json`
  - course-root shared runtime assets under `assets/`

## Source-To-Unit Notes

- 课程总图确认本单元位于 `01_tokenizer_embedding_contextwindow` 之后、
  `03_预训练微调推理角色边界` 之前，是模型结构的第二个基础单元。
- 旧版学习页已经给出本单元的教学主线：attention 直觉、Q/K/V 分工、
  Transformer block、mask 与生成、最小代码验收、误区诊断和练习记录。
- 这次重构保留原有学习目标，但改成 learning-kit 1.0 的共享 shell、
  可检查练习、可导出复盘上下文和更清楚的来源边界。

## Unit Role

- Foundation unit.
- 讲清 Transformer 的核心读法：先看 attention 如何跨 token 读取，
  再看 Q/K/V、残差、LayerNorm、FFN 和 causal mask 如何把这一层补完整。
- 继续承接上一单元的输入边界，但暂不展开更深的多头推导、位置编码
  细节或训练目标。

## Gaps And Notes

- 本次重构没有新增外部公开资料，主要依据课程内已有总图与旧页。
- 代码、形状和 mask 顺序等具体讲法保持与旧页一致，只改写表达和结构。
- 后续如需扩展到更完整的论文式教学，再补公开 lecture、博客或论文来源。
