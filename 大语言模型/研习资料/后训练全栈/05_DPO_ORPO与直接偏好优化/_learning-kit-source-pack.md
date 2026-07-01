# DPO、ORPO 与直接偏好优化｜本地源包

生成日期：2026-06-22

## 取材范围

- `../index.html`
- `../04_偏好数据与奖励建模/学习页.html`
- Hugging Face TRL：`Reward Modeling`、`DPO Trainer`、`ORPO Trainer`
- 论文：`Direct Preference Optimization: Your Language Model is Secretly a Reward Model`
- 论文：`ORPO: Monolithic Preference Optimization without Reference Model`
- 论文：`Scaling Laws for Reward Model Overoptimization`

本源包只整理当前课程地图、相邻单元和官方公开资料，不重新爬取别的页面，也不抄录大段原文。

## 这页要解决的问题

这一页承接“偏好数据与奖励建模”，把读者带到直接偏好优化这一层。需要先把下面几件事分开：

- `DPO` 在优化什么
- `reference model` 在哪里起作用
- `ORPO` 为什么可以不显式依赖 reference model
- 为什么 `reward / margin` 变好，不代表真实质量一定同步变好

这一页不应展开 `PPO / GRPO` 的完整训练环，也不应把更广的 loss 变体当作主线。

## 来自课程地图的结构线索

课程根目录 `index.html` 给出的顺序是：

1. 后训练全景与模型角色
2. SFT 数据模板与 `loss_mask`
3. SFT 训练配置与快速实验
4. 偏好数据与奖励建模
5. DPO、ORPO 与直接偏好优化
6. PPO、GRPO 与 RLHF 训练环
7. 评测、判别器与回归检查
8. 发布边界与安全回退

这说明第 05 单元的职责不是讲“偏好数据本身”，而是把它推进到可直接优化的目标式，并把读者送进下一页的 RLHF 训练环。

## 来自相邻单元的前提

上一页已经讲过：

- `prompt / chosen / rejected`
- `reward model` 的训练目标
- `reward hacking` 的第一批信号

这一页默认这些概念已经熟悉，所以不重复讲偏好样本怎么标、reward model 怎么训，只拿它们当输入。

## 来自官方文档的支撑

- `Reward Modeling`（TRL，访问于 2026-06-22）：`RewardTrainer` 说明 reward model 的输入可以是 preference dataset，支持标准和 conversational 形式。这一页用它来区分“训练 reward model”与“直接偏好优化”。
- `DPO Trainer`（TRL，访问于 2026-06-22）：说明 DPO 训练的是同一 prompt 下的一对 completion，目标是相对 `reference model` 拉开 preferred / dispreferred 的 log-likelihood margin，不需要显式 reward model。
- `ORPO Trainer`（TRL，访问于 2026-06-22）：说明 ORPO 是 reference-model-free 的 preference optimization，把 log odds ratio 项并入 NLL loss，主张在 SFT 阶段同时加入偏好压力。
- `Direct Preference Optimization` 论文（2023，访问于 2026-06-22）：说明 DPO 可以把原本复杂的 RLHF 目标改写成简单的分类式损失，并省掉训练时采样环节。
- `ORPO` 论文（2024，访问于 2026-06-22）：说明 ORPO 认为 SFT 仍然关键，只需对 disfavored generation 施加较小惩罚，同时对 chosen response 加强适配信号。
- `Scaling Laws for Reward Model Overoptimization`（2022，访问于 2026-06-22）：说明 proxy reward 往上走，不代表真实质量一定往上走，Goodhart 风险会在偏好优化里出现。

## 这页应该给出的结论

读者读完后，应该能：

- 说清 `DPO` 的核心读法
- 说清 `ORPO` 为什么能少一个 reference model
- 解释 `beta` 或 `lambda` 这类超参数在偏好优化里管什么
- 识别“训练指标变好，但真实效果变差”的早期信号

## 明确边界

这页应当覆盖：

- `DPO` 的核心目标式和 `reference model` 作用
- `ORPO` 的 SFT + odds ratio 思路
- `reward / margin` 的监控读法
- 过优化和代理目标失真的基本判断

这页不应当硬展开：

- `PPO / GRPO` 的完整 rollout 与 policy update 环
- 更广的 preference loss 变体家族
- 大规模分布式训练策略
- 发布审查与安全回退的完整流程

## 这页适合直接搬进正文的关键判断

- `DPO` 不是“更简单的 PPO”，而是把偏好约束换成直接可优化的 margin。
- `reference model` 在 DPO 里是锚点，不是多余背景。
- `ORPO` 省掉了显式 reference model，但仍然要看 chosen / rejected 的相对压力是否稳定。
- `rewards/margins`、`reward graph`、`log_odds_ratio` 这些指标能看趋势，但不能单独当成真实质量。
- 偏好优化里最常见的坑，不是“不会收敛”，而是“学会了代理信号”。

## 课程衔接

- 读完这一页后，下一页应该接 `PPO、GRPO 与 RLHF 训练环`
- 如果读者还分不清 `chosen`、`reference` 和 `reward` 的关系，先不要跳到更复杂的在线 RL
- 如果读者已经能解释 DPO 和 ORPO 的差别，再进下一页会更顺
