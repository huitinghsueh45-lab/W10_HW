# 確定性檢查腳本執行紀錄：scripts-run2-20261119

- **執行時間**：2026-11-19 14:19
- **對應流程節點**：graph v2 — `A4a`（Wiki 確定性檢查）與 `B4a`（簡報確定性檢查）
- **備註**：本紀錄為 Run 1 完成後導入 `graph v2` 時之首次確定性腳本執行結果，**全數原樣保留（含所有 FAIL 項目）**，未先修改 `wiki/`、`slides/` 或 `report.md`。

---

## 摘要總表

| 腳本 | 對應節點 | 用途 | 結果摘要 | Exit Code |
|---|---|---|---|---:|
| `scripts/check_numbers.py` | A4a | 重算 Wiki 關鍵數值（Softmax、機率總和 ±1%、MSE、Cross Entropy、KL、$\sqrt{5}$ 縮放）並確認存在於 Wiki | `PASS=23, FAIL=1` | `1` |
| `scripts/check_sources.py` | A4a | 檢查 12 頁 Wiki 事實句是否具 `[來源: 檔名 p.X]` 標註 | `FILES=12, FILES_FAIL=7, CHECKED_LINES=341, ISSUES=21` | `1` |
| `scripts/check_links.py` | A4a | 檢查 `[[...]]` 交叉連結、`wiki/index.md` 完整性與 YAML front matter | `PASS=26, FAIL=0` | `0` |
| `scripts/verify_slides.py` | B4a | 驗證 `slides/index.html` 結構、頁尾 Wiki 來源、traceability 對齊與互動元件數據 | `PASS=35, FAIL=0` | `0` |

---

## 一、`python scripts/check_numbers.py` 原始輸出

```text
=== 1. 核心公式與數值重算檢查 ===
[PASS] L02 p.14-19 八哥 Softmax: recomputed=[0.6127, 0.2753, 0.1119] -> rounded=[0.61, 0.28, 0.11], pct=[61, 28, 11] (sum=100%)
[PASS] L02 p.69 單筆平方誤差和: exact=0.8934, rounded_2dp=0.89 (expected 0.89)
[PASS] L03 p.82 MSE 比較: [0.7,0.19,0.11] MSE=0.1382 (≈0.14); [0.7,0.3,0] MSE=0.1800 (≈0.18)
[PASS] L03 p.82 Cross Entropy 比較: both -ln(0.7)=0.3567 (≈0.36), diff=0.000000
[PASS] L03 p.86 Soft Target Q1=[0.7,0.19,0.11]: H(P)=0.8018, H(P,Q1)=0.8025, D_KL(P||Q1)=0.0007
[FAIL] L04 p.17-18 候選字 Softmax: exact_pct=[29.64, 7.53, 40.41, 3.52, 18.9], std_round=[30, 8, 40, 4, 19] (sum=101%), wiki/slide=[30, 7, 40, 4, 19] (sum=100%; 注意第 2 項 7.53% 標準四捨五入為 8%)
[PASS] L04 p.57 Temperature τ=1.0: recomputed_pct=[70, 29, 1] (sum=100%), expected=[70, 29, 1]
[PASS] L04 p.57 Temperature τ=2.0: recomputed_pct=[57, 36, 7] (sum=100%), expected=[57, 36, 7]
[PASS] L04 p.57 Temperature τ=0.5: recomputed_pct=[86, 14, 0] (sum=100%), expected=[86, 14, 0]
[PASS] L05 p.32 原始內積 Softmax: recomputed_pct=[61, 30, 3, 2, 4] (sum=100%), expected=[61, 30, 3, 2, 4]
[PASS] L05 p.33 除以 √5 縮放後數值: recomputed_2dp=[1.74, 1.43, 0.45, 0.13, 0.49], expected=[1.74, 1.43, 0.45, 0.13, 0.49]
[PASS] L05 p.33 縮放後 Softmax（四捨五入總和 99%，容許 ±1%）: from_exact=[40, 29, 11, 8, 11] (sum=99%), from_2dp=[40, 29, 11, 8, 11] (sum=99%), expected=[40, 29, 11, 8, 11]

=== 2. 掃描 Wiki 內所有百分比向量加總檢查（容許 99%～101%） ===
[PASS] wiki\concepts\transformer-and-self-attention.md:44: [61%, 30%, 3%, 2%, 4%] -> sum=100%
[PASS] wiki\concepts\transformer-and-self-attention.md:44: [40%, 29%, 11%, 8%, 11%] -> sum=99%
[PASS] wiki\sources\lecture-04-llm-next-token-prediction.md:30: [30%, 7%, 40%, 4%, 19%] -> sum=100%
[PASS] wiki\sources\lecture-05-sequence-memory-and-attention.md:40: [61%, 30%, 3%, 2%, 4%] -> sum=100%
[PASS] wiki\sources\lecture-05-sequence-memory-and-attention.md:40: [40%, 29%, 11%, 8%, 11%] -> sum=99%

=== 3. 核對關鍵驗算數值是否確實出現於指定 Wiki 頁 ===
[PASS] wiki/sources/lecture-02-neural-networks.md: 全部 4 組關鍵數值皆存在
[PASS] wiki/sources/lecture-03-why-ai-differs-each-time.md: 全部 3 組關鍵數值皆存在
[PASS] wiki/concepts/probability-entropy-and-sampling.md: 全部 3 組關鍵數值皆存在
[PASS] wiki/sources/lecture-04-llm-next-token-prediction.md: 全部 9 組關鍵數值皆存在
[PASS] wiki/concepts/word-embedding-and-sampling-strategies.md: 全部 9 組關鍵數值皆存在
[PASS] wiki/sources/lecture-05-sequence-memory-and-attention.md: 全部 8 組關鍵數值皆存在
[PASS] wiki/concepts/transformer-and-self-attention.md: 全部 8 組關鍵數值皆存在

SUMMARY check_numbers.py: PASS=23, FAIL=1
EXIT=1
```

---

## 二、`python scripts/check_sources.py` 原始輸出

```text
=== Wiki 事實句來源與頁碼檢查（check_sources.py） ===
[FAIL] wiki/concepts\function-mapping.md: checked_lines=18, issues=1
    - L44 [MISSING_SOURCE]: 人類之所以追求能「生成」內容的 AI 模型，源於三個核心動機：
[FAIL] wiki/concepts\neural-networks-and-learning.md: checked_lines=30, issues=3
    - L54 [MISSING_SOURCE]: 電腦如何知道要把參數往哪個方向調，才能讓損失 $L$ 變小？
    - L75 [MISSING_SOURCE]: - **誤解 1：「電腦認得圖片裡是家八哥」**
    - L77 [MISSING_SOURCE]: - **誤解 2：「深度學習就只是高維度的內插法（Interpolation / Curve Fitting）」**
[FAIL] wiki/concepts\probability-entropy-and-sampling.md: checked_lines=25, issues=4
    - L34 [MISSING_SOURCE]: 當真實答案 $y$ 為 One-hot encoding（第 $i$ 類 $y_i=1$、其餘為 0）時，交叉熵簡化為：
    - L59 [MISSING_SOURCE]: - 當神經網路經 Softmax 輸出機率分佈（如 $[0.6, 0.3, 0.1]$）時：
    - L67 [MISSING_SOURCE]: - **誤解 1：「生成式 AI 與鑑別式 AI 的底層原理完全不同；因為生成式 AI 會產生幻覺，所以應該改用鑑別式 AI」**
    - L69 [MISSING_SOURCE]: - **誤解 2：「直接把一組提示詞對應多張不同目標圖片丟進神經網路，就能訓練出有創意的生成模型」**
[FAIL] wiki/concepts\transformer-and-self-attention.md: checked_lines=20, issues=3
    - L14 [MISSING_SOURCE]: 然而，如果模型真的「只輸入前一個字 $x_t$」去預測下一個字 $x_{t+1}$，馬上就會撞上數學矛盾：以 `"今天天氣很好。"` 為例，模型會同時遇到：
    - L15 [MISSING_SOURCE]: - $f_\theta(\text{“天”}) = \text{“天”}$（第一個「天」後面是「天」）
    - L16 [MISSING_SOURCE]: - $f_\theta(\text{“天”}) = \text{“氣”}$（第二個「天」後面是「氣」）
[FAIL] wiki/concepts\transformer-architecture-and-stability.md: checked_lines=25, issues=2
    - L61 [MISSING_SOURCE]: - **誤解 1：「Transformer 裡面每一層的 Attention 都是 Self-Attention（自注意力）」**
    - L63 [MISSING_SOURCE]: - **誤解 2：「位置編碼（Positional Encoding）只是在每個字後面串接一個代表第幾個字的整數 $1, 2, 3, \dots$」**
[FAIL] wiki/concepts\word-embedding-and-sampling-strategies.md: checked_lines=28, issues=3
    - L33 [MISSING_SOURCE]: 透過代理任務訓練出的 Word Embedding 展現了驚人的語意結構：
    - L70 [MISSING_SOURCE]: - **誤解 1：「One-hot encoding 把文字轉成高維度向量後，電腦就能從向量距離看出兩個字意思相近」**
    - L72 [MISSING_SOURCE]: - **誤解 2：「把 Temperature 調高（$\tau > 1$）是為了讓模型變聰明、算得更準」**
[FAIL] wiki/sources\external-vaswani-2017-attention-is-all-you-need.md: checked_lines=28, issues=5
    - L14 [MISSING_SOURCE]: - **專案角色**：作為本專案的**外部交叉查核節點（Cross-Verification Node）**，與第四講 `04LLM只是在猜下一個字？.pdf` 及第五講 `05AI怎麼記得前面說過什麼？.pdf`...
    - L65 [MISSING_SOURCE]: | **Scaled Dot-Product 公式** | 第 4 講 `p.31` 與第 5 講 `p.31`：$\text{Attention}(Q,K,V)=\text{softmax}\left(\frac...
    - L66 [MISSING_SOURCE]: | **為何除以 $\sqrt{d_k}$？** | 第 5 講 `p.31-33`：內積太大時 Softmax「贏者通吃」，除以 $\sqrt{d_k}$ 把數值拉回 0 附近（如同設溫度 $\tau=\sqrt...
    - L67 [MISSING_SOURCE]: | **列向量與矩陣右乘** | 第 4 講 `p.28`、第 5 講 `p.13, p.35`：Google 偏愛列向量，故線性轉換矩陣乘在右邊 $Q=XW^Q$ | `p.5`：$\text{head}_i =...
    - L68 [MISSING_SOURCE]: | **位置編碼足標與直覺** | 第 5 講 `p.46-50`：指出足標 $k$ 應從 0 開始，$\omega_k = 1/10000^{2k/d}$，並以單位圓時鐘解釋 $(\sin, \cos)$ | `...
[PASS] wiki/sources\lecture-01-learn-ai-without-anxiety.md: checked_lines=24, issues=0
[PASS] wiki/sources\lecture-02-neural-networks.md: checked_lines=35, issues=0
[PASS] wiki/sources\lecture-03-why-ai-differs-each-time.md: checked_lines=32, issues=0
[PASS] wiki/sources\lecture-04-llm-next-token-prediction.md: checked_lines=45, issues=0
[PASS] wiki/sources\lecture-05-sequence-memory-and-attention.md: checked_lines=31, issues=0

SUMMARY check_sources.py: FILES=12, FILES_FAIL=7, CHECKED_LINES=341, ISSUES=21
EXIT=1
```

---

## 三、`python scripts/check_links.py` 原始輸出

```text
=== 1. 檢查所有頁面 [[...]] 交叉連結 ===
[PASS] wiki/index.md: 12 links all valid
[PASS] wiki/sources\external-vaswani-2017-attention-is-all-you-need.md: 2 links all valid
[PASS] wiki/sources\lecture-01-learn-ai-without-anxiety.md: 1 links all valid
[PASS] wiki/sources\lecture-02-neural-networks.md: 2 links all valid
[PASS] wiki/sources\lecture-03-why-ai-differs-each-time.md: 3 links all valid
[PASS] wiki/sources\lecture-04-llm-next-token-prediction.md: 4 links all valid
[PASS] wiki/sources\lecture-05-sequence-memory-and-attention.md: 2 links all valid
[PASS] wiki/concepts\function-mapping.md: 3 links all valid
[PASS] wiki/concepts\neural-networks-and-learning.md: 6 links all valid
[PASS] wiki/concepts\probability-entropy-and-sampling.md: 9 links all valid
[PASS] wiki/concepts\transformer-and-self-attention.md: 9 links all valid
[PASS] wiki/concepts\transformer-architecture-and-stability.md: 5 links all valid
[PASS] wiki/concepts\word-embedding-and-sampling-strategies.md: 5 links all valid

=== 2. 檢查 wiki/index.md 收錄完整性（無孤立頁） ===
[PASS] wiki/index.md 收錄全部 12 頁，無孤立頁或無效項目

=== 3. 檢查 YAML Front Matter 欄位 ===
[PASS] wiki/sources\external-vaswani-2017-attention-is-all-you-need.md: type=source, status=linted, updated=2026-11-18
[PASS] wiki/sources\lecture-01-learn-ai-without-anxiety.md: type=source, status=linted, updated=2026-11-18
[PASS] wiki/sources\lecture-02-neural-networks.md: type=source, status=linted, updated=2026-11-18
[PASS] wiki/sources\lecture-03-why-ai-differs-each-time.md: type=source, status=linted, updated=2026-11-18
[PASS] wiki/sources\lecture-04-llm-next-token-prediction.md: type=source, status=linted, updated=2026-11-18
[PASS] wiki/sources\lecture-05-sequence-memory-and-attention.md: type=source, status=linted, updated=2026-11-18
[PASS] wiki/concepts\function-mapping.md: type=concept, status=linted, updated=2026-11-18
[PASS] wiki/concepts\neural-networks-and-learning.md: type=concept, status=linted, updated=2026-11-18
[PASS] wiki/concepts\probability-entropy-and-sampling.md: type=concept, status=linted, updated=2026-11-18
[PASS] wiki/concepts\transformer-and-self-attention.md: type=concept, status=linted, updated=2026-11-18
[PASS] wiki/concepts\transformer-architecture-and-stability.md: type=concept, status=linted, updated=2026-11-18
[PASS] wiki/concepts\word-embedding-and-sampling-strategies.md: type=concept, status=linted, updated=2026-11-18

SUMMARY check_links.py: PASS=26, FAIL=0
EXIT=0
```

---

## 四、`python scripts/verify_slides.py` 原始輸出

```text
=== 1. 單一自足 HTML 與基本結構檢查 ===
[PASS] 零外部 CDN 依賴: external_refs=[]
[PASS] 投影片總頁數: found 13 slides (expected 13)
[PASS] 鍵盤左右鍵翻頁事件: ArrowRight & ArrowLeft handlers present

=== 2. 逐頁頁尾 Wiki 來源格式與檔案存在性檢查 ===
[PASS] Slide 1 頁尾來源 (2 頁): items=['concepts/function-mapping.md', 'sources/lecture-01-learn-ai-without-anxiety.md']
[PASS] Slide 2 頁尾來源 (2 頁): items=['concepts/function-mapping.md', 'concepts/probability-entropy-and-sampling.md']
[PASS] Slide 3 頁尾來源 (2 頁): items=['concepts/function-mapping.md', 'sources/lecture-02-neural-networks.md']
[PASS] Slide 4 頁尾來源 (2 頁): items=['concepts/neural-networks-and-learning.md', 'sources/lecture-02-neural-networks.md']
[PASS] Slide 5 頁尾來源 (2 頁): items=['concepts/word-embedding-and-sampling-strategies.md', 'concepts/transformer-and-self-attention.md']
[PASS] Slide 6 頁尾來源 (2 頁): items=['concepts/neural-networks-and-learning.md', 'concepts/probability-entropy-and-sampling.md']
[PASS] Slide 7 頁尾來源 (2 頁): items=['concepts/probability-entropy-and-sampling.md', 'concepts/word-embedding-and-sampling-strategies.md']
[PASS] Slide 8 頁尾來源 (2 頁): items=['concepts/transformer-and-self-attention.md', 'sources/external-vaswani-2017-attention-is-all-you-need.md']
[PASS] Slide 9 頁尾來源 (2 頁): items=['concepts/transformer-architecture-and-stability.md', 'sources/external-vaswani-2017-attention-is-all-you-need.md']
[PASS] Slide 10 頁尾來源 (3 頁): items=['concepts/function-mapping.md', 'concepts/neural-networks-and-learning.md', 'concepts/transformer-and-self-attention.md']
[PASS] Slide 11 頁尾來源 (4 頁): items=['concepts/probability-entropy-and-sampling.md', 'concepts/word-embedding-and-sampling-strategies.md', 'concepts/transformer-and-self-attention.md', 'concepts/transformer-architecture-and-stability.md']
[PASS] Slide 12 頁尾來源 (4 頁): items=['concepts/function-mapping.md', 'concepts/neural-networks-and-learning.md', 'concepts/probability-entropy-and-sampling.md', 'concepts/transformer-and-self-attention.md']
[PASS] Slide 13 頁尾來源 (6 頁): items=['concepts/function-mapping.md', 'concepts/neural-networks-and-learning.md', 'concepts/probability-entropy-and-sampling.md', 'concepts/word-embedding-and-sampling-strategies.md', 'concepts/transformer-and-self-attention.md', 'concepts/transformer-architecture-and-stability.md']

=== 3. 比對 checks/traceability.md 來源一致性 ===
[PASS] Traceability ↔ HTML Slide 1: match (2 pages)
[PASS] Traceability ↔ HTML Slide 2: match (2 pages)
[PASS] Traceability ↔ HTML Slide 3: match (2 pages)
[PASS] Traceability ↔ HTML Slide 4: match (2 pages)
[PASS] Traceability ↔ HTML Slide 5: match (2 pages)
[PASS] Traceability ↔ HTML Slide 6: match (2 pages)
[PASS] Traceability ↔ HTML Slide 7: match (2 pages)
[PASS] Traceability ↔ HTML Slide 8: match (2 pages)
[PASS] Traceability ↔ HTML Slide 9: match (2 pages)
[PASS] Traceability ↔ HTML Slide 10: match (3 pages)
[PASS] Traceability ↔ HTML Slide 11: match (4 pages)
[PASS] Traceability ↔ HTML Slide 12: match (4 pages)
[PASS] Traceability ↔ HTML Slide 13: match (6 pages)

=== 4. 互動元件數據與數學重算驗證 ===
[PASS] Slide 7 溫度模擬器 τ=0.5: html=[86, 14, 0], recomputed=[86, 14, 0] (sum=100%)
[PASS] Slide 7 溫度模擬器 τ=2.0: html=[57, 36, 7], recomputed=[57, 36, 7] (sum=100%)
[PASS] Slide 7 溫度模擬器 τ=1.0: html=[70, 29, 1], recomputed=[70, 29, 1] (sum=100%)
[PASS] Slide 8 √d_k 切換器（原始內積）: html=[61, 30, 3, 2, 4], recomputed=[61, 30, 3, 2, 4] (sum=100%)
[PASS] Slide 8 √d_k 切換器（除以 √5）: html=[40, 29, 11, 8, 11], recomputed=[40, 29, 11, 8, 11] (sum=99%)
[PASS] Slide 13 自我檢測題數與解析來源: quiz_items=5, ans_sources=5, missing=[]

SUMMARY verify_slides.py: PASS=35, FAIL=0
EXIT=0
```
