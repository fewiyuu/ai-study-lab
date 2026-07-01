# Learning-Kit 学习页改革方案

> **核心纠正**：`Agent/研习资料/Claude Code工作流` 这套课程的本质定位是 **Codex + GPT 工作流**（以 Claude Code 源码为解剖对象，面向 Codex / GPT 类命令行 Agent 的工程实践）。以下方案中统一称其为 **"Codex + GPT 工作流"**。

---

## 一、现状速览（基于 364 页全量扫描）

| 课程 | 页面数 | 壳层状态 | 样式模式 | 主要问题 |
|------|--------|----------|----------|----------|
| PyTorch 深度学习实践 | 13 | 共享壳层 ✅ | 外部 CSS | 参考答案模板化 |
| Codex + GPT 工作流 | 24 | 声明了 v2，但 23 页内联 11KB CSS | 内联 + 外部混杂 | 样式不统一、维护成本高 |
| GPU 性能工程 | 8 | 共享壳层 ✅ | 外部 CSS | Triton 页渲染错误 |
| 生成式 LLM 课程 | 62 | 共享壳层 ✅ | 每页内联 21KB CSS | 样式冗余、体积膨胀 |
| 概率论与深度学习 | 58 | 共享壳层 ✅ | 每页内联 20KB CSS | 样式冗余 |
| Agent 基础与工程 | 30+ | 共享壳层 ✅ | 外部 CSS | 质量较高 |
| LoRA 微调 | 3 | **无壳层标记** | 内联 CSS | 完全脱离模板 |

**关键发现**：
- 364 个页面中，361 个声明了 `data-page-shell="study-page-v2"`
- 但**大量页面同时内联了 10~21KB CSS**，导致每个页面体积膨胀、样式无法批量更新
- 3 个 LoRA 页面完全无壳层标记
- PyTorch 系列模板化参考答案出现 **19 次**

---

## 二、改革目标

1. **所有学习页统一使用共享壳层 + 外部 CSS**，删除内联样式块（除页面特定交互所需的少量样式外）
2. **PyTorch 系列参考答案逐题修复**，消灭模板化占位
3. **Triton 页面渲染错误修复**
4. **课程名称统一**（如用户确认，将 "Claude Code 工作流" 改为 "Codex + GPT 工作流"）
5. **建立可复用的批量验证脚本**，防止同类问题复发

---

## 三、P0：本周必须执行（阻塞性问题）

### 3.1 修复 PyTorch 系列模板化参考答案

**影响范围**：`30_研究/PyTorch深度学习实践 刘二大人/研习资料/` 下全部 13 个 `学习页.html`

**问题模式**：开放题的 `<details><summary>参考回答</summary><p>` 内容全部是：
> "先把 NCHW、通道、高宽、展平和分类头的 shape 串起来，再点出卷积和池化的分工。"

**修复步骤**：

步骤一：定位所有问题题目
```bash
rg -n "先把 NCHW、通道、高宽、展平和分类头的 shape 串起来" "30_研究/PyTorch深度学习实践 刘二大人/研习资料/"
```

步骤二：逐页编写题目特定参考答案。以 `10_卷积神经网络基础` 为例：

| 题目 | 错误参考答案 | 正确参考答案方向 |
|------|-------------|----------------|
| Q2: MaxPool2d(2) 改变通道数 | 模板句 | 错误。MaxPool2d 只压缩空间尺寸，通道数不变。它是在每个通道内部做下采样。 |
| Q3: RGB 输入通道数 | 模板句 | 3。灰度是 1，RGB 彩色图像是 3 通道。 |
| Q4: Conv2d(1,10,5) 后 shape | 模板句 | [64, 10, 24, 24]。高宽各减 kernel_size-1 = 4。 |
| Q6: x.view(x.size(0), -1) | 模板句 | 把卷积输出的 4D 张量展平为 2D，保留 batch 维度，把其余通道×高×宽合并成特征向量。 |
| Q8: expected 10 channels got 1 | 模板句 | 第二卷积层的 in_channels 应该等于第一层的 out_channels（10），而不是 1。 |
| Q19: 费曼解释 CNN 流程 | 模板句 | 需要 6-9 句话完整串起 NCHW→Conv→ReLU→Pool→Flatten→Linear→CrossEntropy。 |

步骤三：委托代理批量修复。建议按以下方式分配：
- **主线程**：准备每道题的参考答案文本（可以基于页面讲义内容提取）
- **工作代理**：每代理负责 3-4 个页面，逐题替换 `<details>` 中的 `<p>` 内容
- **验收**：运行验证脚本，确认模板句出现次数为 0

**验收标准**：
```bash
rg -c "先把 NCHW、通道、高宽、展平和分类头的 shape 串起来" "30_研究/PyTorch深度学习实践 刘二大人/研习资料/"
# 期望输出：0
```

---

### 3.2 修复 Triton 页面 HTML 渲染错误

**文件**：`30_研究/AI基础设施/研习资料/GPU性能工程/05_Triton编程模型与块级思维/学习页.html`

**问题**：正文中 `&lt;code&gt;BLOCK_SIZE&lt;/code&gt;` 等被双重 HTML 实体编码。

**修复**：
```bash
sed -i 's/&lt;code&gt;\(.*\?)&lt;\/code&gt;/<code>\1<\/code>/g' \
  "30_研究/AI基础设施/研习资料/GPU性能工程/05_Triton编程模型与块级思维/学习页.html"
```

**验证**：在浏览器中打开页面，检查 "性能参数" 章节中的 `BLOCK_SIZE` / `BLOCK_M` / `BLOCK_N` 是否正常渲染为等宽字体代码块。

---

### 3.3 统一 "Codex + GPT 工作流" 课程名称（如用户确认）

**如果用户确认改名**：

需要修改的文件：
1. `30_研究/Agent/研习资料/Claude Code工作流/index.html`
   - 标题：`Claude Code 工作流｜课程地图` → `Codex + GPT 工作流｜课程地图`
   - 品牌名：`Claude Code 工作流` → `Codex + GPT 工作流`
   - 描述中的 "Claude Code" 保留作为来源说明，但课程主体名称改为 "Codex + GPT 工作流"
   
2. `30_研究/Agent/研习资料/Claude Code工作流/` 下 24 个 `学习页.html`
   - 每个页面的 `<title>`、`<body data-course="...">`、`<div class="brand"><strong>...` 中的课程名称

3. `30_研究/Agent/研习资料/Claude Code工作流/course-shell.json`（如有）

4. 可选：目录重命名
   - `Claude Code工作流` → `Codex + GPT工作流`
   - 注意：如果重命名目录，需要更新所有引用此路径的 `index.html` 链接

**批量修改命令（不改目录名时）**：
```bash
# 修改课程根目录 index.html
sed -i 's/Claude Code 工作流/Codex + GPT 工作流/g' \
  "30_研究/Agent/研习资料/Claude Code工作流/index.html"

# 修改所有学习页中的课程品牌名
for f in "30_研究/Agent/研习资料/Claude Code工作流"/*/学习页.html; do
  sed -i 's/Claude Code 工作流/Codex + GPT 工作流/g' "$f"
  sed -i 's/Claude Code 工作流/Codex + GPT 工作流/g' "$f"
done
```

> 注意：如果用户**不想改名**，可以跳过此步骤。但建议在页面中增加说明："本课程以 Claude Code 源码为解剖对象，面向 Codex、GPT 及同类命令行 Agent 的工程实践。"

---

## 四、P1：本月重点执行（结构性问题）

### 4.1 清理 Codex + GPT 工作流系列的内联样式

**现状**：24 个页面中，约 23 个页面内联了 ~11KB CSS（在 `<head>` 中以 `<style>` 形式存在），而 01 页面使用外部 `../assets/study-page.css`。

**问题**：
- 页面体积膨胀（37KB 中约 30% 是 CSS）
- 全局样式更新时需要手动改 24 个文件
- 违反 SKILL.md 的"可复用资产"原则

**修复方案**：

步骤一：确认 `assets/study-page.css` 已包含所有必要样式
- 对比 `01_本地启动最小Agent/学习页.html`（使用外部 CSS）和 `05_行动之前先规划/学习页.html`（使用内联 CSS）的视觉效果
- 如果两者视觉上一致，说明内联 CSS 与外部 CSS 是等价的，可以直接删除内联块

步骤二：批量删除内联样式并统一引用外部 CSS

对于每个有内联样式的页面，执行：
1. 删除 `<head>` 中从 `<style>` 到 `</style>` 的全部内容
2. 确保 `<head>` 中包含：
   ```html
   <link rel="stylesheet" href="../assets/vendor/katex/katex.min.css">
   <link rel="stylesheet" href="../assets/vendor/prism/prism-tomorrow.min.css">
   <link rel="stylesheet" href="../assets/vendor/prism/prism-line-numbers.min.css">
   <link rel="stylesheet" href="../assets/study-page.css">
   ```
3. 删除页面底部的内联 `<script>`（如果存在），替换为：
   ```html
   <script src="../assets/study-page.js"></script>
   ```

**建议**：委托一个工作代理专门处理这 24 个页面，逐页阅读、修改、验证。主线程只负责验收。

---

### 4.2 清理生成式 LLM 课程和概率论课程的内联样式

**影响范围**：
- `30_研究/微调模型/研习资料/生成式LLM课程/`：62 个页面，每页内联 21KB CSS
- `30_研究/概率论  深度学习/研习资料/`：58 个页面，每页内联 20KB CSS

**修复方案**：

与 4.1 类似，但规模更大。建议：
1. 先确认这些课程目录下是否有 `assets/study-page.css`（概率论和生成式 LLM 课程可能还没有）
2. 如果没有，从 `PyTorch 深度学习实践/研习资料/assets/` 复制一套 `study-page.css` + `study-page.js` + `vendor/` 到对应目录
3. 批量删除内联 `<style>` 和 `<script>`，替换为外部引用

**Python 批量脚本**：
```python
import os, re, glob

def extract_inline_css(html_path):
    """从 HTML 中提取内联样式，返回 (clean_html, css_content)"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 <style>...</style>
    match = re.search(r'<style>.*?</style>', content, re.DOTALL)
    if not match:
        return content, None
    
    css = match.group(0)
    # 替换为外部引用
    clean = content.replace(css, '''<link rel="stylesheet" href="../assets/vendor/katex/katex.min.css">
<link rel="stylesheet" href="../assets/vendor/prism/prism-tomorrow.min.css">
<link rel="stylesheet" href="../assets/vendor/prism/prism-line-numbers.min.css">
<link rel="stylesheet" href="../assets/study-page.css">''')
    
    return clean, css

def extract_inline_js(html_path):
    """提取底部的内联 script，替换为外部引用"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配最后一个 <script>...</script>（通常是自己写的 JS）
    # 注意：不要匹配 vendor script 标签
    match = re.search(r'<script>[^<]*const navLinks.*?</script>', content, re.DOTALL)
    if match:
        js = match.group(0)
        clean = content.replace(js, '<script src="../assets/study-page.js"></script>')
        return clean, js
    return content, None

# 对目标目录批量执行
for course_dir in [
    r"30_研究/微调模型/研习资料/生成式LLM课程",
    r"30_研究/概率论  深度学习/研习资料",
    r"30_研究/Agent/研习资料/Claude Code工作流"
]:
    for html_file in glob.glob(os.path.join(course_dir, "*", "学习页.html")):
        # 先确保 assets 目录存在
        assets_dir = os.path.join(course_dir, "assets")
        if not os.path.exists(assets_dir):
            # 从 PyTorch 课程复制一套 assets
            pass
        
        clean, css = extract_inline_css(html_file)
        if css:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(clean)
            print(f"Fixed CSS: {html_file}")
```

> **重要**：这个脚本只是骨架。实际执行前，必须手动检查 1-2 个样本页面，确认外部 CSS 能完全替代内联样式（包括页面特定的交互样式如 `.todo-render`、`.tile-board` 等）。如果页面有特定交互样式，应保留这些样式在内联 `<style>` 中，只删除与共享壳层重复的全局样式。

---

### 4.3 修复 LoRA 微调课程的 3 个孤儿页面

**文件**：
- `30_研究/微调模型/研习资料/LoRA微调/01_.../学习页.html`
- `30_研究/微调模型/研习资料/LoRA微调/02_.../学习页.html`
- `30_研究/微调模型/研习资料/LoRA微调/03_.../学习页.html`

**问题**：
- 没有 `data-page-shell="study-page-v2"` 标记
- 没有引用共享 CSS
- 完全内联了 ~10KB CSS

**修复**：
1. 为这 3 个页面添加 `data-page-shell="study-page-v2"` 到 `<html>` 标签
2. 复制一套 assets 到 `LoRA微调/assets/`
3. 删除重复的全局内联样式，保留页面特定交互样式
4. 添加 `<link rel="stylesheet" href="../assets/study-page.css">` 和 `<script src="../assets/study-page.js">`
5. 创建 `LoRA微调/index.html` 课程地图（如果不存在）

---

### 4.4 统一中文标签

**问题**：导航标签和章节标签中残留英文，如 `CONTENTS`、`goals`、`map`、`flow`、`vocab`、`ledger`、`practice`、`diagnostic` 等。

**批量替换词表**：

| 英文 | 中文替换 | 出现位置 |
|------|----------|----------|
| CONTENTS | 目录 | PyTorch 页面导航标题 |
| goals | 学习目标 | 章节标签 |
| map | 概念地图 | 章节标签 |
| flow | 主线 | 章节标签 |
| vocab | 术语 | 章节标签 |
| ledger | 账本 | 章节标签 |
| mechanism | 机制 | 章节标签 |
| result | 结果 | 章节标签 |
| fix | 修法 | 章节标签 |
| debug | 调试 | 章节标签 |
| bridge | 桥接 | 章节标签 |
| evaluation / bfcl | 评测 | 章节标签 |
| source | 参考 | 章节标签 |
| practice | 练习 | 章节标签 |
| diagnostic | 诊断 | 章节标签 |
| export | 导出 | 章节标签 |
| markdown | Markdown | 章节标签 |
| text | 文本 | 章节标签 |
| table | 表格 | 章节标签 |
| python | Python | 章节标签 |
| math | 公式 | 章节标签 |
| js | JS | 章节标签 |
| choice | 选择 | 题型标签 |
| true/false | 判断 | 题型标签 |
| fill | 填空 | 题型标签 |
| short fill | 短填空 | 题型标签 |
| code reading | 代码阅读 | 题型标签 |
| error diagnosis | 错误诊断 | 题型标签 |
| scenario | 场景 | 题型标签 |
| synthesis | 综合 | 题型标签 |
| protocol | 协议 | 题型标签 |
| ordering | 排序 | 题型标签 |
| feynman | 费曼 | 题型标签 |
| checklist | 检查清单 | 题型标签 |
| list | 清单 | 题型标签 |
| boundary | 边界 | 章节标签 |
| ops-ledger | 运行台账 | 章节标签 |
| visible state | 可见状态 | 章节标签 |
| guardrails | 约束 | 章节标签 |
| stay aligned | 保持对齐 | 章节标签 |
| planning quality | 计划质量 | 章节标签 |
| check understanding | 检查理解 | 章节标签 |
| self check | 自查 | 题型标签 |
| program / block | 程序/块 | 题型标签 |
| offsets / mask | 偏移/掩码 | 题型标签 |
| mask / other | 掩码/填充 | 题型标签 |
| grid / launch | 网格/启动 | 题型标签 |
| broadcast / stride | 广播/步幅 | 题型标签 |
| autotune / hypothesis | 调参/假设 | 题型标签 |
| compile-time | 编译期 | 题型标签 |
| stride / layout | 步幅/布局 | 题型标签 |
| failure / fix | 失败/修复 | 题型标签 |
| decision | 决策 | 题型标签 |
| context | 上下文 | 题型标签 |
| parallel | 并行 | 题型标签 |
| specialization | 专业化 | 题型标签 |
| handoff | 交接 | 题型标签 |
| verification | 验证 | 题型标签 |
| cost | 成本 | 题型标签 |
| trace | 追踪 | 题型标签 |
| feynman | 费曼 | 题型标签 |
| system design | 系统设计 | 题型标签 |
| COURSE MAP | 课程地图 | 标签 |
| START HERE IF | 适合人群 | 标签 |
| SOURCE BOUNDARY | 来源边界 | 标签 |
| ROADMAP | 学习路线 | 标签 |
| UNITS | 单元列表 | 标签 |
| NEXT | 后续推荐 | 标签 |

**批量执行**：
```bash
# 在 30_研究 根目录下执行
find . -name "学习页.html" -o -name "index.html" | xargs sed -i \
  -e 's/CONTENTS/目录/g' \
  -e 's/goals/学习目标/g' \
  -e 's/map/概念地图/g' \
  -e 's/flow/主线/g' \
  -e 's/vocab/术语/g' \
  -e 's/ledger/账本/g' \
  -e 's/mechanism/机制/g' \
  -e 's/fix/修法/g' \
  -e 's/debug/调试/g' \
  -e 's/bridge/桥接/g' \
  -e 's/evaluation/评测/g' \
  -e 's/bfcl/评测/g' \
  -e 's/source/参考/g' \
  -e 's/practice/练习/g' \
  -e 's/diagnostic/诊断/g' \
  -e 's/export/导出/g' \
  -e 's/COURSE MAP/课程地图/g' \
  -e 's/START HERE IF/适合人群/g' \
  -e 's/SOURCE BOUNDARY/来源边界/g' \
  -e 's/ROADMAP/学习路线/g' \
  -e 's/UNITS/单元列表/g' \
  -e 's/NEXT/后续推荐/g'
```

> 注意：批量替换有**误伤风险**（如 `source` 可能出现在 `<a href>` 中）。建议先在一个副本上测试，确认无误后再执行。更好的方式是使用 Python 脚本，只替换标签文本（如 `<span class="tag">...</span>` 和 `<span class="pill">...</span>` 内部的内容），而不是全局替换。

---

## 五、P2：中期优化（下季度）

### 5.1 合并 PyTorch 页面冗余章节

**文件**：`10_卷积神经网络基础：通道、卷积核与池化/学习页.html`

**冗余章节**：
- `worked-example`（完整样例）
- `bridge-chain`（故障链）
- `consistency-note`（一致性补充）

这三个章节都在讲同一件事：MNIST 图像从 `[N,1,28,28]` 经过 Conv→Pool→Flatten→Linear 的 shape 变化。

**建议合并为**：
- 保留 `worked-example` 作为完整教学链
- 将 `bridge-chain` 和 `consistency-note` 中**独有的**内容（如故障排查表、块大小取舍）合并进 `worked-example`
- 删除重复表格和车轱辘话
- 目标：将 3 个冗余章节压缩为 1 个紧凑的 "shape 追踪与故障排查" 章节

---

### 5.2 增强批量验证脚本

在 `.agents/skills/learning-kit/scripts/` 下新增 `content_audit.py`：

```python
#!/usr/bin/env python3
"""学习页内容质量审计脚本"""
import glob, re, sys, os

def audit_file(path):
    issues = []
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 检查模板化参考答案
    # 统计同一句话在 <details> 中出现的次数
    details_blocks = re.findall(r'<details>.*?</details>', content, re.DOTALL)
    answer_texts = []
    for block in details_blocks:
        p_tags = re.findall(r'<p>(.*?)</p>', block, re.DOTALL)
        answer_texts.extend(p_tags)
    
    # 如果超过 3 个不同题目的答案文本完全相同，则标记
    from collections import Counter
    text_counts = Counter(answer_texts)
    for text, count in text_counts.items():
        if count >= 3 and len(text) > 20:
            issues.append(f"模板化参考答案出现 {count} 次: {text[:50]}...")
    
    # 2. 检查内联样式块大小
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if style_match:
        style_len = len(style_match.group(1))
        if style_len > 5000:  # 超过 5KB 的内联样式
            issues.append(f"内联样式块过大: {style_len} bytes")
    
    # 3. 检查页面壳层标记
    if 'data-page-shell="study-page-v2"' not in content:
        issues.append("缺少 data-page-shell='study-page-v2' 标记")
    
    # 4. 检查双重转义
    if '&lt;code&gt;' in content:
        issues.append("存在双重 HTML 转义: &lt;code&gt;")
    
    # 5. 检查是否引用了外部 CSS
    if '../assets/study-page.css' not in content and 'assets/study-page.css' not in content:
        issues.append("未引用共享 study-page.css")
    
    return issues

def main():
    base = r"D:\Users\yyh\Downloads\笔记库\30_研究"
    files = glob.glob(os.path.join(base, "**", "学习页.html"), recursive=True)
    
    total_issues = 0
    for f in files:
        issues = audit_file(f)
        if issues:
            total_issues += len(issues)
            rel = os.path.relpath(f, base)
            print(f"\n[WARNING] {rel}")
            for issue in issues:
                print(f"  - {issue}")
    
    print(f"\n\n总计: {len(files)} 个文件, {total_issues} 个问题")
    sys.exit(0 if total_issues == 0 else 1)

if __name__ == "__main__":
    main()
```

---

### 5.3 建立"基础课程"专项打磨队列

从全量扫描结果看，**PyTorch 深度学习实践**、**概率论与深度学习**、**生成式 LLM 课程**这类"基础/通识课程"的质量问题比 **Agent 工程**、**系统协议**、**工具调用契约**等"专业课程"更多。

**建议**：
1. 把这些基础课程从"批量生成池"中捞出，分配**独立的编辑审阅资源**
2. 不再用"生成基础课 = 走模板"的心态对待它们
3. 为每个基础课程指定一个"课程负责人"，负责逐页验收
4. 参考 Agent 基础与工程系列的质量标准（该系列页面质量最高），把同样的标准应用到基础课

---

## 六、执行时间表

| 周 | 任务 | 负责人建议 | 验收方式 |
|----|------|-----------|----------|
| 第 1 周 | P0 全部完成：修复参考答案、修复渲染错误、确认课程名称 | 主线程 + 1 个工作代理 | `rg` 验证模板句为 0 |
| 第 2 周 | P1-4.1：清理 Codex + GPT 工作流 24 页内联样式 | 1 个工作代理逐页处理 | 浏览器打开抽查 |
| 第 3 周 | P1-4.2：清理生成式 LLM 62 页 + 概率论 58 页内联样式 | 2 个工作代理并行 | 浏览器打开抽查 + 文件大小对比 |
| 第 4 周 | P1-4.3 + 4.4：LoRA 孤儿页面修复 + 中文标签统一 | 1 个工作代理 | 审计脚本全绿 |
| 第 2 月起 | P2：合并冗余章节、部署审计脚本、建立打磨队列 | 主线程统筹 | 月度审计报告 |

---

## 七、关键决策点（需要用户确认）

1. **是否将 "Claude Code 工作流" 改名为 "Codex + GPT 工作流"？**
   - 如果改：需要修改 24 个页面 + 1 个 index.html + 课程根目录名
   - 如果不改：建议在 `index.html` 导语中增加一句定位说明

2. **内联样式清理策略**：
   - **激进方案**：全部删除内联样式，只保留外部 CSS（如果某些交互样式丢失，后续补充）
   - **保守方案**：先人工检查 2-3 个样本页面，确认哪些样式是"页面特定交互"需要保留的，再批量删除其余部分

3. **是否现在就执行 P1 的大规模样式清理？**
   - 建议先完成 P0（内容修复），再进入 P1（结构清理）
   - 或者如果用户时间充裕，可以 P0 + P1-4.1 并行执行

---

> **最后**：这套 learning-kit 系统的教学设计框架已经相当成熟。改革的重点不是推翻重来，而是**把已经建好的东西打磨到统一标准**。最大的工作量在"清理内联样式"（约 147 个页面受影响），但这是一劳永逸的：清理完成后，未来的全局样式更新只需要改一个 `study-page.css` 文件。
