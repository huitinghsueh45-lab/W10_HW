# 生成式 AI 入門：從函數 $f_\theta$ 到 Transformer（LLM Wiki & 教學 HTML 簡報）

> **文件時點註記**：本檔初版為 2026-11-18 Run 1 時點的紀錄，後續 `graph v2` 修正與最新統計一律以 [`report.md`](report.md) 為準。

本專案為 TAICA《生成式 AI：文字與圖像生成的原理與實務》Week 10 作業成果，依據 Andrej Karpathy 之 **LLM Wiki 模式**（`raw → wiki → slides`，核心操作為 **Ingest / Query / Lint**）建立結構化知識庫，並以 Wiki 為唯一知識來源製作單一自足的教學型互動 HTML 簡報。

## 🔗 快速連結

- 📊 **教學 HTML 簡報（GitHub Pages 線上瀏覽）**：[https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html](https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html)
- 📚 **LLM Wiki 知識庫目錄**：[`wiki/index.md`](wiki/index.md)
- 🔍 **簡報 ↔ Wiki ↔ 原始講義可追溯性對照表**：[`checks/traceability.md`](checks/traceability.md)
- 🧪 **檢查與獨立審查紀錄（Run 1 Lint＋Run 2 Reviewer／稽核）**：[`checks/`](checks/)
- ⚙️ **確定性檢查腳本（graph v2）**：[`scripts/`](scripts/)
- 📝 **操作與錯誤紀錄（含 Run 1／Run 2 完整紀錄）**：[`log.md`](log.md)
- 📄 **完整作業報告（最新統計與 graph v1 / v2 演進）**：[`report.md`](report.md)

## 📁 專案目錄結構

```text
W10_HW/
├── AGENTS.md          # 專案規則（Run 1 基礎規則 + Run 2 新增之 graph v2 與獨立 Reviewer 規則）
├── log.md             # 完整操作與真實錯誤紀錄（Run 1 原樣保留 + Run 2 追加紀錄）
├── report.md          # 最終作業報告（最新統計與雙階段流程演進以此檔為準）
├── raw/               # 原始資料（唯讀，課程講義 PDF 為授課教材未公開上傳，外部論文隨附）
│   └── external/      # Vaswani et al. (2017) Attention Is All You Need 原論文（公開資料）
├── wiki/              # LLM 整理並經 Run 1 Lint 與 Run 2 獨立審查修正之知識頁（共 12 頁）
│   ├── index.md       # 所有頁面目錄與一句話摘要
│   ├── sources/       # 6 篇原始資料來源摘要頁（含分段範圍與頁碼標註）
│   └── concepts/      # 6 篇跨來源整合概念頁（雙向 [[...]] 交叉連結）
├── scripts/           # graph v2 確定性檢查腳本（precheck_pdf_coords / check_numbers / check_sources / check_links / verify_slides）
├── checks/            # 檢查與審查紀錄
│   ├── lint-20261118-01~06.md       # Run 1 每次 Ingest 後的 6 項 Lint 紀錄
│   ├── audit-run1-20261119.md       # Run 1 唯讀稽核報告
│   ├── scripts-run2-20261119*.md    # Run 2 確定性腳本原樣執行結果（含 Retry 2 明文豁免）
│   ├── review-run2-wiki.md          # Run 2 獨立 Reviewer Wiki 審查報告
│   ├── review-run2-slides.md        # Run 2 獨立 Reviewer 簡報審查報告
│   ├── traceability.md              # 簡報 13 頁 ↔ Wiki 頁 ↔ raw 原始資料與頁碼對照表
│   └── b4-slides-verification.md    # 簡報驗證、B5 人工抽查 3 頁與線上版實測紀錄
└── slides/
    └── index.html     # 單一自足教學 HTML 簡報（支援方向鍵翻頁、互動模擬器與自我檢測）
```
