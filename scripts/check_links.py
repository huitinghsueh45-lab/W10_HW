# 用途：檢查 wiki/ 頁間 [[...]] 交叉連結、YAML front matter 與 wiki/index.md 收錄完整性。
"""
check_links.py
Deterministic link & index integrity checker for LLM Wiki (graph v2 - A4a).
Verifies:
  1. All `[[target]]` wikilinks in wiki/**/*.md resolve to an existing file in wiki/sources/ or wiki/concepts/.
  2. All wiki/sources/*.md and wiki/concepts/*.md pages are listed in wiki/index.md (no orphan pages).
  3. All pages have valid YAML front matter with required fields (title, type, sources, updated, status).
"""

from __future__ import annotations
import glob
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WIKILINK_RE = re.compile(r"\[\[([^\[\]|]+)(?:\|[^\[\]]+)?\]\]")
REQUIRED_FM = ["title", "type", "sources", "updated", "status"]


def parse_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main() -> int:
    source_files = sorted(glob.glob("wiki/sources/*.md"))
    concept_files = sorted(glob.glob("wiki/concepts/*.md"))
    all_pages = source_files + concept_files
    index_path = "wiki/index.md"

    # Build slug map: stem -> relative path
    slug_map: dict[str, str] = {}
    for p in all_pages:
        stem = os.path.splitext(os.path.basename(p))[0]
        slug_map[stem] = p

    passed = 0
    failed = 0

    print("=== 1. 檢查所有頁面 [[...]] 交叉連結 ===")
    for path in [index_path] + all_pages:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        targets = WIKILINK_RE.findall(text)
        broken = [t for t in targets if t.strip() not in slug_map]
        if not broken:
            passed += 1
            print(f"[PASS] {path}: {len(targets)} links all valid")
        else:
            failed += 1
            print(f"[FAIL] {path}: broken links = {broken}")

    print("\n=== 2. 檢查 wiki/index.md 收錄完整性（無孤立頁） ===")
    with open(index_path, encoding="utf-8") as f:
        index_text = f.read()
    index_targets = set(t.strip() for t in WIKILINK_RE.findall(index_text))
    all_stems = set(slug_map.keys())
    orphans = sorted(all_stems - index_targets)
    extra = sorted(index_targets - all_stems)
    if not orphans and not extra:
        passed += 1
        print(f"[PASS] wiki/index.md 收錄全部 {len(all_stems)} 頁，無孤立頁或無效項目")
    else:
        failed += 1
        print(f"[FAIL] wiki/index.md 差異: orphans={orphans}, extra={extra}")

    print("\n=== 3. 檢查 YAML Front Matter 欄位 ===")
    for path in all_pages:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm = parse_front_matter(text)
        missing = [k for k in REQUIRED_FM if not fm.get(k)]
        expected_type = "source" if "sources" in os.path.dirname(path) else "concept"
        type_ok = fm.get("type") == expected_type
        if not missing and type_ok:
            passed += 1
            print(f"[PASS] {path}: type={fm.get('type')}, status={fm.get('status')}, updated={fm.get('updated')}")
        else:
            failed += 1
            print(f"[FAIL] {path}: missing={missing}, type={fm.get('type')} (expected {expected_type})")

    print(f"\nSUMMARY check_links.py: PASS={passed}, FAIL={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
