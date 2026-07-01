# SFT 训练配置与快速实验｜本地源包

生成日期：2026-06-21

## 取材范围

- `../index.html`
- `../02_SFT数据模板与loss_mask/学习页.html`
- Hugging Face TRL 文档：`SFTTrainer`、`SFTConfig`、`packing`、`assistant_only_loss`、`completion_only_loss`
- Hugging Face Transformers 文档：`chat templating`、`apply_chat_template`、`add_generation_prompt`
- Hugging Face PEFT 文档：LoRA 的 `r`、`target_modules`、`alpha`、`dropout`
- Hugging Face Alignment Handbook：SFT 配方、smoke test、保存与评测习惯

本页只使用这些公开材料和当前课程地图，不重新爬取其他外部资料。

## 这页要解决的问题

读者已经知道一条 SFT 样本应该怎么被模板化、怎么划分 `labels`、哪些 token 应该进入 loss。这个单元继续往前走一步，回答“怎么把这条理解变成一份能跑的小实验”：

- `per_device_train_batch_size`、`gradient_accumulation_steps` 和 `max_length` 怎么一起控制显存和吞吐
- `packing` 什么时候适合开，什么时候应该先关掉
- `assistant_only_loss`、`completion_only_loss` 和 `dataset_text_field` 如何对应不同的数据形状
- `LoRA` 的 `r`、`target_modules`、`alpha`、`dropout` 和 `learning_rate` 分别在影响什么
- `logging_steps`、`save_steps`、`save_total_limit`、`seed` 和 `output_dir` 怎么让一次实验可复盘

## 来自课程地图的结构线索

课程根目录 `index.html` 把这门课排成：

1. 后训练全景与模型角色
2. SFT 数据模板与 loss_mask
3. SFT 训练配置与快速实验
4. 偏好数据与奖励建模
5. DPO、ORPO 与直接偏好优化
6. PPO、GRPO 与 RLHF 训练环
7. 评测、判别器与回归检查
8. 发布边界与安全回退

这说明第 03 单元应该承担“把样本层的理解翻译成可执行配置”的职责，而不是重新讲样本格式本身，也不该提前展开偏好优化或强化学习算法。

## 来自上一单元的可复用前提

上一页已经解决了：

- `messages` / `prompt-completion` 的边界怎么认
- `apply_chat_template` 怎么把结构化对话变成训练文本
- `assistant_only_loss` 和 `completion_only_loss` 为什么要跟着数据形状走
- `packing` 只改装箱方式，不修数据质量

因此第 03 单元只需要继续回答训练参数、实验节奏和故障排查，不再重复那些边界知识。

## 本页应该给出的结论

读者读完后，应该能：

- 设计一份小规模 SFT smoke test
- 解释为什么某个配置在省显存、提吞吐或保留可观测性
- 看到 OOM、输出重复、loss 不动或保存太慢时，先查哪个旋钮
- 知道什么时候该回到上一单元重新看样本边界，什么时候可以直接进入下一单元的偏好数据内容

## 明确边界

这页应当覆盖：

- SFT 配置的最小可运行结构
- batch、accumulation、`max_length`、`packing`、`LoRA`、`learning_rate`、日志和 checkpoint 的关系
- 训练小实验的排障顺序

这页不应当硬展开：

- 具体分布式训练策略的全部细节
- DPO / PPO / GRPO 的目标函数推导
- 各种新版本 TRL 的完整 CLI 参数表
- 更大规模实验中的系统工程优化

## 需要保留的学习语气

- 先看哪一个旋钮改了哪一层
- 先做 smoke test，再谈扩展
- 先确认边界没错，再开 packing
- 先让实验可解释，再追求更大吞吐

## 适合搬进新页的关键判断

- `per_device_train_batch_size` 直接影响每卡一次前向/反向的样本数
- `gradient_accumulation_steps` 影响有效 batch 和更新频率，不等于把显存无限放大
- `max_length` 影响序列长度和显存压力
- `packing` 只提高 token 利用率，不解决坏样本
- `LoRA` 的 `r`、`target_modules` 和 `learning_rate` 决定可训练容量和更新幅度
- `logging_steps`、`save_steps` 和 `save_total_limit` 决定实验是否容易回看和回滚

## 课程衔接

- 如果上一页的样本边界还不稳，先回 `02_SFT数据模板与loss_mask/学习页.html`
- 如果 smoke test 已经能跑通，下一步就去看 `04_偏好数据与奖励建模/学习页.html`
- 这页的目标是把 SFT 从“会看”变成“会跑”
