# 学习页 .md → .html 转换规范

本文档描述"一份合格的 `学习页.md` 会被转成什么样的 HTML"。不涉及具体 CSS 样式、脚本实现或构建工具——只定义输入格式和输出结构的对应关系。

---

## 1. 整体页面结构

每个 `学习页.md` 生成一个完整的 `.html` 文件，页面包含以下固定区域：

| 区域 | 来源 | 说明 |
|------|------|------|
| 页面标题 | frontmatter `title` | `<title>` 和 `<h1>` |
| 左侧导航栏 | 正文 section 标题 + `course_links` | 自动生成锚点导航 |
| Hero 区 | frontmatter `kicker`、`title`、`summary`、`can_do`、`course_links` | 页面顶部的导语块 |
| 正文区 | 所有 section | 按顺序渲染 |
| 导出区 | 固定模板 | 练习记录导出控件，始终存在 |
| 参考资料区 | `# 参考资料` section | 自动识别并放入 `<section id="sources">` |
| 页脚脚本 | 固定模板 | KaTeX、代码高亮、交互脚本，由 `assets/` 提供 |

---

## 2. Frontmatter 字段映射

Markdown 文件开头 `---` 包裹的 YAML 块，字段与 HTML 的对应关系：

```yaml
---
course: "课程名"           # → <body data-course="..."> + 侧边栏标题
unit: "01"                 # → <body data-unit="..."> + 侧边栏副标题
title: "页面标题"          # → <title> + <h1>
kicker: "副标题"           # → hero 区 .kicker
kicker_en: "英文副标题"    # → hero 区 .kicker 后的附加文本
summary: "概述"            # → hero 区 <p>
side_note: "侧边栏提示"    # → 左侧导航下方的提示文字
can_do:                    # → hero 区右侧"读完应该能做什么"清单
  - "能力项 1"
  - "能力项 2"
course_links:              # → hero 区底部导航链接
  - text: "课程地图"
    href: "../index.html"
  - text: "下一节"
    href: "../下一节/学习页.html"
---
```

### 字段要求

- `course`、`unit`、`title`、`summary`：**必填**。缺一不可。
- `kicker`、`kicker_en`、`side_note`：可选。不填则对应区域不渲染。
- `can_do`：建议填写 2-5 条。不填则 hero 区右侧空白。
- `course_links`：建议至少包含"课程地图"链接和上/下一节链接。

---

## 3. Section（正文章节）

### 3.1 基本结构

```markdown
# 章节标题 {#section-id}
<!-- tag: 标签文字 -->
<!-- layout: grid2 -->

章节内容...
```

对应 HTML：

```html
<section id="section-id">
  <div class="head">
    <h2>章节标题</h2>
    <span class="tag">标签文字</span>
  </div>
  <!-- 内容按 layout 包裹 -->
</section>
```

### 3.2 规则

- `# 标题 {#id}` 中 `{#id}` 是可选的。不写则自动用标题生成 id。
- `<!-- tag: xxx -->` 可选，控制标题旁的标签文字。
- `<!-- layout: grid2 -->` 或 `<!-- layout: grid -->` 可选，让内容以双列/网格排列。
- 两个 `#` 标题之间，或 `#` 标题到 `---` 之间，为一个 section。
- `---`（单独一行）表示 section 结束分隔符。

### 3.3 特殊 section id

| id | 行为 |
|----|------|
| `export` | 跳过，由模板自动生成导出区 |
| `sources` | 跳过正文渲染，内容自动放入页面底部"参考资料"区 |
| 其他 | 正常渲染为正文 section |

---

## 4. Box（提示块）

```markdown
## box
### 标题
内容段落。支持**粗体**、`代码`等行内格式。

## box soft
### 标题
绿色边框的柔和提示。

## box info
### 标题
蓝色边框的信息提示。

## box warn
### 标题
橙色边框的警告提示。
```

对应 HTML：

```html
<div class="box">
  <h3>标题</h3>
  <p>内容段落。</p>
</div>

<div class="box soft">
  <h3>标题</h3>
  ...
</div>

<div class="box info">...</div>
<div class="box warn">...</div>
```

### 规则

- `## box` 后必须紧跟 `### 标题`。标题为必填。
- 支持的变体：无后缀（默认）、`soft`、`info`、`warn`。
- Box 内支持段落、列表、代码块、表格、公式等所有行内和块级元素。

---

## 5. Callout（标准提示语法）

采用 GitHub / Notion / Obsidian 通用的 blockquote 语法：

```markdown
> [!NOTE] 标题文字
> 这是普通信息提示。
> 支持多行。

> [!TIP] 小技巧
> 效率提示内容。

> [!WARNING] 注意
> 重要警告内容。

> [!DANGER] 危险
> 危险操作提示。

> [!INFO] 补充信息
> 背景知识或扩展阅读。
```

对应 HTML：

```html
<div class="callout note">
  <div class="callout-title">标题文字</div>
  <p>这是普通信息提示。</p>
</div>

<div class="callout tip">...</div>
<div class="callout warning">...</div>
<div class="callout danger">...</div>
<div class="callout info">...</div>
```

### 规则

- 类型不区分大小写：`[!note]` 和 `[!NOTE]` 等价。
- 标题可选。不写标题则只显示图标。
- 支持的 callout 类型：`NOTE`、`TIP`、`WARNING`、`DANGER`、`INFO`。
- Box 和 Callout 都可以在正文中使用。新内容建议优先用 Callout。

---

## 6. 代码块

```markdown
```python
def hello():
    print("hello")
```
```

如果要给代码块命名和自定义 id：

```markdown
```python {id="code-loop" label="Agent 主循环"}
while True:
    step()
```
```

对应 HTML：

```html
<div class="code-example">
  <div class="codebar">
    <span>Agent 主循环</span>
    <button class="copy" data-copy="code-loop">复制</button>
  </div>
  <pre id="code-loop"
       data-export-context="Agent 主循环"
       data-export-lang="python">
    <code class="language-python">...</code>
  </pre>
</div>
```

如果代码块后紧跟说明文字，两者会一起包进同一个 `<div class="code-example">`。

### 规则

- `{id="..."}` 和 `{label="..."}` 均为可选。不写则自动生成 `code-{section-id}-{序号}`。
- 支持的语言标签会被保留为 CSS class `language-xxx`。
- 代码自动 HTML 转义，不需要手写 `&lt;`。

---

## 7. 表格

```markdown
| 列A | 列B | 列C |
|-----|-----|-----|
| 值1 | 值2 | 值3 |
| 值4 | 值5 | 值6 |
```

对应 HTML：

```html
<div class="table-wrap">
  <table class="metric-table">
    <tr><th>列A</th><th>列B</th><th>列C</th></tr>
    <tr><td>值1</td><td>值2</td><td>值3</td></tr>
    <tr><td>值4</td><td>值5</td><td>值6</td></tr>
  </table>
</div>
```

### 规则

- 表头行和内容行之间必须有 `|---|---|` 分隔行。
- 至少需要 2 行（表头 + 分隔行 + 至少 1 行数据）。
- 单元格内容支持行内 Markdown（粗体、代码、链接）。

---

## 8. 公式

行内公式使用 `` `$...$` ``（反引号包裹）：

```markdown
损失函数用 `$\mathcal{L}$` 表示。
```

对应 HTML：`<span class="math-inline">$\mathcal{L}$</span>`

块级公式使用 `$$...$$`：

```markdown
$$
\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
```

对应 HTML：

```html
<div class="formula" data-export-context="公式" data-export-lang="math">
$$
\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
</div>
```

### 规则

- 行内公式必须用 `` `$...$` `` 格式（反引号包裹，防止 Markdown 解析器误处理）。
- 块级公式直接 `$$...$$`。
- 公式由 KaTeX 在浏览器端渲染。`.md` 中只需保证 LaTeX 语法正确。

---

## 9. 练习区

### 9.1 练习组

```markdown
<!-- practice-group: 一、基础概念 -->
<!-- quick-review: 回顾：token 是模型处理文字的基本单位。 -->

### 01 choice
**Q:** tokenizer 的主要输出是什么？

- [ ] 训练后的模型参数
- [x] token 和 token id
- [ ] 最终回答文本

Answer: token 和 token id
Explain: tokenizer 的核心任务就是把字符串切成 token 并分配 id。

### 02 fill
**Q:** 模型可选 token 的全集叫什么？

Answer: vocabulary
```

对应 HTML：

```html
<div class="practice-group">
  <div class="group-head">
    <div><h3>一、基础概念</h3></div>
    <div class="quick-review">回顾：token 是模型处理文字的基本单位。</div>
  </div>
  <div class="drill-grid">
    <article class="q" data-question="q01" data-answer="token 和 token id">
      <div class="q-meta">
        <span class="pill">01</span>
        <span class="pill">choice</span>
      </div>
      <h3>tokenizer 的主要输出是什么？</h3>
      <div class="choices">
        <label><input type="radio" name="q01" value="训练后的模型参数">训练后的模型参数</label>
        <label><input type="radio" name="q01" value="token 和 token id">token 和 token id</label>
        <label><input type="radio" name="q01" value="最终回答文本">最终回答文本</label>
      </div>
      <button class="check" type="button">检查</button>
      <div class="feedback"></div>
      <details>
        <summary>参考答案 / 评分要点</summary>
        <p>token 和 token id。tokenizer 的核心任务就是把字符串切成 token 并分配 id。</p>
      </details>
    </article>
    <!-- 后续题目... -->
  </div>
</div>
```

### 9.2 题目类型

| .md 标注 | HTML 题型标签 | 输入方式 |
|----------|-------------|---------|
| `### 01 choice` | choice | 单选按钮，选项来自 `- [ ]` 行 |
| `### 02 true/false` | true/false | 单选按钮，选项来自 `- [ ]` 行 |
| `### 03 fill` | fill | 文本输入框 |
| `### 04 short-answer` | short answer | 多行文本框 |
| `### 05 ordering` | ordering | 多行文本框 |
| `### 06 code-reading` | code reading | 多行文本框 |
| `### 07 diagnosis` | error diagnosis | 多行文本框 |
| `### 08 synthesis` | synthesis | 多行文本框 |
| `### 09 scenario` | scenario transfer | 多行文本框 |
| `### 10 checklist` | checklist | 多行文本框 |

### 9.3 题目字段

| 字段 | 写法 | 说明 |
|------|------|------|
| 题目标题 | `**Q:** 问题文字` | 必填。`**Q:**` 之后的内容为题目标题 |
| 选项 | `- [ ] 选项A` 或 `- [x] 正确答案` | 仅 choice / true/false 需要 |
| 答案 | `Answer: 正确答案` | 必填。用于本地检查比对 |
| 解释 | `Explain: 解释文字` | 可选。会附在参考答案后面 |
| 补充 | `Details: 更多细节` | 可选。额外的反馈内容 |
| 提示 | `::input` 或 `::textarea` | 可选。输入框占位提示 |

### 9.4 练习导语（可选）

```markdown
<!-- practice-intro -->
## box
**答题目标**：检查你是否理解...
<!-- end-practice-intro -->
```

渲染为 `.practice-intro` 区块，放在题目列表之前。

### 9.5 规则

- 每个练习组以 `<!-- practice-group: 名称 -->` 开始，`<!-- end-practice-group -->` 结束。
- 每个题目以 `### 编号 类型` 开始，到下一个 `###` 或组结束标记为止。
- `Answer:` 的值就是本地检查的正确答案。对于选择/判断题，检查时会比对用户选择和 Answer 是否一致。
- `Explain:` 会出现在展开的"参考答案/评分要点"中。
- 如果题目没有 `Answer:` 也没有 `Explain:`，渲染的"检查"按钮不会给出明确正误判断。

---

## 10. 练习题导出

页面**始终**包含一个导出区：

```html
<section id="export">
  <h2>导出练习记录</h2>
  <div id="quality"><!-- 完整性提示 --></div>
  <div id="record"><!-- 生成的 Markdown 记录 --></div>
  <button onclick="generateRecord()">生成记录</button>
  <button onclick="copyRecord()">复制 Markdown</button>
</section>
```

导出逻辑由 `assets/study-page.js` 提供。`.md` 作者无需在 Markdown 中写任何导出相关标记——它自动出现。

---

## 11. 参考资料

```markdown
# 参考资料 {#sources}
<!-- tag: source -->

- **论文**：Attention Is All You Need (Vaswani et al., 2017)
- **课程地图**：`index.html`
```

`# 参考资料` 或 `# 来源`（id 为 `sources` 或 `source`）的 section 会被自动识别。内容不会出现在正文区，而是渲染到页面底部的固定参考资料区。

---

## 12. 行内格式

正文、box、callout 内部支持的标准 Markdown 行内格式：

| 写法 | 输出 |
|------|------|
| `**粗体**` | `<b>粗体</b>` |
| `*斜体*` | `<i>斜体</i>` |
| `` `代码` `` | `<code>代码</code>` |
| `[链接文字](url)` | `<a href="url">链接文字</a>` |
| `` `$\frac{1}{2}$` `` | `<span class="math-inline">$\frac{1}{2}$</span>` |

---

## 13. 导航链接自动生成

左侧导航栏的链接由两部分组成：

1. **固定链接**：返回课程地图（`../index.html`）和搜索页。
2. **正文锚点**：每个 `# 标题 {#id}` 自动生成一个导航项 `<a href="#id">标题</a>`。

`export` 和 `sources` section 的导航项自动追加在末尾。

---

## 14. 页面壳层标记

生成的 HTML 页面必须包含以下标记，用于验证工具识别：

```html
<html lang="zh-CN" data-page-shell="study-page-v2">
<body data-course="课程名" data-unit="单元编号">
```

```html
<!-- learning-kit:nav:start -->
...
<!-- learning-kit:nav:end -->
```

这些标记由转换器自动生成，`.md` 作者不需要手写。

---

## 15. 一份完整示例

```markdown
---
course: "LLM 基础"
unit: "01"
title: "tokenizer 与 context window"
kicker: "LLM foundation"
summary: "文本怎样进入大模型：切分、编号、向量化和窗口预算。"
side_note: "先把输入链路看清。"
can_do:
  - "说清 tokenizer 的输入输出"
  - "能计算一次对话的窗口预算"
course_links:
  - text: "课程地图"
    href: "../index.html"
  - text: "下一节"
    href: "../02_Transformer/学习页.html"
---

# 学习目标 {#goals}
<!-- tag: goals -->

## box soft
### 读完就能做的事
- 把句子拆成 token
- 解释为什么 id 大小不代表语义

---

# 核心机制 {#mechanism}
<!-- layout: grid2 -->

步骤tokenizer 做什么读什么写什么
切分把字符串切成模型认识的片段词表与切分规则token 列表与编号
查表把 token id 映射为连续向量embedding 表`[B, N, D]` 向量

---

# 例子 {#examples}

```python {id="code-tokenize" label="最小 tokenize"}
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
print(tokenizer.encode("请解释 RAG"))
```

---

# 练习 {#practice}
<!-- tag: diagnostic -->

<!-- practice-group: 基础概念 -->

### 01 choice
**Q:** tokenizer 的主要输出是什么？

- [ ] 模型参数
- [x] token 和 token id

Answer: token 和 token id
Explain: tokenizer 把字符串切分并编号。

### 02 fill
**Q:** 模型可选 token 的全集叫什么？

Answer: vocabulary

<!-- end-practice-group -->

---

# 参考资料 {#sources}

- HuggingFace tokenizer 文档
- 课程地图 `index.html`
```
