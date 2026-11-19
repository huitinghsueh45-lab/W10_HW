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

---

## 三、Run 2 階段 B5：人工閘門抽查 3 頁紀錄（2026-11-19）

> 依據 `AGENTS.md` graph v2 之 **B5 人工閘門**要求，由使用者親自抽查 **Slide 3、Slide 5、Slide 6**（共 3 頁），對照頁尾 Wiki 頁與原始課程講義頁碼完成人工核對：

| 抽查頁次 | 對照之 Wiki 頁與原始講義頁碼 | 人工抽查項目 | 人工抽查結果 |
|---|---|---|---|
| **Slide 3**（函數映射與張量） | `concepts/function-mapping.md`、`sources/lecture-02-neural-networks.md`（`L01 p.46–48`, `L02 p.4–5, p.9–22`） | 0～3 階張量實例、函數映射式與八哥 Softmax `(1.9, 1.1, 0.2) → (61%, 28%, 11%)` | **確認無誤** |
| **Slide 5**（LLM 猜下一個字與詞嵌入） | `concepts/word-embedding-and-sampling-strategies.md`、`concepts/transformer-and-self-attention.md`（`L04 p.8–18, p.66–83`） | 「今天天氣很好。」一對多違反函數、Word2Vec CBOW / Skip-Gram、`W^T x = h` 與語意關係（已修正 `S-05`） | **確認無誤** |
| **Slide 6**（損失函數、Cross Entropy 與梯度下降） | `concepts/neural-networks-and-learning.md`、`concepts/probability-entropy-and-sampling.md`、`sources/lecture-02-neural-networks.md`（`L02 p.63–104`, `L03 p.64–90`） | MSE（SSE 註記）`0.14 / 0.18` vs. Cross Entropy `0.36`、KL 散度 3 倍差、梯度下降與偏微分例題（已修正 `S-06` 頁尾） | **確認無誤** |

---

## 四、線上版實測（GitHub Pages 部署與驗證）

- **線上瀏覽網址**：`https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html`
- **部署問題與處置歷程**：
  1. 初次推送至 GitHub 後，GitHub Pages 預設啟用 Jekyll 建置程序，因專案 Markdown 內含 LaTeX / Liquid 樣式語法導致 Jekyll 建置失敗。
  2. 於專案根目錄新增空檔 `.nojekyll`（初版 commit `4fca11e`，已納入 git 追蹤）以跳過 Jekyll 建置，並修正曾誤於錯誤工作目錄執行 git 指令之操作失誤後重新推送。
  3. 透過 GitHub Actions 確認 `pages-build-deployment` 工作流之 `build` 與 `deploy` 皆為成功，並於**一般登入視窗與無痕視窗**實測開啟上述線上網址，確認排版、鍵盤翻頁、互動元件與 5 題自我檢測皆可正常運作。
- **流程教訓**：B4／B5 驗證不應僅停留在「本機雙擊開啟」，必須涵蓋**線上部署後實測（含無痕視窗確認無權限／快取依賴）**。
