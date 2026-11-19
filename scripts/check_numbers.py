# 用途：確定性驗算 Wiki 中出現的可重算數值（Softmax、機率總和 ±1%、MSE、Cross Entropy、KL 散度與 √5 縮放）並確認其存在於 Wiki 檔案。
"""
check_numbers.py
Deterministic numerical verification for LLM Wiki (graph v2 - A4a).
Recomputes key formulas (Softmax, probability sums within 100% ±1%, MSE, Cross Entropy,
KL Divergence, sqrt(5) scaling) and scans wiki/ pages for percentage-list sums.
"""

from __future__ import annotations
import glob
import math
import os
import re
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def softmax(vals: list[float], tau: float = 1.0) -> list[float]:
    scaled = [v / tau for v in vals]
    m = max(scaled)
    exps = [math.exp(v - m) for v in scaled]
    s = sum(exps)
    return [e / s for e in exps]


def mse_sum_sq(y_true: list[float], y_pred: list[float]) -> float:
    return sum((t - p) ** 2 for t, p in zip(y_true, y_pred))


def cross_entropy_ln(p_true: list[float], q_pred: list[float]) -> float:
    return -sum(p * math.log(q) for p, q in zip(p_true, q_pred) if p > 0)


def entropy_ln(p_true: list[float]) -> float:
    return -sum(p * math.log(p) for p in p_true if p > 0)


def kl_divergence_ln(p_true: list[float], q_pred: list[float]) -> float:
    return sum(p * math.log(p / q) for p, q in zip(p_true, q_pred) if p > 0)


def check_formula_cases() -> tuple[int, int]:
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

    print("=== 1. 核心公式與數值重算檢查 ===")

    # Case 1: Lecture 02 p.14-19 Softmax (1.9, 1.1, 0.2) -> (0.61, 0.28, 0.11)
    sm_l2 = softmax([1.9, 1.1, 0.2])
    sm_l2_r = [round(x, 2) for x in sm_l2]
    sm_l2_pct = [round(x * 100) for x in sm_l2]
    ok = sm_l2_r == [0.61, 0.28, 0.11] and (99 <= sum(sm_l2_pct) <= 101)
    record(
        "L02 p.14-19 八哥 Softmax",
        ok,
        f"recomputed={[round(x, 4) for x in sm_l2]} -> rounded={sm_l2_r}, pct={sm_l2_pct} (sum={sum(sm_l2_pct)}%)",
    )

    # Case 2: Lecture 02 p.69 平方誤差和 (1-0.23)^2 + (0-0.43)^2 + (0-0.34)^2 = 0.8934 ≈ 0.89
    sse_l2 = mse_sum_sq([1, 0, 0], [0.23, 0.43, 0.34])
    ok = round(sse_l2, 2) == 0.89 and abs(sse_l2 - 0.8934) < 1e-9
    record(
        "L02 p.69 單筆平方誤差和",
        ok,
        f"exact={sse_l2:.4f}, rounded_2dp={round(sse_l2, 2)} (expected 0.89)",
    )

    # Case 3: Lecture 03 p.82 MSE & Cross Entropy (Hard Target y=[1,0,0])
    mse_a = mse_sum_sq([1, 0, 0], [0.7, 0.19, 0.11])
    mse_b = mse_sum_sq([1, 0, 0], [0.7, 0.3, 0.0])
    ce_a = cross_entropy_ln([1, 0, 0], [0.7, 0.19, 0.11])
    ce_b = cross_entropy_ln([1, 0, 0], [0.7, 0.3, 0.0])
    ok_mse = round(mse_a, 2) == 0.14 and round(mse_b, 2) == 0.18
    ok_ce = round(ce_a, 2) == 0.36 and round(ce_b, 2) == 0.36
    record(
        "L03 p.82 MSE 比較",
        ok_mse,
        f"[0.7,0.19,0.11] MSE={mse_a:.4f} (≈0.14); [0.7,0.3,0] MSE={mse_b:.4f} (≈0.18)",
    )
    record(
        "L03 p.82 Cross Entropy 比較",
        ok_ce,
        f"both -ln(0.7)={ce_a:.4f} (≈0.36), diff={abs(ce_a - ce_b):.6f}",
    )

    # Case 4: Lecture 03 p.86 Soft Target P=[0.7,0.2,0.1]
    p_soft = [0.7, 0.2, 0.1]
    q1 = [0.7, 0.19, 0.11]
    q2 = [0.7, 0.3, 0.0]  # Note: q2 has 0 -> check if Lecture 03 p.86 used [0.7, 0.29, 0.01] or similar; let's inspect exact wiki text too!
    ce_s1 = cross_entropy_ln(p_soft, q1)
    kl_s1 = kl_divergence_ln(p_soft, q1)
    # Check Q2 candidate from L03 p.86: let's check both [0.7, 0.25, 0.05] or [0.7, 0.27, 0.03] etc. via wiki inspection below
    record(
        "L03 p.86 Soft Target Q1=[0.7,0.19,0.11]",
        round(ce_s1, 2) == 0.80 or round(ce_s1, 2) == 0.81,
        f"H(P)={entropy_ln(p_soft):.4f}, H(P,Q1)={ce_s1:.4f}, D_KL(P||Q1)={kl_s1:.4f}",
    )

    # Case 5: Lecture 04 p.17-18 候選字 Softmax [1.40, 0.03, 1.71, -0.73, 0.95] -> [30%, 7%, 40%, 4%, 19%]
    # Note (E3 W-15 人工確認): 精確值為 [29.64%, 7.53%, 40.41%, 3.52%, 18.90%]，標準四捨五入為 [30, 8, 40, 4, 19] (101%)，
    # 原投影片將第 2 項 7.53% 下修為 7% 以使總和等於 100%，單項與精確值差異 <= 1%。
    sm_l4 = softmax([1.40, 0.03, 1.71, -0.73, 0.95])
    sm_l4_pct = [round(x * 100) for x in sm_l4]
    sm_l4_exact_pct = [round(x * 100, 2) for x in sm_l4]
    slide_l4 = [30, 7, 40, 4, 19]
    ok = all(abs(e - s) <= 1.0 for e, s in zip(sm_l4_exact_pct, slide_l4)) and (99 <= sum(slide_l4) <= 101)
    record(
        "L04 p.17-18 候選字 Softmax（含 E3 W-15 原文捨入註記）",
        ok,
        f"exact_pct={sm_l4_exact_pct}, std_round={sm_l4_pct} (sum={sum(sm_l4_pct)}%), wiki/slide={slide_l4} (sum=100%; 原文將 7.53% 下修為 7% 以湊滿 100%，每項誤差 <= 1%)",
    )

    # Case 6: Lecture 04 p.57 Temperature τ=1, 2, 0.5 on [4.3, 3.4, 0.2]
    temp_scores = [4.3, 3.4, 0.2]
    for tau, expected in [(1.0, [70, 29, 1]), (2.0, [57, 36, 7]), (0.5, [86, 14, 0])]:
        sm_t = [round(x * 100) for x in softmax(temp_scores, tau=tau)]
        ok = sm_t == expected and (99 <= sum(sm_t) <= 101)
        record(
            f"L04 p.57 Temperature τ={tau}",
            ok,
            f"recomputed_pct={sm_t} (sum={sum(sm_t)}%), expected={expected}",
        )

    # Case 7: Lecture 05 p.32 原始內積 [3.9, 3.2, 1.0, 0.3, 1.1] -> [61%, 30%, 3%, 2%, 4%]
    raw_dots = [3.9, 3.2, 1.0, 0.3, 1.1]
    sm_raw = [round(x * 100) for x in softmax(raw_dots)]
    ok = sm_raw == [61, 30, 3, 2, 4] and (99 <= sum(sm_raw) <= 101)
    record(
        "L05 p.32 原始內積 Softmax",
        ok,
        f"recomputed_pct={sm_raw} (sum={sum(sm_raw)}%), expected=[61, 30, 3, 2, 4]",
    )

    # Case 8: Lecture 05 p.33 除以 √5 縮放 -> [1.74, 1.43, 0.45, 0.13, 0.49] -> [40%, 29%, 11%, 8%, 11%]
    sqrt5 = math.sqrt(5)
    scaled_exact = [v / sqrt5 for v in raw_dots]
    scaled_2dp = [round(v, 2) for v in scaled_exact]
    expected_scaled = [1.74, 1.43, 0.45, 0.13, 0.49]
    sm_scaled_exact = [round(x * 100) for x in softmax(scaled_exact)]
    sm_scaled_2dp = [round(x * 100) for x in softmax(scaled_2dp)]
    ok_vals = scaled_2dp == expected_scaled
    ok_sm = sm_scaled_exact == [40, 29, 11, 8, 11] and (99 <= sum(sm_scaled_exact) <= 101)
    record(
        "L05 p.33 除以 √5 縮放後數值",
        ok_vals,
        f"recomputed_2dp={scaled_2dp}, expected={expected_scaled}",
    )
    record(
        "L05 p.33 縮放後 Softmax（四捨五入總和 99%，容許 ±1%）",
        ok_sm,
        f"from_exact={sm_scaled_exact} (sum={sum(sm_scaled_exact)}%), from_2dp={sm_scaled_2dp} (sum={sum(sm_scaled_2dp)}%), expected=[40, 29, 11, 8, 11]",
    )

    return passed, failed


def scan_wiki_percentage_lists() -> tuple[int, int]:
    print("\n=== 2. 掃描 Wiki 內所有百分比向量加總檢查（容許 99%～101%） ===")
    passed = 0
    failed = 0
    pct_list_re = re.compile(r"[\[\(](\s*\d+(?:\.\d+)?%\s*(?:,\s*\d+(?:\.\d+)?%\s*){1,})[\]\)]")

    for path in sorted(glob.glob("wiki/**/*.md", recursive=True)):
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                for m in pct_list_re.finditer(line):
                    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", m.group(1))]
                    total = sum(nums)
                    ok = 99.0 <= total <= 101.0
                    status = "PASS" if ok else "FAIL"
                    if ok:
                        passed += 1
                    else:
                        failed += 1
                    print(f"[{status}] {path}:{lineno}: {m.group(0)} -> sum={total:g}%")

    if passed == 0 and failed == 0:
        print("(未掃描到括號型百分比向量)")
    return passed, failed


def check_key_numbers_present_in_wiki() -> tuple[int, int]:
    print("\n=== 3. 核對關鍵驗算數值是否確實出現於指定 Wiki 頁 ===")
    checks = [
        ("wiki/sources/lecture-02-neural-networks.md", [("0.61", "61%"), ("0.28", "28%"), ("0.11", "11%"), ("0.89",)]),
        ("wiki/sources/lecture-03-why-ai-differs-each-time.md", [("0.14",), ("0.18",), ("0.36",)]),
        ("wiki/concepts/probability-entropy-and-sampling.md", [("0.14",), ("0.18",), ("0.36",)]),
        (
            "wiki/sources/lecture-04-llm-next-token-prediction.md",
            [("0.70", "70%"), ("0.29", "29%"), ("0.01", "1%"), ("0.57", "57%"), ("0.36", "36%"), ("0.07", "7%"), ("0.86", "86%"), ("0.14", "14%"), ("0.00", "0%")],
        ),
        (
            "wiki/concepts/word-embedding-and-sampling-strategies.md",
            [("0.70", "70%"), ("0.29", "29%"), ("0.01", "1%"), ("0.57", "57%"), ("0.36", "36%"), ("0.07", "7%"), ("0.86", "86%"), ("0.14", "14%"), ("0.00", "0%")],
        ),
        ("wiki/sources/lecture-05-sequence-memory-and-attention.md", [("3.9",), ("3.2",), ("61%",), ("30%",), ("1.74",), ("1.43",), ("40%",), ("29%",)]),
        ("wiki/concepts/transformer-and-self-attention.md", [("3.9",), ("3.2",), ("61%",), ("30%",), ("1.74",), ("1.43",), ("40%",), ("29%",)]),
    ]
    passed = 0
    failed = 0
    for path, token_groups in checks:
        if not os.path.exists(path):
            failed += 1
            print(f"[FAIL] {path}: 檔案不存在")
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        missing = [grp[0] for grp in token_groups if not any(t in text for t in grp)]
        if not missing:
            passed += 1
            print(f"[PASS] {path}: 全部 {len(token_groups)} 組關鍵數值皆存在")
        else:
            failed += 1
            print(f"[FAIL] {path}: 缺少 {missing}")
    return passed, failed


def main() -> int:
    p1, f1 = check_formula_cases()
    p2, f2 = scan_wiki_percentage_lists()
    p3, f3 = check_key_numbers_present_in_wiki()
    total_p = p1 + p2 + p3
    total_f = f1 + f2 + f3
    print(f"\nSUMMARY check_numbers.py: PASS={total_p}, FAIL={total_f}")
    return 0 if total_f == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
