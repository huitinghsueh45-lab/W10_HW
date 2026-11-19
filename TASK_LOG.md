# TASK_LOG.md：W10 作業「用 LLM Wiki 做教學 HTML 簡報」專案進度與 Claude 交叉審閱交接包

> **文件時點註記**：本檔初版為 2026-11-18 Run 1 時點的紀錄（2026-11-19 追加 Run 2 進度），後續修正與最新統計一律以 `report.md` 為準。  
> **專案名稱**：生成式 AI 入門：從函數 $f_\theta$ 到 Transformer（LLM Wiki & 教學互動 HTML 簡報）  
> **最後更新時間**：2026-11-19 16:15  
> **繳交期限**：2026-11-23 23:59（遲交期限 11/24 16:00）  
> **後續 Git 規則**：**後續所有檔案變更皆由使用者自行執行 `git add / commit / push`，AI 不自動上傳。**

---

## 一、目前完成進度（Current Progress）

### Run 1（2026-11-18，graph v1 單一 AI 自查 — 歷史紀錄保持原樣）
- [x] **階段 0：專案初始化與規則建立**：建立 `AGENTS.md`、`log.md`、`wiki/index.md` 與標準目錄結構；確認採用 **方案 A（沿用講義＋1 篇外部論文）** 與 **方案 1（Week 01～05 講義 + Vaswani et al. 2017 原論文，共 6 篇）**。
- [x] **階段 A：6 篇資料 Ingest / Lint 循環**：產出 6 篇 `wiki/sources/`、6 篇 `wiki/concepts/`（共 12 頁）與 6 份 `checks/lint-20261118-01~06.md`。
- [x] **階段 B：教學 HTML 簡報生成與本機實測**：產出 `checks/traceability.md`、單一自足 `slides/index.html`（13 頁）與 `checks/b4-slides-verification.md`。
- [x] **階段 C：初次 GitHub 推送與 `.nojekyll` 修復**：commit `613b3e9`（初版）、`0eb8d05`（調整 `.gitignore` 排除 `raw/lectures/*.pdf`、`HW_Plan/`、`desktop.ini`）、`4fca11e`（新增 `.nojekyll` 解決 GitHub Pages Jekyll 建置失敗）。

### Run 2（2026-11-19，依 `HW_Plan/2_Antigravity_提示語_Run2.md` 執行 graph v2 與獨立 Reviewer）
- [x] **提示語 0（唯讀稽核）**：不改任何檔案，依檔案與 `git log` 查核 A1.5 實際加入時間（確認 Run 1 並未執行 A1.5，第 5 講 `p.32-33` 係於 A4 Lint 抓出）、重整完整錯誤表（10 件，補齊漏列 4 件）、從 PDF 抽取授課單位與教師原文（`L01 p.4`：TAICA / 政治大學 / 蔡炎龍老師；`p.9, 99, 112` 與 `L04 p.60`：政大應用數學系）、核對 `report.md` 無證據說法與漏對之處。已另存為 **`checks/audit-run1-20261119.md`**。
- [x] **提示語 1（建立 graph v2 與確定性腳本）**：
  - 更新 `AGENTS.md` 新增 `graph v2` 章節（`A1.5`、`A4a/A4b`、`B4a/B4b`、`E1~E5` 條件分流、連續 3 次迴圈保護、獨立 Reviewer 唯讀隔離規則）。
  - 建立 `scripts/` 確定性檢查腳本：`check_numbers.py`、`check_sources.py`、`check_links.py`、`verify_slides.py`，初次原樣執行結果保存於 `checks/scripts-run2-20261119.md`。
  - 在 `log.md` 追加 `GRAPH v2` 紀錄（Run 1 歷史不改寫）。
- [x] **提示語 2（獨立新對話 Reviewer 審查，唯讀）**：
  - 於全新獨立對話完成審查，產出 **`checks/review-run2-wiki.md`**（12 頁 × 8 項＝96 項抽樣＋PDF 視覺頁面渲染＋Python 重算；發現 **15 件**：E1 3 件、E2 9 件、E3 3 件，0 件無法確認）與 **`checks/review-run2-slides.md`**（13 頁 100% 普查＋2 互動元件＋5 題自我檢測；發現 **16 件獨立異常**：E4 12 件、E5 6 件，其中 3 件同涉 E4+E5、1 件連動 Wiki E2，0 件無法確認）。
- [x] **提示語 3（依錯誤碼分流修正，第 1 次重試）**：
  - **E1 → A1（3 件：`W-01`, `W-02`, `W-03`）**：補強新增 `scripts/precheck_pdf_coords.py`（A1.5 視覺座標排序與倒置偵測），重抽修正 `L02 p.60`（土八哥猜成 16%/12%/72% 家八哥）與移除 `L02 p.67` 類別對調誤判。
  - **E2 → A3（9 件：`W-04`～`W-12`＋2 處簡體「与」）**：修正 `W-07` Multi-Head 公式變數衝突、`W-04/05/09` 頁碼誤植或漏列、`W-06` `√5 ≈ 2.236` 獨立反推註記、`W-08/10/11/12` 未載例句／術語／引語，並於 `lecture-04` 與 `word-embedding` 補入座標核實之 `a=4.3, b=3.4, c=0.2`。
  - **E3 → A2 人工閘門（3 件：`W-13`, `W-14`, `W-15`）**：暫停交由使用者裁決；使用者已於 `2026-11-19 15:18` 確認採用建議**選項 A**（加註 `L02 p.21` 順序差異、`L03 p.62/82` MSE 實為 SSE、`L04 p.18` `7.53%→7%` 原文捨入與 `L04 p.80` / `L05 p.46-64` / `L02 p.118` 原文排版勘誤）。
  - **E4 → B1 & E5 → B3（16 件：`S-01`～`S-16`）**：全數修正 `slides/index.html`（含高嚴重度 `S-08` Slide 7 溫度模擬器倒置標籤修正為 `候選字 a (4.3) / b (3.4) / c (0.2)`、移除非 Wiki 內容與未轉譯反引號、補齊 Slide 6/10/11/12 頁尾來源、修正簡體「指数」與頁碼格式），並更新 `checks/traceability.md`（同步頁尾與 Slide 13 展開為 Q1～Q5 逐題 Wiki 與 raw 頁碼）。
  - **B5 人工閘門抽查 3 頁**：使用者已親自抽查 **Slide 3、Slide 5、Slide 6** 確認無誤，紀錄補入 `checks/b4-slides-verification.md` 第三節。
  - **確定性腳本複檢**：`check_numbers.py`（PASS=24, FAIL=0；註：為容納已裁決之 `W-15` 原文捨入瑕疵而調整檢查規則，非修正 Wiki 錯誤）、`check_sources.py` Retry 2（補齊 5 行事實來源＋明文豁免 16 行，`ISSUES=0, EXEMPTED=16`，詳見 `checks/scripts-run2-20261119-retry2.md`）、`check_links.py`（PASS=26, FAIL=0）、`verify_slides.py`（PASS=35, FAIL=0）。
  - **報告與紀錄更新**：更新 `log.md`（`RUN 2`、`E3 DECISION & B5 HUMAN CHECK`、`DEPLOY`）與 `report.md`（第一～四、六、七節；**第五節反思保留「待撰寫」**，待帶回 Claude 一併整理）。
- [x] **提示語 4（提交、推送與線上驗證）**：
  - 已推送 commit `1c73c71`（`Add graph v2, independent reviewer run 2, and report fixes`）至 `origin/main`（`.nojekyll` 受追蹤）。
  - GitHub Actions `pages-build-deployment`（Run `#44479000466`）確認 `build` / `report-build-status` / `deploy` 全數綠燈 `success`。
  - 線上網址 `https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html` 驗證 HTTP 200，已載入 Run 2 修正內容（`候選字 a (4.3)`、`Slide 1 / 13`）。
  - `checks/b4-slides-verification.md` 已補入「第四節：線上版實測」。
  - *註*：因「我想要自己上傳GIT」訊息抵達時系統正在執行上一輪推送，故 `1c73c71` 已先行推送；之後所有變更均**保留於本地未提交**，全交由使用者自行上傳。
- [x] **收尾提示語（`HW_Plan/3_收尾提示語與反思草稿.md` 第一部分）**：
  - **`check_sources.py` 21 行逐項處理**：回查 `raw/` PDF 原頁後補齊 5 行事實陳述來源（`probability-entropy-and-sampling.md` L34, L61、`transformer-and-self-attention.md` L14–16）；另 16 行（純引導句 `R1=3`、誤解標題 `R2=8`、專案角色 `R3=1`、跨來源比對表 `R4=4`）於 `scripts/check_sources.py` 開頭與執行輸出明文列舉豁免規則與豁免行數，複檢結果原樣存於 `checks/scripts-run2-20261119-retry2.md`（`ISSUES=0, EXEMPTED=16`）。
  - **`check_numbers.py` 規則調整透明揭露**：於 `report.md` 第四節註 2 與 `log.md` 明確標示 `PASS=24` 係因「為容納已裁決之 `W-15` 原文瑕疵而調整檢查規則」，並非修正 Wiki 錯誤。
  - **同步 `README.md` 與 `TASK_LOG.md`**：頂部加上時點與準據註記（以 `report.md` 為準），並補齊目錄與 Run 2 說明。
  - **`report.md` 用語與協作透明度**：第二節改為「Run 1 完成後的檢討發現」；第六節新增 **Claude（對話式 AI）** 協作列（規劃、流程討論、Run 2 提示語與交叉審閱；不直接操作檔案，由 Antigravity 執行）；**第五節反思維持原樣未動**。

---

## 二、核心架構決策演進（Run 1 → Run 2）

1. **歷史不改寫原則**：Run 1（2026-11-18）的所有紀錄保持原樣；`graph v2`、5 支確定性檢查腳本與獨立 Reviewer 均如實標記為 Run 1 完成後（2026-11-19）導入。
2. **從「單一 AI 自查 Loop（graph v1）」升級為「錯誤分流＋獨立 Reviewer（graph v2）」**：
   - 新增 **A1.5 確定性視覺座標預檢**（`scripts/precheck_pdf_coords.py`），主動偵測 Keynote/PDF 文字流上下倒置（實測於 `L02 p.21/60/67`、`L03 p.82`、`L04 p.57` 全數成功攔截）。
   - 拆分 `A4a / B4a` 確定性腳本與 `A4b / B4b` **上下文隔離之全新對話獨立 Reviewer（唯讀）**，避免寫作與審查共用記憶盲點。
   - 建立 **E1～E5 條件分流**（`E1→A1`、`E2→A3`、`E3→A2 人工閘門`、`E4→B1`、`E5→B3`、`簡報發現 Wiki 誤→A4b`）與**連續 3 次不通過迴圈保護**。
   - **B5 人工閘門與線上實測**：明定必須由人類抽查 3 頁（本次抽查 Slide 3、5、6）並於無痕視窗驗證線上 GitHub Pages 版本。
3. **知識中介層嚴格隔離與資料公開邊界**：課程講義 PDF（`raw/lectures/*.pdf`）為授課教材未公開上傳，外部論文 `Vaswani_2017_Attention_Is_All_You_Need.pdf` 為公開 arXiv 資料隨附於 repo；簡報每頁頁尾強制對齊 `wiki/` 實載內容與 `checks/traceability.md`。

---

## 三、2026-11-19 本次對話操作時序摘要

| 時間 | 執行項目 | 主要產出／結果 |
|---|---|---|
| 14:13–14:15 | **提示語 0：唯讀稽核** | 零修改檔案；查實 A1.5 時序、重整 Run 1 共 10 件問題、從 PDF 抽出政大應數／蔡炎龍老師原文、列出 6 項報告與 log 對不上之處 |
| 14:16–14:21 | **提示語 1：建立 graph v2** | 更新 `AGENTS.md`、`log.md`；新建 `scripts/{check_numbers,check_sources,check_links,verify_slides}.py` 與 `checks/scripts-run2-20261119.md` |
| 14:48–14:51 | **提示語 2：獨立 Reviewer（全新對話）** | 唯讀產出 `checks/review-run2-wiki.md`（15 件）與 `checks/review-run2-slides.md`（16 件） |
| 14:55–15:05 | **提示語 3：分流修正（Retry #1）** | 新增 `scripts/precheck_pdf_coords.py`；修正 E1(3)、E2(9)、E4(12)、E5(6) 與 `traceability.md`、`report.md`、`log.md`；E3(3) 暫停退回 A2 請人工裁決 |
| 15:18–15:22 | **E3 裁決＋B5 抽查＋提示語 4 部署驗證** | 使用者確認 E3（選項 A）與 B5 抽查（Slide 3、5、6）；腳本複檢全過（24/26/35 PASS, 0 FAIL）；更新 `b4-slides-verification.md`、`report.md`、`log.md`；推送 `1c73c71` 並確認 Actions `#44479000466` 全綠、線上 HTTP 200 |
| 15:25–15:29 | **產出稽核報告檔與更新 `TASK_LOG.md`** | 產出 `checks/audit-run1-20261119.md`、更新本 `TASK_LOG.md`（未自動執行 Git） |
| 16:09–16:15 | **收尾提示語（`3_收尾提示語與反思草稿.md` 第一部分）** | 處理 `check_sources.py` 21 行（補 5 行來源＋明文豁免 16 行 R1–R4）存於 `checks/scripts-run2-20261119-retry2.md`；於 `report.md` / `log.md` 揭露 `check_numbers.py` 規則調整；第六節新增 Claude 協作列；同步 `README.md` / `TASK_LOG.md`（未動第五節、未執行 Git） |

---

## 四、帶回 Claude 撰寫「第五節反思」與最終審閱之交接包

### 1. 線上公開連結
- **GitHub 儲存庫**：`https://github.com/huitinghsueh45-lab/W10_HW`
- **LLM Wiki 連結**：`https://github.com/huitinghsueh45-lab/W10_HW/tree/main/wiki`
- **教學 HTML 簡報連結（GitHub Pages）**：`https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html`
- **確定性腳本與審查報告**：`https://github.com/huitinghsueh45-lab/W10_HW/tree/main/scripts`、`https://github.com/huitinghsueh45-lab/W10_HW/tree/main/checks`

### 2. Run 1 vs. Run 2 錯誤統計總覽（直接支撐第五節反思）
- **Run 1（單一 AI 自查，經唯讀稽核重整，共 10 件）**：**E1 = 5 件**（含漏列之第 1 講頁碼字型、第 4 講數字字型）、**E2 = 1 件**、**E3 = 1 件**、**E4 = 0 件**（僅自查 4 頁）、**E5 = 3 件**（含漏列之 B4 瀏覽器逾時與 GitHub Pages Jekyll 建置失敗）。
- **Run 2（graph v2 確定性腳本＋全新對話獨立 Reviewer）**：
  - **Wiki 審查（96 項抽樣＋視覺渲染，共 15 件）**：**E1 = 3 件**（1 高 / 2 中）、**E2 = 9 件**（1 高 / 5 中 / 3 低）、**E3 = 3 件**（2 中 / 1 低）。
  - **簡報審查（13 頁 100% 普查，共 16 件獨立異常）**：**E4 = 12 件**（1* 高 / 7 中 / 4 低）、**E5 = 6 件**（1* 高 / 2* 中 / 3 低）、**連動 Wiki E2 = 1 件**（`S-10` → `W-06`）。

### 3. 最意外且最具反思價值的真實發現（Run 1 + Run 2）
1. **獨立 Reviewer 直接戳破「單一 AI 自查通過」的假象（高嚴重度雙重倒置）**：
   - **Wiki `W-01`（E1 高）**：Run 1 自查已宣告通過的 `lecture-02`（`L02 p.60`），竟因 `pypdf` 垂直文字流倒置，把「將**土八哥**照片猜成 `16% 土八哥、12% 白尾八哥、72% 家八哥`」整個顛倒寫成「把**家八哥**猜成 `72% 土八哥、12% 家八哥、16% 白尾八哥`」，且連帶誤判 `p.67` 圖示順序對調（`W-02, W-03`）。
   - **簡報 `S-08`（E4 + E5 高）**：Run 1 自查曾抽查 Slide 7 並宣告「完全一致」，但 Run 2 獨立 Reviewer 竟抓出 Slide 7 溫度模擬器繞過 Wiki 直接看 `L04 p.57`，並掉進 PDF 文字流倒置陷阱，把三條長條圖標籤整個標反成 `候選字 c (4.3) / b (3.4) / a (0.2)`（視覺原圖實為 `a=4.3, b=3.4, c=0.2`）！
2. **「寫與查共用上下文」容易合理化過度推論與記憶滲漏**：
   - Run 2 揪出多處 Run 1 自查完全沒發現的 **E2**（如 `W-07` 把 Vaswani 與第 5 講 Multi-Head 公式硬拼導致左右變數 `(Q,K,V)` 與 `X` 衝突、`W-06` 把反推的 `√5 ≈ 2.236` 寫成原文、`W-08` 憑記憶補入「狗咬人／人咬狗」）與 **E4**（如 `S-01` 混入全 Wiki 沒有的 Claude/Gemini/Grok、`S-15` 直接引用 `raw` 的「陽春／先不要直接寫成品」）。
3. **Run 1 經典案例（仍保留作反思對照）**：第 5 講 `p.32-33` 自訂字型將數字 `3` 編碼為 ASCII `'1'`，觸發 LLM 腦補 `[51%, 20%, 4%, 3%, 8%]`，靠 A4 機率總和 `86% ≠ 100%` 抓出並破譯字型映射表還原（縮放後四捨五入總和為 `99%`）。

### 4. 請帶回 Claude 的 6 份檔案
1. `checks/audit-run1-20261119.md`（提示語 0 唯讀稽核結果）
2. `checks/scripts-run2-20261119-retry2.md`（`check_sources.py` 21 行處置與明文豁免明細）
3. `checks/review-run2-wiki.md`（Run 2 獨立 Reviewer Wiki 審查報告）
4. `checks/review-run2-slides.md`（Run 2 獨立 Reviewer 簡報審查報告）
5. `log.md`（含 Run 1 完整原樣紀錄 + Run 2 graph v2 / 分流修正 / E3 裁決 / B5 抽查 / DEPLOY / CLOSURE 紀錄）
6. `report.md`（已完成第一～四、六、七節與 Claude 協作透明度修正，第五節反思待貼入改寫後版本）

---

## 五、最後待辦事項（Final Checklist）

- [x] GitHub Pages 已啟用並驗證最新 `pages-build-deployment`（Run `#44479000466`）`build` 與 `deploy` 全為綠色成功。
- [ ] 使用者以**無痕視窗**開啟 `https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html` 親自確認線上版互動元件（特別是 Slide 7 `候選字 a/b/c` 與 Slide 8 `τ = √d_k`）。
- [ ] 將 `HW_Plan/3_收尾提示語與反思草稿.md` 第二部分「第五節反思」改寫為自己的文字並貼入 `report.md`（其中第 95 行可填入：`原檢出 21 行，回查 raw 後補齊 5 行事實陳述來源，其餘 16 行依明文豁免規則 R1–R4 標記，複檢 ISSUES=0, EXEMPTED=16`），再回到 Claude 做繳交前最後檢查。
- [ ] 由**使用者自行執行 Git 提交與推送**（切記先 `cd` 進專案資料夾再執行）：
  ```powershell
  cd "F:\我的雲端硬碟\NCHU\115-1\TAICA_生成式AI：文字與圖像生成的原理與實務\W10\W10_HW"
  git status
  git add README.md TASK_LOG.md log.md report.md scripts/check_sources.py wiki/ checks/audit-run1-20261119.md checks/scripts-run2-20261119-retry2.md
  git commit -m "Finalize check_sources exemptions, transparency updates, and section 5 reflection"
  git push origin main
  ```
- [ ] 於 11/23 23:59 前完成作業繳交（標題：`中興 8113026207 科管博 薛慧婷 生成式AI入門：從函數到Transformer`）。
