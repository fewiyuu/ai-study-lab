#!/usr/bin/env python3
"""
生成全站搜索索引 JSON。

用法:
    python scripts/build-search-index.py

从 catalog.json.pages 读取公开页面列表，生成 assets/search-index.json。
与 build_catalog.py 共用同一白名单，确保搜索索引和公开目录一致。
"""

import json
import re
from pathlib import Path


def extract_meta(html_path):
    """从 HTML 文件中提取标题、课程名、摘要。"""
    text = html_path.read_text(encoding='utf-8')
    
    # 提取 <title>
    title_m = re.search(r'<title>(.+?)</title>', text)
    title = title_m.group(1) if title_m else html_path.parent.name
    
    # 提取 body 中的可见文本作为摘要
    body_m = re.search(r'<main>(.*?)</main>', text, re.DOTALL)
    excerpt = ''
    if body_m:
        body = body_m.group(1)
        clean = re.sub(r'<[^>]+>', ' ', body)
        clean = re.sub(r'\s+', ' ', clean).strip()
        excerpt = clean[:200]
    
    # 提取课程名
    course_m = re.search(r'data-course="([^"]+)"', text)
    course = course_m.group(1) if course_m else ''
    
    return {
        'title': title,
        'course': course,
        'excerpt': excerpt
    }


def main():
    repo_root = Path(__file__).resolve().parent.parent
    
    # 读取 catalog.json（公开目录白名单）
    catalog_path = repo_root / 'catalog.json'
    if not catalog_path.exists():
        print('ERROR: catalog.json not found. Run build_catalog.py first.')
        return
    
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    pages = catalog.get('pages', [])
    
    if not pages:
        print('ERROR: catalog.json has no pages. Run build_catalog.py first.')
        return
    
    entries = []
    for page in pages:
        rel_path = page.get('path', '')
        html_path = repo_root / rel_path
        if not html_path.exists():
            print(f'  SKIP (not found): {rel_path}')
            continue
        
        try:
            meta = extract_meta(html_path)
            entry = {
                'title': meta['title'],
                'course': meta['course'],
                'path': rel_path,
                'excerpt': meta['excerpt']
            }
            entries.append(entry)
            print(f'  Indexed: {rel_path}')
        except Exception as e:
            print(f'  SKIP {rel_path}: {e}')
    
    # 按课程名排序
    entries.sort(key=lambda e: (e['course'], e['title']))
    
    # 写入 JSON
    output = repo_root / 'assets' / 'search-index.json'
    output.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nDone: {len(entries)} pages indexed -> {output}')
    print(f'catalog.json has {len(pages)} pages, search index has {len(entries)} entries')


if __name__ == '__main__':
    main()
