# 用途：graph v2 A1.5 確定性預檢腳本 — 依 PDF 視覺座標 (y 由高到低, x 由左到右) 重排文字物件，偵測 Keynote/PDF 文字流倒置陷阱。
"""
precheck_pdf_coords.py
Deterministic A1.5 PDF coordinate pre-check script (graph v2).
Extracts text items with their (y, x) coordinates from key slides and flags potential
vertical reading-order inversions compared to default pypdf stream order.
"""

from __future__ import annotations
import logging
import os
import sys

logging.getLogger("pypdf").setLevel(logging.ERROR)
from pypdf import PdfReader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


KEY_PAGES = [
    ("raw/lectures/02神經網路的概念.pdf", 21, "八哥類別順序 (y1/y2/y3)"),
    ("raw/lectures/02神經網路的概念.pdf", 60, "未經訓練模型預測土八哥 (p1/p2/p3 機率)"),
    ("raw/lectures/02神經網路的概念.pdf", 67, "八哥辨識輸出向量順序 (p1/p2/p3)"),
    ("raw/lectures/03AI為什麼每次都不一樣？.pdf", 82, "MSE vs Cross Entropy 比較表"),
    ("raw/lectures/04LLM只是在猜下一個字？.pdf", 57, "Temperature τ 效果表 (a/b/c 對應 4.3/3.4/0.2)"),
]


def inspect_page(pdf_path: str, page_num: int, desc: str) -> bool:
    if not os.path.exists(pdf_path):
        print(f"[SKIP] {pdf_path} p.{page_num} ({desc}): 本地無檔案")
        return True
    reader = PdfReader(pdf_path)
    page = reader.pages[page_num - 1]
    stream_items: list[tuple[int, float, float, str]] = []

    def visitor(text, cm, tm, font_dict, font_size):
        t = text.strip()
        if t:
            x = float(tm[4] if tm[4] != 0 else cm[4])
            y = float(tm[5] if tm[5] != 0 else cm[5])
            stream_items.append((len(stream_items), round(y, 1), round(x, 1), t))

    page.extract_text(visitor_text=visitor)
    # Filter main body region (exclude footer y < 60 and title y > 850)
    body = [it for it in stream_items if 60 <= it[1] <= 850]
    coord_sorted = sorted(body, key=lambda z: (-z[1], z[2]))

    # Count vertical inversions: pair (i, j) where stream index i < j but y_i < y_j - 20
    inversions = 0
    for a in range(len(body)):
        for b in range(a + 1, len(body)):
            if body[a][1] + 20 < body[b][1]:
                inversions += 1

    flag = "INVERSION_DETECTED" if inversions > 0 else "ORDER_OK"
    print(f"[{flag}] {os.path.basename(pdf_path)} p.{page_num} ({desc}): body_tokens={len(body)}, vertical_inversions={inversions}")
    # Print compact top-to-bottom summary grouped by y-band (~20pt)
    rows: list[list[tuple[int, float, float, str]]] = []
    for it in coord_sorted:
        if not rows or abs(rows[-1][0][1] - it[1]) > 20:
            rows.append([it])
        else:
            rows[-1].append(it)
    for r in rows:
        r.sort(key=lambda z: z[2])
        y_avg = round(sum(z[1] for z in r) / len(r), 1)
        joined = " | ".join(z[3] for z in r)
        print(f"    y≈{y_avg:6.1f}: {joined}")
    return True


def main() -> int:
    print("=== A1.5 PDF 視覺座標排序預檢（precheck_pdf_coords.py） ===")
    for pdf_path, pno, desc in KEY_PAGES:
        inspect_page(pdf_path, pno, desc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
