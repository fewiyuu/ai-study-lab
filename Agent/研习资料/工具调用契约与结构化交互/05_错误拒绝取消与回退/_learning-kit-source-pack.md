# 05｜错误、拒绝、取消与回退 本地 source pack

## Source Boundary

- Course: 工具调用契约与结构化交互
- Unit: `05_错误拒绝取消与回退/学习页.html`
- Snapshot date: 2026-06-21
- 访问日期: 2026-06-21
- Local reading base: 课程首页 `index.html`、当前单元旧版 `学习页.html`
- Public source families used in this pass:
  - OpenAI Structured Outputs guide: https://developers.openai.com/api/docs/guides/structured-outputs
  - OpenAI Function Calling guide: https://developers.openai.com/api/docs/guides/function-calling
  - MCP Tools spec 2025-06-18: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
  - MCP cancellation / lifecycle pages: https://modelcontextprotocol.io/specification/2025-03-26/basic/utilities/cancellation and https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle
  - BFCL V4 leaderboard: https://gorilla.cs.berkeley.edu/leaderboard.html
- No additional web crawl was used to fill in the local lesson draft beyond the public docs above.

## What The Course Index Establishes

课程首页把这门课排成一条连贯路线：

1. 先讲工具调用的契约思维
2. 再讲函数调用基础、描述选择与分发
3. 接着讲结构化输出与 JSON Schema
4. 然后进入 MCP 工具规范与协议边界
5. 本单元继续处理错误、拒绝、取消与回退
6. 后面再到 BFCL 评测和可维护工具面的设计准则

对本单元最重要的约束是：

- 不把“失败”写成一个笼统名词
- 不把拒绝、取消、业务错误和回退混成一层
- 不把回退理解成“失败后随便换一个更强工具”
- 不把评测只写成成功样例展示

## What The Old Page Already Covers

旧页已经有一条可用的教学骨架，方向是对的：

- 失败是契约的一部分，不是例外
- Structured Outputs 解决的是形状稳定，不解决所有语义问题
- MCP 需要把协议错误和工具错误分开
- 取消应该被当作生命周期控制
- 回退要比重试更窄
- BFCL 强调不调用也是一种能力
- 练习已经覆盖概念判断、场景诊断和评测设计

## Source-To-Unit Mapping

### 1. 课程首页

支持内容：

- 本单元在整门课里的位置
- 这页前后应该接什么
- 课程范围到哪里为止

### 2. 当前单元旧页

支持内容：

- 失败、拒绝、取消、回退的教学顺序
- 具体案例与错误对象草案
- 练习题材和负例方向

### 3. OpenAI Structured Outputs

支持内容：

- 结构化输出和 schema 约束的边界
- refusal 如何单独成分支
- 为什么“能解析”不等于“业务一定正确”

### 4. OpenAI Function Calling

支持内容：

- 函数 / 工具描述如何影响选择
- 失败分支如何影响后续动作
- 把动作交给宿主程序执行时的契约意识

### 5. MCP Tools + Cancellation / Lifecycle

支持内容：

- 工具结果如何表达成功与失败
- `notifications/cancelled` 的请求 ID 与原因
- 取消是停止继续处理，不是普通业务失败

### 6. BFCL V4

支持内容：

- 负例、相关性、多步和异常处理
- “不调用”本身也是评测维度
- 把失败路径纳入回归集

## What To Keep

重构时要保留的不是旧 HTML 壳，而是旧页的教学主线：

1. 先把失败分成几类
2. 再把每一类对应到契约字段和恢复动作
3. 用错误对象、取消通知和 fallback policy 串起来
4. 最后把这些动作放进可测的负例集合

## What To Sharpen

- 把 refusal、error、cancel、fallback 的边界拆得更清楚
- 给出一张可执行的分流表，让读者知道每类问题先看哪一层
- 加一个可迁移的错误对象示例，让恢复语义落到字段
- 把“回退”写成比重试更窄的动作，不要写成继续扩张能力
- 在练习里补足“无适用工具”和“晚到结果”这两类负例

## Gaps And Boundaries

- 这份 source pack 只依赖本地已有页面和公开文档家族，没有重新爬取整套站点
- 本页不要扩成 Structured Outputs 总览；那是上一单元的延伸，不是这一页的主线
- 本页不要扩成 MCP 协议总览；这里只讲错误、拒绝、取消与回退如何进入契约
- 本页不要扩成 BFCL 大赛说明；这里只借用它的测试拆分方式
- 本页不要把 fallback 写成“多调一个工具试试”，那会越过授权和边界
