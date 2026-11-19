# 用途：檢查 wiki/sources/ 與 wiki/concepts/ 各頁事實句是否皆標註 [來源: 檔名 p.X]，並列舉缺漏位置。
"""
check_sources.py
Deterministic citation checker for LLM Wiki (graph v2 - A4a).
Checks every factual bullet/paragraph/table row in wiki/sources/*.md and wiki/concepts/*.md
to verify it carries a `[來源: ... p.X]` citation (or explicitly marked `[頁碼未確認]` / `[待查證]`).
Reports all missing lines verbatim without hiding failures.
"""

from __future__ import annotations
import glob
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Matches `[來源: 檔名 p.頁碼]` (allowing multiple pages/ranges/sections or multiple sources)
STRICT_SOURCE_RE = re.compile(r"\[來源:\s*[^\[\]]+?p\.\s*\d+[^\[\]]*\]")
ANY_SOURCE_RE = re.compile(r"\[來源:\s*[^\[\]]+\]|\[頁碼未確認\]|\[待查證\]")
LINK_ONLY_RE = re.compile(r"^[-*]\s*(?:\[\[[^\]]+\]\]|[\s、,，;；—–\-（）()「」\w\u4e00-\u9fff]*\[\[[^\]]+\]\][^\[]*)$")


def strip_front_matter(lines: list[str]) -> list[tuple[int, str]]:
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return [(idx + 1, lines[idx]) for idx in range(i + 1, len(lines))]
    return [(idx + 1, line) for idx, line in enumerate(lines)]


def is_structural_or_non_factual(line: str, in_code: bool, in_math: bool, in_related_section: bool) -> bool:
    s = line.strip()
    if not s or in_code or in_math:
        return True
    if s.startswith("#") or s.startswith("---") or s.startswith("```") or s.startswith("$$"):
        return True
    if re.match(r"^\|[\s:\-|]+\|$", s):  # Markdown table separator
        return True
    if in_related_section and "[[" in s:
        return True
    # Metadata blockquote at top of source summary (e.g., > **原始資料**...)
    if s.startswith(">") and any(k in s for k in ["原始資料", "分段範圍", "核心問題", "原始檔案", "頁數"]):
        return True
    return False


def check_file(path: str) -> tuple[int, int, list[tuple[int, str, str]]]:
    with open(path, encoding="utf-8") as f:
        raw_lines = f.read().splitlines()

    body = strip_front_matter(raw_lines)
    in_code = False
    in_math = False
    in_related = False
    checked = 0
    missing_items: list[tuple[int, str, str]] = []

    for idx, (lineno, line) in enumerate(body):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if s == "$$":
            in_math = not in_math
            continue
        if s.startswith("#"):
            in_related = any(k in s for k in ["相關概念", "延伸閱讀", "交叉連結", "相關頁面", "來源文件", "對應概念頁"])
            continue

        if is_structural_or_non_factual(line, in_code, in_math, in_related):
            continue

        # Skip pure bold outline/section label ending in colon (e.g. `1. **小標題**：` or `- **分段讀取範圍**...：`)
        if re.match(r"^(?:[-*]|\d+\.)\s+\*\*[^*]+\*\*(?:（[^）]*）)?[:：]\s*$", s):
            continue

        # Skip pure wikilink bullet (e.g. `- [[concept-name]]`)
        if re.match(r"^[-*]\s+\[\[[^\]]+\]\]\s*$", s):
            continue

        # Skip markdown table header row if next line is separator
        if s.startswith("|") and idx + 1 < len(body) and re.match(r"^\|[\s:\-|]+\|$", body[idx + 1][1].strip()):
            continue

        # Skip standalone display math lines `$$...$$`
        if s.startswith("$$") and s.endswith("$$"):
            continue

        checked += 1
        if STRICT_SOURCE_RE.search(s):
            continue
        elif ANY_SOURCE_RE.search(s):
            missing_items.append((lineno, "NO_PAGE_NUM", s))
        else:
            missing_items.append((lineno, "MISSING_SOURCE", s))

    return checked, len(missing_items), missing_items


def main() -> int:
    files = sorted(glob.glob("wiki/sources/*.md") + glob.glob("wiki/concepts/*.md"))
    total_checked = 0
    total_issues = 0
    files_failed = 0

    print("=== Wiki 事實句來源與頁碼檢查（check_sources.py） ===")
    for path in files:
        checked, n_miss, items = check_file(path)
        total_checked += checked
        total_issues += n_miss
        status = "PASS" if n_miss == 0 else "FAIL"
        if n_miss > 0:
            files_failed += 1
        print(f"[{status}] {path}: checked_lines={checked}, issues={n_miss}")
        for lineno, kind, text in items:
            preview = text if len(text) <= 110 else text[:107] + "..."
            print(f"    - L{lineno} [{kind}]: {preview}")

    print(
        f"\nSUMMARY check_sources.py: FILES={len(files)}, FILES_FAIL={files_failed}, "
        f"CHECKED_LINES={total_checked}, ISSUES={total_issues}"
    )
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
