---
course: "测试课程"
unit: "01"
title: "Markdown 转换测试页"
kicker: "测试 / 规范验证"
summary: "这个页面用来验证 md-to-study-page.py 转换器是否能正确生成学习页 HTML。"
side_note: "先熟悉 Markdown 规范，再写内容。"
can_do:
  - "能把 Markdown 规范里的 frontmatter、section、box、代码、表格、练习正确写出来"
  - "能用脚本把 .md 转成 .html，不需要手动写 HTML"
  - "能在面试时讲清 tokenizer、embedding、context window 的关系"
---

# 学习目标 {#goals}
<!-- tag: goals -->
<!-- layout: grid2 -->

## box
### 先认结构

把 Markdown 的 frontmatter、section、box、代码块、表格和练习区分开。不再把它们混成同一种写法。

## box soft
### 这页的边界

这里只验证转换器的基本功能。复杂的交互组件（如 shape tracer、terminal lab）先保持为内联 HTML，后续版本再扩展。

---

# 先抓主线 {#overview}
<!-- tag: overview -->
<!-- layout: grid2 -->

## box
### 为什么需要 Markdown 规范

原来 AI 直接写 HTML，每页都要处理 CSS 类、结构嵌套、JS 属性。现在 AI 只写 Markdown，通用脚本负责转成 HTML。样式和交互由脚本模板统一控制，AI 只需要关心内容。

## box info
### 转换流程

1. 写 `学习页.md`（按规范）
2. 运行 `python scripts/md-to-study-page.py 学习页.md`
3. 自动生成 `学习页.html`
4. 浏览器打开验证

---

# 核心机制 {#mechanism}
<!-- tag: trace -->

## box
### 脚本的工作方式

脚本做三件事：解析 YAML frontmatter、解析 Markdown 正文结构、套用 HTML 模板输出。AI 不需要读脚本，只需要按规范写 Markdown。

```python
# 转换命令
python scripts/md-to-study-page.py 输入.md 输出.html
```

## box soft
### 支持的 Markdown 元素

- **标题**：`# 标题 {#id}` 生成 section
- **Box**：`## box` / `## box soft` / `## box info` / `## box warn`
- **代码**：fenced code block，支持 `{id="..." label="..."}` 属性
- **表格**：标准 Markdown 表格，自动包装为 metric-table
- **练习**：`<!-- practice-group -->` 标记练习组

---

# 例子 {#example}
<!-- tag: example -->
<!-- layout: grid2 -->

## box
### 表格示例

<!-- table-export: 状态台账示例 -->
| 对象 | 读什么 | 写什么 | 什么时候会脏 |
|------|--------|--------|-------------|
| messages | 历史、工具返回 | 新观察 | 工具结果没写回 |
| state | 预算、事实 | 更新边界 | 状态和消息不同步 |
| permissions | 用户权限 | 拒绝/授权 | 没检查写动作 |

## box soft
### 代码示例

```python {id="code-example" label="最小示例"}
def hello():
    print("转换成功")
    return True
```

---

# 常见误区 {#mistakes}
<!-- tag: debug -->
<!-- layout: grid2 -->

## box
### 把 Markdown 当 HTML 写

不需要在 Markdown 里写 `<div class="box">`，用 `## box` 就行。脚本会自动转换。

## box warn
### 忘记 section 分隔线

每个 section 之间用 `---` 分隔，否则脚本会把内容合并到上一个 section。

---

# 练习 {#practice}
<!-- tag: diagnostic -->

<!-- practice-intro -->
## box
**答题目标**

检查你能不能区分 Markdown 规范里的各种结构标记。

## box info
**检查重点**

优先看 frontmatter 是否完整、section 是否有 id、box 是否有内容。
<!-- end-practice-intro -->

<!-- practice-group: 基础判断 -->
<!-- quick-review: 先区分 frontmatter 和正文 -->

### 01 choice

**Q:** Markdown 规范中，frontmatter 用什么符号包裹？

- [ ] HTML 标签
- [ ] `---`
- [ ] XML 声明

Answer: `---`

### 02 true/false

**Q:** AI 在写 Markdown 时需要读取和修改转换脚本。

Answer: 错

### 05 fill

**Q:** Box 的五种变体分别是：____、____、____、____、____。

Answer: box;soft;info;warn;redsoft
Explain: 普通 box 以及四种变体。

### 10 short-answer

**Q:** 用 2-3 句话解释为什么把内容从 HTML 中分离到 Markdown 更好。

Answer: 因为 AI 只需要写内容，不需要处理样式和交互。样式由稳定脚本控制，跨会话一致性更好。

<!-- end-practice-group -->

---

# 参考资料 {#sources}
<!-- tag: source -->

- **规范文档**：`99_系统/规范/学习页Markdown规范.md`
- **转换脚本**：`scripts/md-to-study-page.py`
- **模板示例**：`99_系统/模板/study-page-example.md`
