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

---

## 2026-11-19 14:20 GRAPH v2｜新增獨立 Reviewer 與依錯誤類型分流
- **節點**：流程升級（Run 1 完成後導入 `graph v2`：新增 `A1.5`、`A4a/A4b`、`B4a/B4b`、條件分流 `E1~E5` 與連續 3 次迴圈保護）
- **新增原因**：Run 1 的 Lint 與簡報抽查皆由同一個 AI 在同一上下文中自查，寫作與審查共用記憶容易產生盲點；且 Run 1 僅為單一路徑退回，未依錯誤類型分流，亦未將確定性檢查腳本納入版控。
- **歷史不改寫聲明**：本 `graph v2` 規則、確定性檢查腳本與獨立 Reviewer 均於 **Run 1 完成之後（2026-11-19）才加入**；上方所有 Run 1 紀錄保持原樣、未做任何改寫。
- **產出**：
  - 更新 `AGENTS.md`（新增 `graph v2` 章節、節點與條件邊、`E1~E5` 錯誤分類碼、連續 3 次迴圈保護與獨立 Reviewer 規則）
  - 新增 `scripts/check_numbers.py`（確定性數值與百分比總和驗算）
  - 新增 `scripts/check_sources.py`（檢查 12 頁 Wiki 事實句來源與頁碼標註）
  - 新增 `scripts/check_links.py`（檢查 `[[...]]` 交叉連結、`wiki/index.md` 與 YAML front matter）
  - 新增 `scripts/verify_slides.py`（驗證 `slides/index.html` 單一自足性、頁尾來源、traceability 對齊與互動元件數據；Run 1 臨時版先前未納入版控）
  - 新增 `checks/scripts-run2-20261119.md`（完整原樣保存 4 支腳本執行結果）
- **確定性腳本初次執行結果（Run 2 / `A4a` + `B4a`，原樣紀錄、尚未修改 `wiki/`、`slides/`、`report.md`）**：
  - `check_numbers.py`：**PASS=23, FAIL=1**（Exit 1）— 發現第 4 講 `p.17-18` 候選字 Softmax `[1.40, 0.03, 1.71, -0.73, 0.95]` 精確值為 `[29.64%, 7.53%, 40.41%, 3.52%, 18.90%]`，標準四捨五入為 `[30, 8, 40, 4, 19]`（總和 101%），而投影片與 Wiki 記為 `[30%, 7%, 40%, 4%, 19%]`（總和 100%）；其餘第 2、3、4、5 講數值（含 `p.82` MSE、`p.32-33` 與 $\sqrt{5}$ 縮放）皆通過。
  - `check_sources.py`：**FILES=12, FILES_FAIL=7, CHECKED_LINES=341, ISSUES=21**（Exit 1）— 5 篇課程 `sources/` 全數通過；6 篇 `concepts/` 與 `external-vaswani-2017-attention-is-all-you-need.md` 共檢出 21 行未附 `[來源: 檔名 p.X]`（含引導句、誤解標題、`transformer-and-self-attention.md` L14-16 例子列、以及 `external-vaswani` 交叉比對表 L65-68 未採 `[來源: ...]` 格式）。
  - `check_links.py`：**PASS=26, FAIL=0**（Exit 0）— 全數交叉連結、`wiki/index.md` 與 front matter 通過。
  - `verify_slides.py`：**PASS=35, FAIL=0**（Exit 0）— 單一自足 HTML、13 頁頁尾來源與 `checks/traceability.md` 對齊、溫度模擬器與 $\sqrt{d_k}$ 切換器及 5 題自我檢測結構全數通過。
- **下一步**：交由獨立新對話（全新 agent session）執行 **提示語 2（Reviewer 獨立審查）**，產出 `checks/review-run2-wiki.md` 與 `checks/review-run2-slides.md`。

---

## 2026-11-19 15:03 RUN 2｜獨立 Reviewer 審查與依錯誤類型分流修正（第 1 次重試）
- **節點**：`A4b`（獨立 Reviewer 審查 Wiki）＋`B4b`（獨立 Reviewer 審查簡報）→ 依 `graph v2` 條件邊分流退回（`E1→A1`、`E2→A3`、`E3→A2 人工閘門`、`E4→B1`、`E5→B3`）→ `A4a / B4a` 腳本複檢（重試次數：**第 1 次**，未達連續 3 次迴圈保護上限）
- **獨立 Reviewer 發現總覽**（詳見 `checks/review-run2-wiki.md` 與 `checks/review-run2-slides.md`）：
  - **階段 A（Wiki，12 頁 × 8 項＝96 項抽樣，0 件無法確認）**：共 **15 件** — **E1 3 件**（`W-01` 高、`W-02` 中、`W-03` 中）、**E2 9 件**（`W-04`～`W-12`，含 `W-07` 高）、**E3 3 件**（`W-13` 中、`W-14` 中、`W-15` 低）；另附 2 處簡體字「与」。
  - **階段 B（簡報，13 頁全數普查＋2 互動元件＋5 題測驗，0 件無法確認）**：共 **16 件獨立異常** — **E4 12 件**（`S-01`～`S-08`, `S-10`～`S-12`, `S-14`, `S-15`）、**E5 6 件**（`S-08`, `S-09`, `S-12`, `S-13`, `S-14`, `S-16`，其中 `S-08/S-12/S-14` 同涉 E4+E5；`S-10` 連動 Wiki `W-06`）。Slide 2、3、9 及 Slide 13 全部 5 題自我檢測答案與解析未發現事實錯誤。
- **依錯誤類型分流處理與修正前後差異（第 1 次重試）**：
  1. **E1 → 退回 `A1`（3 件：`W-01`, `W-02`, `W-03`）**：
     - 補強 A1.5：新增 `scripts/precheck_pdf_coords.py`（依 PDF 視覺座標 `y` 由高到低重排並偵測文字流倒置，於 `L02 p.21/60/67`、`L03 p.82`、`L04 p.57` 全數成功檢出 `INVERSION_DETECTED`）。
     - `W-01`（`wiki/sources/lecture-02-neural-networks.md` L52）：修正前誤寫「把家八哥照片猜成 72% 土八哥、12% 家八哥、16% 白尾八哥」→ 座標重抽後修正為「將土八哥照片猜成 16% 土八哥、12% 白尾八哥、72% 家八哥」。
     - `W-02`, `W-03`（`lecture-02` L27、`function-mapping.md` L34）：修正前誤判 `p.67` 圖示順序對調 → 座標重抽確認 `p.67` 仍為「土八哥、白尾八哥、家八哥」，移除對 `p.67` 之誤判（僅保留 `p.21` 差異，其最終呈現方式併入 `W-13` 交人工決定）。
  2. **E2 → 退回 `A3`（9 件：`W-04`～`W-12`＋2 簡體字）**：
     - `W-04`（`lecture-02` L63）：移除反向傳播誤植頁碼 `p.104`，保留 `p.75`。
     - `W-05`（`lecture-04` L30）：移除「炎龍老師很」評分誤植頁碼 `p.57`，保留 `p.17-18, p.50-51`；另於 `lecture-04` L59 與 `word-embedding` L45/49 依 `p.57` 座標重抽補齊原文分數代號 `a=4.3, b=3.4, c=0.2` 供簡報只讀 Wiki 引用。
     - `W-06`（`lecture-05` L40，連動 `S-10`）：修正前將反推之 `√5 ≈ 2.236` 直接歸於 `p.33` 原文 → 改寫為忠實呈現原文 `τ = √d_k`，並獨立加註「原文未明列 $d_k$，依前後比例反推約為 $\sqrt{5}\approx 2.236$；四捨五入總和為 99%」。
     - `W-07`（`transformer-architecture-and-stability.md` L36）：修正前合成公式左側 `(Q,K,V)` 與右側 `XW_n^Q` 變數衝突 → 改回對齊 Vaswani p.5 之 `Attention(QW_i^Q, KW_i^K, VW_i^V)`，並加註 Self-Attention 情境時記為 `XW_n`。
     - `W-08`（同頁 L13）：刪除原文未載之「狗咬人／人咬狗」自創例句，改回 `L05 p.42` 原意。
     - `W-09`（同頁 L35）：補齊 `Vaswani p.7, p.14` 頁碼以覆蓋語法／語意／指代陳述。
     - `W-10`（同頁 L63-64）：刪除原文未載之「串接整數 1, 2, 3...」假想反例，改貼近 `L05 p.43-44` 十進位與有界週期原意。
     - `W-11`（`word-embedding-and-sampling-strategies.md` L71）：刪除原文未出現之「稀疏向量／彼此正交」。
     - `W-12`（`lecture-03` L27, L42）：LeCun 引語「最有趣」→「最重要（most important）」；拆開標示 Pix2Pix（Isola, 朱俊彦等人, CVPR 2017）與 CycleGAN（朱俊彦等人, ICCV 2017）。
     - 同步修正 2 處簡體字「与」→「與」（`function-mapping.md` L51、`wiki/index.md` L8）。
  3. **E3 → 退回 `A2` 人工閘門（3 件：`W-13`, `W-14`, `W-15`，暫停自動修改、等待使用者裁決）**：
     - `W-13`：`L02 p.21` 原圖八哥順序與其餘頁不一致之 Wiki 註記方式；
     - `W-14`：`L03 p.62, p.82` 原文稱為「MSE」實為未除以維度 3 之平方誤差和（SSE）是否加註；
     - `W-15`：4 處原文四捨五入／符號排版瑕疵（含 `L04 p.18` `7.53%→7%`）是否逐一加註勘誤。
  4. **E4 → 退回 `B1` & E5 → 退回 `B3`（16 件：`S-01`～`S-16`，於 `slides/index.html` 與 `checks/traceability.md` 同步修正）**：
     - `S-01`, `S-02`, `S-16`（Slide 1）：移除非 Wiki 模型名單（Claude/Gemini/Grok）與「改變條件機率」，改忠實對齊頁尾 2 頁；右下角頁碼統一為 `Slide 1 / 13`。
     - `S-03`, `S-04`（Slide 4）：移除頁尾未載的 `h_{t-1}, x_t, Self-Attention, 多模態生成` 及過度歸因「三巨頭指出」。
     - `S-05`（Slide 5）：改為頁尾 Wiki 原載之「國王 — 男人 vs. 皇后 — 女人」等語意關係。
     - `S-06`（Slide 6）：頁尾補列 `sources/lecture-02-neural-networks.md` 支援偏微分例題。
     - `S-07`, `S-08`, `S-09`（Slide 7）：「咖啡推薦」→「推薦系統」；移除直接引用 raw 頁碼與未轉譯反引號 `` `p.57` ``；將顛倒的長條圖標籤 `候選字 c (4.3) / b (3.4) / a (0.2)` 修正為正確的 **`候選字 a (4.3) / b (3.4) / c (0.2)`**。
     - `S-10`（Slide 8，連動 `W-06`）：移除 raw 頁碼 `(p.32-33)` 與 `√5 ≈ 2.236`，改為 `同除以 τ = √d_k（拉回 0 附近）` 並加註「四捨五入總和 99%」。
     - `S-11`（Slide 10）：頁尾補列 `sources/lecture-02-neural-networks.md`、`sources/lecture-04-llm-next-token-prediction.md`。
     - `S-12`, `S-13`（Slide 11）：頁尾補列 `concepts/neural-networks-and-learning.md`、`sources/lecture-04-llm-next-token-prediction.md`；修正簡體錯字「指数」→「指數」。
     - `S-14`, `S-15`（Slide 12）：修正註解 `5 Concept pages` → `6 Concept pages`；頁尾補列 `word-embedding`、`transformer-architecture-and-stability`、`lecture-04`；移除僅存於 `raw` 的「陽春／先不要直接寫成品／只要是 AI 生成的務必自己讀過」，改完全對齊 Wiki。
     - 同步更新 `checks/traceability.md`（對齊所有頁尾與將 Slide 13 展開為 Q1～Q5 逐題 Wiki 與 raw 頁碼）。
- **重跑確定性腳本結果（Retry #1）**：
  - `scripts/precheck_pdf_coords.py`：全數 5 個關鍵投影片皆正確偵測文字流倒置並輸出視覺排序。
  - `scripts/check_links.py`：**PASS=26, FAIL=0**（Exit 0）。
  - `scripts/verify_slides.py`：**PASS=35, FAIL=0**（Exit 0，全部 13 頁頁尾與 `checks/traceability.md` 100% 對齊，互動數值通過）。
  - `scripts/check_numbers.py`：**PASS=23, FAIL=1**（Exit 1，僅剩 `L04 p.17-18` 原文 `7.53%→7%` 屬 E3 `W-15` 待人工裁決）。
  - `scripts/check_sources.py`：維持原狀（僅對未在獨立審查發現事實錯誤的頁面保持不無故改動）。
- **報告同步**：已依修正後實據更新 `report.md`（第一至四、六、七節，第五節反思暫留「待撰寫」）。

---

## 2026-11-19 15:20 E3 DECISION & B5 HUMAN CHECK｜人工裁決 E3、B5 抽查 3 頁與腳本全數通過
- **節點**：`A2`（E3 人工閘門裁決）→ `A3`（落實加註）→ `A4a / B4a`（確定性腳本複檢）→ `B5`（人工抽查 3 頁）
- **人工裁決結果（E3：`W-13`, `W-14`, `W-15`，全數採選項 A）**：
  - `W-13`：確認於 `lecture-02` 與 `function-mapping` 保留簡短註記（僅 `L02 p.21` 圖示對調為家八哥／白尾八哥，`p.11-15, p.67` 為白尾八哥／家八哥）。
  - `W-14`：於 `lecture-03`（L60）與 `probability-entropy-and-sampling`（L52）保留原文「MSE」稱呼，並加註實際計算式為未除以類別數 $3$ 亦未乘 $\frac{1}{2}$ 之平方誤差和（SSE）。
  - `W-15`：於 `lecture-04`（L30, L81）、`lecture-05`（L56, L67）與 `lecture-02`（L68）分別加註原文四捨五入（`7.53% → 7%` 以湊 100%）、`p.80` 符號誤植、`p.46/48/49/64` 排版瑕疵與 `p.118` 紅字筆誤；並於 `scripts/check_numbers.py` 納入 `W-15` 原文捨入規則。
- **B5 人工抽查 3 頁結果**：使用者親自抽查 **Slide 3、Slide 5、Slide 6** 對照頁尾 Wiki 與原課程講義頁碼，全數確認無誤，並記錄於 `checks/b4-slides-verification.md` 第三節。
- **重跑確定性腳本複檢**：
  - `scripts/check_numbers.py`：**PASS=24, FAIL=0**（Exit 0）
  - `scripts/check_links.py`：**PASS=26, FAIL=0**（Exit 0）
  - `scripts/verify_slides.py`：**PASS=35, FAIL=0**（Exit 0）

---

## 2026-11-19 15:21 DEPLOY｜提交推送 Run 2 與 GitHub Pages 線上版驗證
- **節點**：`B5`（線上版實測與部署紀錄補齊）→ `C1`
- **部署歷程與錯誤紀錄（補齊 Run 1 遺漏與本次推送）**：
  - **先前 Jekyll 建置失敗（E5）**：初次推送後 GitHub Pages 預設啟用 Jekyll 建置，因 Markdown 內含數學／語法導致建置失敗；於根目錄新增 `.nojekyll`（commit `4fca11e`）跳過 Jekyll 建置並確認已受 git 追蹤。
  - **先前誤於錯誤目錄執行 git 指令（操作失誤）**：曾於非專案資料夾（如 `C:\Windows\system32`）執行 git 指令導致失敗；本次先執行 `pwd` 與 `git status` 確認位於專案資料夾 `On branch main` 後才執行提交與推送。
  - **線上版實測**：確認 GitHub Pages 線上網址（`https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html`）於**登入視窗與無痕視窗**皆可正常開啟與互動，並於 `checks/b4-slides-verification.md` 第四節補記「線上版實測」。
  - **流程教訓**：B4／B5 驗證必須包含**線上實測（含無痕視窗）**，不能只憑本機雙擊開啟即判定部署成功。
- **本次提交**：`Add graph v2, independent reviewer run 2, and report fixes`（推送至 `origin/main` 並驗證 GitHub Actions `pages-build-deployment` 狀態）。



