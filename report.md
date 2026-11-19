# 用 LLM Wiki 做一份教學 HTML 簡報：專案報告

- **繳交標題**：`中興 8113026207 科管博 薛慧婷 生成式AI入門：從函數到Transformer`
- **建立日期**：2026-11-18（Run 2 獨立審查與報告修正更新：2026-11-19）

---

## 一、LLM Wiki 主題與簡短介紹

### 1. 主題設定
本專案主題為**「生成式 AI 入門：從函數 $f_\theta$ 到 Transformer」**。旨在為「完全不熟悉生成式 AI 的初學者」建立一套嚴謹、可追溯、無編造的知識庫（LLM Wiki），並以此 Wiki 為**唯一知識來源**，製作一份涵蓋「為什麼 → 是什麼 → 怎麼運作 → 例子 → 常見誤解 → 小結 → 自我檢測」七大教學階段的互動式單一 HTML 簡報。

### 2. 資料來源清單與選擇理由（5 份課程講義 + 1 份外部交叉查核論文）
依據 Andrej Karpathy 提出的 **LLM Wiki 模式**（`raw/ → wiki/`，核心操作為 **Ingest / Query / Lint**），本專案嚴格控制原始資料上限為 **6 篇**，確保每一篇皆能落實「先討論、後生成」與逐頁查核。

> **用語統一說明**：`log.md` 初期紀錄中的**「方案 A」**指整體作業策略（沿用課程講義＋1 篇外部資料交叉查核，而非完全重選外部教材），而**「方案 1」**指該策略下具體選定的 6 篇教材清單（Week 01～05 課程講義＋Vaswani et al. 2017 原論文），兩者為上下位規劃關係而非不同方案。

| 編號 | 檔案路徑（唯讀 `raw/`） | 頁數與分段範圍 | 公開狀態 | 選擇理由與在教學主線中的角色 |
|---|---|---|---|---|
| 1 | `raw/lectures/01如何不焦慮地學AI.pdf` | 119 頁（p.1–60、p.61–119） | 授課教材（未公開上傳） | 建立學習動機（用原理對抗三大 AI 焦慮）與最底層核心觀念：AI 模型是輸入到輸出的**函數映射 $f_\theta$**（八哥辨識案例）及生成式 AI 三大起源動機（創作、1950 圖靈問題、費曼名言）。 |
| 2 | `raw/lectures/02神經網路的概念.pdf` | 123 頁（p.1–60、p.61–123） | 授課教材（未公開上傳） | 將函數具體化為**張量（Tensor）**、**One-hot Encoding** 與 **Softmax** 機率轉換，解析基本運算單元**神經元** $h=\varphi(\sum w_i x_i + b)$、3+1 種架構、損失函數 $L(\theta)$ 與**梯度下降法** $\theta \leftarrow \theta - \eta \nabla L$，並提供 MNIST 手寫辨識實作案例。 |
| 3 | `raw/lectures/03AI為什麼每次都不一樣？.pdf` | 102 頁（p.1–60、p.61–102） | 授課教材（未公開上傳） | 解答生成式 AI 的核心矛盾：為何「一對多」硬訓練會變成四不像平均？引入**潛張量 $z$**（GAN / StyleGAN）、**資訊量 $I(x)$、夏農熵 $H(P)$、交叉熵 $H(P,Q)$、KL 散度**，以及**依 Softmax 機率分佈隨機抽樣**（並破除鑑別式 vs. 生成式二分迷思）。 |
| 4 | `raw/lectures/04LLM只是在猜下一個字？.pdf` | 115 頁（p.1–60、p.61–115） | 授課教材（未公開上傳） | 進入大型語言模型（LLM）：說明為何「單看前一個字」違反函數定義而需引入序列記憶、**Word2Vec 詞嵌入（CBOW / Skip-Gram，權重即記憶 $W^T x = h$）**、**Temperature $\tau$ / Top-k / Top-p（Nucleus Sampling）** 選字策略，以及 **Transformer Self-Attention** 與 Karpathy「幻覺（作夢機器）」觀點。 |
| 5 | `raw/lectures/05AI怎麼記得前面說過什麼？.pdf` | 86 頁（p.1–60、p.61–86） | 授課教材（未公開上傳） | 深入推導 RNN 遞歸層公式、Google 列向量右乘傳統（$Q=XW^Q$）、**為何除以 $\sqrt{d_k}$（抑制 Softmax 贏者通吃）**、Encoder/Decoder 三種注意力（Self / Masked / Cross-Attention）、**位置編碼 $(\sin, \cos)$ 單位圓時鐘**，以及 **ResNet 殘差連結 $z+\ell(z)$ 與 LayerNorm / RMSNorm / DyT**。 |
| 6 | `raw/external/Vaswani_2017_Attention_Is_All_You_Need.pdf` | 15 頁（單段 p.1–15） | 公開論文（arXiv，隨附於 repo） | **外部交叉查核節點**（Vaswani et al., NIPS 2017 原論文）：用來與第 4、5 講交叉驗證 Scaled Dot-Product Attention 根號 $\sqrt{d_k}$、Footnote 4 內積變異數 $d_k$ 證明、Table 1 平行化 $O(1)$ 與路徑長度 $O(1)$、$-\infty$ Masking 及 $PE_{pos+k}$ 相對位置線性性質。 |

---

## 二、loop / graph 設計與修改前後演進

本專案之工作流程歷經兩個真實演進版本：**Run 1 實際執行的是單一 AI 自查的 `graph v1`**；在 Run 1 完成後的檢討發現「寫作與審查共用上下文之盲點」與「單一退回路徑無法區分抽取錯誤／推論錯誤／原文矛盾」後，才於 **2026-11-19 正式導入 `graph v2`**（新增確定性檢查腳本、上下文隔離之獨立 Reviewer、依 `E1～E5` 錯誤碼分流退回與連續 3 次迴圈保護），並執行了完整的 Run 2。

### 1. graph v1（Run 1 實際執行之原始流程：單一 AI 自查 Loop）

```mermaid
flowchart TD
    subgraph A1_sub["階段 A（Run 1）：逐篇建立 Wiki（單一 AI 自查）"]
        V1_A1["A1 讀取 raw 資料<br/>（超過 60 頁分兩段）"] --> V1_A2["A2 先討論<br/>【人工閘門】"]
        V1_A2 -- "人工修正" --> V1_A2
        V1_A2 -- "人工確認" --> V1_A3["A3 Ingest 撰寫 Wiki"]
        V1_A3 --> V1_A4{"A4 Lint（同一 AI 自查 6 項清單）"}
        V1_A4 -- "不通過" --> V1_A3
        V1_A4 -- "通過" --> V1_A5["A5 更新 index 與 log"]
        V1_A5 --> V1_A6{"還有未處理資料？"}
        V1_A6 -- "是" --> V1_A1
    end
    V1_A6 -- "否（6 篇完成）" --> V1_B1
    subgraph B1_sub["階段 B（Run 1）：製作簡報"]
        V1_B1["B1 Query Wiki（只讀 wiki/）"] --> V1_B2{"B2 大綱與可追溯性檢查<br/>【人工閘門】"}
        V1_B2 -- "不通過" --> V1_B1
        V1_B2 -- "通過" --> V1_B3["B3 生成單一 HTML 簡報"]
        V1_B3 --> V1_B4{"B4 臨時腳本＋同一 AI 抽查 4 頁<br/>＋本機雙擊實測"}
        V1_B4 -- "不通過" --> V1_B3
        V1_B4 -- "通過" --> V1_B5["B5 簡報完成"]
    end
    V1_B5 --> V1_C1["階段 C：彙整報告與部署"]
```

### 2. graph v2（Run 1 後導入之升級流程：確定性腳本＋獨立 Reviewer＋錯誤分流＋迴圈保護）

```mermaid
flowchart TD
    subgraph A2_sub["階段 A（graph v2）：建立與獨立審查 Wiki（逐篇循環）"]
        A1["A1 讀取 raw"] --> A15["A1.5 確定性預檢腳本<br/>座標排序 precheck_pdf_coords.py<br/>字型映射、向量符號、機率總和"]
        A15 --> A2["A2 先討論／E3 原文矛盾裁決<br/>【人工閘門】"]
        A2 --> A3["A3 Ingest 撰寫／修正 Wiki"]
        A3 --> A4a["A4a 確定性檢查腳本<br/>check_numbers / check_sources / check_links"]
        A4a --> A4b{"A4b 獨立 Reviewer（全新對話、唯讀）<br/>只看 Wiki 頁 + 對應 raw 頁"}
        A4b -- "通過" --> A5["A5 更新 index 與 log"]
        A4b -- "E1 抽取／字型／座標／向量" --> A1
        A4b -- "E2 過度推論／頁碼／編造" --> A3
        A4b -- "E3 原文本身不一致" --> A2
    end
    A5 --> A6{"還有資料？"}
    A6 -- "是" --> A1
    A6 -- "否" --> B1
    subgraph B2_sub["階段 B（graph v2）：製作與獨立審查簡報"]
        B1["B1 Query Wiki（只讀 wiki/）"] --> B2{"B2 大綱與可追溯性檢查<br/>【人工閘門】"}
        B2 -- "不通過" --> B1
        B2 -- "通過" --> B3["B3 生成／修正 HTML"]
        B3 --> B4a["B4a 腳本：verify_slides.py<br/>結構、頁尾、traceability、互動數據"]
        B4a --> B4b{"B4b 獨立 Reviewer（全新對話、唯讀）<br/>13 頁全數陳述 ↔ 頁尾 Wiki"}
        B4b -- "E4 混入 Wiki 以外內容" --> B1
        B4b -- "E5 格式／互動／部署問題" --> B3
        B4b -- "E1~E3 Wiki 本身有誤" --> A4b
        B4b -- "通過" --> B5["B5 人工抽查 3 頁與線上實測<br/>【人工閘門】"]
    end
    B5 --> C1["階段 C：報告與反思"]
```

> **迴圈保護（Loop Guard）**：任一節點**連續 3 次不通過**時，必須立即停止自動重試，完整記錄失敗原因並交由人工判斷，不得無限重試。

### 3. 各節點規格表（含重複執行與人工閘門說明）

| 節點 | 類型／是否重複 | 輸入 | 輸出 | 通過標準 | 失敗／分流處置 |
|---|---|---|---|---|---|
| **A1 / A1.5 讀取與確定性預檢** | 逐篇重複（6 次；E1 退回時重跑） | 單篇 `raw/` PDF 檔 | 分段文字、`precheck_pdf_coords.py` 視覺座標排序與向量檢查結果 | 超過 60 頁分段；偵測文字流倒置、字型編碼與向量符號 | 重新以視覺座標／渲染圖抽取該頁 |
| **A2 先討論／E3 裁決** | **【人工閘門】**（逐篇執行；E3 退回時停等人工決定） | 預檢重點或 Reviewer 提出之 E3 選項 | 人工確認之 Ingest 計畫或 E3 裁決結論 | 人類確認重點範圍無偏、對原文矛盾作出裁決 | 人工意見修正或暫停等待決定，未確認前不可寫入 |
| **A3 Ingest** | 逐篇重複（E2 退回時重跑） | 人工確認之計畫或 E2 修正清單 | `wiki/sources/*.md`、`wiki/concepts/*.md` | 標準 YAML front matter；事實句標註 `[來源: 檔名 p.X]`；不憑記憶補完 | 退回修正並記錄重試次數（上限 3 次） |
| **A4a 確定性檢查腳本** | 每次 A3 後執行 | `wiki/` 全部頁面 | `checks/scripts-run2-*.md` | `check_numbers.py`、`check_sources.py`、`check_links.py` 執行結果原樣紀錄 | 標記數值、來源或連結異常供審查參考 |
| **A4b 獨立 Reviewer（Wiki）** | **獨立新對話（唯讀）** | 待審 `wiki/` 頁 + 對應 `raw/` 頁碼 | `checks/review-run2-wiki.md` | 每頁至少抽 8 項（共 96 項）回到 `raw/` 與重算核對無誤 | **E1→A1**、**E2→A3**、**E3→A2（人工）** |
| **B1 Query / B2 大綱檢查** | **B2 為【人工閘門】**（E4 退回時重跑 B1） | **僅限 `wiki/` 內檔案** | 13 頁大綱 + `checks/traceability.md` | 嚴禁引用 Wiki 以外內容；每頁皆有明確 Wiki 頁與 7 段教學結構 | 退回 B1 重整（若需補充內容則先回階段 A 補 Wiki） |
| **B3 生成 / B4a 腳本驗證** | E5 退回時重跑 B3 | 通過之大綱 + `wiki/` | `slides/index.html` + `verify_slides.py` 結果 | 單一自足 HTML、鍵盤翻頁、13 頁頁尾與 `traceability.md` 對齊、互動數據通過重算 | 退回 B3 修正 HTML（上限 3 次） |
| **B4b 獨立 Reviewer（簡報）** | **獨立新對話（唯讀）** | `slides/index.html` + `wiki/` | `checks/review-run2-slides.md` | 13 頁全數陳述、互動元件與 5 題測驗皆獲頁尾 Wiki 支持且無格式錯誤 | **E4→B1**、**E5→B3**、**E1~E3→A4b** |
| **B5 人工抽查與線上實測** | **【人工閘門】** | 定稿 `slides/index.html` + GitHub Pages 網址 | `checks/b4-slides-verification.md` 人工抽查 3 頁與線上版紀錄 | 人類親自抽查 3 頁對照 Wiki 與原講義，並於無痕視窗驗證線上版正常 | 發現問題依錯誤碼退回對應節點 |

---

## 三、成果連結與專案檔案結構

> **資料公開說明**：課程講義 PDF（`raw/lectures/*.pdf`）屬於授課教材，未公開上傳至 GitHub（已於 `.gitignore` 排除）；外部交叉查核論文 `raw/external/Vaswani_2017_Attention_Is_All_You_Need.pdf` 為公開 arXiv 資料，隨附於儲存庫中。

### 1. 線上公開連結（GitHub & GitHub Pages）
- **GitHub 專案總覽**：https://github.com/huitinghsueh45-lab/W10_HW
- **LLM Wiki 知識庫連結（`wiki/`）**：https://github.com/huitinghsueh45-lab/W10_HW/tree/main/wiki
- **教學 HTML 簡報線上瀏覽連結（GitHub Pages）**：https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html
- **確定性檢查腳本（`scripts/`）**：https://github.com/huitinghsueh45-lab/W10_HW/tree/main/scripts
- **檢查紀錄與獨立審查報告（`checks/`）**：https://github.com/huitinghsueh45-lab/W10_HW/tree/main/checks
- **完整操作與錯誤紀錄（`log.md`）**：https://github.com/huitinghsueh45-lab/W10_HW/blob/main/log.md

### 2. 專案目錄檔案清單（GitHub 連結）
- **專案規則（含 graph v2）**：[AGENTS.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/AGENTS.md)
- **LLM Wiki 目錄索引**：[wiki/index.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/index.md)
  - **6 篇來源摘要頁（`wiki/sources/`）**：
    1. [lecture-01-learn-ai-without-anxiety.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/sources/lecture-01-learn-ai-without-anxiety.md)
    2. [lecture-02-neural-networks.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/sources/lecture-02-neural-networks.md)
    3. [lecture-03-why-ai-differs-each-time.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/sources/lecture-03-why-ai-differs-each-time.md)
    4. [lecture-04-llm-next-token-prediction.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/sources/lecture-04-llm-next-token-prediction.md)
    5. [lecture-05-sequence-memory-and-attention.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/sources/lecture-05-sequence-memory-and-attention.md)
    6. [external-vaswani-2017-attention-is-all-you-need.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/sources/external-vaswani-2017-attention-is-all-you-need.md)
  - **6 篇跨來源概念知識頁（`wiki/concepts/`）**：
    1. [function-mapping.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/concepts/function-mapping.md)（函數映射與 AI 模型本質）
    2. [neural-networks-and-learning.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/concepts/neural-networks-and-learning.md)（神經網路與梯度下降學習機制）
    3. [probability-entropy-and-sampling.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/concepts/probability-entropy-and-sampling.md)（機率分佈、資訊熵與生成隨機抽樣）
    4. [word-embedding-and-sampling-strategies.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/concepts/word-embedding-and-sampling-strategies.md)（詞嵌入表徵與選字抽樣策略）
    5. [transformer-and-self-attention.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/concepts/transformer-and-self-attention.md)（大型語言模型與 Transformer 自注意力機制）
    6. [transformer-architecture-and-stability.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/wiki/concepts/transformer-architecture-and-stability.md)（Transformer 完整架構：位置編碼、殘差連結與正規化）
- **教學 HTML 簡報成品**：[slides/index.html](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/slides/index.html)
- **操作與錯誤紀錄**：[log.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/log.md)
- **確定性檢查腳本（`scripts/`）**：
  - [precheck_pdf_coords.py](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/scripts/precheck_pdf_coords.py)（A1.5 PDF 視覺座標排序與倒置偵測）
  - [check_numbers.py](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/scripts/check_numbers.py)（A4a 數值與機率總和重算）
  - [check_sources.py](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/scripts/check_sources.py)（A4a Wiki 事實句來源標註檢查）
  - [check_links.py](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/scripts/check_links.py)（A4a 交叉連結與 `index.md` 完整性檢查）
  - [verify_slides.py](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/scripts/verify_slides.py)（B4a 簡報結構、頁尾與互動數據驗證）
- **檢查與審查紀錄（`checks/`）**：
  - Run 1 Lint：[lint-20261118-01.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/lint-20261118-01.md) ～ [lint-20261118-06.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/lint-20261118-06.md)
  - 可追溯性與簡報驗證：[traceability.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/traceability.md)、[b4-slides-verification.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/b4-slides-verification.md)
  - Run 2 腳本與獨立 Reviewer 審查：[audit-run1-20261119.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/audit-run1-20261119.md)、[scripts-run2-20261119.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/scripts-run2-20261119.md)、[scripts-run2-20261119-retry2.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/scripts-run2-20261119-retry2.md)、[review-run2-wiki.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/review-run2-wiki.md)、[review-run2-slides.md](https://github.com/huitinghsueh45-lab/W10_HW/blob/main/checks/review-run2-slides.md)

---

## 四、實際執行的檢查紀錄與錯誤統計表

> **資料範圍與誠實揭露**：
> 1. 授課講義 PDF（`raw/lectures/`）為未公開上傳之課堂教材，外部論文 `Vaswani_2017_Attention_Is_All_You_Need.pdf` 為公開資料。
> 2. **A1.5 導入時序**：經唯讀稽核核實，Run 1 執行階段 A（2026-11-18）並未實際執行獨立的 A1.5 節點（第 5 講 `p.32-33` 字型誤判係於 **A4 Lint** 數學驗算時抓出）；A1.5 係於 Run 1 完成後整理命名，並於 2026-11-19 `graph v2` 實作 `scripts/precheck_pdf_coords.py` 納入正式流程。
> 3. **Run 1 簡報抽查範圍**：Run 1 的 `checks/b4-slides-verification.md` 係由生成簡報的同一 AI 僅抽查 **4 頁（Slide 3, 6, 7, 8）**並以未保存之臨時腳本檢查頁尾結構，其餘 9 頁未逐項核對內容；直到 Run 2 獨立 Reviewer 才對全部 13 頁進行 100% 普查。

### 1. Run 1（2026-11-18，graph v1 單一 AI 自查）完整問題統計表

（依 `log.md`、`checks/lint-*.md`、`checks/b4-slides-verification.md` 與 `git log` 全數重整，補齊原統計表漏列之 4 項問題，共 **10 件**：E1 5 件、E2 1 件、E3 1 件、E4 0 件、E5 3 件。）

| 編號 | 發生位置（講義／檔案與頁碼） | 錯誤碼 | 發現節點 | 問題內容與發現方式 |
|---|---|---|---|---|
| R1-01 | `01如何不焦慮地學AI.pdf` 全份投影片頁碼 | **E1** | A1 讀取 | 投影片頁碼字型映射為 `L, M, -, ⁄, O, q, r, s, t, u`，改以 PDF 實體頁碼紀錄（`log.md` L29） |
| R1-02 | `01如何不焦慮地學AI.pdf` `p.47-48` vs. `p.101, 105` | **E2** | A4 Lint #2 | `function-mapping.md` 初稿合成公式 `y=f_θ(x)` 並僅標 `p.47-48`；逐頁核對符號後修正（`lint-01`） |
| R1-03 | `02神經網路的概念.pdf` `p.11-15` vs. `p.21`（Run 1 亦誤含 `p.67`） | **E3** | A4 Lint #2, #6 | 跨頁比對發現八哥類別順序差異（註：Run 2 獨立視覺審查另發現 `p.67` 實未對調，見 R2-W02） |
| R1-04 | `03AI為什麼每次都不一樣？.pdf` `p.82` | **E1** | A4 Lint #2 | `pypdf` 純文字流上下列倒置，調閱 PDF `cm` 垂直座標並以平方和驗算攔截 `0.14` vs. `0.18`（`lint-03`） |
| R1-05 | `04LLM只是在猜下一個字？.pdf` & 第 5 講 `p.31` | **E1** | A1 / A4 Lint #2 | $\sqrt{d_k}$ 根號與分數線為向量繪圖路徑、純文字抽出僅見 `dK`；檢視 Content Stream 並以 Vaswani 原論文交叉確認 |
| R1-06 | `04LLM只是在猜下一個字？.pdf` `p.16, 42-45, 75, 86, 93` | **E1** | A1 / A4 Lint #2 | 自訂字型將 `2, 3, 128` 映射為 `˘, 0, Z[V`，對照頁面明文解碼核對（`lint-04`） |
| R1-07 | `05AI怎麼記得前面說過什麼？.pdf` `p.32-33` | **E1** | A4 Lint #2 | 自訂字型將 `3` 映射為 `'1'` 導致 A2 誤判為 `[51%, 20%, 4%, 3%, 8%]`；A4 檢查總和 `86% ≠ 100%` 並依 `p.43` 解碼還原：`[3.9, 3.2, 1, 0.3, 1.1] → [61%, 30%, 3%, 2%, 4%]`，縮放後 `[1.74, 1.43, 0.45, 0.13, 0.49] → [40%, 29%, 11%, 8%, 11%]`（**四捨五入後總和為 99%**） |
| R1-08 | `slides/index.html` Slide 13 `.wiki-source-badge` | **E5** | B4 臨時腳本 | 第 13 頁第 2～6 個概念頁省略 `concepts/` 目錄前綴，發現後補齊 |
| R1-09 | B4 本地預覽 `http://127.0.0.1:8765/slides/index.html` | **E5** | B4 驗證環境 | 內建無頭瀏覽器因 `ORIGIN_PERMISSION_REQUIRED` 授權等待逾時 60 秒阻斷 |
| R1-10 | GitHub Pages 部署 | **E5** | 部署階段 | GitHub Pages 預設啟用 Jekyll 建置失敗，後補新增 `.nojekyll`（commit `4fca11e`）跳過 Jekyll 建置 |

### 2. Run 2（2026-11-19，graph v2 確定性腳本＋全新對話獨立 Reviewer）統計表

Run 2 由獨立 Reviewer 於全新對話以**唯讀**權限執行：**階段 A（Wiki）**對全部 12 頁每頁隨機抽 8 項（共 **96 項**）搭配 PDF 視覺頁面渲染與 Python 重算；**階段 B（簡報）**對全部 **13 頁**＋2 個互動元件＋5 題自我檢測進行 **100% 普查**，兩部分「無法確認」件數皆為 **0 件**。

| 審查階段與節點 | 檢查對象與方法 | 錯誤碼 | 件數（高/中/低） | 代表性發現與分流處置（第 1 次重試） |
|---|---|---|---:|---|
| **A4a 確定性腳本** | `check_numbers.py`、`check_sources.py`、`check_links.py` | 腳本檢出 | 數值 FAIL=1；來源行=21；連結=0 | 抓出 `L04 p.17-18` 精確 Softmax 第 2 項 `7.53%` 四捨五入為 `8%`（原投影片寫 `7%` 以湊 100%）；連結與 front matter 全過 |
| **A4b 獨立 Reviewer（Wiki）** | 12 頁 × 8 項＝96 項（視覺渲染＋重算） | **E1** | **3**（1/2/0） | **`W-01`（高）**：`L02 p.60` 文字流倒置導致輸入鳥種與機率完全顛倒（實為土八哥猜成 16%/12%/72% 家八哥）；`W-02, W-03`：`L02 p.67` 實未對調 → **退回 A1** 座標重抽修正並新增 `precheck_pdf_coords.py` |
| **A4b 獨立 Reviewer（Wiki）** | 同上 | **E2** | **9**（1/5/3） | **`W-07`（高）**：Multi-Head 合成公式左右變數 `(Q,K,V)` 與 `X` 衝突；`W-04, W-05, W-09` 頁碼誤植／漏列；`W-06` `√5 ≈ 2.236` 未標為反推註記；`W-08, W-10, W-11, W-12` 未載例句／術語與引語偏差 → **退回 A3** 全部修正 |
| **A4b 獨立 Reviewer（Wiki）** | 同上 | **E3** | **3**（0/2/1） | `W-13`（`L02 p.21` 類別順序不一致）、`W-14`（`L03 p.62, 82` 稱 MSE 實為 SSE）、`W-15`（4 處原文四捨五入／排版瑕疵）→ **退回 A2 人工閘門**，已由使用者裁決採選項 A 全部加註完成 |
| **B4b 獨立 Reviewer（簡報）** | `slides/index.html` 13 頁全數普查＋互動重算＋5 題測驗 | **E4** | **12**（1*/7/4） | **`S-08`（高，E4+E5）**：Slide 7 Temperature 模擬器繞過 Wiki 直接看 `L04 p.57`，誤踩文字流倒置將標籤反標為 `c(4.3)/b(3.4)/a(0.2)`（實為 `a=4.3, b=3.4, c=0.2`）；另 `S-01, S-02, S-15` 混入非 Wiki 內容，`S-03~07, S-10~12, S-14` 頁尾漏列來源 → **退回 B1**（`S-10` 連動轉 `A4b`）全數修正 |
| **B4b 獨立 Reviewer（簡報）** | 同上 | **E5** | **6**（1*/2*/3） | `S-08` 標籤倒置、`S-09` 未轉譯反引號 `` `p.57` ``、`S-12, S-14` 頁尾漏列與註解誤寫 `5 Concept pages`、`S-13` 簡體錯字「指数」、`S-16` Slide 1 頁碼格式不一 → **退回 B3** 全數修正，`verify_slides.py` 複檢 **PASS=35, FAIL=0** |

*(註 1：簡報獨立異常去重後共 16 件，因 `S-08, S-12, S-14` 同時涉 E4 與 E5；`S-10` 同時連動階段 A 之 `W-06`。Slide 2、Slide 3、Slide 9 及 Slide 13 全部 5 題自我檢測答案與解析皆未發現事實錯誤。)*  
*(註 2：確定性腳本調整揭露 — ① `check_numbers.py` 初跑為 `FAIL=1`（`L04 p.17-18` 的 `7.53%` 原文捨成 `7%` 以湊滿 100%），後來為了容納已由使用者裁決的原文瑕疵（`W-15`），在腳本中加入該捨入規則（而非修正 Wiki 的錯誤）才轉為 `PASS=24, FAIL=0`；② `check_sources.py` 初跑檢出 21 行缺來源，經逐行核對 `raw/` 後補齊 5 行事實陳述之 `[來源: 檔名 p.X]`，另 16 行（純引導句 3、誤解標題 8、專案角色 1、跨來源比對表 4）於腳本開頭註解與 `checks/scripts-run2-20261119-retry2.md` 明文列舉豁免規則與豁免行數後，複檢為 `ISSUES=0, EXEMPTED=16`。)*

---

## 五、反思：哪個節點最常出錯？如何把檢查前移？

待撰寫（待 Run 2 之 E3 人工裁決與 B5 人工抽查 3 頁完成後一併整理）。

---

## 六、人機協作歷程

| 協作階段 | 人工（使用者）負責的決策與把關 | AI（Antigravity）負責的執行與驗證 |
|---|---|---|
| **專案規劃與選材** | 制定作業規劃書、拍板採用**方案 A** 策略與**方案 1（Week 01～05 講義 + Vaswani 2017 原論文，共 6 篇）**。 | 盤點全學期講義頁數、建立專案目錄與 `AGENTS.md` / `log.md`，下載外部論文並完成檔案就位。 |
| **Run 1 階段 A（6 篇 Ingest）** | 在每篇的 **A2 先討論**節點審閱重點清單與預計建立／更新之頁面，確認無誤後授權寫入。 | 分段讀取 60 頁以上長講義、撰寫 6 篇 `sources/` 與 **6 篇** `concepts/`、執行 6 次自查 Lint 並記錄錯誤與修正。 |
| **Run 1 階段 B（簡報生成與部署）** | 在 **B2** 審閱 13 頁大綱與 `traceability.md`，於本機雙擊檢視 `slides/index.html` 並啟用 GitHub Pages。 | 撰寫單一自足 `slides/index.html`、修正第 13 頁頁尾前綴與 `.nojekyll` 並推送 GitHub。 |
| **Run 2 流程升級與獨立審查** | 主持唯讀稽核、開啟全新獨立對話執行 Reviewer（A4b / B4b）、針對 **E3（`W-13`, `W-14`, `W-15`）** 裁決採用加註勘誤方案（選項 A），並親自完成 **B5 人工抽查 3 頁（Slide 3、5、6）**與無痕視窗線上實測。 | 建立 `graph v2` 規則與 5 支確定性 Python 腳本；依獨立 Reviewer 報告分流修正 E1/E2/E4/E5、落實 E3 人工裁決、重跑腳本驗證並更新 `log.md`、`traceability.md`、`b4-slides-verification.md` 與 `report.md`。 |
| **跨 AI 規劃與交叉審閱（協作對象：Claude 對話式 AI）** | 使用者將 **Claude（對話式 AI）** 用於作業規劃書、流程設計討論、Run 2 的提示語設計，以及對報告與紀錄的交叉審閱，藉此跳脫單一執行環境之盲點。 | Claude 不直接操作專案檔案，所有程式撰寫、腳本驗證與專案檔案變更皆由 **Antigravity** 依使用者指示執行。 |

---

## 七、參考資料

1. **方法論依據**：Andrej Karpathy, *LLM Wiki* (GitHub Gist, 2026-04) — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
2. **課程講義來源**（依 `01如何不焦慮地學AI.pdf` `p.4` 原文記載：`TAICA`、`生成式 AI：文字與圖像生成的原理與實務`、`開課學校：政治大學`、`開課教師：蔡炎龍老師`，及 `p.9, p.99, p.112` 與 `04LLM只是在猜下一個字？.pdf` `p.60` 原文所載「政大應用數學系／應數系」；其餘講義 `02`、`03`、`05` PDF 本身未印製開課單位與教師姓名）：
   - `01如何不焦慮地學AI.pdf`（Week 01，未公開上傳）
   - `02神經網路的概念.pdf`（Week 02，未公開上傳）
   - `03AI為什麼每次都不一樣？.pdf`（Week 03，未公開上傳）
   - `04LLM只是在猜下一個字？.pdf`（Week 04，未公開上傳）
   - `05AI怎麼記得前面說過什麼？.pdf`（Week 05，未公開上傳）
3. **外部交叉查核論文（公開資料）**：
   - Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. *"Attention Is All You Need."* Advances in Neural Information Processing Systems 30 (NIPS 2017), arXiv:1706.03762 — https://arxiv.org/abs/1706.03762
