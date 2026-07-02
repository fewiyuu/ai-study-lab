#!/usr/bin/env python3
"""
重写所有子课程目录下的 index.html 为 v2 风格。
子课程目录 = 课程/研习资料/下的子目录，包含 index.html 和子单元。
"""
import re
from pathlib import Path

SUBCOURSE_TEMPLATE = """<!doctype html>
<html lang="zh-CN" data-page-shell="subcourse-index-v2">
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
        <a href="{{course_path}}index.html">{{course_name}}</a>
        <span class="sep">/</span>
        <span>{{title}}</span>
      </div>
      <div class="top-nav-right">
        <a href="{{root_path}}search.html" class="nav-pill">🔍 搜索</a>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <header class="hero">
    <div class="hero-inner">
      <div class="hero-kicker">{{course_name}}</div>
      <h1 class="hero-title">{{title}}</h1>
      <p class="hero-desc">{{desc}}</p>
    </div>
  </header>

  <!-- Unit List -->
  <main class="content">
    <section class="section">
      <div class="section-head">
        <h2>单元列表</h2>
        <span class="section-tag">{{count}} 单元</span>
      </div>
      <div class="unit-list">
{{units}}
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="site-footer-inner">
      <span><a href="{{course_path}}index.html" style="color: var(--text-muted); text-decoration: none;">← 返回 {{course_name}}</a></span>
      <span>AI Study Lab</span>
    </div>
  </footer>

</body>
</html>
"""

UNIT_ITEM_TEMPLATE = """        <a class="unit-item" href="{{unit_dir}}/学习页.html">
          <div class="unit-num">{{num}}</div>
          <div class="unit-title">{{unit_name}}</div>
          <div class="unit-arrow">→</div>
        </a>"""


def extract_name(dir_name):
    """去掉数字前缀。"""
    return re.sub(r'^[A-Z]?\d+[_\-]', '', dir_name)


def rewrite_subcourse_index(subcourse_dir, course_name, root_path, course_path):
    """重写单个子课程目录的 index.html。"""
    subcourse_name = subcourse_dir.name
    title = extract_name(subcourse_name)
    
    # 收集子单元
    units = []
    for entry in sorted(subcourse_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith(('_', '.')):
            continue
        has_page = (entry / "学习页.html").exists() or (entry / "学习页.md").exists()
        if has_page:
            units.append(entry.name)
    
    if not units:
        return False
    
    # 构建单元 HTML
    units_html = []
    for i, unit_dir in enumerate(units, 1):
        unit_name = extract_name(unit_dir)
        unit_dir_esc = unit_dir.replace(' ', '%20')
        item = UNIT_ITEM_TEMPLATE.replace("{{num}}", f"{i:02d}")\
                                   .replace("{{unit_name}}", unit_name)\
                                   .replace("{{unit_dir}}", unit_dir_esc)
        units_html.append(item)
    
    # 尝试从旧的 index.html 提取描述
    desc = ""
    old_index = subcourse_dir / "index.html"
    if old_index.exists():
        try:
            content = old_index.read_text(encoding='utf-8')
            # 提取 description meta
            m = re.search(r'<meta name="description" content="([^"]+)"', content)
            if m:
                desc = m.group(1)
        except:
            pass
    if not desc:
        desc = f"{title} 的 {len(units)} 个单元学习页。"
    
    # 计算 assets_path (从子课程目录到 assets/)
    # 子课程目录在 课程/研习资料/子课程/
    # 到 assets/ 是 ../../../assets/
    assets_path = "../../../assets/"
    
    html = SUBCOURSE_TEMPLATE.replace("{{title}}", title)\
                             .replace("{{course_name}}", course_name)\
                             .replace("{{desc}}", desc)\
                             .replace("{{count}}", str(len(units)))\
                             .replace("{{units}}", "\n".join(units_html))\
                             .replace("{{assets_path}}", assets_path)\
                             .replace("{{root_path}}", root_path)\
                             .replace("{{course_path}}", course_path)
    
    old_index.write_text(html, encoding='utf-8')
    return True


def main():
    repo_root = Path("D:/Users/yyh/Downloads/ai-study-lab")
    
    # 课程到显示名称的映射
    course_names = {
        "大语言模型": "大语言模型",
        "Agent": "Agent",
        "AI基础设施": "AI 基础设施",
        "深度学习": "深度学习",
        "算法": "算法",
    }
    
    total = 0
    for course_key, course_name in course_names.items():
        study_dir = repo_root / course_key / "研习资料"
        if not study_dir.exists():
            continue
        
        for entry in sorted(study_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith(('_', '.')):
                continue
            if entry.name in ('sources', '__pycache__'):
                continue
            
            has_index = (entry / "index.html").exists()
            has_units = any(
                (d / "学习页.html").exists() or (d / "学习页.md").exists()
                for d in entry.iterdir() if d.is_dir()
            )
            
            if has_index and has_units:
                # root_path: 从 课程/研习资料/子课程/ 到根 = ../../../
                # course_path: 从 课程/研习资料/子课程/ 到 课程/研习资料/ = ../
                ok = rewrite_subcourse_index(entry, course_name, "../../../", "../")
                if ok:
                    total += 1
                    print(f"  重写: {entry}")
    
    print(f"\n共重写 {total} 个子课程索引页")

if __name__ == '__main__':
    main()
