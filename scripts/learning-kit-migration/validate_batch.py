import argparse
import json
import subprocess
import sys
from pathlib import Path


def classify(output: str) -> str:
    lowered = output.lower()
    if "visible text is too thin" in lowered or "visible depth" in lowered:
        return "thin-content"
    if "private/internal pattern" in lowered or "internal marker leaked" in lowered:
        return "internal-leak"
    if "missing nav markers" in lowered or "course shell check failed" in lowered:
        return "shell-sync"
    if "missing" in lowered and "asset" in lowered:
        return "missing-asset"
    if "browser" in lowered or "playwright" in lowered or "console" in lowered:
        return "browser-smoke"
    if "lint failed" in lowered:
        return "lint"
    return "validation"


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.returncode, completed.stdout


def manifest_profile(page: Path, fallback: str) -> str:
    manifest = page.parent / "_learning-kit-run-manifest.json"
    if not manifest.exists():
        return fallback
    try:
        data = json.loads(manifest.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return fallback
    profile = data.get("profile")
    return profile if profile in {"default", "technical-deep"} else fallback


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a learning-kit migration batch.")
    parser.add_argument("batch_json", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--skip-browser", action="store_true")
    parser.add_argument("--profile", choices=["manifest", "default", "technical-deep"], default="manifest")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--max-output", type=int, default=1200)
    args = parser.parse_args()

    repo = args.repo.resolve()
    data = json.loads(args.batch_json.read_text(encoding="utf-8-sig"))
    scripts = repo / ".agents" / "skills" / "learning-kit" / "scripts"

    failures: list[tuple[str, str, str]] = []
    for item in data.get("items", []):
        page = Path(item["page"])
        course_root = Path(item["courseRoot"])
        profile = manifest_profile(page, "default") if args.profile == "manifest" else args.profile
        rel_page = page.relative_to(repo) if page.is_absolute() and page.is_relative_to(repo) else page
        print(f"\n== {item.get('nickname', item.get('agent'))}: {rel_page} [{profile}]")

        checks = [
            [
                sys.executable,
                str(scripts / "lint_learning_html.py"),
                "--profile",
                profile,
                str(page),
            ],
            [
                sys.executable,
                str(scripts / "quick_check_page.py"),
                str(page),
                "--profile",
                profile,
                "--course-root",
                str(course_root),
            ],
        ]
        if not args.skip_browser:
            checks.append(
                [
                    sys.executable,
                    str(scripts / "browser_smoke_check.py"),
                    str(page),
                    "--course-root",
                    str(course_root),
                ]
            )

        for cmd in checks:
            label = Path(cmd[1]).name
            code, output = run(cmd, repo)
            status = "ok" if code == 0 else "fail"
            failure_class = classify(output) if code != 0 else ""
            suffix = f" ({failure_class})" if failure_class else ""
            print(f"-- {label}: {status}{suffix}")
            if code != 0:
                failures.append((str(rel_page), label, failure_class))
                if args.verbose:
                    print(output[-args.max_output :])

        manifest = page.parent / "_learning-kit-run-manifest.json"
        if not manifest.exists():
            failures.append((str(rel_page), "manifest", "missing-manifest"))
            print("-- manifest: missing")
        else:
            print("-- manifest: ok")

    if failures:
        print("\nFAILED SUMMARY:")
        for rel_page, label, failure_class in failures:
            print(f"- {rel_page}: {label} ({failure_class})")
        return 1

    print("\nAll batch checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
