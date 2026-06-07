---
title: 推理型提示：CoT、Self-Consistency 与生成知识
aliases:
  - Chain-of-Thought
  - Self-Consistency
  - Generated Knowledge Prompting
  - 思维链
tags:
  - AI/提示工程
  - AI/大模型
  - AI/推理
  - 学习笔记/course-forge
source: https://www.aneasystone.com/archives/2024/01/prompt-engineering-notes.html
created: 2026-06-06
---

> [!question] 为什么简单任务不一定需要 CoT？
> CoT 会增加输出长度和成本。翻译、格式转换、简单提取这类任务通常直接提示更清楚。

> [!question] Zero-shot CoT 和 Few-shot CoT 怎么选？
> 没有示例、临时处理多步题时先用 Zero-shot CoT；重复型任务、能准备高质量样例时用 Few-shot CoT。

> [!question] Self-Consistency 为什么能提高稳定性？
> 它多次生成不同推理路径，对最终答案做聚合，减少单次采样偶然错误。

> [!question] Generated Knowledge 和 RAG 有什么区别？
> Generated Knowledge 使用模型自己生成的候选知识；RAG 使用外部资料。前者不能当作可靠来源。

> [!abstract] 核心主线
> 复杂任务失败常来自三类原因：步骤不清、单次不稳、背景不足。CoT 让模型显式分解问题；Self-Consistency 用多路径投票提高稳定性；Generated Knowledge 先生成相关知识，再基于知识回答。涉及权威事实时，应优先检索资料。

## 概念精讲

### Chain-of-Thought

引导模型生成中间推理步骤再回答。价值是减少跳步，便于检查推理路径。边界是推理文本可能合理但错误。

### Zero-shot CoT

不提供示例，只用“请逐步分析”这类触发语引导分步推理。低成本，但稳定性不如高质量示例。

### Few-shot CoT

提供少量“问题 + 推理链 + 答案”的示例，让模型模仿任务格式和推理粒度。示例质量、顺序和多样性都会影响结果。

### Self-Consistency

采样多条推理路径，对最终答案多数投票。它提升的是稳定性，不是真理保证。

### Generated Knowledge Prompting

先让模型生成相关知识，再把知识作为上下文回答。生成知识只能当候选背景，不能替代可引用来源。

## 最小可操作样例

```text
请逐步分析问题，最后单独给出最终答案。

问题：
{question}

输出格式：
已知条件：
- ...

关键步骤：
1. ...
2. ...

最终答案：
...

可能的错误来源：
- ...
```

> [!todo] 行动清单
> - [ ] 遇到多步问题时，先判断是否需要 CoT。
> - [ ] 常见重复任务积累 2-5 个高质量 Few-shot CoT 示例。
> - [ ] 对高波动问题尝试 5 次以上采样并投票。
> - [ ] 对常识题使用“先生成知识、再回答”的两阶段提示。
> - [ ] 对事实敏感问题，不用 Generated Knowledge 替代检索。
> - [ ] 所有推理型输出都单独标出最终答案。
> - [ ] JSON 场景只输出结构化字段，不在 JSON 外写解释。

## 应用与迁移问答

### 写文章能用 CoT 吗？

可以，但更像“先规划再生成”。先列主题、论点、结构，再写正文。

### 代码调试能用 Self-Consistency 吗？

可以让模型提出多个可能原因，再按日志和测试筛选。最终仍要靠复现实验验证。

### 知识问答应该用 Generated Knowledge 吗？

常识解释可以用；涉及最新、权威、专业事实时，应优先检索资料或提供上下文。

> [!quote] 费曼解释润色版
> 推理型提示解决的是复杂任务里的跳步问题。CoT 让模型先写关键步骤，再给答案，适合多步计算、逻辑判断和需要解释路径的任务。Self-Consistency 不相信一次生成，而是让模型走多条路径，再看最终答案是否一致。Generated Knowledge 先列出相关背景知识，再基于这些知识回答，适合常识推理。它们都有边界：步骤看起来合理不代表正确，多数答案不代表事实，模型生成的知识也不能当可靠来源。

> [!warning] 易错卡片：把 CoT 当成事实校验
> 误区：模型写了完整推理，所以答案一定对。
> 正确说法：推理步骤仍要检查条件、计算和来源。
> 提醒：推理文本可能是在合理化错误。

> [!warning] 易错卡片：Few-shot 示例没有推理链
> 误区：示例只给答案，最后要求模型推理。
> 正确说法：示例和目标输出要同构。
> 提醒：问题、步骤、答案都要出现在样例里。

> [!warning] 易错卡片：Self-Consistency 路径不独立
> 误区：一次回答里生成多条路径再投票。
> 正确说法：优先多次独立调用，再聚合答案。
> 提醒：一次回答中的路径会互相影响。

> [!warning] 易错卡片：Generated Knowledge 不校验
> 误区：模型生成什么知识就直接采用。
> 正确说法：生成知识是候选背景。
> 提醒：高风险或事实敏感场景改用检索。
