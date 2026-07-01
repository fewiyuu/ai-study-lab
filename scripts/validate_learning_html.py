from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HTML_ROOT = ROOT

OLD_SHELL_PATTERNS = [
    "--navy",
    "#1b2a4a",
    "#f4f6f9",
]

PRIVATE_PATTERNS = [
    "course-forge",
    "自制学习资料",
    "Vault",
    "agent 日志",
    "批量生成",
    "D:/",
    "D:\\",
    "C:/Users",
    "C:\\Users",
]

SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.IGNORECASE | re.DOTALL)
SCRIPT_TYPE_RE = re.compile(r"""\btype\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
HREF_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)
MAIN_MAX_WIDTH_RE = re.compile(
    r"main\s*\{[^}]*max-width\s*:\s*(?:12\d{2}|13\d{2}|14\d{2}|15\d{2})px",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class Problem:
    path: Path
    kind: str
    detail: str


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def is_external(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:"))
        or lowered.startswith("#")
    )


def expected_shell(path: Path) -> str:
    if path.name in {"index.html", "课程索引.html"}:
        return "index-page-v1"
    return "study-page-v2"


def check_shell(path: Path, text: str) -> list[Problem]:
    problems: list[Problem] = []
    expected = expected_shell(path)
    if f'data-page-shell="{expected}"' not in text:
        problems.append(Problem(path, "shell-marker", f"missing {expected}"))

    if expected == "study-page-v2":
        required = ["<aside"]
    else:
        required = ["<aside", "<nav"]
    for marker in required:
        if marker not in text:
            problems.append(Problem(path, "shell-structure", f"missing marker: {marker}"))

    if expected == "study-page-v2":
        has_export = any(
            marker in text
            for marker in ["Markdown", "导出", "练习记录", "copyRecord", "export"]
        )
        if not has_export:
            problems.append(Problem(path, "shell-structure", "missing export/practice record"))
        has_progress = 'class="progress"' in text or "class='progress'" in text or ".progress" in text
        if not has_progress:
            problems.append(Problem(path, "shell-structure", "missing progress indicator"))

    for marker in OLD_SHELL_PATTERNS:
        if marker in text:
            problems.append(Problem(path, "old-shell", marker))
    return problems


def check_private(path: Path, text: str) -> list[Problem]:
    return [
        Problem(path, "private-residue", marker)
        for marker in PRIVATE_PATTERNS
        if marker in text
    ]


def check_layout(path: Path, text: str) -> list[Problem]:
    if MAIN_MAX_WIDTH_RE.search(text):
        return [
            Problem(
                path,
                "layout-width",
                "main content has desktop max-width; it should fill the space right of the sidebar",
            )
        ]
    return []


def check_links(path: Path, text: str) -> list[Problem]:
    problems: list[Problem] = []
    for target in HREF_RE.findall(text):
        clean = urlsplit(target).path
        if not clean or is_external(target):
            continue
        clean = unquote(clean)
        if clean.startswith("/"):
            problems.append(Problem(path, "absolute-link", target))
            continue
        resolved = (path.parent / clean).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            problems.append(Problem(path, "outside-link", target))
            continue
        if not resolved.exists():
            problems.append(Problem(path, "broken-link", target))
    return problems


def node_check(script: str) -> str | None:
    probe = (
        "new Function("
        + json.dumps(script)
        + ");"
    )
    result = subprocess.run(
        ["node", "-e", probe],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return (result.stderr or result.stdout).strip()
    return None


def is_javascript_script(attrs: str) -> bool:
    match = SCRIPT_TYPE_RE.search(attrs)
    if not match:
        return True
    script_type = match.group(1).strip().lower()
    return script_type in {"module", "text/javascript", "application/javascript"} or (
        "javascript" in script_type
    )


def check_scripts(path: Path, text: str) -> list[Problem]:
    problems: list[Problem] = []
    for index, (attrs, script) in enumerate(SCRIPT_RE.findall(text), start=1):
        if not is_javascript_script(attrs):
            continue
        err = node_check(script)
        if err:
            first_line = err.splitlines()[0] if err else "syntax error"
            problems.append(Problem(path, "script-syntax", f"script {index}: {first_line}"))
    return problems


def resolve_target(raw: str) -> Path:
    target = Path(raw)
    if not target.is_absolute():
        cwd_target = (Path.cwd() / target).resolve()
        root_target = (ROOT / target).resolve()
        target = cwd_target if cwd_target.exists() else root_target
    target = target.resolve()
    if not target.exists():
        raise SystemExit(f"Target does not exist: {raw}")
    try:
        target.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise SystemExit(f"Target must be under {ROOT}: {raw}") from exc
    return target


def collect_html_files(targets: list[str]) -> list[Path]:
    if not targets:
        return sorted(HTML_ROOT.rglob("*.html"))
    files: set[Path] = set()
    for raw in targets:
        target = resolve_target(raw)
        if target.is_file():
            if target.suffix.lower() not in {".html", ".htm"}:
                raise SystemExit(f"Target file is not HTML: {raw}")
            files.add(target)
            continue
        files.update(path for path in target.rglob("*.html") if path.is_file())
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate learning-kit HTML files. Defaults to all HTML under 30_研究."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Optional HTML file(s) or directory/directories to check for fast local validation.",
    )
    parser.add_argument(
        "--skip-script-check",
        action="store_true",
        help="Skip inline JavaScript syntax checks. Useful for very fast text-only validation.",
    )
    args = parser.parse_args()

    files = collect_html_files(args.targets)
    problems: list[Problem] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        problems.extend(check_shell(path, text))
        problems.extend(check_private(path, text))
        problems.extend(check_layout(path, text))
        problems.extend(check_links(path, text))
        if not args.skip_script_check:
            problems.extend(check_scripts(path, text))

    summary: dict[str, int] = {}
    for problem in problems:
        summary[problem.kind] = summary.get(problem.kind, 0) + 1

    print(f"HTML files: {len(files)}")
    if summary:
        print("Problems:")
        for kind, count in sorted(summary.items()):
            print(f"  {kind}: {count}")
        print("\nFirst problems:")
        for problem in problems[:120]:
            print(f"- {problem.kind}: {rel(problem.path)} :: {problem.detail}")
    else:
        print("No problems found.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
