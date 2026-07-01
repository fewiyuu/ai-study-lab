# P4：评估生成式人工智能能力时可能遇到的各种陷阱｜本地 source pack

## Source Boundary

- 课程：李宏毅 LLM 课程
- 单元：03_P04_第4讲：评估生成式人工智能能力时可能遇到的各种陷阱
- 整理快照：2026-06-21
- 主要输入：课程地图 `index.html`、课程根 `README.md`、旧版 `03_P04_.../学习页.html`
- 本讲关注的是生成式 AI 的评估方法和常见陷阱：benchmark、ground truth、metric、aggregation、人类评估、LLM judge、verifier、prompt 敏感、data leakage、jailbreak、prompt injection、偏见和部署指标。

## 这一讲要依赖什么

- 课程地图 `index.html`
  - 确认 P4 位于课程前段，紧接在剖析模型内部之后。
  - 确认后续课程会继续进入机器学习基础、训练技巧、学习历程、安全、可解释性、多模态和作业实践。
- 旧版 `03_P04_.../学习页.html`
  - 提供本页的原始知识骨架：benchmark、ground truth、metric、BLEU/ROUGE/BERTScore、Goodhart、幻觉、MOS、人类评分、LLM judge、verifier、泄题、安全和偏见。
  - 提供可观察的例子：摘要评估、排行榜误导、LLM 评委偏见、泄题样本、地理题 prompt 敏感、攻击预算和 lower-bound 风险。
  - 提供误区边界：只看排行榜、只看平均分、把格式错误当知识错误、把自动评分当绝对真相、把安全通过当长期安全。
- 课程根 `README.md`
  - 提供课程资料组织方式和本地目录约定。
  - 用来确认本页仍然属于同一套长期研习资料，而不是独立摘出的评估笔记。

## 本单元的教学合同

- 这一页只讲评估与诊断，不展开模型结构、训练细节、RAG 管线、多模态生成或作业题全文。
- 评估链路统一写成：任务定义 -> benchmark -> prompt -> metric -> aggregation -> decision，必要时再加入 human judge / LLM judge / verifier。
- 页面里的代码只作为观察路线，不承诺任何外部服务在本地环境一定可直接运行。

## 这页准备回答什么

- 为什么生成式 AI 的分数不能只看一个排行榜数字。
- 有标准答案、没有标准答案、以及安全对抗场景下，评估分别该怎么做。
- exact match、BLEU/ROUGE、BERTScore、人类评分、LLM judge、verifier 各自适合什么任务。
- Goodhart 定律、prompt 敏感、data leakage、jailbreak 和 prompt injection 为什么会把分数带偏。

## Open Gaps

- 当前单元目录没有独立字幕正文文件，重构时只能把旧学习页中已经整理出的内容当作本地事实边界。
- 如果后续补齐课堂原文或官方字幕，可继续校对模型名、课堂示例和评估表述的精确措辞。
