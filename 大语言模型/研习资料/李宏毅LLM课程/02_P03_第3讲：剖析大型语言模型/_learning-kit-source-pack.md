# P03：剖析大型语言模型｜本地 source pack

## Source Boundary

- 课程：李宏毅 LLM 课程
- 单元：02_P03_第3讲：剖析大型语言模型
- 整理快照：2026-06-21
- 主要输入：课程地图 `index.html`、课程根 `README.md`、旧版 `02_P03_第3讲：剖析大型语言模型/学习页.html`
- 这次重构的目标：把这一讲从旧壳迁入 learning-kit 1.0 的共享学习页结构，保留“模型内部怎么剖开”的主线。

## 这一讲要依赖什么

- 课程地图 `index.html`
  - 确认 P03 位于课程的早期核心位置，紧接在“建立入口”的 P01 之后。
  - 确认后续还会继续进入评估、机器学习基础、训练技巧、可解释性、RAG、Transformer、安全、多模态等主题。
- 旧版 `02_P03_第3讲：剖析大型语言模型/学习页.html`
  - 提供本页的原始知识骨架：LM head、logits、softmax、temperature、representation、logit lens、patch scope、Q/K/V、attention matrix、FFN。
  - 提供可观察的例子：Hugging Face 的 hidden states / attentions 路线、最小模型前向检查、模型内部表示怎么变。
  - 提供误区边界：把 token id 当语义大小、把 attention 当唯一解释、把 logit lens 当最终答案、把 FFN 忽略成“附属层”。
- 课程根 `README.md`
  - 提供课程资料组织方式和本地目录约定。
  - 用来确认本页仍然属于同一套长期研习资料，而不是单独摘出来的孤立笔记。

## 本单元的教学合同

- 这一页只讲训练好之后的前向剖析，不展开训练过程、RLHF、RAG、检索管线或多模态生成。
- anchor example 统一使用一小段可追踪的 token 序列和其中的 `apple` / `The apple is green` 类上下文，方便跨章节比较表示漂移、attention 方向和 logit lens 投影。
- 页面里的代码只作为观察路线，不承诺所有模型都能在同一环境里直接跑通；涉及模型卡、显存和授权时，默认以课程里可观察的最小路线为准。

## 这页准备回答什么

- 一个 token 是怎样进入 embedding，再经过若干层 Transformer 变成 contextualized representation 的。
- 为什么中间层的表示可以被 `logit lens` 重新投影成候选 token 分布。
- attention matrix、Q/K/V 和 residual / FFN 各自负责什么，出了问题时优先看哪一层。
- 用 Hugging Face 的 `output_hidden_states` / `output_attentions` / `lm_head` 路线，怎样把课堂概念变成可打印、可检查的对象。

## Open Gaps

- 当前目录没有独立字幕正文文件，重构时只能把旧学习页中已经整理出的内容当作本地事实边界。
- 如果后续补齐课堂原文或官方字幕，可继续校对模型名、课堂示例和示意代码的精确措辞。
