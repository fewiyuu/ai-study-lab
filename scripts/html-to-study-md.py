#!/usr/bin/env python3
"""
学习页 HTML → Markdown 反向转换器。

将 md-to-study-page.py 生成的 学习页.html 转换回标准 Markdown，
遵循 learning-kit 的 study-page-markdown-spec.md 规范。

用法:
    python scripts/html-to-study-md.py 输入.html 输出.md
    python scripts/html-to-study-md.py --batch 目录/       # 批量转换
    python scripts/html-to-study-md.py --batch --overwrite 目录/
"""

import sys, re, os, argparse, json
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag


# ── helpers ──

def unwrap_inline(tag):
    """递归提取标签内的纯文本和内联标记（粗体、斜体、代码、链接、公式）。"""
    parts = []
    for child in tag.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            name = child.name
            text = unwrap_inline(child)
            if name in ('b', 'strong'):
                parts.append(f'**{text}**')
            elif name in ('i', 'em'):
                parts.append(f'*{text}*')
            elif name == 'code':
                parts.append(f'`{text}`')
            elif name == 'a':
                href = child.get('href', '')
                parts.append(f'[{text}]({href})')
            elif name == 'span' and 'math-inline' in child.get('class', []):
                parts.append(f'${text}$')
            elif name == 'br':
                parts.append('\n')
            else:
                parts.append(text)
    return ''.join(parts)


def extract_text(tag):
    """提取标签内纯文本（无标记）。"""
    return tag.get_text(' ', strip=True)


def class_has(tag, *names):
    """检查标签是否有某个 CSS 类。"""
    cls = tag.get('class', [])
    return any(n in cls for n in names)


# ── main converter ──

def html_to_md(html_text):
    """将学习页 HTML 转换为 Markdown 字符串。"""
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # ── 1. 提取 frontmatter ──
    fm = {}
    
    # title
    title_tag = soup.find('title')
    fm['title'] = title_tag.text.strip() if title_tag else ''
    
    # course, unit from body
    body = soup.find('body')
    fm['course'] = body.get('data-course', '') if body else ''
    fm['unit'] = body.get('data-unit', '') if body else ''
    
    # kicker
    kicker_tag = soup.select_one('.hero .kicker')
    if kicker_tag:
        kicker_text = extract_text(kicker_tag)
        # split at · for kicker_en
        if ' · ' in kicker_text:
            parts = kicker_text.split(' · ', 1)
            fm['kicker'] = parts[0].strip()
            fm['kicker_en'] = parts[1].strip()
        else:
            fm['kicker'] = kicker_text
            fm['kicker_en'] = ''
    
    # summary
    summary_tag = soup.select_one('.hero > div > p')
    fm['summary'] = extract_text(summary_tag) if summary_tag else ''
    
    # side_note
    side_note_tag = soup.select_one('aside .side-note')
    fm['side_note'] = extract_text(side_note_tag) if side_note_tag else ''
    
    # can_do
    can_do = []
    can_do_ul = soup.select_one('.hero .box.soft ul')
    if can_do_ul:
        for li in can_do_ul.find_all('li'):
            can_do.append(extract_text(li))
    fm['can_do'] = can_do
    
    # course_links
    course_links = []
    links_div = soup.select_one('.hero .course-links')
    if links_div:
        for a in links_div.find_all('a'):
            course_links.append({
                'text': extract_text(a),
                'href': a.get('href', '')
            })
    fm['course_links'] = course_links
    
    # ── 2. 构建 frontmatter YAML ──
    md = '---\n'
    md += f'course: "{fm["course"]}"\n'
    md += f'unit: "{fm["unit"]}"\n'
    md += f'title: "{fm["title"]}"\n'
    md += f'kicker: "{fm.get("kicker", "")}"\n'
    if fm.get('kicker_en'):
        md += f'kicker_en: "{fm["kicker_en"]}"\n'
    md += f'summary: "{fm["summary"]}"\n'
    md += '\n'
    md += f'side_note: "{fm["side_note"]}"\n'
    md += '\n'
    if fm['can_do']:
        md += 'can_do:\n'
        for item in fm['can_do']:
            md += f'  - "{item}"\n'
        md += '\n'
    if fm['course_links']:
        md += 'course_links:\n'
        for link in fm['course_links']:
            md += f'  - text: "{link["text"]}"\n'
            md += f'    href: "{link["href"]}"\n'
        md += '\n'
    md += '---\n\n'
    
    # ── 3. 处理 main 中的 sections ──
    main = soup.find('main')
    if not main:
        return md + '(no main content found)\n'
    
    sections_processed = set()
    
    for child in main.children:
        if not isinstance(child, Tag):
            continue
        
        if child.name == 'section':
            sec_id = child.get('id', '')
            if sec_id in ('export',):
                continue
            md += render_section(child)
            sections_processed.add(sec_id)
    
    # ── 4. 处理 sources section（可能在末尾） ──
    sources_section = soup.find('section', id='sources')
    if sources_section:
        md += render_sources(sources_section)
    
    return md


def render_section(section):
    """渲染一个 <section> 为 Markdown。"""
    sec_id = section.get('id', '')
    
    # 提取 head 区域的标题和 tag
    head = section.find('div', class_='head')
    title = ''
    tag = ''
    layout = ''
    
    if head:
        h2 = head.find('h2')
        if h2:
            title = extract_text(h2)
        tag_span = head.find('span', class_='tag')
        if tag_span:
            tag = extract_text(tag_span)
    
    # 检查是否有 grid2/grid 布局 wrapper
    grid_div = section.find('div', class_=lambda c: c and ('grid2' in c or 'grid' in c))
    # Actually, layout is set via a wrapper div with class grid2/grid that wraps content
    # The template uses: <div class="grid2"> content... </div>
    # Let's check for direct children that are layout wrappers
    
    # Build markdown
    md = ''
    if sec_id == 'sources':
        return md  # handled separately
    
    # Skip sections with empty titles (broken hand-written HTML)
    if not title:
        return md
    
    md += f'# {title} {{#{sec_id}}}\n'
    if tag:
        md += f'<!-- tag: {tag} -->\n'
    
    # Check if first non-head child is a grid wrapper
    first_content = None
    for c in section.children:
        if isinstance(c, Tag) and not (c.name == 'div' and class_has(c, 'head')):
            first_content = c
            break
    
    if first_content and isinstance(first_content, Tag):
        if class_has(first_content, 'grid2'):
            layout = 'grid2'
        elif class_has(first_content, 'grid'):
            layout = 'grid'
    
    if layout:
        md += f'<!-- layout: {layout} -->\n'
    md += '\n'
    
    # Process all children: grid/grid2 wrappers contain some items,
    # but remaining siblings (h3, p, callout, table, etc.) also need processing.
    for c in section.children:
        if isinstance(c, Tag):
            if c.name == "div" and class_has(c, "head"):
                continue
            if c.name == "div" and (class_has(c, "grid2") or class_has(c, "grid")):
                for cc in c.children:
                    if isinstance(cc, Tag):
                        md += render_element(cc, "")
                continue
            md += render_element(c, "")
    
    md += '\n---\n\n'
    return md


def render_element(el, indent=''):
    """渲染单个 HTML 元素为 Markdown。"""
    md = ''
    
    # Box 元素
    if el.name == 'div' and 'box' in el.get('class', []):
        variant = ''
        if class_has(el, 'soft'):
            variant = ' soft'
        elif class_has(el, 'info'):
            variant = ' info'
        elif class_has(el, 'warn'):
            variant = ' warn'
        elif class_has(el, 'redsoft'):
            variant = ' redsoft'
        
        md += f'## box{variant}\n'
        # Process children: h3 → ###, then content
        for child in el.children:
            if isinstance(child, NavigableString):
                text = str(child).strip()
                if text:
                    md += text + '\n'
            elif isinstance(child, Tag):
                if child.name == 'h3':
                    md += f'### {unwrap_inline(child)}\n'
                elif child.name == 'p':
                    md += inline_to_md(child.children) + '\n'
                elif child.name in ('ul', 'ol'):
                    md += render_list(child)
                elif child.name == 'pre':
                    md += render_code(child)
                else:
                    text = unwrap_inline(child).strip()
                    if text:
                        md += text + '\n'
        md += '\n'
        return md
    
    # Callout
    if el.name == 'div' and 'callout' in el.get('class', []):
        callout_type = 'NOTE'  # default for generic callouts
        for t in ['note', 'tip', 'warning', 'danger', 'info']:
            if class_has(el, t):
                callout_type = t.upper()
                break
        
        title_div = el.find('div', class_='callout-title')
        title_text = extract_text(title_div) if title_div else ''
        
        # For generic callouts: use <strong> as title if present
        if not title_text:
            strong_tag = el.find('strong')
            if strong_tag:
                title_text = extract_text(strong_tag)
        
        md += f'> [!{callout_type}]'
        if title_text:
            md += f' {title_text}'
        md += '\n'
        
        body_extracted = False  # avoid double-processing after strong extraction
        for child in el.children:
            if isinstance(child, Tag) and class_has(child, 'callout-title'):
                continue
            if isinstance(child, Tag) and child.name in ('strong', 'b'):
                if title_text and extract_text(child) == title_text:
                    rest = el.get_text().strip()
                    if rest.startswith(title_text):
                        rest = rest[len(title_text):].strip()
                    if rest:
                        md += f'> {rest}\n'
                    body_extracted = True
                else:
                    md += f'> **{unwrap_inline(child)}**\n'
            elif isinstance(child, Tag) and child.name == 'p':
                text = unwrap_inline(child)
                if text:
                    md += f'> {text}\n'
            elif isinstance(child, NavigableString):
                if not body_extracted:
                    text = str(child).strip()
                    if text and (not title_text or not text.strip().startswith(title_text)):
                        md += f'> {text}\n'
            elif isinstance(child, Tag):
                text = unwrap_inline(child).strip()
                if text:
                    md += f'> {text}\n'
        md += '\n'
        return md
    
    # Practice intro
    if el.name == 'div' and class_has(el, 'practice-intro'):
        md += '<!-- practice-intro -->\n'
        for child in el.children:
            if isinstance(child, Tag) and 'box' in child.get('class', []):
                variant = ''
                if class_has(child, 'soft'): variant = ' soft'
                elif class_has(child, 'info'): variant = ' info'
                elif class_has(child, 'warn'): variant = ' warn'
                md += f'## box{variant}\n'
                for cc in child.children:
                    if isinstance(cc, Tag):
                        if cc.name == 'h3':
                            md += f'### {unwrap_inline(cc)}\n'
                        elif cc.name == 'p':
                            md += inline_to_md(cc.children) + '\n'
                        elif cc.name in ('ul', 'ol'):
                            md += render_list(cc)
                        else:
                            text = unwrap_inline(cc).strip()
                            if text:
                                md += text + '\n'
                md += '\n'
        md += '<!-- end-practice-intro -->\n\n'
        return md
    
    # Practice group
    if el.name == 'div' and class_has(el, 'practice-group'):
        group_head = el.find('div', class_='group-head')
        group_name = ''
        quick_review = ''
        if group_head:
            h3 = group_head.find('h3')
            if h3:
                group_name = extract_text(h3)
            qr = group_head.find('div', class_='quick-review')
            if qr:
                quick_review = extract_text(qr)
        
        md += f'<!-- practice-group: {group_name} -->\n'
        if quick_review:
            md += f'<!-- quick-review: {quick_review} -->\n'
        md += '\n'
        
        # Find questions in drill-grid
        drill = el.find('div', class_='drill-grid')
        if drill:
            for q_el in drill.find_all(['article', 'div'], class_='q'):
                md += render_question(q_el)
        
        md += '<!-- end-practice-group -->\n\n'
        return md
    
    # Headings
    if el.name == 'h2':
        md += f'## {unwrap_inline(el)}\n\n'
        return md
    if el.name == 'h3':
        if el.parent and el.parent.name == 'div' and 'box' in el.parent.get('class', []):
            return md  # handled by box rendering
        md += f'### {unwrap_inline(el)}\n\n'
        return md
    if el.name == 'h4':
        md += f'#### {unwrap_inline(el)}\n\n'
        return md
    
    # Paragraph
    if el.name == 'p':
        text = inline_to_md(el.children)
        if text.strip():
            md += text + '\n\n'
        return md
    
    # Lists
    if el.name in ('ul', 'ol'):
        md += render_list(el) + '\n'
        return md
    
    # Code block (pre > code)
    if el.name == 'pre':
        md += render_code(el)
        return md
    
    # Formula
    if el.name == 'div' and class_has(el, 'formula'):
        text = el.get_text().strip()
        # remove $$ wrappers if present
        if text.startswith('$$'):
            text = text[2:]
        if text.endswith('$$'):
            text = text[:-2]
        md += f'$$\n{text.strip()}\n$$\n\n'
        return md
    
    # Table
    if el.name == 'table':
        md += render_table(el) + '\n'
        return md
    
    # Inline note
    if el.name == 'div' and class_has(el, 'inline-note'):
        b = el.find('b')
        if b:
            md += f'> **{extract_text(b)}**'
            rest = el.get_text().replace(extract_text(b), '', 1).strip()
            if rest:
                md += f' {rest}'
            md += '\n\n'
        return md
    
    # Shape tracer, token demo, terminal lab etc. → skip (complex interactive, keep as HTML comment)
    if el.name == 'div' and any(class_has(el, c) for c in ['shape-tracer', 'token-demo', 'terminal-lab', 'shift-demo']):
        md += f'<!-- interactive: {el.get("class", [])} → keep as HTML -->\n\n'
        return md
    
    # Generic fallback for any other element
    text = unwrap_inline(el).strip()
    if text:
        md += text + '\n\n'
    return md


def inline_to_md(children):
    """将内联子元素转换为 Markdown 行内文本。"""
    parts = []
    for child in children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            name = child.name
            text = inline_to_md(child.children)
            if name in ('b', 'strong'):
                parts.append(f'**{text}**')
            elif name in ('i', 'em'):
                parts.append(f'*{text}*')
            elif name == 'code':
                parts.append(f'`{text}`')
            elif name == 'a':
                href = child.get('href', '')
                parts.append(f'[{text}]({href})')
            elif name == 'span':
                parts.append(text)
            elif name == 'br':
                parts.append('\n')
            else:
                parts.append(text)
    return ''.join(parts).strip()


def render_list(el):
    """渲染 <ul> 或 <ol> 为 Markdown 列表。"""
    md = ''
    is_ordered = el.name == 'ol'
    for i, li in enumerate(el.find_all('li', recursive=False)):
        prefix = f'{i+1}.' if is_ordered else '-'
        text = inline_to_md(li.children)
        md += f'{prefix} {text}\n'
    return md


def render_code(pre_el):
    """渲染 <pre><code> 为 fenced code block。"""
    code = pre_el.find('code')
    if not code:
        text = pre_el.get_text()
        return f'```\n{text.strip()}\n```\n\n'
    
    lang = 'text'
    cls = code.get('class', [])
    for c in cls:
        if c.startswith('language-'):
            lang = c[9:]
    
    text = code.get_text()
    return f'```{lang}\n{text.strip()}\n```\n\n'


def render_table(table_el):
    """渲染 <table> 为 Markdown 表格。"""
    rows = table_el.find_all('tr')
    if len(rows) < 2:
        return ''
    
    # Extract header
    header_cells = rows[0].find_all(['th', 'td'])
    header = [extract_text(c) for c in header_cells]
    
    # Build markdown table
    md = '| ' + ' | '.join(header) + ' |\n'
    md += '| ' + ' | '.join(['---'] * len(header)) + ' |\n'
    
    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        cell_texts = [extract_text(c) for c in cells]
        # Pad to match header length
        while len(cell_texts) < len(header):
            cell_texts.append('')
        md += '| ' + ' | '.join(cell_texts[:len(header)]) + ' |\n'
    
    return md


def render_question(q_el):
    """渲染 .q 元素（兼容 div.q 和 article.q）为练习 Markdown。"""
    # Extract question number from data-question (e.g. "q1", "q02")
    q_num_raw = q_el.get('data-question', '?')
    q_num = q_num_raw.lstrip('q') if q_num_raw.startswith('q') else q_num_raw
    
    # Extract type: check pills OR data attributes
    meta = q_el.find('div', class_='q-meta')
    pills = meta.find_all('span', class_='pill') if meta else []
    
    q_type = 'choice'
    if pills:
        pill_texts = [extract_text(p).strip() for p in pills]
        # New format: first pill is number, second is type (e.g. ["02", "choice"])
        # Old format: first pill is type, second is sub-category (e.g. ["choice", "triage"])
        if len(pill_texts) >= 1 and pill_texts[0].isdigit():
            if len(pill_texts) >= 2:
                q_type = pill_texts[1].replace(' ', '-')
        else:
            q_type = pill_texts[0].replace(' ', '-') if pill_texts else 'choice'
    
    # Question text from h3
    h3 = q_el.find('h3')
    q_text = inline_to_md(h3.children) if h3 else ''
    if q_text.startswith('**Q:**'):
        q_text = q_text[5:].strip()
    
    # Options: check .choices wrapper first, then direct <label> children
    options = []
    choices_div = q_el.find('div', class_='choices')
    labels = choices_div.find_all('label') if choices_div else q_el.find_all('label')
    for label in labels:
        input_el = label.find('input')
        checked = input_el and input_el.get('checked') is not None
        prefix = '[x]' if checked else '[ ]'
        opt_text = extract_text(label).strip()
        if input_el and input_el.get('value'):
            val = input_el.get('value')
            # Only strip value prefix if text starts with it AND has more content after
            if opt_text.startswith(val) and len(opt_text) > len(val):
                opt_text = opt_text[len(val):].strip()
        options.append(f'- {prefix} {opt_text}')
    
    # Answer: convert single-letter (old format) to option text
    answer = q_el.get('data-answer', '')
    if len(answer) == 1 and answer.isupper() and labels:
        # Map letter to option text by matching input value attribute
        for label in labels:
            inp = label.find('input')
            if inp and inp.get('value', '').strip() == answer:
                answer = extract_text(label).strip()
                # Remove the value prefix if present
                if answer.startswith(inp.get('value', '')):
                    answer = answer[len(inp.get('value', '')):].strip()
                break
    
    # Explain: check data-explain (old) or <details> (new)
    explain = q_el.get('data-explain', '')
    if not explain:
        details = q_el.find('details')
        if details:
            p = details.find('p')
            if p:
                details_text = extract_text(p)
                if details_text and details_text != answer:
                    if '。' in details_text:
                        parts = details_text.split('。', 1)
                        if parts[0].strip() == answer.strip():
                            explain = parts[1].strip() if len(parts) > 1 else ''
                        else:
                            explain = details_text
                    else:
                        explain = details_text
    
    # Build markdown
    md = f'### {q_num} {q_type}\n\n'
    md += f'**Q:** {q_text}\n\n'
    
    if options:
        md += '\n'.join(options) + '\n\n'
    
    if answer:
        md += f'Answer: {answer}\n'
    
    if explain:
        md += f'Explain: {explain}\n'
    
    md += '\n'
    return md
def render_sources(section):
    """渲染 sources section。"""
    md = '# 参考资料 {#sources}\n'
    md += '<!-- tag: source -->\n\n'
    
    ul = section.find('ul', class_='source-list')
    if ul:
        for li in ul.find_all('li'):
            text = inline_to_md(li.children)
            md += f'- {text}\n'
    else:
        # Fallback: extract all text
        for child in section.children:
            if isinstance(child, Tag) and class_has(child, 'head'):
                continue
            if isinstance(child, Tag) and child.name == 'ul':
                for li in child.find_all('li'):
                    text = inline_to_md(li.children)
                    md += f'- {text}\n'
    
    md += '\n---\n'
    return md


# ── main ──

def main():
    parser = argparse.ArgumentParser(description='学习页 HTML → Markdown 反向转换器')
    parser.add_argument('input', nargs='?', help='输入 .html 文件或目录')
    parser.add_argument('output', nargs='?', help='输出 .md 文件（单文件模式）')
    parser.add_argument('--batch', action='store_true', help='批量转换目录下所有 学习页.html')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已有 .md')
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input)

    if args.batch or input_path.is_dir():
        # 批量模式：找所有 学习页.html
        html_files = list(input_path.rglob('学习页.html'))
        for html_file in html_files:
            md_file = html_file.with_name('学习页.md')
            if md_file.exists() and not args.overwrite:
                print(f'  SKIP {html_file} -> {md_file} (已存在)')
                continue
            try:
                text = html_file.read_text(encoding='utf-8')
                md = html_to_md(text)
                md_file.write_text(md, encoding='utf-8')
                print(f'  OK   {html_file} -> {md_file}')
            except Exception as e:
                print(f'  FAIL {html_file}: {e}')
                import traceback
                traceback.print_exc()
    else:
        # 单文件模式
        text = input_path.read_text(encoding='utf-8')
        md = html_to_md(text)
        output = args.output or input_path.with_suffix('.md')
        Path(output).write_text(md, encoding='utf-8')
        print(f'已生成: {output}')


if __name__ == '__main__':
    main()
