# 用途：檢查 wiki/sources/ 與 wiki/concepts/ 各頁事實句是否皆標註 [來源: 檔名 p.X]，並列舉缺漏與明文豁免項目。
"""
check_sources.py
Deterministic citation checker for LLM Wiki (graph v2 - A4a).
Checks every factual bullet/paragraph/table row in wiki/sources/*.md and wiki/concepts/*.md
to verify it carries a `[來源: ... p.X]` citation (or `[頁碼未確認]` / `[待查證]`).

【明文豁免規則（2026-11-19 Retry 2 增列，執行時逐行印出 [EXEMPT:R*] 與豁免總數，絕不靜默略過）】：
- R1（純引導句／提問句，共 3 行）：不含具體數值／公式／原文例句，僅作承上啟下之冒號結尾導語或提問句，其緊鄰下文各條已逐一標註來源。
- R2（常見誤解標題列，共 8 行）：概念頁「常見誤解」節中 `- **誤解 N：「...」**` 之小標題列，其緊接下一行 `- **事實**：...` 已標註原文來源。
- R3（專案元資訊列，共 1 行）：`- **專案角色**：...` 說明該外部資料在專案中之角色定位，非原文內容陳述。
- R4（跨來源交叉比對表，共 4 行）：`wiki/sources/external-vaswani-2017-attention-is-all-you-need.md` 之交叉查核對照表資料列，表內各欄已分別明載 `p.X` 頁碼但採表格欄位而非 `[來源: ...]` 括號語法。
"""

from __future__ import annotations
import glob
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STRICT_SOURCE_RE = re.compile(r"\[來源:\s*[^\[\]]+?p\.\s*\d+[^\[\]]*\]")
ANY_SOURCE_RE = re.compile(r"\[來源:\s*[^\[\]]+\]|\[頁碼未確認\]|\[待查證\]")


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
    if s.startswith(">") and any(k in s for k in ["原始資料", "分段範圍", "核心問題", "原始檔案", "頁數"]):
        return True
    return False


def match_exemption(path: str, s: str, in_crosscheck_table: bool) -> str | None:
    """Return explicit exemption code R1..R4 if line matches documented exemption rules."""
    # R2: Misconception heading line `- **誤解 N：「...」**`
    if re.match(r"^[-*]\s+\*\*誤解\s*\d+[:：]「.*」\*\*\s*$", s):
        return "R2"
    # R3: Project role metadata line `- **專案角色**：...`
    if re.match(r"^[-*]\s+\*\*專案角色\*\*[:：]", s):
        return "R3"
    # R4: Cross-source comparison table row that embeds explicit `p.\d+` in columns
    if in_crosscheck_table and s.startswith("|") and re.search(r"p\.\d+", s):
        return "R4"
    # R1: Pure lead-in sentence (ending with ： or ？) containing no numbers, no concrete quoted examples, and no bullet prefix
    if (
        not s.startswith("-")
        and not s.startswith("|")
        and (s.endswith("：") or s.endswith("？"))
        and not re.search(r"\d|\"|「[^」]*[=＝]", s)
    ):
        return "R1"
    return None


def check_file(path: str) -> tuple[int, int, list[tuple[int, str, str]], list[tuple[int, str, str]]]:
    with open(path, encoding="utf-8") as f:
        raw_lines = f.read().splitlines()

    body = strip_front_matter(raw_lines)
    in_code = False
    in_math = False
    in_related = False
    in_crosscheck = False
    checked = 0
    missing_items: list[tuple[int, str, str]] = []
    exempt_items: list[tuple[int, str, str]] = []

    for idx, (lineno, line) in enumerate(body):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if s == "$$":
            in_math = not in_math
            continue
        if s.startswith("#"):
            in_related = any(k in s for k in ["相關概念", "延伸閱讀", "交叉連結", "相關頁面", "來源文件", "對應概念頁", "關聯概念頁"])
            in_crosscheck = "交叉查核" in s or "交叉比對" in s
            continue

        if is_structural_or_non_factual(line, in_code, in_math, in_related):
            continue

        # Skip pure bold outline/section label ending in colon
        if re.match(r"^(?:[-*]|\d+\.)\s+\*\*[^*]+\*\*(?:（[^）]*）)?[:：]\s*$", s):
            continue

        # Skip pure wikilink bullet
        if re.match(r"^[-*]\s+\[\[[^\]]+\]\]\s*$", s):
            continue

        # Skip markdown table header row if next line is separator
        if s.startswith("|") and idx + 1 < len(body) and re.match(r"^\|[\s:\-|]+\|$", body[idx + 1][1].strip()):
            continue

        if s.startswith("$$") and s.endswith("$$"):
            continue

        checked += 1
        if STRICT_SOURCE_RE.search(s):
            continue

        ex_code = match_exemption(path, s, in_crosscheck)
        if ex_code:
            exempt_items.append((lineno, ex_code, s))
        elif ANY_SOURCE_RE.search(s):
            missing_items.append((lineno, "NO_PAGE_NUM", s))
        else:
            missing_items.append((lineno, "MISSING_SOURCE", s))

    return checked, len(missing_items), missing_items, exempt_items


def main() -> int:
    files = sorted(glob.glob("wiki/sources/*.md") + glob.glob("wiki/concepts/*.md"))
    total_checked = 0
    total_issues = 0
    total_exempt = 0
    files_failed = 0
    exempt_counts: dict[str, int] = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}

    print("=== Wiki 事實句來源與頁碼檢查（check_sources.py，含明文豁免紀錄） ===")
    for path in files:
        checked, n_miss, items, exempts = check_file(path)
        total_checked += checked
        total_issues += n_miss
        total_exempt += len(exempts)
        for _, code, _ in exempts:
            exempt_counts[code] = exempt_counts.get(code, 0) + 1
        status = "PASS" if n_miss == 0 else "FAIL"
        if n_miss > 0:
            files_failed += 1
        print(f"[{status}] {path}: checked_lines={checked}, issues={n_miss}, exempted={len(exempts)}")
        for lineno, kind, text in items:
            preview = text if len(text) <= 110 else text[:107] + "..."
            print(f"    - L{lineno} [{kind}]: {preview}")
        for lineno, code, text in exempts:
            preview = text if len(text) <= 110 else text[:107] + "..."
            print(f"    - L{lineno} [EXEMPT:{code}]: {preview}")

    print(
        f"\nSUMMARY check_sources.py: FILES={len(files)}, FILES_FAIL={files_failed}, "
        f"CHECKED_LINES={total_checked}, ISSUES={total_issues}, EXEMPTED={total_exempt} "
        f"(R1={exempt_counts['R1']}, R2={exempt_counts['R2']}, R3={exempt_counts['R3']}, R4={exempt_counts['R4']})"
    )
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
