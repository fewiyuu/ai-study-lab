from __future__ import annotations

import argparse
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "course-shell.json"
START = "<!-- learning-kit:nav:start -->"
END = "<!-- learning-kit:nav:end -->"


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if "id" in attrs:
            self.ids.add(attrs["id"])


def load_config() -> dict[str, Any]:
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {CONFIG}: {exc}") from exc
    if not isinstance(data.get("pages"), list) or not data["pages"]:
        raise SystemExit(f"{CONFIG} must contain a non-empty pages list")
    return data


def page_ids(path: Path) -> set[str]:
    parser = AnchorParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.ids


def validate_config(data: dict[str, Any]) -> None:
    seen: set[str] = set()
    for page in data["pages"]:
        rel = page.get("path")
        nav = page.get("nav")
        if not isinstance(rel, str) or not isinstance(nav, list):
            raise SystemExit("Each page entry needs a string path and nav list")
        if rel in seen:
            raise SystemExit(f"Duplicate page entry: {rel}")
        seen.add(rel)
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Configured page does not exist: {rel}")
        text = path.read_text(encoding="utf-8")
        if START not in text or END not in text:
            raise SystemExit(f"Missing nav markers: {path}")
        anchors = page_ids(path)
        for item in nav:
            href = item.get("href") if isinstance(item, dict) else None
            label = item.get("label") if isinstance(item, dict) else None
            if not href or not label:
                raise SystemExit(f"Nav item in {rel} needs href and label")
            if href.startswith("#"):
                if href[1:] not in anchors:
                    raise SystemExit(f"Nav anchor not found in {rel}: {href}")
                continue
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target_part, _, anchor = href.partition("#")
            target = (path.parent / target_part).resolve()
            if not target.exists():
                raise SystemExit(f"Nav target missing in {rel}: {href}")
            if anchor and target.suffix.lower() in {".html", ".htm"}:
                if anchor not in page_ids(target):
                    raise SystemExit(f"Nav target anchor missing in {rel}: {href}")


def render_nav(items: list[dict[str, str]], indent: str) -> str:
    lines = [START]
    for item in items:
        href = escape(item["href"], quote=True)
        label = escape(item["label"])
        lines.append(f'{indent}<a href="{href}"><span class="dot"></span>{label}</a>')
    lines.append(f"{indent}{END}")
    return "\n".join(lines)


def sync_page(page: dict[str, object], *, check: bool) -> bool:
    path = ROOT / str(page["path"])
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(?P<indent>[ \t]*){re.escape(START)}.*?^[ \t]*{re.escape(END)}",
        re.S | re.M,
    )
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"Missing nav markers: {path}")
    replacement = render_nav(page["nav"], match.group("indent"))
    updated = text[: match.start()] + match.group("indent") + replacement + text[match.end() :]
    changed = updated != text
    if changed and not check:
        path.write_text(updated, encoding="utf-8", newline="")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync learning-kit course nav blocks from course-shell.json."
    )
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args()

    data = load_config()
    validate_config(data)
    changed = [page["path"] for page in data["pages"] if sync_page(page, check=args.check)]
    if changed:
        print("Nav drift:" if args.check else "Synced nav:")
        for path in changed:
            print(f"- {path}")
        return 1 if args.check else 0
    print("Course nav is in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
