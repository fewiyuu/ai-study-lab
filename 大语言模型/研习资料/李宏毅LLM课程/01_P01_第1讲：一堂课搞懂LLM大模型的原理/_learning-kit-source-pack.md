# P1：一堂课搞懂 LLM 大模型的原理｜本地 source pack

## Source Boundary

- 课程：李宏毅 LLM 课程
- 单元：01_P01_第1讲：一堂课搞懂 LLM 大模型的原理
- 整理时间：2026-06-21
- 主要输入：课程根 `README.md`、课程地图 `index.html`、旧版 `01_P01/学习页.html`
- 原始字幕线索：`README.md` 指向的 P1 中文字幕文件名为「P1【第1讲：一堂课搞懂LLM大模型的原理】—【2026-04-23】-中文.md」。当前可见课程根内未放置该字幕正文，重构以旧学习页已经整理出的 P1 内容为本地事实边界。

## 本单元主要依赖什么

- 课程地图 `index.html`
  - 确认 P1 是整套课的第一节核心讲义。
  - 确认它位于“建立入口”阶段，后面会接 P3「剖析大型语言模型」、评估、训练、RAG、Transformer、安全、多模态等主题。
- 旧版 `01_P01/学习页.html`
  - 提供本讲主线：LLM 不是一次性写完整答案，而是按 prompt 逐步预测下一个 token。
  - 提供术语边界：token、token id、vocabulary、Hugging Face token、prompt、chat template、system prompt、context engineering。
  - 提供机制链：prompt -> tokenizer -> token id -> model -> vocabulary 概率分布 -> 采样 -> 追加 token -> 直到结束符或长度上限。
  - 提供工程观察路线：`tokenizer.encode/decode`、`apply_chat_template`、`model.generate`、`pipeline`。
  - 提供误区：把 LLM 当数据库、把 token 当字数、把 chat template 当装饰、以为多轮对话靠模型自动记忆、把 system prompt 当万能控制。
- 课程 README
  - 确认这一套资料是多单元长期学习包，每个单元以 `学习页.html` 呈现，原始材料由 README 链接追踪。

## Source-To-Unit Notes

- 本页只讲 LLM 的工作直觉和最小工程观察面，不展开 Transformer 内部、预训练损失、RLHF、安全对齐、多模态扩散模型或生产级 RAG。
- 核心锚点例子保留「人工 -> 智/呼/程」这一类 next-token 候选，帮助学习者看见概率分布和采样。
- Hugging Face 代码只作为观察路线，不承诺具体模型可在任意本地环境运行。Llama 系列授权、显存、模型卡说明都可能变化，实际执行要以模型卡和运行环境为准。
- 练习重点应检查学习者能否把一次聊天回答拆成可排查流程：模型真正看到什么、哪一步生成概率、采样怎样引入差异、错误怎样被上下文继续放大。

## Open Gaps

- 当前单元目录没有独立字幕正文文件，页面参考资料需说明这一限制。
- 如果后续补齐原始字幕，可进一步校对 Hugging Face 演示中具体模型名称、上下文日期和课堂原话。
