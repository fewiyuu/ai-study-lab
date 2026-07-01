# 03 Transformer 最小实现｜本地源包

## 单元边界

这一页只负责把最小 decoder-only Transformer 的前向结构讲清楚：输入 token ids、embedding、causal attention、MLP、残差、归一化和输出头。它不展开完整训练循环、优化器调参、分布式训练或 checkpoint 细节，这些留给下一单元。

## 公开来源边界

### 1. Stanford CS336: Language Modeling from Scratch

- 访问日期：2026-06-21
- 用途：确定课程主线、基础实现顺序和“从零实现语言模型”该先学什么
- 支持内容：tokenizer 之后如何进入 Transformer、最小实现应包含哪些模块、训练前后接口如何衔接

### 2. CS336 Assignment 1: Basics

- 访问日期：2026-06-21
- 用途：提供最小实现的具体组件参考
- 支持内容：embedding、attention、MLP、残差、归一化、输出头这些基础结构如何放进一个可运行的语言模型

### 3. karpathy/llm.c

- 访问日期：2026-06-21
- 用途：提供从 PyTorch 参照到 C/CUDA 训练实现的公开对照
- 支持内容：前向路径、训练接口、权重绑定、性能与实现细节之间的关系

### 4. OLMo 2 论文与项目页

- 访问日期：2026-06-21
- 用途：观察现代开放模型公开披露的架构选择
- 支持内容：RMSNorm、QK-Norm、SwiGLU、RoPE、输出侧归一化等设计选择

### 5. Transformers OLMo2 文档

- 访问日期：2026-06-21
- 用途：核对现代开放模型在 Hugging Face 体系里的公开组件命名与接口
- 支持内容：模型组件、位置编码、归一化与实现选择的公开说明

## 本页应复用的 anchor 例子

- `input_ids -> embedding -> block -> logits` 这条数据流要贯穿整页
- `B, T, C, H, V` 这组符号要在形状页、公式页、代码页和练习里保持一致
- `x = x + Attention(norm1(x))`、`x = x + MLP(norm2(x))` 这一类残差写法要和代码示例对齐

## 需要保留的教学判断

- 先讲前向结构，再讲训练循环
- 先区分 attention 与 MLP 的职责，再讲残差和归一化
- 先用最小实现解释 shape，再引入 RoPE、QK-Norm、FlashAttention、KV cache 这些扩展
- 先让 learner 能读懂 `forward(input_ids) -> logits`，再进入 loss、backward 和参数更新

## 已知边界

- 不把这一页写成“完整训练系统说明”
- 不把现代架构变体全部塞进同一个 block
- 不把权重共享、位置编码、归一化和输出头混成一条模糊叙述
- 不把公式、代码和形状表分开成彼此无关的卡片
