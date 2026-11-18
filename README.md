# 生成式 AI 入門：從函數 $f_\theta$ 到 Transformer（LLM Wiki & 教學 HTML 簡報）

本專案為 TAICA《生成式 AI：文字與圖像生成的原理與實務》Week 10 作業成果，依據 Andrej Karpathy 之 **LLM Wiki 模式**（`raw → wiki → slides`，核心操作為 **Ingest / Query / Lint**）建立結構化知識庫，並以 Wiki 為唯一知識來源製作單一自足的教學型互動 HTML 簡報。

## 🔗 快速連結

- 📊 **教學 HTML 簡報（GitHub Pages 線上瀏覽）**：[https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html](https://huitinghsueh45-lab.github.io/W10_HW/slides/index.html)
- 📚 **LLM Wiki 知識庫目錄**：[`wiki/index.md`](wiki/index.md)
- 🔍 **簡報 ↔ Wiki ↔ 原始講義可追溯性對照表**：[`checks/traceability.md`](checks/traceability.md)
- 🧪 **6 次 Ingest 之 Lint 檢查紀錄**：[`checks/`](checks/)
- 📝 **操作與錯誤紀錄（含錯誤統計表）**：[`log.md`](log.md)
- 📄 **完整作業報告（含 Loop/Graph 設計與反思）**：[`report.md`](report.md)

## 📁 專案目錄結構

```text
W10_HW/
├── AGENTS.md          # 專案規則（唯讀 raw/、先討論後生成、事實標註頁碼、6 項 Lint 清單）
├── log.md             # 完整操作與真實錯誤紀錄（含錯誤統計表）
├── report.md          # 最終作業報告（含 Loop/Graph 流程圖與檢查前移反思）
├── raw/               # 原始資料（唯讀，大型課程講義 PDF 於本地保存，外部論文隨附）
│   └── external/      # Vaswani et al. (2017) Attention Is All You Need 原論文
├── wiki/              # LLM 整理並通過 6 項 Lint 檢查之知識頁（共 12 頁）
│   ├── index.md       # 所有頁面目錄與一句話摘要
│   ├── sources/       # 6 篇原始資料來源摘要頁（含分段範圍與頁碼標註）
│   └── concepts/      # 6 篇跨來源整合概念頁（雙向 [[...]] 交叉連結）
├── checks/            # 檢查紀錄
│   ├── lint-20261118-01~06.md  # 每次 Ingest 後的 6 項 Lint 結果與錯誤修正紀錄
│   ├── traceability.md         # 簡報 13 頁 ↔ Wiki 頁 ↔ raw 原始資料與頁碼對照表
│   └── b4-slides-verification.md # 簡報結構與內容抽查驗證紀錄
└── slides/
    └── index.html     # 單一自足教學 HTML 簡報（支援方向鍵翻頁、互動模擬器與自我檢測）
```
