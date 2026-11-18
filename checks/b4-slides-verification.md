# 簡報驗證與內容抽查紀錄：b4-slides-verification

- **檢查時間**：2026-11-18 16:39
- **檢查對象**：`slides/index.html`（共 13 頁教學簡報）
- **對照依據**：`checks/traceability.md` 與 `wiki/concepts/*.md`、`wiki/sources/*.md`

---

## 一、結構、互動與可追溯性檢查

1. **單一自足 HTML 架構**：`slides/index.html` 內嵌完整 CSS、SVG 概念流程圖、原生分數／根號／向量數學排版與互動 JavaScript，無外部 CDN 依賴，離線或直接雙擊皆可完整渲染。
2. **鍵盤翻頁與進度導覽**：支援 `ArrowRight` / `PageDown` / `Space`（下一頁）、`ArrowLeft` / `PageUp`（上一頁）、`Home` / `End` 及頂部 7 大教學階段導覽膠囊切換。
3. **頁尾來源格式檢查（初檢發現 1 項路徑前綴省略並完成修正）**：
   - **初檢發現問題**：透過 `verify_slides.py` 檢查 13 頁 `.wiki-source-badge` 時，發現第 13 頁（自我檢測）頁尾寫為 `來源 Wiki：concepts/function-mapping.md、neural-networks-and-learning.md...`，第 2～6 個概念頁省略了 `concepts/` 目錄前綴，不符合規劃書第七節 `來源 Wiki：concepts/xxx.md` 之統一格式。
   - **修正結果**：已將第 13 頁頁尾補齊為完整相對路徑 `concepts/neural-networks-and-learning.md` 等，複檢 13 頁全部通過。
   - *註*：初次嘗試以內建無頭瀏覽器開啟本地伺服器 `http://127.0.0.1:8765/slides/index.html` 時，因沙盒環境的 `ORIGIN_PERMISSION_REQUIRED` 授權提示等待逾時（60 秒）而未載入，改以 Python 結構剖析腳本結合本地直接開啟驗證。

---

## 二、內容抽查（抽查 4 頁與 Wiki 知識庫逐一核對）

| 抽查頁次 | 抽查內容與數值 | 對照 Wiki 頁面 | 核對結果 |
|---|---|---|---|
| **Slide 3**（函數映射與張量） | 0～3 階張量例子（`9487`、`[9,4,8,7]`、$20\times N$ 股價矩陣、RGB 彩色影像）；八哥辨識分數 `(1.9, 1.1, 0.2)` 經 Softmax 轉為 `(61%, 28%, 11%)` | `concepts/function-mapping.md`<br>`sources/lecture-02-neural-networks.md` | **完全一致**（無任何 Wiki 以外之編造內容） |
| **Slide 6**（損失函數與梯度下降） | 正解 `y=[1,0,0]` 下，`[0.7, 0.19, 0.11]` 與 `[0.7, 0.3, 0]` 之 MSE 為 `0.14` vs. `0.18`、Cross Entropy 同為 `0.36`；KL 散度在 Soft Target `[0.7, 0.2, 0.1]` 下為 `0.01` vs. `0.03`（3 倍）；梯度下降公式 $\theta \leftarrow \theta - \eta \nabla L$ | `concepts/neural-networks-and-learning.md`<br>`concepts/probability-entropy-and-sampling.md` | **完全一致** |
| **Slide 7**（溫度 $\tau$ 與 Top-p） | 互動模擬器分數 `[4.3, 3.4, 0.2]` 在 $\tau=1$ 為 `[70%, 29%, 1%]`、$\tau=2$ 為 `[57%, 36%, 7%]`、$\tau=0.5$ 為 `[86%, 14%, 0%]`；Top-p (Nucleus Sampling, ICLR 2020) 公式 $\sum_{i=1}^N p_i > p$ 與 $p'_k = p_k / P$ | `concepts/word-embedding-and-sampling-strategies.md` | **完全一致** |
| **Slide 8**（Transformer 自注意力） | $\text{Attention}(Q,K,V)=\text{softmax}(QK^T/\sqrt{d_k})V$；內積變異數 $d_k$（Vaswani Footnote 4）與第五講數值 `[3.9, 3.2, 1, 0.3, 1.1]` $\to$ `[61%, 30%, 3%, 2%, 4%]`、除以 $\sqrt{5}$ 後 `[1.74, 1.43, 0.45, 0.13, 0.49]` $\to$ `[40%, 29%, 11%, 8%, 11%]` | `concepts/transformer-and-self-attention.md`<br>`sources/external-vaswani-2017-attention-is-all-you-need.md` | **完全一致** |
