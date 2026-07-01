# 学习页 Markdown 规范 v1

> 把学习页拆成"内容"和"模板"。AI 只写 Markdown，通用脚本负责转成 HTML。

## 目录结构

```
课程/
  研习资料/
    单元名/
      学习页.md          ← AI 写这个
      学习页.html         ← 脚本自动生成（不需要 AI 碰）
```

## 文件规范

一个有效的学习页 Markdown 文件包含两部分：

1. **YAML frontmatter** — 元数据、导航、Hero 区域
2. **Markdown 正文** — 用标准 Markdown + HTML 注释标记结构

---

## Frontmatter 字段

```yaml
---
# === 基础信息 ===
course: "课程名"           # 侧边栏 brand 的课程名
unit: "01"                 # 侧边栏 brand 的单元编号
title: "页面标题"          # <title> 和 <h1>
kicker: "中文副标题"       # hero 的 .kicker
kicker_en: "英文副标题"    # hero 的 .kicker（可选，英文标识）
summary: "页面概述"        # hero 的 <p> 简介

# === 侧边栏 ===
side_note: "侧边栏提示文字"

# === Hero 能力清单 ===
can_do:
  - "读完本页应该能做什么 1"
  - "读完本页应该能做什么 2"
  - "读完本页应该能做什么 3"

# === 课程导航 ===
course_links:
  - text: "课程地图"
    href: "../index.html"
  - text: "下一节"
    href: "../下一节/学习页.html"
---
```

---

## 正文结构标记

用 HTML 注释标记结构，标准 Markdown 写内容。注释在阅读器里不可见，不影响阅读。

### Section 区域

```markdown
# 学习目标 {#goals}
<!-- tag: goals -->
<!-- layout: grid2 -->

内容...

---
```

- `# 标题 {#id}` → `<section id="id">`
- `<!-- tag: xxx -->` → `<div class="head"><h2>标题</h2><span class="tag">xxx</span></div>`
- `<!-- layout: grid2 -->` → `<div class="grid2">`（自动包裹后续内容直到下一个 `---` 或新 section）
- `---`（水平分隔线）表示 section 结束

### Box 变体

```markdown
## box
### 标题

普通 box 内容

## box soft
### 标题

绿色背景提示

## box info
### 标题

蓝色信息提示

## box warn
### 标题

黄色警告提示

## box redsoft
### 标题

红色警告
```

- `## box` → `<div class="box">`
- `## box soft` → `<div class="box soft">`
- `## box info` → `<div class="box info">`
- `## box warn` → `<div class="box warn">`
- `## box redsoft` → `<div class="box redsoft">`

### 代码块

```markdown
```python
# 代码
```
```

脚本会自动添加 `codebar` 和 `pre` 包装，并生成复制按钮。如果希望给代码块指定 ID，用 fenced code 的属性语法：

```markdown
```python {id="code-loop" label="受控 Agent Loop"}
# 代码内容
```
```

### 表格

```markdown
| 列A | 列B | 列C |
|-----|-----|-----|
| 1   | 2   | 3   |
| 4   | 5   | 6   |
```

脚本会自动包装为 `<table class="metric-table">`，并添加 `data-export-context` 属性。

如果表格需要导出上下文，在表格前加注释：

```markdown
<!-- table-export: Agent 状态台账 -->
| 对象 | 读什么 | 写什么 | ... |
```

### 练习区域

```markdown
# 练习 {#practice}
<!-- tag: diagnostic -->

<!-- practice-intro -->
## box
**答题目标**
...

## box info
**检查重点**
...
<!-- end-practice-intro -->

<!-- practice-group: 概念辨认 -->
<!-- quick-review: 复盘提示... -->

### 01 choice

**Q:** 如果系统按固定顺序执行...它更接近什么？

- [ ] Workflow
- [ ] Agent
- [ ] Multi-Agent

Answer: Workflow

### 02 true/false

**Q:** 只要模型能调用搜索工具，就可以称为 Agent。

Answer: 错

### 05 fill

**Q:** ReAct 的三个基本环节可以概括为：____、____、____。

Answer: 思考;行动;观察
Explain: 按本页主线写出三个环节即可。

### 07 ordering

**Q:** 把最小 Agent Loop 排序...

Answer: C → B → D → A → E
Details: 目标先进入系统...

### 09 code-reading

**Q:** 读伪代码：为什么工具执行后要把结果追加回 messages？

Answer: 因为下一轮模型要基于观察继续决定动作...

### 10 short-answer

**Q:** 用 2-3 句话解释 Workflow 和 Agent 的核心区别。

Answer: Workflow 的步骤由代码固定，Agent 让模型根据观察决定下一步...

<!-- end-practice-group -->
```

### 参考资料

```markdown
# 参考资料 {#sources}
<!-- tag: source -->

- **课程地图**：课程根目录的 `index.html`
- **现有学习页**：同目录旧版 `学习页.html`
```

---

## 转换命令

```bash
# 转换单个文件
python scripts/md-to-study-page.py 输入.md 输出.html

# 批量转换某目录下所有 .md
python scripts/md-to-study-page.py --batch 课程/研习资料/单元名/

# 生成并自动覆盖（用于 CI）
python scripts/md-to-study-page.py --batch --overwrite 课程/研习资料/单元名/
```

---

## 完整示例

见 `99_系统/模板/study-page-example.md`。

---

## 版本

- v1: 2026-07-01 初始版本，支持基础 section、box、表格、代码、练习区域
