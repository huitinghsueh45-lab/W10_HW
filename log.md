# log.md

## 2026-11-18 INIT
- 比對上週 Docsify 專案與本週要求，確認缺少 Wiki 層、ingest、簡報、loop 設計與檢查紀錄，新開專案。
- 選定方案 A：沿用課程講義 + 1 篇外部資料交叉查核。
- 方法依據：Karpathy LLM Wiki（raw → wiki，Ingest / Query / Lint）。
- 限制來源上限 6 篇，確保每篇可討論與查核。
- 建立專案目錄結構（`AGENTS.md`、`log.md`、`wiki/index.md`、`wiki/sources/`、`wiki/concepts/`、`checks/`、`slides/`、`raw/lectures/`、`raw/external/`）。
- 人工確認採用**方案 1**（共 6 篇來源資料）：
  - `raw/lectures/01如何不焦慮地學AI.pdf`（119 頁）
  - `raw/lectures/02神經網路的概念.pdf`（123 頁）
  - `raw/lectures/03AI為什麼每次都不一樣？.pdf`（102 頁）
  - `raw/lectures/04LLM只是在猜下一個字？.pdf`（115 頁）
  - `raw/lectures/05AI怎麼記得前面說過什麼？.pdf`（86 頁）
  - `raw/external/Vaswani_2017_Attention_Is_All_You_Need.pdf`（15 頁，外部交叉查核節點）
  - **選擇理由**：串起「函數映射 → 神經網路 → 機率與熵／隨機抽樣 → Next-token 與 Transformer → 序列記憶與 Attention」的完整教學主線，並以 Vaswani et al. (2017) 原論文作為跨來源交叉查核節點。

## 2026-11-18 14:44 INGEST｜01如何不焦慮地學AI.pdf
- **節點**：A2 → A3 → A4 → A5
- **分段範圍**：第一段 p.1–60、第二段 p.61–119（共 119 頁）
- **討論結論**：人工確認 4 大重點（三大 AI 焦慮与原理學習、AI 作為函數映射 $f_\theta$ 與八哥辨識案例、生成式 AI 三大起源動機、Colab 函數視覺化與互動）及預計建立之 2 個頁面。
- **產出**：
  - 建立 `wiki/sources/lecture-01-learn-ai-without-anxiety.md`
  - 建立 `wiki/concepts/function-mapping.md`
  - 建立 `checks/lint-20261118-01.md`
  - 更新 `wiki/index.md`
- **Lint 結果**：初檢不通過（1 項公式與頁碼對應不精確）→ 修正後複檢通過
- **錯誤紀錄**：
  - 錯誤類型：頁碼錯誤 / 公式合成過度推論（另外在 A1 讀取階段發現 LaTeX Beamer 投影片編號字型編碼將數字映射為 `L, M, -, ⁄, O, q, r, s, t, u`，已統一改用 PDF 實體頁碼避免頁碼錯亂）
  - 發生位置：`wiki/concepts/function-mapping.md` 第二節公式
  - 如何發現：A4 Lint 逐頁核對原文公式符號與頁碼時發現，`p.47-48` 原文僅畫出 `輸入 → f_θ → [y_1, y_2, y_3]`，並未寫出 `y = f_θ(x)`（`f(x)` 出現在 `p.101` 與 `p.105`）
  - 處理方式：將公式修正為原文 `p.47-48` 的映射表示並補齊 `p.101, p.105` 頁碼標註，重跑 Lint 全部通過。

## 2026-11-18 15:04 INGEST｜02神經網路的概念.pdf
- **節點**：A2 → A3 → A4 → A5
- **分段範圍**：第一段 p.1–60、第二段 p.61–123（共 123 頁）
- **討論結論**：人工確認 4 大重點（張量與 One-hot / Softmax 機率轉換、神經元與 3+1 種架構及萬用近似定理、損失函數 $L(\theta)$ 與梯度下降法 $\theta - \eta \nabla L$、MNIST 手寫數字辨識 DNN 實作）及預計新建／更新之 3 個頁面。
- **產出**：
  - 建立 `wiki/sources/lecture-02-neural-networks.md`
  - 建立 `wiki/concepts/neural-networks-and-learning.md`
  - 更新 `wiki/concepts/function-mapping.md`
  - 建立 `checks/lint-20261118-02.md`
  - 更新 `wiki/index.md`
- **Lint 結果**：通過（於跨頁矛盾檢查發現原始教材內部圖示類別順序差異並加註消解）
- **錯誤紀錄**：
  - 錯誤類型：跨頁類別順序不一致（原始投影片內部差異導致的潛在矛盾）與數值四捨五入標註
  - 發生位置：`02神經網路的概念.pdf` 之 `p.11-15`（及第一講 `p.48`）將八哥三類別順序定為「土八哥、白尾八哥、家八哥」，但同份講義 `p.21, p.60, p.67` 圖示將第 2、3 類順序標為「土八哥、家八哥、白尾八哥」；另 `p.69` 平方誤差和 $(1-0.23)^2+(0-0.43)^2+(0-0.34)^2$ 精確值為 $0.8934$，原文取兩位小數寫為 $0.89$。
  - 如何發現：A4 Lint 第 2 項（數字核對）與第 6 項（與既有頁面無矛盾）交叉比對第一講與第二講各頁圖示時發現。
  - 處理方式：於 `lecture-02-neural-networks.md` 與 `function-mapping.md` 明確加註頁次間的類別順序差異與四捨五入說明，確保讀者與後續簡報引用時不會混淆。

## 2026-11-18 15:18 INGEST｜03AI為什麼每次都不一樣？.pdf
- **節點**：A2 → A3 → A4 → A5
- **分段範圍**：第一段 p.1–60、第二段 p.61–102（共 102 頁）
- **討論結論**：人工確認 3 大重點（一對多平均困境與潛張量 $z$ 及 GAN/StyleGAN 演進、資訊量 $I(x)$／夏農熵 $H(P)$／交叉熵 $H(P,Q)$／KL 散度 $D_{KL}$、隨機性抽樣來源與鑑別式／生成式同源性）及預計新建／更新之 3 個頁面。
- **產出**：
  - 建立 `wiki/sources/lecture-03-why-ai-differs-each-time.md`
  - 建立 `wiki/concepts/probability-entropy-and-sampling.md`
  - 更新 `wiki/concepts/neural-networks-and-learning.md`
  - 建立 `checks/lint-20261118-03.md`
  - 更新 `wiki/index.md`
- **Lint 結果**：通過（攔截並修正 PDF 表格文字流順序倒置造成的數值錯配風險）
- **錯誤紀錄**：
  - 錯誤類型：PDF 表格物件抽取順序倒置導致的數值錯配風險（數字與公式核對）
  - 發生位置：`03AI為什麼每次都不一樣？.pdf` 之 `p.82`（MSE 與 Cross Entropy 比較表）
  - 如何發現：`pypdf` 抽取 `p.82` 純文字流時，將表格數值 `0.14 0.36 | 0.18 0.36` 與列標籤 `[0.7,0.3,0] | [0.7,0.19,0.11]` 上下顛倒輸出；若直接照文字流順序配對，會誤把 `[0.7,0.3,0]` 配成 MSE `0.14`。經調閱 PDF `cm` 垂直座標（`[0.7,0.19,0.11]` 在上列 `cy=304.5`、`[0.7,0.3,0]` 在下列 `cy=144.6`）並以平方和公式驗算（$0.3^2+0.19^2+0.11^2=0.1382\approx 0.14$ vs. $0.3^2+0.3^2+0=0.18$）發現此問題。
  - 處理方式：依座標與數學驗算結果將正確對應關係寫入 Wiki 與 `checks/lint-20261118-03.md`（此案例亦證明將「公式驗算與座標檢查」前移至讀取／Lint 階段的重要性）。

## 2026-11-18 15:38 INGEST｜04LLM只是在猜下一個字？.pdf
- **節點**：A2 → A3 → A4 → A5
- **分段範圍**：第一段 p.1–60、第二段 p.61–115（共 115 頁）
- **討論結論**：人工確認 4 大重點（Next-token prediction 與單字一對多違反函數需引入序列記憶、RNN vs. Transformer Self-Attention 四步驟與公式、Karpathy 幻覺觀點與 GPT-3/Llama 3 規模、Temperature/Top-k/Top-p 選字策略與 Word2Vec 詞嵌入）及預計新建／更新之 4 個頁面。
- **產出**：
  - 建立 `wiki/sources/lecture-04-llm-next-token-prediction.md`
  - 建立 `wiki/concepts/word-embedding-and-sampling-strategies.md`
  - 建立 `wiki/concepts/transformer-and-self-attention.md`
  - 更新 `wiki/concepts/probability-entropy-and-sampling.md`
  - 建立 `checks/lint-20261118-04.md`
  - 更新 `wiki/index.md`
- **Lint 結果**：通過（攔截 PDF 向量繪圖根號遺漏風險與自訂字型數字編碼）
- **錯誤紀錄**：
  - 錯誤類型：公式符號抽取遺漏風險（PDF 向量路徑繪製根號 $\sqrt{\phantom{x}}$）與特殊字型數字映射
  - 發生位置：`04LLM只是在猜下一個字？.pdf` 之 `p.31`（Attention 公式中 $\sqrt{d_K}$ 的根號線為 PDF 向量路徑，純文字抽取僅得 `dK`）與 `p.42-45, p.75`（字型將 `2, 3, 128` 映射為 `˘, 0, Z[V`）
  - 如何發現：在讀取與 A4 Lint 階段檢查 PDF Content Stream 繪圖指令（`1455.551 493.756 m ...`）並對照頁面上下文文字（如 `p.75` 下方明文「128 個神經元」）發現。
  - 處理方式：確認向量繪圖根號存在後以完整公式 $\text{softmax}\left(\frac{QK^T}{\sqrt{d_K}}\right)V$ 寫入 Wiki，並預計於第 6 篇 Vaswani et al. (2017) 原論文進行跨來源交叉查核。

## 2026-11-18 15:54 INGEST｜05AI怎麼記得前面說過什麼？.pdf
- **節點**：A2 → A3 → A4 → A5
- **分段範圍**：第一段 p.1–60、第二段 p.61–86（共 86 頁）
- **討論結論**：人工確認 4 大重點（RNN 遞歸層公式與列向量線性組合、QKV 推導與除以 $\sqrt{d_k}$ 抑制 Softmax 贏者通吃、Multi-Head 與 Encoder/Decoder 三種注意力及 Positional Encoding 時鐘直覺、ResNet 殘差連結與 LayerNorm/RMSNorm/DyT）及預計新建／更新之 3 個頁面。
- **產出**：
  - 建立 `wiki/sources/lecture-05-sequence-memory-and-attention.md`
  - 建立 `wiki/concepts/transformer-architecture-and-stability.md`
  - 更新 `wiki/concepts/transformer-and-self-attention.md`
  - 建立 `checks/lint-20261118-05.md`
  - 更新 `wiki/index.md`
- **Lint 結果**：初檢不通過（抓出 A2 摘要中對 `p.32-33` 自訂字型數字的誤讀）→ 修正後複檢通過
- **錯誤紀錄**：
  - 錯誤類型：數字不符（PDF 自訂字型將數字 `3` 映射為字元 `'1'`、將數字 `1` 映射為字元 `'"'` 造成的人機初讀誤判）
  - 發生位置：`05AI怎麼記得前面說過什麼？.pdf` 之 `p.32-33`（Softmax 贏者通吃與除以 $\sqrt{d_k}$ 的數值例子）
  - 如何發現：在 A2 初讀時因看到 `'1.Ô 1.{ " !.1 "."'` 的字元 `'1'`，誤以為是 `1.9, 1.3...` 並推估百分比為 `[51%, 20%, 4%, 3%, 8%]`；在執行 A4 Lint 第 2 項（數字與公式驗算）時，發現百分比總和僅 $86\% \neq 100\%$，且與 $\text{softmax}$ 計算不符！遂根據 `p.43` 明文對照 `[Ô, Y, z, w] = [9, 4, 8, 7]` 完整解出字型映射表（`!=0, "=1, {=2, 1=3, Y=4, $=5, j=6, w=7, z=8, Ô=9`），驗算出正確原值為 `[3.9, 3.2, 1, 0.3, 1.1]` $\xrightarrow{\text{softmax}}$ `[61%, 30%, 3%, 2%, 4%]`，除以 $\sqrt{5}$ 後為 `[1.74, 1.43, 0.45, 0.13, 0.49]` $\xrightarrow{\text{softmax}}$ `[40%, 29%, 11%, 8%, 11%]`。
  - 處理方式：將驗證無誤之真實數值寫入 `lecture-05-sequence-memory-and-attention.md` 與 `transformer-and-self-attention.md`，並將此「字型映射陷阱與機率總和驗算」完整記錄於 `checks/lint-20261118-05.md`。

## 2026-11-18 16:05 INGEST｜Vaswani_2017_Attention_Is_All_You_Need.pdf
- **節點**：A2 → A3 → A4 → A5
- **分段範圍**：單段 p.1–15（共 15 頁，未超過 60 頁）
- **討論結論**：人工確認 4 大重點（Table 1 平行化 $O(1)$ 與路徑長度 $O(1)$、Scaled Dot-Product Attention 變異數 $d_k$ 縮放證明、Multi-Head Attention $h=8, d_{\text{model}}=512$ 與 $-\infty$ Masking、Positional Encoding 相對位置線性函數性質）及預計新建／更新之 3 個頁面。
- **產出**：
  - 建立 `wiki/sources/external-vaswani-2017-attention-is-all-you-need.md`
  - 更新 `wiki/concepts/transformer-and-self-attention.md`
  - 更新 `wiki/concepts/transformer-architecture-and-stability.md`
  - 建立 `checks/lint-20261118-06.md`
  - 更新 `wiki/index.md`
- **Lint 結果**：通過（完成第 4、5 講與原論文之 4 項跨來源交叉查核）
- **錯誤紀錄**：無新增錯誤；成功以原論文 Equation (1) 與 Footnote 4 跨來源驗證第四、五講 PDF 向量繪圖根號 $\sqrt{d_k}$ 與縮放原理。

## 2026-11-18 16:06 QUERY & OUTLINE CHECK｜簡報大綱與可追溯性檢查
- **節點**：B1 → B2
- **討論結論**：只讀 `wiki/` 擬定 13 頁教學型 HTML 簡報大綱，完整涵蓋「為什麼（Slides 1–2）→ 是什麼（Slides 3–5）→ 怎麼運作（Slides 6–9）→ 例子（Slide 10）→ 常見誤解（Slide 11）→ 小結（Slide 12）→ 自我檢測（Slide 13）」七大教學段落。
- **產出**：建立 `checks/traceability.md`（簡報頁 ↔ Wiki 來源頁 ↔ raw 原始資料與頁碼對照表）。
- **大綱檢查（B2）結果**：通過（13 頁簡報每頁皆明確對應 1～5 個 Wiki 頁面，無任何 Wiki 以外之內容）。

## 2026-11-18 16:39 SLIDES GENERATION & VERIFICATION｜slides/index.html
- **節點**：B3 → B4 → B5
- **討論結論**：人工確認 13 頁簡報大綱與 `checks/traceability.md` 後，生成單一自足 HTML 簡報並執行結構與內容抽查驗證。
- **產出**：
  - 建立 `slides/index.html`（13 頁互動式教學簡報，含鍵盤翻頁、溫度 $\tau$ 模擬器、$\sqrt{d_k}$ 縮放切換器、5 題自我檢測問答）
  - 建立 `checks/b4-slides-verification.md`
- **驗證結果（B4）**：初檢發現 1 項頁尾來源路徑前綴省略問題 → 修正後複檢通過
- **錯誤紀錄**：
  - 錯誤類型：格式問題（頁尾 Wiki 來源路徑前綴不一致）與內建瀏覽器沙盒權限逾時
  - 發生位置：`slides/index.html` 第 13 頁 `.wiki-source-badge`
  - 如何發現：執行 `verify_slides.py` 自動解析全部 13 頁頁尾標籤時，發現第 13 頁僅第一個檔案寫出 `concepts/function-mapping.md`，其餘 5 個檔案省略了 `concepts/` 前綴；另內建瀏覽器代理連線本地伺服器時因 `ORIGIN_PERMISSION_REQUIRED` 等待使用者點擊逾時 60 秒而阻斷。
  - 處理方式：補齊第 13 頁所有概念頁之 `concepts/` 路徑前綴，並以腳本完成全部 13 頁 DOM 結構、互動數據與 Wiki 存在性驗證，記錄於 `checks/b4-slides-verification.md`。

---

## 錯誤統計表（階段 C 總結，支撐反思）

| 節點 | 執行次數 | 出錯／攔截次數 | 主要錯誤類型 | 如何發現 |
|---|---|---|---|---|
| **A2 先討論** | 6 | 1 | PDF 自訂字型將數字 `3` 映射為 `'1'` 導致初讀誤判（第 5 講 `p.32`） | 進入 A4 Lint 執行機率總和（$86\% \neq 100\%$）與 $\text{softmax}$ 數學驗算時發現 |
| **A3 Ingest** | 6 | 1 | 公式合成過度推論與頁碼未精確分離（第 1 講 `p.47-48` vs. `p.101, 105`） | A4 Lint 逐頁核對原文符號時發現 |
| **A4 Lint（含原文抽取核對）** | 6 | 3（成功攔截原文/抽取陷阱） | ① 原始投影片內部類別順序不一致（第 2 講 `p.11-15` vs. `p.21, 67`）<br>② PDF 表格文字流上下倒置（第 3 講 `p.82` MSE `0.14` vs. `0.18`）<br>③ PDF 根號 $\sqrt{d_k}$ 為向量繪圖路徑、純文字抽取遺漏（第 4、5 講 `p.31`） | ① 跨頁與跨來源矛盾檢查（Lint #6）<br>② 調閱 PDF `cm` 垂直座標與 MSE 公式驗算（Lint #2）<br>③ 檢查 PDF Content Stream 繪圖指令並與第 6 篇 Vaswani 原論文交叉查核 |
| **B1 Query / B2 大綱檢查** | 1 | 0 | 無（大綱階段即強制建立 `checks/traceability.md` 鎖定 Wiki 來源） | B2 大綱檢查一次通過 |
| **B3 生成 HTML / B4 實測** | 1 | 1 | 第 13 頁頁尾 `.wiki-source-badge` 省略部分 `concepts/` 前綴 | B4 結構驗證腳本與抽查發現並立即修正 |

## 2026-11-18 16:49 DOCS & TASK LOG｜report.md、TASK_LOG.md
- **節點**：C1（完成報告與專案進度彙整）
- **產出**：
  - 建立 `report.md`（完整 7 節作業報告，含修改前後 Loop/Graph 流程圖、錯誤統計與檢查前移反思）
  - 建立 `TASK_LOG.md`（整理目前完成進度、三大架構決策與後續 GitHub Pages 部署／繳交待辦事項）

## 2026-11-18 16:55 DEPLOY｜.gitignore 調整、公開網址補入 report.md 與推送 GitHub
- **節點**：B4（人工本機實測完成）→ C1（部署上線與最終報告定稿）
- **討論結論**：
  - 使用者已完成本機雙擊檢視 `slides/index.html` 並體驗互動元件，確認無誤。
  - 調整 `.gitignore` 排除超大課程講義 PDF（`raw/lectures/*.pdf`）、`HW_Plan/` 與 `desktop.ini`。
  - 將 GitHub 與 GitHub Pages 公開連結補入 `report.md` 第三節並推送至遠端儲存庫 `origin`（`https://github.com/huitinghsueh45-lab/W10_HW.git`）。
- **產出**：更新 `.gitignore`、`report.md`、`README.md`、`TASK_LOG.md` 並完成 Git Commit & Push。



