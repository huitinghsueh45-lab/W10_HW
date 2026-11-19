# 用途：驗證 slides/index.html 結構、單一自足性、每頁頁尾 Wiki 來源路徑、traceability 對齊與互動元件數據。
"""
verify_slides.py
Deterministic slide verification script (graph v2 - B4a).
Verifies:
  1. Single self-contained HTML (no external http/https script or stylesheet CDN links).
  2. Slide count (13 slides), sequential slide numbers, and keyboard navigation handler.
  3. Every slide footer `.wiki-source-badge` uses valid `concepts/*.md` or `sources/*.md` paths
     that actually exist in `wiki/`.
  4. Footer Wiki sources match `checks/traceability.md`.
  5. Interactive JS data (Slide 7 Temperature τ, Slide 8 √5 scaling, Slide 13 5 quiz items)
     matches deterministic math recomputation.
"""

from __future__ import annotations
import math
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def softmax(vals: list[float], tau: float = 1.0) -> list[int]:
    scaled = [v / tau for v in vals]
    m = max(scaled)
    exps = [math.exp(v - m) for v in scaled]
    s = sum(exps)
    return [round(e / s * 100) for e in exps]


def main() -> int:
    html_path = "slides/index.html"
    trace_path = "checks/traceability.md"
    passed = 0
    failed = 0

    def record(name: str, ok: bool, detail: str) -> None:
        nonlocal passed, failed
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"[{status}] {name}: {detail}")

    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    print("=== 1. 單一自足 HTML 與基本結構檢查 ===")
    ext_refs = re.findall(r"""(?:src|href)\s*=\s*["']https?://[^"']+["']""", html, re.I)
    record("零外部 CDN 依賴", len(ext_refs) == 0, f"external_refs={ext_refs}")

    slides = re.findall(r"<section\b[^>]*class=[\"'][^\"']*\bslide\b[^\"']*[\"'][^>]*>.*?</section>", html, re.S)
    record("投影片總頁數", len(slides) == 13, f"found {len(slides)} slides (expected 13)")

    has_kbd = "ArrowRight" in html and "ArrowLeft" in html
    record("鍵盤左右鍵翻頁事件", has_kbd, "ArrowRight & ArrowLeft handlers present" if has_kbd else "missing")

    print("\n=== 2. 逐頁頁尾 Wiki 來源格式與檔案存在性檢查 ===")
    slide_wiki_map: dict[int, list[str]] = {}
    for i, sec in enumerate(slides, 1):
        m = re.search(r"class=[\"']wiki-source-badge[\"'][^>]*>(.*?)</span>", sec, re.S)
        if not m:
            record(f"Slide {i} 頁尾標籤", False, "缺少 .wiki-source-badge")
            continue
        badge = re.sub(r"\s+", " ", m.group(1)).strip()
        # Strip prefix "來源 Wiki："
        body = re.sub(r"^來源\s*Wiki\s*[:：]\s*", "", badge)
        raw_items = [x.strip() for x in re.split(r"[、,，]+", body) if x.strip()]
        bad_prefix = [x for x in raw_items if not (x.startswith("concepts/") or x.startswith("sources/"))]
        missing_files = [x for x in raw_items if not os.path.exists(os.path.join("wiki", x))]
        slide_wiki_map[i] = raw_items
        ok = len(raw_items) > 0 and not bad_prefix and not missing_files
        record(
            f"Slide {i} 頁尾來源 ({len(raw_items)} 頁)",
            ok,
            f"items={raw_items}" + (f", bad_prefix={bad_prefix}" if bad_prefix else "") + (f", missing={missing_files}" if missing_files else ""),
        )

    print("\n=== 3. 比對 checks/traceability.md 來源一致性 ===")
    if os.path.exists(trace_path):
        with open(trace_path, encoding="utf-8") as f:
            trace_text = f.read()
        for i in range(1, len(slides) + 1):
            row_m = re.search(rf"^\|\s*\*\*Slide\s+{i}\*\*\s*\|.*$", trace_text, re.M)
            if not row_m:
                record(f"Traceability Slide {i}", False, "traceability.md 中找不到該列")
                continue
            cols = [c.strip() for c in row_m.group(0).strip("|").split("|")]
            trace_wikis = re.findall(r"(?:concepts|sources)/[a-z0-9\-]+\.md", cols[3]) if len(cols) >= 4 else []
            html_wikis = slide_wiki_map.get(i, [])
            ok = set(trace_wikis) == set(html_wikis)
            record(
                f"Traceability ↔ HTML Slide {i}",
                ok,
                f"match ({len(html_wikis)} pages)" if ok else f"trace={trace_wikis} vs html={html_wikis}",
            )
    else:
        record("checks/traceability.md", False, "檔案不存在")

    print("\n=== 4. 互動元件數據與數學重算驗證 ===")
    # Slide 7 Temperature Simulator
    for tau, var_hint in [(0.5, "tau === 0.5"), (2.0, "tau === 2.0"), (1.0, "else")]:
        expected = softmax([4.3, 3.4, 0.2], tau=tau)
        # Extract the block in setTau
        if tau == 0.5:
            bm = re.search(r"if\s*\(tau\s*===\s*0\.5\)\s*\{(.*?)\}\s*else if", html, re.S)
        elif tau == 2.0:
            bm = re.search(r"else if\s*\(tau\s*===\s*2\.0\)\s*\{(.*?)\}\s*else\s*\{", html, re.S)
        else:
            bm = re.search(r"else if\s*\(tau\s*===\s*2\.0\)\s*\{.*?\}\s*else\s*\{(.*?)\}", html, re.S)
        vals = [int(x) for x in re.findall(r"v\d\.textContent\s*=\s*'(\d+)%'", bm.group(1))] if bm else []
        ok = vals == expected and (99 <= sum(vals) <= 101)
        record(f"Slide 7 溫度模擬器 τ={tau}", ok, f"html={vals}, recomputed={expected} (sum={sum(vals)}%)")

    # Slide 8 sqrt(d_k) toggle
    raw_expected = softmax([3.9, 3.2, 1.0, 0.3, 1.1])
    scaled_expected = softmax([v / math.sqrt(5) for v in [3.9, 3.2, 1.0, 0.3, 1.1]])
    dk_vals_matches = re.findall(r"vals:\s*\[([^\]]+)\]", html)
    if len(dk_vals_matches) >= 2:
        scaled_html = [int(x.strip()) for x in dk_vals_matches[0].split(",")]
        raw_html = [int(x.strip()) for x in dk_vals_matches[1].split(",")]
        record(
            "Slide 8 √d_k 切換器（原始內積）",
            raw_html == raw_expected,
            f"html={raw_html}, recomputed={raw_expected} (sum={sum(raw_html)}%)",
        )
        record(
            "Slide 8 √d_k 切換器（除以 √5）",
            scaled_html == scaled_expected,
            f"html={scaled_html}, recomputed={scaled_expected} (sum={sum(scaled_html)}%)",
        )
    else:
        record("Slide 8 √d_k 切換器", False, f"無法解析 vals 陣列 (found {len(dk_vals_matches)})")

    # Slide 13 Quiz items
    quiz_items = re.findall(r"class=[\"']quiz-item[\"']", html)
    quiz_ans_sources = re.findall(r"\[來源\s*Wiki：((?:concepts|sources)/[^\]]+\.md)\]", html)
    missing_q_src = [s for s in quiz_ans_sources if not os.path.exists(os.path.join("wiki", s))]
    record(
        "Slide 13 自我檢測題數與解析來源",
        len(quiz_items) == 5 and len(quiz_ans_sources) == 5 and not missing_q_src,
        f"quiz_items={len(quiz_items)}, ans_sources={len(quiz_ans_sources)}, missing={missing_q_src}",
    )

    print(f"\nSUMMARY verify_slides.py: PASS={passed}, FAIL={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
