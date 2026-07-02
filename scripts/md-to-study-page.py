#!/usr/bin/env python3
"""
学习页 Markdown 到 HTML 转换器 v1

用法:
    python scripts/md-to-study-page.py 输入.md 输出.html
    python scripts/md-to-study-page.py --batch 目录/    # 转换目录下所有 .md
    python scripts/md-to-study-page.py --batch --overwrite 目录/  # 覆盖已有 .html

规范文档: 99_系统/规范/学习页Markdown规范.md
"""
import sys, re, os, argparse, json, html
from pathlib import Path

# ==================== 模板常量 ====================

HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN" data-page-shell="study-page-v2">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
  <link rel="stylesheet" href="{{assets_path}}vendor/katex/katex.min.css">
  <link rel="stylesheet" href="{{assets_path}}vendor/prism/prism-tomorrow.min.css">
  <link rel="stylesheet" href="{{assets_path}}vendor/prism/prism-line-numbers.min.css">
  <link rel="stylesheet" href="{{assets_path}}study-page-v2.css">
</head>
<body data-course="{{course}}" data-unit="{{unit}}">

  <!-- Top Navigation -->
  <nav class="top-nav">
    <div class="top-nav-inner">
      <div class="top-nav-left">
        <a href="../index.html">{{course}}</a>
        <span class="sep">/</span>
        <span>{{unit}}</span>
      </div>
      <div class="top-nav-right">
        <a href="{{search_link}}" class="nav-pill">🔍 搜索</a>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <header class="hero">
    <div class="hero-main">
      <div class="kicker">{{kicker}}</div>
      <div class="hero-meta">
        <span class="hero-badge">{{unit}}</span>
      </div>
      <h1 class="hero-title">{{title}}</h1>
      <p class="hero-desc">{{summary}}</p>
      <div class="course-links">
{{course_links}}
      </div>
    </div>
    <div class="hero-side">
      <div class="can-do">
        <h3>读完本页应该能做什么</h3>
        <ul>
{{can_do}}
        </ul>
      </div>
    </div>
  </header>

  <!-- learning-kit:nav:start -->
  <div class="quick-toc">
    <div class="quick-toc-inner">
{{nav_links}}
    </div>
  </div>
  <!-- learning-kit:nav:end -->

  <!-- Content -->
  <article class="content">
{{content}}
    <section id="export">
      <h2>导出练习记录</h2>
      <div class="quality" id="quality">完成 0 题</div>
      <div class="export" id="record">还没有生成练习记录。</div>
      <div class="actions">
        <button class="action" onclick="generateRecord()">生成记录</button>
        <button class="ghost" onclick="copyRecord()">复制 Markdown</button>
      </div>
    </section>
    <section id="sources">
      <h2>参考资料</h2>
      <ul class="source-list">
{{sources}}
      </ul>
    </section>
  </article>

  <div class="footer-nav">
    <a href="../index.html">← 返回课程地图</a>
  </div>

  <script src="{{assets_path}}vendor/katex/katex.min.js"></script>
  <script src="{{assets_path}}vendor/katex/auto-render.min.js"></script>
  <script src="{{assets_path}}vendor/prism/prism-core.min.js"></script>
  <script src="{{assets_path}}vendor/prism/prism-clike.min.js"></script>
  <script src="{{assets_path}}vendor/prism/prism-python.min.js"></script>
  <script src="{{assets_path}}vendor/prism/prism-bash.min.js"></script>
  <script src="{{assets_path}}vendor/prism/prism-json.min.js"></script>
  <script src="{{assets_path}}vendor/prism/prism-line-numbers.min.js"></script>
  <script src="{{assets_path}}study-page-v2.js"></script>
</body>
</html>
"""

# ==================== 基础 Markdown 转换器 ====================

def md_inline_to_html(text):
    """转换行内 Markdown 到 HTML。"""
    # 先处理反引号中的数学内容（避免被后续代码替换覆盖）
    def _render_backtick(m):
        content = m.group(1)
        # 检测是否像数学公式：含 { } \ ^ _ 或常见数学命令
        if re.search(r'[\{}^_]', content) or re.match(r'^(hat|bar|vec|tilde|dot|ddot|mathcal|nabla|alpha|beta|gamma|delta|theta|eta|lambda|mu|pi|sigma|tau|phi|psi|omega|infty|pm|times|div|cdot|leq|geq|neq|approx|sqrt|frac|sum|int|prod|lim|partial)\b', content, re.I):
            # 为常见命令补反斜杠
            for cmd in ['hat', 'bar', 'vec', 'tilde', 'dot', 'ddot', 'mathcal', 'nabla', 'sqrt', 'frac', 'sum', 'int', 'prod', 'lim', 'partial']:
                content = re.sub(r'(?<!\\)' + cmd + r'(\{|$)', r'\\' + cmd + r'\1', content)
            for greek in ['alpha', 'beta', 'gamma', 'delta', 'theta', 'eta', 'lambda', 'mu', 'pi', 'sigma', 'tau', 'phi', 'psi', 'omega']:
                content = re.sub(r'(?<!\\)' + greek + r'\b', r'\\' + greek, content)
            return f'<span class="math-inline">${content}$</span>'
        return f'<code>{content}</code>'
    
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # 粗体
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    # 斜体
    text = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', text)
    # 链接
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def _is_grid_header_candidate(line):
    """快速判断一行是否可能是非标准网格表格的表头。"""
    s = line.strip()
    if not s or len(s) > 40:
        return False
    if re.match(r'^##\s+', s):
        return False
    if s.startswith(('>', '<!--', '$$', '```', '|', '- ', '* ', '+ ')):
        return False
    if re.match(r'^\d+[\.\)]\s+', s):
        return False
    if re.search(r'[。，；！？,.!?]', s):
        return False
    return True


def _try_grid_table_block(lines, start):
    """检测块内的旧式网格表格，保持线性、有界，供 box/callout 内部使用。"""
    i = start
    headers = []
    max_header_lines = 12
    while i < len(lines) and lines[i].strip():
        if not _is_grid_header_candidate(lines[i]):
            return None
        headers.append(lines[i].strip())
        i += 1
        if len(headers) > max_header_lines:
            return None

    if len(headers) < 3:
        return None

    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return None

    col_count = len(headers)
    data_groups = []
    while i < len(lines):
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines):
            break

        s = lines[i].strip()
        if re.match(r'^##\s+', s) or s.startswith(('>', '<!--', '$$', '```', '|')):
            break

        group_start = i
        group = []
        while i < len(lines) and lines[i].strip() and len(group) < col_count:
            s = lines[i].strip()
            if re.match(r'^##\s+', s) or s.startswith(('>', '<!--', '$$', '```', '|')):
                break
            group.append(s)
            i += 1

        if len(group) == col_count:
            data_groups.append(group)
            continue

        if data_groups:
            # 当前行不是完整数据组，留给后续普通段落渲染。
            i = group_start
            break
        return None

    if not data_groups:
        return None

    return {'headers': headers, 'data': data_groups, 'next': i}


def md_block_to_html(lines):
    """将 Markdown 块转换为 HTML 字符串，支持代码块、表格、标题、列表、段落。"""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 空行
        if not stripped:
            i += 1
            continue

        # HTML 注释（跳过 table-export 等）
        if stripped.startswith('<!--'):
            i += 1
            continue

        # 短标题 + 短标签 + 代码块，渲染为带 codebar 的代码示例。
        if (
            i + 2 < len(lines)
            and lines[i + 1].strip()
            and lines[i + 2].strip().startswith('```')
            and len(stripped) <= 40
            and len(lines[i + 1].strip()) <= 40
            and not stripped.startswith(('#', '-', '*', '+', '|', '$$', '```', '>'))
            and not lines[i + 1].strip().startswith(('#', '-', '*', '+', '|', '$$', '```', '>'))
        ):
            label = md_inline_to_html(stripped)
            sublabel = md_inline_to_html(lines[i + 1].strip())
            fence = lines[i + 2].strip()
            lang = fence[3:].strip().split()[0] if len(fence) > 3 else 'text'
            i += 3
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            escaped = '\n'.join(code_lines).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            result.append(
                f'<div class="code-example">\n'
                f'<div class="codebar"><span>{label}</span><span>{sublabel}</span></div>\n'
                f'<pre><code class="language-{lang}">{escaped}</code></pre>\n'
                f'</div>'
            )
            continue

        # 代码块
        if stripped.startswith('```'):
            lang = stripped[3:].strip().split()[0] if len(stripped) > 3 else 'text'
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip ```
            escaped = '\n'.join(code_lines).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            result.append(f'<pre><code class="language-{lang}">{escaped}</code></pre>')
            continue

        # 表格
        if stripped.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            if len(table_lines) >= 2:
                header = [c.strip() for c in table_lines[0].split('|')[1:-1]]
                data_rows = []
                for r in table_lines[2:]:
                    cells = [c.strip() for c in r.split('|')[1:-1]]
                    if cells:
                        data_rows.append(cells)
                th = ''.join(f'<th>{md_inline_to_html(c)}</th>' for c in header)
                trs = ''
                for dr in data_rows:
                    tds = ''.join(f'<td>{md_inline_to_html(c)}</td>' for c in dr)
                    trs += f'\n<tr>{tds}</tr>'
                result.append(f'<table class="metric-table">\n<tr>{th}</tr>{trs}\n</table>')
            continue

        # 标题 h3 (###)
        if stripped.startswith('### '):
            text = stripped[4:].strip()
            result.append(f'<h3>{md_inline_to_html(text)}</h3>')
            i += 1
            continue

        # 标题 h4 (##)
        if stripped.startswith('## '):
            text = stripped[3:].strip()
            result.append(f'<h4>{md_inline_to_html(text)}</h4>')
            i += 1
            continue

        # 标题 h2 (#)
        if stripped.startswith('# '):
            text = stripped[2:].strip()
            result.append(f'<h2>{md_inline_to_html(text)}</h2>')
            i += 1
            continue

        # 无序列表
        if stripped.startswith('- ') or stripped.startswith('* '):
            list_items = []
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                item_text = lines[i].strip()[2:]
                list_items.append(f'<li>{md_inline_to_html(item_text)}</li>')
                i += 1
            result.append(f'<ul>\n' + '\n'.join(list_items) + '\n</ul>')
            continue

        # 有序列表
        if re.match(r'^\d+\.\s', stripped):
            list_items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                item_text = re.sub(r'^\d+\.\s', '', lines[i].strip())
                list_items.append(f'<li>{md_inline_to_html(item_text)}</li>')
                i += 1
            result.append(f'<ol>\n' + '\n'.join(list_items) + '\n</ol>')
            continue

        # 旧式网格表格：N 行表头 + 空行 + 每组 N 行数据。
        grid = _try_grid_table_block(lines, i)
        if grid:
            th = ''.join(f'<th>{md_inline_to_html(h)}</th>' for h in grid['headers'])
            trs = ''
            for group in grid['data']:
                tds = ''.join(f'<td>{md_inline_to_html(c)}</td>' for c in group)
                trs += f'\n<tr>{tds}</tr>'
            result.append(f'<div class="table-wrap"><table class="metric-table">\n<tr>{th}</tr>{trs}\n</table></div>')
            i = grid['next']
            continue

        # 普通段落
        result.append(f'<p>{md_inline_to_html(stripped)}</p>')
        i += 1

    return '\n'.join(result)


# ==================== 结构解析器 ====================

class StudyPageParser:
    def __init__(self, text):
        self.text = text
        self.lines = text.splitlines()
        self.idx = 0
        self.frontmatter = {}
        self.sections = []
        self._used_section_ids = set()
        self._parse()

    def _parse(self):
        # 解析 YAML frontmatter
        if self.lines and self.lines[0].strip() == '---':
            self.idx = 1
            yaml_lines = []
            while self.idx < len(self.lines) and self.lines[self.idx].strip() != '---':
                yaml_lines.append(self.lines[self.idx])
                self.idx += 1
            self.idx += 1  # 跳过 ---
            self.frontmatter = self._parse_yaml('\n'.join(yaml_lines))

        # 跳过空行
        while self.idx < len(self.lines) and not self.lines[self.idx].strip():
            self.idx += 1

        # 解析正文
        while self.idx < len(self.lines):
            self._parse_section()

    def _parse_yaml(self, text):
        """解析 YAML frontmatter，支持简单键值对、列表和嵌套对象。"""
        data = {}
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                i += 1
                continue

            m = re.match(r'^(\w+):\s*(.*)$', stripped)
            if not m:
                i += 1
                continue

            key, val = m.group(1), m.group(2).strip()

            # 纯值（有内容）
            if val:
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                data[key] = val
                i += 1
                continue

            # 空值，可能是列表或对象开始
            i += 1
            items = []
            current_obj = None
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.strip()
                if not next_stripped or next_stripped.startswith('#'):
                    i += 1
                    continue
                # 列表项
                if next_stripped.startswith('- '):
                    # 保存之前的对象
                    if current_obj is not None:
                        items.append(current_obj)
                        current_obj = None
                    item_text = next_stripped[2:].strip()
                    obj_match = re.findall(r'(\w+):\s*"([^"]+)"', item_text)
                    if obj_match:
                        obj = {}
                        for k, v in obj_match:
                            obj[k] = v
                        # 如果还有未解析的属性（同一行），继续检查
                        current_obj = obj
                    else:
                        if item_text.startswith('"') and item_text.endswith('"'):
                            item_text = item_text[1:-1]
                        elif item_text.startswith("'") and item_text.endswith("'"):
                            item_text = item_text[1:-1]
                        items.append(item_text)
                    i += 1
                    continue
                # 同一级别的键（不是列表项）
                if re.match(r'^(\w+):\s*', next_stripped) and not next_stripped.startswith('- '):
                    # 如果当前有未完成的对象，且这行是对象属性
                    if current_obj is not None:
                        attr_match = re.findall(r'(\w+):\s*"([^"]+)"', next_stripped)
                        if attr_match:
                            for k, v in attr_match:
                                current_obj[k] = v
                            i += 1
                            continue
                    break
                else:
                    break

            # 保存最后一个对象
            if current_obj is not None:
                items.append(current_obj)

            if items:
                data[key] = items

        return data

    def _parse_section(self):
        """解析一个 section。"""
        line = self.lines[self.idx].strip() if self.idx < len(self.lines) else ''

        # Section 标题: # 标题 {#id}
        m = re.match(r'^#\s+(.+?)\s*\{#([^}]+)\}\s*$', line)
        if not m:
            # 也支持没有 id 的标题
            m = re.match(r'^#\s+(.+?)\s*$', line)
            if m:
                title = m.group(1).strip()
                section_id = self._slug(title)
            else:
                self.idx += 1
                return
        else:
            title = m.group(1).strip()
            section_id = m.group(2).strip()

        section_id = self._unique_section_id(section_id)

        self.idx += 1

        section = {
            'id': section_id,
            'title': title,
            'tag': '',
            'layout': '',
            'items': []
        }

        # 读取 tag 和 layout 注释
        while self.idx < len(self.lines):
            l = self.lines[self.idx].strip()
            if l.startswith('<!-- tag:'):
                section['tag'] = re.search(r'tag:\s*(\S+)', l).group(1) if re.search(r'tag:\s*(\S+)', l) else ''
                self.idx += 1
            elif l.startswith('<!-- layout:'):
                section['layout'] = re.search(r'layout:\s*(\S+)', l).group(1) if re.search(r'layout:\s*(\S+)', l) else ''
                self.idx += 1
            else:
                break

        # 读取内容直到下一个 section 或文件结束
        content_lines = []
        in_code = False
        while self.idx < len(self.lines):
            l = self.lines[self.idx]
            stripped = l.strip()

            # 切换代码块状态
            if stripped.startswith('```'):
                in_code = not in_code

            if not in_code:
                if re.match(r'^#\s+', stripped):
                    break
                if stripped == '---':
                    self.idx += 1
                    break

            content_lines.append(l)
            self.idx += 1

        section['items'] = self._parse_content_blocks(content_lines)
        self.sections.append(section)

    def _slug(self, text):
        """生成 slug。"""
        s = re.sub(r'[^\w\s]', '', text)
        return s.replace(' ', '-').lower()[:30]

    def _unique_section_id(self, section_id):
        """避免正文 section id 与模板固定 id 或其他 section 冲突。"""
        reserved = {'export', 'record', 'quality', 'top', 'content', 'sources'}
        base = section_id or 'section'
        if base in reserved:
            base = f'section-{base}'
        candidate = base
        suffix = 2
        while candidate in self._used_section_ids or candidate in reserved:
            candidate = f'{base}-{suffix}'
            suffix += 1
        self._used_section_ids.add(candidate)
        return candidate

    def _is_grid_header_candidate(self, line):
        """快速判断一行是否可能是网格表格表头。"""
        s = line.strip()
        if not s:
            return False
        if len(s) > 40:
            return False
        if re.match(r'^##\s+', s):
            return False
        if s.startswith(('>', '<!--', '$$', '```', '|', '- ', '* ', '+ ')):
            return False
        if re.match(r'^\d+[\.\)]\s+', s):
            return False
        # 表头通常是短词/短语；带句子标点的普通段落直接排除。
        if re.search(r'[。，；！？,.!?]', s):
            return False
        return True

    def _looks_like_grid_table_start(self, lines, start):
        """只在高置信度网格表格开头触发完整检测，避免普通文本 O(n²) 扫描。"""
        max_header_lines = 12
        i = start
        header_count = 0

        while i < len(lines) and lines[i].strip():
            if not self._is_grid_header_candidate(lines[i]):
                return False
            header_count += 1
            if header_count > max_header_lines:
                return False
            i += 1

        if header_count < 3:
            return False
        if i >= len(lines) or lines[i].strip():
            return False

        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines):
            return False

        # 只探测首个数据组的形状：必须刚好 header_count 行后遇到空行/块边界。
        for offset in range(header_count):
            j = i + offset
            if j >= len(lines):
                return False
            s = lines[j].strip()
            if not s:
                return False
            if re.match(r'^##\s+', s) or s.startswith(('>', '<!--', '$$', '```', '|')):
                return False

        j = i + header_count
        if j < len(lines):
            s = lines[j].strip()
            if s and not (re.match(r'^##\s+', s) or s.startswith(('>', '<!--', '$$', '```', '|'))):
                return False

        return True

    def _try_detect_grid_table(self, lines, start):
        """检测非标准网格表格格式：N 行标题 + 空行 + 至少一组 N 行数据（组间空行分隔）。
        排除包含 ## box、callout、注释等特殊标记的内容。"""
        i = start
        headers = []
        # 限制 headers 最大数量，避免扫描整个长段落
        MAX_HEADER_LINES = 12
        while i < len(lines) and lines[i].strip():
            # 排除特殊标记行（box、callout、注释、公式、代码、标准表格）
            s = lines[i].strip()
            if re.match(r'^##\s+', s) or s.startswith('>') or s.startswith('<!--') or s.startswith('$$') or s.startswith('```') or s.startswith('|'):
                return None
            # 启发式：如果行太长（超过40字）或包含句子标点，大概率不是表格标题
            if len(s) > 40 or re.search(r'[。，；！？]', s):
                return None
            headers.append(lines[i])
            i += 1
            if len(headers) > MAX_HEADER_LINES:
                return None
        if len(headers) < 3:
            return None
        # 跳过空行
        while i < len(lines) and not lines[i].strip():
            i += 1
        col_count = len(headers)
        data_groups = []
        while i < len(lines):
            group = []
            while i < len(lines) and lines[i].strip():
                s = lines[i].strip()
                # 遇到特殊标记行：已有数据组则结束，否则放弃
                if re.match(r'^##\s+', s) or s.startswith('>') or s.startswith('<!--') or s.startswith('$$') or s.startswith('```') or s.startswith('|'):
                    if not data_groups:
                        return None
                    return {'headers': headers, 'data': data_groups, 'next_idx': i}
                group.append(lines[i])
                i += 1
            if len(group) == col_count:
                data_groups.append(group)
            elif len(group) > 0:
                if not data_groups:
                    return None
                break
            else:
                break
            # 跳过空行
            while i < len(lines) and not lines[i].strip():
                i += 1
            if not data_groups:
                break
        if not data_groups:
            return None
        return {'headers': headers, 'data': data_groups, 'next_idx': i}

    def _parse_content_blocks(self, lines):
        """解析 section 内的内容块（box、表格、代码等）。"""
        items = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            # Box 变体
            box_m = re.match(r'^##\s+box\s*(\w*)\s*$', line)
            if box_m:
                variant = box_m.group(1).strip()
                i += 1
                # 收集 box 内容直到下一个 ## 或文件结束
                box_lines = []
                while i < len(lines):
                    next_line = lines[i].strip()
                    if re.match(r'^##\s+', next_line):
                        break
                    if re.match(r'^<!--\s+end-', next_line):
                        break
                    # Stop at section separators; formulas, code, and tables can live inside a box.
                    if next_line == '---':
                        break
                    box_lines.append(lines[i])
                    i += 1
                items.append({'type': 'box', 'variant': variant, 'content': box_lines})
                continue

            # Callout / Admonition（GitHub/Notion/Obsidian 标准语法）
            callout_m = re.match(r'^>\s+\[!(NOTE|TIP|WARNING|DANGER|INFO)\]\s*(.*)$', line, re.IGNORECASE)
            if callout_m:
                callout_type = callout_m.group(1).lower()
                callout_title = callout_m.group(2).strip()
                i += 1
                callout_lines = []
                while i < len(lines):
                    if not lines[i].strip().startswith('>'):
                        break
                    content = lines[i].lstrip()
                    if content.startswith('>'):
                        content = content[1:].lstrip()
                    callout_lines.append(content)
                    i += 1
                items.append({'type': 'callout', 'callout_type': callout_type, 'title': callout_title, 'lines': callout_lines})
                continue

            # 数学公式
            if line.startswith('$$') and line.endswith('$$') and line != '$$':
                # 单行公式（$$...$$ 在同一行且有实际内容）
                formula = line[2:-2].strip()
                items.append({'type': 'formula', 'content': formula})
                i += 1
                continue
            if line.startswith('$$'):
                # 多行公式
                formula_lines = [line[2:].strip()]
                i += 1
                while i < len(lines) and not lines[i].strip().endswith('$$'):
                    formula_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    last = lines[i].strip()
                    if last.endswith('$$'):
                        formula_lines.append(last[:-2].strip())
                    else:
                        formula_lines.append(last)
                    i += 1
                items.append({'type': 'formula', 'content': '\n'.join(formula_lines)})
                continue

            # 代码块
            if line.startswith('```'):
                lang = line[3:].strip().split()[0] if len(line) > 3 else 'text'
                # 解析代码块属性 {id="..." label="..."}
                attrs = {}
                attr_match = re.search(r'\{([^}]+)\}', line)
                if attr_match:
                    attr_str = attr_match.group(1)
                    for m in re.finditer(r'(\w+)="([^"]*)"', attr_str):
                        attrs[m.group(1)] = m.group(2)
                i += 1
                code_lines = []
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                i += 1  # 跳过 ```
                items.append({'type': 'code', 'lang': lang, 'code': '\n'.join(code_lines), 'attrs': attrs})
                continue

            # 表格
            if line.startswith('|'):
                table_lines = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    table_lines.append(lines[i])
                    i += 1
                items.append({'type': 'table', 'rows': table_lines})
                continue

            # 练习区域标记
            if line.startswith('<!-- practice-intro -->'):
                i += 1
                intro_lines = []
                while i < len(lines) and not lines[i].strip().startswith('<!-- end-practice-intro -->'):
                    intro_lines.append(lines[i])
                    i += 1
                i += 1  # 跳过 end 标记
                # 解析 intro 里的 box
                intro_items = self._parse_content_blocks(intro_lines)
                items.append({'type': 'practice-intro', 'items': intro_items})
                continue

            if line.startswith('<!-- practice-group:'):
                group_name = re.search(r'practice-group:\s*(.+)', line).group(1).strip()
                if group_name.endswith('-->'):
                    group_name = group_name[:-3].strip()
                i += 1
                # quick-review
                quick_review = ''
                if i < len(lines) and lines[i].strip().startswith('<!-- quick-review:'):
                    quick_review = re.search(r'quick-review:\s*(.+)', lines[i]).group(1).strip()
                    i += 1
                # 收集题目
                questions = []
                while i < len(lines) and not lines[i].strip().startswith('<!-- end-practice-group -->'):
                    q_line = lines[i].strip()
                    # 题目: ### 01 choice
                    qm = re.match(r'^###\s+(\S+)\s+([^\s]+)\s*$', q_line)
                    if qm:
                        q_num = qm.group(1)
                        q_type = qm.group(2)
                        i += 1
                        # 收集题目内容
                        q_lines = []
                        while i < len(lines):
                            ql = lines[i].strip()
                            if re.match(r'^###\s+', ql):
                                break
                            if ql.startswith('<!-- end-practice-group -->'):
                                break
                            q_lines.append(lines[i])
                            i += 1
                        questions.append(self._parse_question(q_num, q_type, q_lines))
                        continue
                    i += 1
                i += 1  # 跳过 end 标记
                items.append({'type': 'practice-group', 'name': group_name, 'quick_review': quick_review, 'questions': questions})
                continue

            # 数学公式
            if line.startswith('$$'):
                formula_lines = [line]
                i += 1
                while i < len(lines) and not lines[i].strip().endswith('$$'):
                    formula_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    formula_lines.append(lines[i])
                    i += 1
                items.append({'type': 'formula', 'content': '\n'.join(formula_lines)})
                continue

            # 非标准网格表格检测（在普通文本之前，避免被当作段落处理）
            if self._looks_like_grid_table_start(lines, i):
                grid = self._try_detect_grid_table(lines, i)
                if grid:
                    items.append({'type': 'grid-table', 'headers': grid['headers'], 'data': grid['data']})
                    i = grid['next_idx']
                    continue

            # 普通文本行（积累为段落）
            text_lines = []
            while i < len(lines):
                tl = lines[i].strip()
                if not tl:
                    break
                # 如果遇到特殊标记，停止
                if re.match(r'^##\s+', tl) or tl.startswith('```') or tl.startswith('|') or tl.startswith('<!--') or tl.startswith('$$'):
                    break
                text_lines.append(lines[i])
                i += 1
            if text_lines:
                items.append({'type': 'text', 'lines': text_lines})
            else:
                i += 1

        return items

    def _parse_question(self, num, qtype, lines):
        """解析单个题目。"""
        q = {'num': num, 'type': qtype, 'text': '', 'options': [], 'answer': '', 'explain': '', 'details': ''}
        text_lines = []
        i = 0

        def clean_answer_text(value):
            return re.sub(r'^\s*[.。]\s+', '', value.strip())

        while i < len(lines):
            line = lines[i].strip()

            # 选项
            if line.startswith('- [ ]') or line.startswith('- [x]'):
                q['options'].append(clean_answer_text(line[5:].strip()))
                i += 1
                continue

            # Answer
            if line.startswith('Answer:'):
                q['answer'] = clean_answer_text(line[7:].strip())
                i += 1
                continue

            # Explain
            if line.startswith('Explain:'):
                q['explain'] = line[8:].strip()
                i += 1
                continue

            # Details
            if line.startswith('Details:'):
                q['details'] = line[8:].strip()
                i += 1
                continue

            # 输入框提示
            if line.startswith('::input') or line.startswith('::textarea'):
                q['input_hint'] = line
                i += 1
                continue

            text_lines.append(lines[i])
            i += 1

        q['text'] = '\n'.join(text_lines).strip()
        return q


# ==================== HTML 生成器 ====================

def compute_assets_path(output_file):
    """计算从输出 HTML 文件到仓库根目录 assets/ 的相对路径。

    例如: 输出文件在 Agent/研习资料/Agent基础与工程/学习页.html
         返回: ../../../assets/
    例如: 输出文件在 计算机教育中缺失的一课/研习资料/学习页.html
         返回: ../../assets/
    """
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent  # scripts/ 的父目录即仓库根
    output_dir = Path(output_file).resolve().parent
    rel = os.path.relpath(str(repo_root / 'assets'), str(output_dir))
    # 确保以 / 结尾并统一为 forward slash
    return rel.replace('\\', '/') + '/'


def generate_html(parser, assets_path='../assets/'):
    """根据解析结果生成完整 HTML。"""
    fm = parser.frontmatter

    # 构建导航链接
    nav_links = []
    for sec in parser.sections:
        if sec['id'] and sec['id'] not in ('export', 'sources'):
            sid = sec['id']
            stitle = sec['title']
            nav_links.append(f'      <a href="#{sid}">{stitle}</a>')

    # 构建 course links
    course_links = []
    raw_links = fm.get('course_links', '')
    if isinstance(raw_links, list):
        for link in raw_links:
            if isinstance(link, dict) and 'text' in link and 'href' in link:
                course_links.append(f'            <a href="{link["href"]}">{link["text"]}</a>')
    elif isinstance(raw_links, str):
        # 简单解析：text: href 格式
        for m in re.finditer(r'-?\s*text:\s*"([^"]+)"\s*href:\s*"([^"]+)"', raw_links):
            course_links.append(f'            <a href="{m.group(2)}">{m.group(1)}</a>')

    # 构建 can_do
    can_do = []
    raw_can = fm.get('can_do', '')
    if isinstance(raw_can, str):
        for m in re.finditer(r'-\s+(.+)', raw_can):
            can_do.append(f'            <li>{md_inline_to_html(m.group(1))}</li>')
    elif isinstance(raw_can, list):
        for item in raw_can:
            can_do.append(f'            <li>{md_inline_to_html(item)}</li>')

    # 构建 section HTML
    sections_html = []
    for sec in parser.sections:
        if sec['id'] in ('export', 'sources'):
            continue
        sections_html.append(render_section(sec))

    # 构建 sources
    sources_html = []
    for sec in parser.sections:
        if sec['id'] == 'sources':
            for item in sec['items']:
                if item['type'] == 'text':
                    for line in item['lines']:
                        stripped = line.strip()
                        if stripped.startswith('- '):
                            sources_html.append(f'          <li>{md_inline_to_html(stripped[2:])}</li>')

    # 替换模板
    html = HTML_TEMPLATE
    html = html.replace('{{assets_path}}', assets_path)
    html = html.replace('{{search_link}}', assets_path.replace('assets/', 'search.html'))
    html = html.replace('{{title}}', fm.get('title', '学习页'))
    html = html.replace('{{course}}', fm.get('course', ''))
    html = html.replace('{{unit}}', fm.get('unit', ''))
    html = html.replace('{{kicker}}', fm.get('kicker', '') + (f' · {fm.get("kicker_en", "")}' if fm.get('kicker_en') else ''))
    html = html.replace('{{summary}}', fm.get('summary', ''))
    html = html.replace('{{side_note}}', fm.get('side_note', ''))
    html = html.replace('{{nav_links}}', '\n'.join(nav_links))
    html = html.replace('{{course_links}}', '\n'.join(course_links))
    html = html.replace('{{can_do}}', '\n'.join(can_do))
    html = html.replace('{{content}}', '\n'.join(sections_html))
    html = html.replace('{{sources}}', '\n'.join(sources_html))

    return html


def render_section(sec):
    """渲染单个 section。"""
    tag_html = f'<span class="tag">{sec["tag"]}</span>' if sec['tag'] else ''

    items_html = []
    n = len(sec['items'])
    i = 0
    code_counter = 0  # ensure unique code ids within section
    while i < n:
        item = sec['items'][i]
        if item['type'] == 'box':
            variant = item['variant']
            cls = f'box {variant}' if variant else 'box'
            content = md_block_to_html(item['content'])
            items_html.append(f'        <div class="{cls}">\n{content}\n        </div>')
        elif item['type'] == 'callout':
            callout_type = item['callout_type']
            title = item['title']
            content = md_block_to_html(item['lines'])
            title_html = f'<div class="callout-title">{title}</div>' if title else ''
            items_html.append(f'        <div class="callout {callout_type}">\n{title_html}{content}\n        </div>')
        elif item['type'] == 'code':
            code_counter += 1
            attrs = item.get('attrs', {})
            code_id = attrs.get('id', f'code-{sec["id"]}-{code_counter}')
            label = attrs.get('label', '代码')
            lang = item['lang']
            code = item['code']
            escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            code_html = f'''        <div class="codebar"><span>{label}</span><button class="copy" data-copy="{code_id}">复制</button></div>
        <pre id="{code_id}" data-export-context="{label}" data-export-lang="{lang}"><code class="language-{lang}">{escaped}</code></pre>'''
            # Check if next item is explanatory text
            if i + 1 < n and sec['items'][i + 1]['type'] == 'text':
                next_item = sec['items'][i + 1]
                note_html = md_block_to_html(next_item['lines'])
                items_html.append(f'        <div class="code-example">\n{code_html}\n{note_html}\n        </div>')
                i += 2
                continue
            else:
                items_html.append(f'        <div class="code-example">\n{code_html}\n        </div>')
            i += 1

        elif item['type'] == 'table':
            rows = item['rows']
            if len(rows) < 2:
                i += 1
                continue
            header = [c.strip() for c in rows[0].split('|')[1:-1]]
            data_rows = []
            for r in rows[2:]:
                cells = [c.strip() for c in r.split('|')[1:-1]]
                if cells:
                    data_rows.append(cells)
            th = ''.join(f'<th>{c}</th>' for c in header)
            trs = ''
            for dr in data_rows:
                tds = ''.join(f'<td>{md_inline_to_html(c)}</td>' for c in dr)
                trs += f'<tr>{tds}</tr>'
            items_html.append(f'        <div class="table-wrap"><table class="metric-table">\n          <tr>{th}</tr>\n{trs}\n        </table></div>')
        elif item['type'] == 'grid-table':
            headers = [md_inline_to_html(h.strip()) for h in item['headers']]
            th = ''.join(f'<th>{h}</th>' for h in headers)
            trs = ''
            for group in item['data']:
                tds = ''.join(f'<td>{md_inline_to_html(c.strip())}</td>' for c in group)
                trs += f'\n<tr>{tds}</tr>'
            items_html.append(f'        <div class="table-wrap"><table class="metric-table">\n          <tr>{th}</tr>{trs}\n        </table></div>')

        elif item['type'] == 'text':
            content = md_block_to_html(item['lines'])
            items_html.append(content)
            i += 1

        elif item['type'] == 'formula':
            content = item['content'].strip()
            if content.startswith('$$'):
                content = content[2:]
            if content.endswith('$$'):
                content = content[:-2]
            items_html.append(f'        <div class="formula" data-export-context="公式" data-export-lang="math">\n$$\n{content.strip()}\n$$\n        </div>')
        elif item['type'] == 'practice-intro':
            intro_items = []
            for intro in item['items']:
                if intro['type'] == 'box':
                    variant = intro['variant']
                    cls = f'box {variant}' if variant else 'box'
                    content = md_block_to_html(intro['content'])
                    intro_items.append(f'      <div class="{cls}">\n{content}\n      </div>')
                elif intro['type'] == 'callout':
                    callout_type = intro['callout_type']
                    title = intro['title']
                    content = md_block_to_html(intro['lines'])
                    title_html = f'<div class="callout-title">{title}</div>' if title else ''
                    intro_items.append(f'      <div class="callout {callout_type}">\n{title_html}{content}\n      </div>')
            items_html.append(f'      <div class="practice-intro">\n' + '\n'.join(intro_items) + '\n      </div>')
        elif item['type'] == 'practice-group':
            questions_html = []
            for q in item['questions']:
                questions_html.append(render_question(q))

            quick = f'<div class="quick-review">{item["quick_review"]}</div>' if item['quick_review'] else ''
            questions_joined = '\n'.join(questions_html)
            items_html.append(f'''      <div class="practice-group">
        <div class="group-head">
          <div><h3>{item["name"]}</h3></div>
          {quick}
        </div>
        <div class="drill-grid">
{questions_joined}
        </div>
      </div>''')
        i += 1

    if sec['layout']:
        layout_open = f'      <div class="{sec["layout"]}">\n'
        layout_close = '      </div>'
        content = layout_open + '\n'.join(items_html) + '\n' + layout_close
    else:
        content = '\n'.join(items_html)

    return f'''      <section id="{sec["id"]}">
        <div class="head">
          <h2>{sec["title"]}</h2>
          {tag_html}
        </div>
{content}
      </section>'''


def render_question(q):
    """渲染单个题目。"""
    qtype_map = {
        'choice': 'choice',
        'true/false': 'true/false',
        'fill': 'fill',
        'ordering': 'ordering',
        'code-reading': 'code reading',
        'short-answer': 'short answer',
        'matching': 'matching',
        'synthesis': 'synthesis',
        'diagnosis': 'error diagnosis',
        'scenario': 'scenario transfer',
        'checklist': 'checklist'
    }
    pill_type = qtype_map.get(q['type'], q['type'])
    q_num_attr = html.escape(str(q['num']), quote=True)
    q_answer_attr = html.escape(q['answer'], quote=True)
    q_group_attr = html.escape(q.get('group', ''), quote=True)
    q_title_attr = html.escape(q.get('title', ''), quote=True)

    # 构建选项
    options_html = ''
    if q['options']:
        input_type = 'checkbox' if q['type'] == 'checklist' else 'radio'
        opts = '\n'.join(
            f'      <label><input type="{input_type}" name="q{q_num_attr}" value="{html.escape(opt, quote=True)}">{md_inline_to_html(opt)}</label>'
            for opt in q['options']
        )
        options_html = f'\n      <div class="choices">\n{opts}\n      </div>'

    # 构建输入框
    input_html = ''
    if not q['options'] and q['type'] not in ('choice', 'true/false'):
        input_html = f'\n      <textarea name="q{q_num_attr}"></textarea>'

    # 构建反馈
    feedback_content = q['answer']
    if q['explain']:
        feedback_content += f'。{q["explain"]}'
    if q['details']:
        feedback_content += f'\n{q["details"]}'

    # 题目编号和类型
    num_clean = re.sub(r'[^\w]', '', q['num'])

    return f'''      <article class="q" data-question="q{num_clean}" data-group="{q_group_attr}" data-title="{q_title_attr}" data-answer="{q_answer_attr}">
        <div class="q-meta"><span class="pill">{q["num"]}</span><span class="pill">{pill_type}</span></div>
        <h3>{md_inline_to_html(q["text"])}</h3>
{options_html}
{input_html}
        <button class="check" type="button">检查</button>
        <div class="feedback"></div>
        <details>
          <summary>参考答案 / 评分要点</summary>
          <p>{md_inline_to_html(feedback_content)}</p>
        </details>
      </article>'''


# ==================== 主入口 ====================

def main():
    parser = argparse.ArgumentParser(description='学习页 Markdown 到 HTML 转换器')
    parser.add_argument('input', nargs='?', help='输入 .md 文件或目录')
    parser.add_argument('output', nargs='?', help='输出 .html 文件（单文件模式）')
    parser.add_argument('--batch', action='store_true', help='批量转换目录下所有 .md')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已有 .html')
    parser.add_argument('--check', action='store_true', help='检查规范而不生成')
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input)

    if args.batch or input_path.is_dir():
        # 批量模式
        md_files = list(input_path.rglob('*.md'))
        for md_file in md_files:
            html_file = md_file.with_suffix('.html')
            if html_file.exists() and not args.overwrite:
                print(f'  SKIP {md_file} -> {html_file} (已存在)')
                continue
            try:
                text = md_file.read_text(encoding='utf-8')
                study = StudyPageParser(text)
                assets_path = compute_assets_path(html_file)
                html = generate_html(study, assets_path)
                html_file.write_text(html, encoding='utf-8')
                print(f'  OK   {md_file} -> {html_file}')
            except Exception as e:
                print(f'  FAIL {md_file}: {e}')
    else:
        # 单文件模式
        text = input_path.read_text(encoding='utf-8')
        study = StudyPageParser(text)

        if args.check:
            print('Frontmatter:')
            for k, v in study.frontmatter.items():
                print(f'  {k}: {v}')
            print(f'Sections: {len(study.sections)}')
            for sec in study.sections:
                print(f'  - {sec["id"]}: {sec["title"]} (tag={sec["tag"]}, layout={sec["layout"]}, items={len(sec["items"])})')
            return

        output = args.output or input_path.with_suffix('.html')
        assets_path = compute_assets_path(output)
        html = generate_html(study, assets_path)
        Path(output).write_text(html, encoding='utf-8')
        print(f'已生成: {output}')


if __name__ == '__main__':
    main()
