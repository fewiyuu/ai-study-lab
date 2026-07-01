import os, re, json
from pathlib import Path
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.in_script = False
        self.in_style = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.in_script = tag == 'script'
            self.in_style = tag == 'style'
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.in_script = False
            self.in_style = False
    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            self.texts.append(data)
    def get_text(self):
        return ' '.join(self.texts)

def extract_info(path):
    text = open(path, 'r', encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', text, re.I)
    title = m.group(1).strip() if m else path.name
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', text, re.I)
    desc = m.group(1) if m else ''
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    h1 = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''
    m = re.search(r'<body[^>]+data-course=["\']([^"\']+)', text, re.I)
    course = m.group(1) if m else ''
    m = re.search(r'<body[^>]+data-unit=["\']([^"\']+)', text, re.I)
    unit = m.group(1) if m else ''
    extractor = TextExtractor()
    try:
        extractor.feed(text)
        plain = extractor.get_text()
    except:
        plain = ''
    plain = re.sub(r'\s+', ' ', plain).strip()
    summary = plain[:500] if len(plain) > 500 else plain
    return {
        'title': title,
        'description': desc,
        'h1': h1,
        'course': course,
        'unit': unit,
        'summary': summary,
        'path': str(path).replace('\\', '/').replace('./', ''),
    }

base = Path('.')
entries = []
for p in base.rglob('*.html'):
    sp = str(p)
    if 'assets' in sp or 'vendor' in sp or '_fragment' in sp or 'search' in sp:
        continue
    try:
        info = extract_info(p)
        if info['title'] and info['summary']:
            entries.append(info)
    except Exception as e:
        pass

entries.sort(key=lambda x: x['path'])

with open('search-index.json', 'w', encoding='utf-8') as f:
    json.dump({'entries': entries, 'count': len(entries), 'generatedAt': '2026-07-01'}, f, ensure_ascii=False, indent=2)

print(f'Indexed {len(entries)} pages')
