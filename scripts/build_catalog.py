from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"

PUBLIC_COURSES = [
    {
        "topic": "大语言模型 / LLM 基础与应用工程",
        "root": "大语言模型/研习资料/阶段4-5_LLM基础与应用工程",
        "tags": ["大语言模型", "工程基础"],
    },
    {
        "topic": "大语言模型 / 提示工程",
        "root": "大语言模型/研习资料/提示工程学习笔记",
        "tags": ["大语言模型", "提示工程"],
    },
    {
        "topic": "大语言模型 / RAG 论文精读",
        "root": "大语言模型/研习资料/RAG论文精读",
        "tags": ["大语言模型", "RAG"],
    },
    {
        "topic": "大语言模型 / Harness Engineering",
        "root": "大语言模型/研习资料/Harness Engineering",
        "tags": ["大语言模型", "工程实践"],
    },
    {
        "topic": "大语言模型 / MCP 入门",
        "root": "大语言模型/研习资料/MCP入门",
        "tags": ["大语言模型", "MCP"],
    },
    {
        "topic": "AI 大模型 / 多智能体系统",
        "root": "AI大模型/研习资料/多智能体系统_何时以及如何使用",
        "tags": ["AI大模型", "多智能体"],
    },
    {
        "topic": "Agent",
        "root": "Agent/研习资料",
        "tags": ["Agent"],
    },
    {
        "topic": "Agent Skills",
        "root": "Agent Skills/研习资料",
        "tags": ["Agent", "Skills"],
    },
    {
        "topic": "Context Engineering",
        "root": "Context Engineering/研习资料",
        "tags": ["Agent", "Context Engineering"],
    },
    {
        "topic": "Learn Claude Code",
        "root": "Learn claude code/研习资料",
        "tags": ["Claude Code", "Agent"],
    },
    {
        "topic": "算法",
        "root": "算法/研习资料/01_数据结构与数组字符串",
        "tags": ["算法", "数据结构与数组字符串"],
    },
    {
        "topic": "算法",
        "root": "算法/研习资料/02_树堆图与结构设计",
        "tags": ["算法", "树堆图与结构设计"],
    },
    {
        "topic": "算法",
        "root": "算法/研习资料/03_回溯动态规划与综合题",
        "tags": ["算法", "回溯动态规划与综合题"],
    },
    {
        "topic": "深度学习 / Transformer 论文精读",
        "root": "深度学习/研习资料/Transformer论文精读",
        "tags": ["深度学习", "Transformer"],
    },
    {
        "topic": "PyTorch 深度学习实践",
        "root": "PyTorch深度学习实践 刘二大人/研习资料",
        "tags": ["PyTorch", "深度学习"],
    },
    {
        "topic": "李宏毅 LLM 大模型",
        "root": "李宏毅 LLM大模型/研习资料",
        "tags": ["李宏毅", "大语言模型"],
    },
    {
        "topic": "李宏毅机器学习",
        "root": "李宏毅  机器学习/研习资料",
        "tags": ["李宏毅", "机器学习"],
    },
    {
        "topic": "LoRA 论文精读",
        "root": "LoRA论文精读/研习资料",
        "tags": ["LoRA", "论文精读"],
    },
    {
        "topic": "计算机教育中缺失的一课",
        "root": "计算机教育中缺失的一课/研习资料",
        "tags": ["工程基础"],
    },
]


def to_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def clean_title(path: Path) -> str:
    stem = path.parent.name if path.name == "学习页.html" else path.stem
    stem = re.sub(r"^(P\d+)[_-]?", r"\1 ", stem)
    stem = re.sub(r"^(\d+)[_-]?", r"\1 ", stem)
    return stem.replace("_", " ").strip()


def build_pages() -> list[dict[str, object]]:
    pages: list[dict[str, object]] = []
    seen: set[str] = set()

    for course in PUBLIC_COURSES:
        root = ROOT / course["root"]
        if not root.exists():
            print(f"skip missing: {course['root']}")
            continue

        for page in sorted(root.rglob("学习页.html"), key=lambda item: item.as_posix()):
            rel_path = to_posix(page)
            if rel_path in seen:
                continue
            seen.add(rel_path)
            pages.append(
                {
                    "topic": course["topic"],
                    "title": clean_title(page),
                    "path": rel_path,
                    "tags": course["tags"],
                }
            )

    return pages


def main() -> None:
    tz = timezone(timedelta(hours=8))
    pages = build_pages()
    data = {
        "generatedAt": datetime.now(tz).isoformat(timespec="seconds"),
        "pageCount": len(pages),
        "pages": pages,
    }
    CATALOG_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {CATALOG_PATH.name}: {len(pages)} pages")


if __name__ == "__main__":
    main()
