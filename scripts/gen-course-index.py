#!/usr/bin/env python3
"""
生成课程索引页 (v2 风格)
支持两种目录结构：
  - 一层：子目录直接有学习页 → 链接到 学习页.html
  - 两层：子目录有 index.html（子课程地图）→ 链接到 index.html
  - 混合：两者可能共存
"""
import os, re, json
from pathlib import Path

COURSE_META = {
    "PyTorch深度学习实践 刘二大人": {
        "title": "PyTorch 深度学习实践",
        "kicker": "刘二大人课程精读",
        "desc": "从线性模型到 RNN 的 PyTorch 入门实践。13 个单元覆盖深度学习基础、反向传播、CNN 和 RNN。",
        "badge": "PYTORCH"
    },
    "大语言模型": {
        "title": "大语言模型",
        "kicker": "LLM 全栈",
        "desc": "LLM 应用工程、RAG、MCP、LoRA、训练和后训练。从调用 API 到理解模型能力来源。",
        "badge": "LLM"
    },
    "计算机教育中缺失的一课": {
        "title": "工程基本功",
        "kicker": "MIT Missing Semester",
        "desc": "命令行、Git、调试、安全、构建和自动化。开发者日常工作的底座技能。",
        "badge": "BASIC"
    },
    "李宏毅  机器学习": {
        "title": "机器学习长线课",
        "kicker": "李宏毅",
        "desc": "系统补机器学习、深度学习、生成模型、强化学习和神经网络压缩。58 讲完整课程。",
        "badge": "ML"
    },
    "算法": {
        "title": "算法",
        "kicker": "面试地图",
        "desc": "数组链表、树堆图、回溯、动态规划和面试题型。",
        "badge": "ALGO"
    },
    "深度学习": {
        "title": "深度学习",
        "kicker": "模型基础",
        "desc": "PyTorch、Transformer、训练闭环、RAG 和 Agent 最小流程。",
        "badge": "DL"
    },
    "Agent": {
        "title": "Agent",
        "kicker": "系统设计",
        "desc": "Agent 基础、Context Engineering、Harness、工具契约、可靠性工程和多智能体系统。",
        "badge": "AGENT"
    },
    "AI基础设施": {
        "title": "AI 基础设施",
        "kicker": "Infra",
        "desc": "GPU 性能工程、推理引擎、Serving 架构、分布式训练系统。",
        "badge": "INFRA"
    }
}

HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN" data-page-shell="course-index-v2">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}} — AI Study Lab</title>
  <link rel="stylesheet" href="{{assets_path}}site-v2.css">
</head>
<body>

  <!-- Top Navigation -->
  <nav class="top-nav">
    <div class="top-nav-inner">
      <div class="top-nav-left">
        <a href="{{root_path}}index.html" class="brand-name">AI Study Lab</a>
        <span class="sep">/</span>
        <a href="{{root_path}}index.html">学习地图</a>
        <span class="sep">/</span>
        <span>{{title}}</span>
      </div>
      <div class="top-nav-right">
        <a href="{{root_path}}search.html" class="nav-pill">🔍 搜索</a>
      </div>
    </div>
  </nav>

  <!-- Course Hero -->
  <header class="course-hero">
    <div class="course-hero-inner">
      <div class="course-badge">{{badge}}</div>
      <h1 class="hero-title">{{title}}</h1>
      <p class="hero-desc">{{desc}}</p>
    </div>
  </header>

  <!-- Unit List -->
  <main class="content">
{{sections}}
  </main>

  <footer class="site-footer">
    <div class="site-footer-inner">
      <span><a href="{{root_path}}index.html" style="color: var(--text-muted); text-decoration: none;">← 返回学习地图</a></span>
      <span>AI Study Lab</span>
    </div>
  </footer>

</body>
</html>
"""

# 一层结构：直接列出单元（链接到 学习页.html）
UNIT_SECTION_TEMPLATE = """    <section class="section">
      <div class="section-head">
        <h2>{{section_title}}</h2>
        <span class="section-tag">{{badge}} · {{count}}</span>
      </div>
      <div class="unit-list">
{{units}}
      </div>
    </section>
"""

UNIT_ITEM_TEMPLATE = """        <a class="unit-item" href="{{unit_dir}}/学习页.html">
          <div class="unit-num">{{num}}</div>
          <div class="unit-title">{{unit_name}}</div>
          <div class="unit-arrow">→</div>
        </a>"""

# 两层结构：子课程卡片（链接到 index.html）
SUBCOURSE_SECTION_TEMPLATE = """    <section class="section">
      <div class="section-head">
        <h2>{{section_title}}</h2>
        <span class="section-tag">{{badge}} · {{count}}</span>
      </div>
      <div class="card-grid">
{{cards}}
      </div>
    </section>
"""

SUBCOURSE_CARD_TEMPLATE = """        <a class="card" href="{{sub_dir}}/index.html">
          <div class="card-title">{{sub_name}}</div>
          <div class="card-desc">{{sub_desc}}</div>
        </a>"""


def extract_name(dir_name):
    """从目录名提取显示名称。去掉数字前缀。"""
    s = re.sub(r'^[A-Z]?\d+[_\-]', '', dir_name)
    return s


def collect_entries(study_dir):
    """扫描研习资料目录，区分子课程和单元。"""
    subcourses = []   # 有 index.html 的目录
    units = []        # 直接有学习页（没有 index.html）的目录
    
    for entry in sorted(study_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith('_') or entry.name.startswith('.'):
            continue
        if entry.name in ('sources', '__pycache__'):
            continue
        
        has_index = (entry / "index.html").exists()
        has_page = (entry / "学习页.html").exists() or (entry / "学习页.md").exists()
        
        if has_index:
            # 优先当作子课程
            subcourses.append(entry.name)
        elif has_page:
            # 当作直接单元
            units.append(entry.name)
        else:
            # 两者都没有：检查是否还有子目录（可能是更深层）
            sub_dirs = [d.name for d in entry.iterdir() if d.is_dir() and not d.name.startswith(('_', '.'))]
            if sub_dirs:
                # 有子目录，可能是子课程（即使没 index.html）
                subcourses.append(entry.name)
            else:
                # 纯目录，也列出来
                units.append(entry.name)
    
    return subcourses, units


def generate_course_index(course_dir, course_key):
    """为单个课程生成 index.html。"""
    meta = COURSE_META.get(course_key, {
        "title": course_key, "kicker": "", "desc": "", "badge": "COURSE"
    })
    
    study_dir = Path(course_dir) / "研习资料"
    if not study_dir.exists():
        print(f"  跳过 (不存在研习资料): {course_key}")
        return 0
    
    subcourses, units = collect_entries(study_dir)
    
    sections_html = []
    
    # 子课程区块（两层结构）
    if subcourses:
        cards_html = []
        for sub_name in subcourses:
            display_name = extract_name(sub_name)
            sub_dir = sub_name.replace(' ', '%20')
            # 尝试从子课程目录的 index.html 提取描述
            sub_desc = "进入子课程"
            sub_index = study_dir / sub_name / "index.html"
            if sub_index.exists():
                try:
                    content = sub_index.read_text(encoding='utf-8')
                    # 简单提取描述：找第一个段落
                    m = re.search(r'<p[^>]*>([^<]+)</p>', content)
                    if m:
                        sub_desc = m.group(1).strip()[:80]
                except:
                    pass
            
            card = SUBCOURSE_CARD_TEMPLATE.replace("{{sub_dir}}", sub_dir)\
                                           .replace("{{sub_name}}", display_name)\
                                           .replace("{{sub_desc}}", sub_desc)
            cards_html.append(card)
        
        section = SUBCOURSE_SECTION_TEMPLATE.replace("{{section_title}}", "子课程")\
                                             .replace("{{badge}}", meta["badge"])\
                                             .replace("{{count}}", f"{len(subcourses)} 门")\
                                             .replace("{{cards}}", "\n".join(cards_html))
        sections_html.append(section)
    
    # 单元区块（一层结构）
    if units:
        units_html = []
        for i, unit_dir in enumerate(units, 1):
            unit_name = extract_name(unit_dir)
            unit_dir_escaped = unit_dir.replace(' ', '%20')
            item = UNIT_ITEM_TEMPLATE.replace("{{num}}", f"{i:02d}")\
                                     .replace("{{unit_name}}", unit_name)\
                                     .replace("{{unit_dir}}", unit_dir_escaped)
            units_html.append(item)
        
        section = UNIT_SECTION_TEMPLATE.replace("{{section_title}}", "单元列表")\
                                         .replace("{{badge}}", meta["badge"])\
                                         .replace("{{count}}", f"{len(units)} 单元")\
                                         .replace("{{units}}", "\n".join(units_html))
        sections_html.append(section)
    
    # 确定路径
    assets_path = "../../assets/"
    root_path = "../../"
    
    html = HTML_TEMPLATE.replace("{{title}}", meta["title"])\
                        .replace("{{desc}}", meta["desc"])\
                        .replace("{{badge}}", meta["badge"])\
                        .replace("{{sections}}", "\n".join(sections_html))\
                        .replace("{{assets_path}}", assets_path)\
                        .replace("{{root_path}}", root_path)
    
    output = Path(course_dir) / "研习资料" / "index.html"
    output.write_text(html, encoding='utf-8')
    print(f"  生成: {output} (子课程={len(subcourses)}, 单元={len(units)})")
    return len(subcourses) + len(units)


def main():
    repo_root = Path("D:/Users/yyh/Downloads/ai-study-lab")
    
    for course_key in COURSE_META:
        course_dir = repo_root / course_key
        if not course_dir.exists():
            print(f"  跳过 (不存在): {course_key}")
            continue
        count = generate_course_index(course_dir, course_key)
        print(f"  {course_key}: 共 {count} 个条目")

if __name__ == '__main__':
    main()
