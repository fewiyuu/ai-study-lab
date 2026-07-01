# 偏好数据与奖励建模｜本地源包

生成日期：2026-06-21

## 取材范围

- `../index.html`
- `../03_SFT训练配置与快速实验/学习页.html`
- Hugging Face TRL：`Reward Modeling`（`RewardTrainer`）、`DPO Trainer`、`GRPO Trainer`、`Quickstart`
- Hugging Face TRL：`Reward Functions`（用于理解奖励函数和 reward model 的边界）
- Hugging Face Alignment Handbook：偏好优化、评测和训练习惯

本源包只整理现有课程地图、相邻单元和公开官方文档，不重新爬取其他外部资料。

## 这页要解决的问题

这一页承接 SFT 配置实验，进入偏好数据与奖励建模阶段。读者需要先把下面四件事分开：

- 偏好样本怎么长
- `chosen / rejected` 说明的是什么
- 奖励模型在训练里学什么
- `reward hacking` 为什么会出现

这页不应直接展开 DPO、ORPO、PPO 或 GRPO 的完整算法推导；它只负责把“比较数据”与“奖励信号”讲清楚。

## 来自课程地图的结构线索

课程根目录 `index.html` 给出的顺序是：

1. 后训练全景与模型角色
2. SFT 数据模板与 loss_mask
3. SFT 训练配置与快速实验
4. 偏好数据与奖励建模
5. DPO、ORPO 与直接偏好优化
6. PPO、GRPO 与 RLHF 训练环
7. 评测、判别器与回归检查
8. 发布边界与安全回退

这说明第 04 单元应该承担“从 SFT 走到偏好优化”的桥梁职责。先把比较数据、噪声、奖励模型和 reward hacking 讲清，下一页再进入 DPO / ORPO。

## 来自相邻单元的前提

上一页已经把 SFT 配置与 smoke test 的思路讲过，包含 batch、packing、LoRA、学习率、日志和 checkpoint 的基本判断。这里不再重复这些配置细节，只复用一个结论：训练跑通以后，下一步要学会分辨“数据偏好”与“奖励代理”。

## 这页应该给出的结论

读者读完后，应该能：

- 解释一个偏好样本为什么能训练
- 看出标注噪声会从哪里扭曲 reward
- 说清 `RewardTrainer` 的输入、输出和训练目标
- 识别 `reward hacking` 的常见表面信号

## 明确边界

这页应当覆盖：

- `pairwise preference`
- `rubric` 与标注噪声
- `reward model` 的训练逻辑和评价方式
- `reward hacking` 的症状和检查顺序

这页不应当硬展开：

- DPO / ORPO 的完整公式
- PPO / GRPO 的完整训练环
- 更大规模分布式训练策略
- 发布审核和安全回退的完整流程

## 需要保留的学习语气

- 先看样本，再看分数
- 先看比较标准，再看模型
- 先看高分样本是否真的更好，再看训练曲线
- 先把 reward 当代理目标，再看它会不会被钻空子

## 适合搬进新页的关键判断

- `chosen` 不是完美答案，只是同一对里更可取的答案
- `RewardTrainer` 学的是偏好排序，不是生成完整回答
- `reward` 的绝对值通常不能直接跨设置比较
- `label noise` 不只来自标错，也来自 rubric 模糊、任务歧义和展示偏差
- `reward hacking` 是代理目标失真，不是单纯“训练没收敛”

## 课程衔接

- 读完这一页后，下一页应该接 `DPO、ORPO 与直接偏好优化`
- 如果读者还分不清 `chosen / rejected` 和 reward 的关系，先不要跳到 PPO / GRPO
- 如果读者已经能说明偏好样本如何训练，再进入直接偏好优化会更顺
