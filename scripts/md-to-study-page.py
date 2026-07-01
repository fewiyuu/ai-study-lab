#!/usr/bin/env python3
"""
学习页 Markdown 到 HTML 转换器 v1

用法:
    python scripts/md-to-study-page.py 输入.md 输出.html
    python scripts/md-to-study-page.py --batch 目录/    # 转换目录下所有 .md
    python scripts/md-to-study-page.py --batch --overwrite 目录/  # 覆盖已有 .html

规范文档: 99_系统/规范/学习页Markdown规范.md
"""
import sys, re, os, argparse, json
from pathlib import Path

# ==================== 模板常量 ====================

HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN" data-page-shell="study-page-v2">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
  <link rel="stylesheet" href="../assets/vendor/katex/katex.min.css">
  <link rel="stylesheet" href="../assets/vendor/prism/prism-tomorrow.min.css">
  <link rel="stylesheet" href="../assets/vendor/prism/prism-line-numbers.min.css">
  <link rel="stylesheet" href="../assets/study-page.css">
</head>
<body data-course="{{course}}" data-unit="{{unit}}">
  <div class="progress" id="progress"></div>
  <div class="layout">
    <aside>
      <div class="brand">
        <strong>{{course}}</strong>
        <span>{{unit}}</span>
      </div>
      <nav>
        <!-- learning-kit:nav:start -->
        <a href="../index.html"><span class="dot"></span>返回课程地图</a>
{{nav_links}}
        <!-- learning-kit:nav:end -->
      </nav>
      <div class="side-note">{{side_note}}</div>
    </aside>
    <main>
      <div class="hero">
        <div>
          <div class="kicker">{{kicker}}</div>
          <h1>{{title}}</h1>
          <p>{{summary}}</p>
          <div class="course-links">
{{course_links}}
          </div>
        </div>
        <div class="box soft">
          <h3>读完本页应该能做什么</h3>
          <ul>
{{can_do}}
          </ul>
        </div>
      </div>
{{content}}
      <section id="export">
        <div class="head">
          <h2>导出练习记录</h2>
          <span class="tag">markdown</span>
        </div>
        <div id="quality" class="quality"></div>
        <div id="record" class="export">还没有生成练习记录。</div>
        <div class="actions">
          <button class="action" onclick="generateRecord()">生成记录</button>
          <button class="ghost" onclick="copyRecord()">复制 Markdown</button>
        </div>
      </section>
      <section id="sources">
        <div class="head">
          <h2>参考资料</h2>
          <span class="tag">source</span>
        </div>
        <ul class="source-list">
{{sources}}
        </ul>
      </section>
    </main>
  </div>
  <script src="../assets/vendor/katex/katex.min.js"></script>
  <script src="../assets/vendor/katex/auto-render.min.js"></script>
  <script src="../assets/vendor/prism/prism-core.min.js"></script>
  <script src="../assets/vendor/prism/prism-clike.min.js"></script>
  <script src="../assets/vendor/prism/prism-python.min.js"></script>
  <script src="../assets/vendor/prism/prism-bash.min.js"></script>
  <script src="../assets/vendor/prism/prism-json.min.js"></script>
  <script src="../assets/vendor/prism/prism-line-numbers.min.js"></script>
  <script src="../assets/study-page.js"></script>
</body>
</html>
"""

# ==================== 基础 Markdown 转换器 ====================

def md_inline_to_html(text):
    """转换行内 Markdown 到 HTML。"""
    # 粗体
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    # 斜体
    text = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', text)
    # 行内代码
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # 链接
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    return text


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
                    trs += f'<tr>{tds}</tr>'
                result.append(f'<table class="metric-table">\n<tr>{th}</tr>\n{trs}\n</table>')
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
        """简单 YAML 解析器（只处理本规范用到的字段）。"""
        data = {}
        current_key = None
        current_list = None
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # 列表项
            if stripped.startswith('- '):
                if current_list is not None:
                    current_list.append(stripped[2:].strip().strip('"\''))
                continue

            # 键值对
            m = re.match(r'^(\w+):\s*(.*)$', stripped)
            if m:
                key, val = m.group(1), m.group(2).strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                if val:
                    data[key] = val
                    current_key = key
                    current_list = None
                else:
                    # 空值，可能是列表开始
                    current_key = key
                    current_list = []
                    data[key] = current_list
            else:
                # 可能是多行字符串的延续
                pass
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
                    box_lines.append(lines[i])
                    i += 1
                items.append({'type': 'box', 'variant': variant, 'content': box_lines})
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
                    qm = re.match(r'^###\s+(\S+)\s+(\w+)\s*$', q_line)
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
        while i < len(lines):
            line = lines[i].strip()

            # 选项
            if line.startswith('- [ ]') or line.startswith('- [x]'):
                q['options'].append(line[5:].strip())
                i += 1
                continue

            # Answer
            if line.startswith('Answer:'):
                q['answer'] = line[7:].strip()
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

def generate_html(parser):
    """根据解析结果生成完整 HTML。"""
    fm = parser.frontmatter

    # 构建导航链接
    nav_links = []
    for sec in parser.sections:
        if sec['id'] and sec['id'] not in ('export', 'sources'):
            sid = sec['id']
            stitle = sec['title']
            nav_links.append(f'        <a href="#{sid}"><span class="dot"></span>{stitle}</a>')

    # 构建 course links
    course_links = []
    raw_links = fm.get('course_links', '')
    if isinstance(raw_links, str):
        # 简单解析：text: href 格式
        for m in re.finditer(r'-?\s*text:\s*"([^"]+)"\s*href:\s*"([^"]+)"', raw_links):
            course_links.append(f'            <a href="{m.group(2)}">{m.group(1)}</a>')

    # 构建 can_do
    can_do = []
    raw_can = fm.get('can_do', '')
    if isinstance(raw_can, str):
        for m in re.finditer(r'-\s+(.+)', raw_can):
            can_do.append(f'            <li>{m.group(1)}</li>')
    elif isinstance(raw_can, list):
        for item in raw_can:
            can_do.append(f'            <li>{item}</li>')

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
    for item in sec['items']:
        if item['type'] == 'box':
            variant = item['variant']
            cls = f'box {variant}' if variant else 'box'
            content = md_block_to_html(item['content'])
            items_html.append(f'        <div class="{cls}">\n{content}\n        </div>')

        elif item['type'] == 'code':
            attrs = item.get('attrs', {})
            code_id = attrs.get('id', f'code-{sec["id"]}')
            label = attrs.get('label', '代码')
            lang = item['lang']
            code = item['code']
            escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            items_html.append(f'''        <div class="codebar"><span>{label}</span><button class="copy" data-copy="{code_id}">复制</button></div>
        <pre id="{code_id}" data-export-context="{label}" data-export-lang="{lang}"><code class="language-{lang}">{escaped}</code></pre>''')

        elif item['type'] == 'table':
            rows = item['rows']
            if len(rows) < 2:
                continue
            # 解析表头
            header = [c.strip() for c in rows[0].split('|')[1:-1]]
            # 跳过分隔行
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
            items_html.append(f'        <table class="metric-table">\n          <tr>{th}</tr>\n{trs}\n        </table>')

        elif item['type'] == 'text':
            content = md_block_to_html(item['lines'])
            items_html.append(content)

        elif item['type'] == 'formula':
            items_html.append(f'        <div class="formula" data-export-context="公式" data-export-lang="math">\n{item["content"]}\n        </div>')

        elif item['type'] == 'practice-intro':
            intro_items = []
            for intro in item['items']:
                if intro['type'] == 'box':
                    variant = intro['variant']
                    cls = f'box {variant}' if variant else 'box'
                    content = md_block_to_html(intro['content'])
                    intro_items.append(f'      <div class="{cls}">\n{content}\n      </div>')
            items_html.append(f'      <div class="practice-intro">\n' + '\n'.join(intro_items) + '\n      </div>')

        elif item['type'] == 'practice-group':
            questions_html = []
            for q in item['questions']:
                questions_html.append(render_question(q))

            quick = f'<div class="quick-review">{item["quick_review"]}</div>' if item['quick_review'] else ''
            items_html.append(f'''      <div class="practice-group">
        <div class="group-head">
          <div><h3>{item["name"]}</h3></div>
          {quick}
        </div>
        <div class="drill-grid">
{'\n'.join(questions_html)}
        </div>
      </div>''')

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

    # 构建选项
    options_html = ''
    if q['options']:
        opts = '\n'.join(f'      <label><input type="radio" name="q{q["num"]}" value="{opt}">{opt}</label>' for opt in q['options'])
        options_html = f'\n      <div class="choices">\n{opts}\n      </div>'

    # 构建输入框
    input_html = ''
    if q['type'] in ('fill', 'short-answer', 'ordering', 'matching', 'synthesis', 'diagnosis', 'scenario', 'checklist', 'code-reading'):
        input_html = '\n      <textarea name="q{}"></textarea>'.format(q['num'])
    elif q['type'] == 'fill':
        input_html = f'\n      <input type="text" name="q{q["num"]}" data-answer="{q["answer"]}" placeholder="输入答案">'

    # 构建反馈
    feedback_content = q['answer']
    if q['explain']:
        feedback_content += f'。{q["explain"]}'
    if q['details']:
        feedback_content += f'\n{q["details"]}'

    # 题目编号和类型
    num_clean = re.sub(r'[^\w]', '', q['num'])

    return f'''      <article class="q" data-question="q{num_clean}" data-group="{q.get("group", "")}" data-title="{q.get("title", "")}" data-answer="{q["answer"]}">
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
                html = generate_html(study)
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
        html = generate_html(study)
        Path(output).write_text(html, encoding='utf-8')
        print(f'已生成: {output}')


if __name__ == '__main__':
    main()
