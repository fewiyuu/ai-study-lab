from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, asdict
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE = "https://labuladong.online"
QUICK = f"{BASE}/zh/algo/intro/quick-learning-plan/"
OUT_JSON = Path("30_研究/算法/labuladong速成目录题单.json")
OUT_MD = Path("30_研究/算法/labuladong速成目录题单.md")


@dataclass
class Problem:
    number: str
    title: str
    slug: str | None = None


@dataclass
class ProblemSet:
    title: str
    url: str
    source_section: str
    problems: list[Problem]


def fetch(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=25)
    resp.raise_for_status()
    return resp.content.decode("utf-8", errors="replace")


def clean(text: str) -> str:
    return " ".join(unescape(text).split())


def quick_problemset_links(html: str) -> list[tuple[str, str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[tuple[str, str, str]] = []
    current_section = ""

    for tag in soup.find_all(["h2", "h3", "a"]):
        text = clean(tag.get_text(" ", strip=True))
        if tag.name in {"h2", "h3"} and text:
            current_section = text.replace("¶ ", "")
            continue
        if tag.name != "a":
            continue
        href = tag.get("href") or ""
        if "/zh/algo/problem-set/" not in href:
            continue
        title = text
        url = urljoin(BASE, href)
        if title and (title, url, current_section) not in links:
            links.append((title, url, current_section))
    return links


def extract_page_title(soup: BeautifulSoup, fallback: str) -> str:
    h1 = soup.find("h1")
    if h1:
        return clean(h1.get_text(" ", strip=True))
    title = soup.find("title")
    if title:
        return clean(title.get_text(" ", strip=True))
    return fallback


def extract_toc_problems(html: str) -> list[Problem]:
    # Next.js embeds a clean tocItems array in the hydration payload.
    pairs = re.findall(
        r'\{\\"title\\":\\"(\d+)\. ([^"\\]+?)\\",\\"href\\":\\"#slug_([^"\\]+?)\\",\\"depth\\":2\}',
        html,
    )
    seen: set[tuple[str, str]] = set()
    problems: list[Problem] = []
    for number, title, slug in pairs:
        key = (number, title)
        if key in seen:
            continue
        seen.add(key)
        problems.append(Problem(number=number, title=title, slug=slug))
    return problems


def extract_visible_problems(soup: BeautifulSoup) -> list[Problem]:
    seen: set[tuple[str, str]] = set()
    problems: list[Problem] = []
    pattern = re.compile(r"^(\d+)\.\s+(.+)$")

    for tag in soup.find_all(["h2", "h3", "li", "p"]):
        text = clean(tag.get_text(" ", strip=True))
        m = pattern.match(text)
        if not m:
            continue
        number, title = m.groups()
        title = title.strip()
        if len(title) > 80:
            continue
        key = (number, title)
        if key in seen:
            continue
        seen.add(key)
        problems.append(Problem(number=number, title=title))
    return problems


def extract_problemset(title: str, url: str, section: str) -> ProblemSet:
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    page_title = extract_page_title(soup, title)
    problems = extract_toc_problems(html)
    if not problems:
        problems = extract_visible_problems(soup)
    return ProblemSet(title=page_title, url=url, source_section=section, problems=problems)


def write_markdown(problemsets: list[ProblemSet]) -> None:
    total = sum(len(ps.problems) for ps in problemsets)
    lines: list[str] = [
        "---",
        "title: labuladong速成目录题单",
        "aliases:",
        "  - labuladong 速成题单",
        "tags:",
        "  - algorithms",
        "  - labuladong",
        "  - problemset",
        "source: https://labuladong.online/zh/algo/intro/quick-learning-plan/",
        "---",
        "",
        "# labuladong 速成目录题单",
        "",
        "> [!info]",
        "> 这份题单从 labuladong「速成目录学习规划」及其链接到的经典习题页抽取。总目录页给路线，具体题号主要分布在各个 `problem-set` 页面。",
        "",
        f"- 题单页数量：{len(problemsets)}",
        f"- 抽取到的题目数：{total}",
        "- 用法：先学对应框架文章，再做本组题。不要把这份清单当成从上到下硬刷的公司题单。",
        "",
        "## 总览",
        "",
        "| 分组 | 题单页 | 题数 | 来源 |",
        "|---|---:|---:|---|",
    ]
    for ps in problemsets:
        lines.append(
            f"| {ps.source_section or '未标注'} | [{ps.title}]({ps.url}) | {len(ps.problems)} | labuladong |"
        )
    lines.append("")

    for ps in problemsets:
        lines.extend(
            [
                f"## {ps.title}",
                "",
                f"- 来源分组：{ps.source_section or '未标注'}",
                f"- 页面：[{ps.url}]({ps.url})",
                "",
            ]
        )
        if not ps.problems:
            lines.extend(["> [!warning]", "> 这个页面没有从公开 HTML 中抽到具体题号，可能需要插件、登录或页面动态加载。", ""])
            continue
        lines.extend(["| 题号 | 题目 | 状态 | 备注 |", "|---:|---|---|---|"])
        for p in ps.problems:
            lines.append(f"| {p.number} | {p.title} | 未做 |  |")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    quick_html = fetch(QUICK)
    links = quick_problemset_links(quick_html)
    problemsets: list[ProblemSet] = []
    for idx, (title, url, section) in enumerate(links, start=1):
        print(f"[{idx}/{len(links)}] {title} {url}")
        try:
            problemsets.append(extract_problemset(title, url, section))
        except Exception as exc:
            print(f"  failed: {exc}")
            problemsets.append(ProblemSet(title=title, url=url, source_section=section, problems=[]))
        time.sleep(0.25)

    OUT_JSON.write_text(
        json.dumps([asdict(ps) for ps in problemsets], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(problemsets)
    print(f"wrote {OUT_MD} and {OUT_JSON}")


if __name__ == "__main__":
    main()
