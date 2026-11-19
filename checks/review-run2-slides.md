# 獨立審查報告（Run 2 — 階段 B：簡報審查）

- **審查日期**：2026-11-19 14:51 (+08:00)
- **審查角色**：獨立 Reviewer（遵循 `AGENTS.md` graph v2 獨立 Reviewer 規則；未參與簡報撰寫，上下文隔離，僅依據 `slides/index.html` 與 `wiki/` 全部 12 頁審查，並於發現疑似繞過 Wiki 混入 `raw/` 內容時核對 `raw/` 確認來源；嚴守唯讀權限）
- **審查範圍**：`slides/index.html` 全部 **13 頁**（L1–L1341）、5 題自我檢測（Slide 13）、2 個互動元件（Slide 7 Temperature 模擬器、Slide 8 $\sqrt{d_k}$ 切換器），以及單檔自足性、鍵盤翻頁、七段教學結構與頁尾來源標示。
- **抽樣數量與方法**：
  - **全數普查（100% 覆蓋）**：逐頁（Slide 1～13）完整盤點所有事實陳述、數學公式、數值實例與測驗題目／答案／解析。
  - **嚴格頁尾可追溯規則**：依專案規則與審查規範，每一項陳述皆須能在**該頁頁尾（`.wiki-source-badge`）明確標示的 Wiki 頁**中找到支持；找不到者標為 **E4（混入該頁頁尾 Wiki 以外內容）**，並進一步區分「存在於其他未列頁尾之 Wiki 頁」與「整個 `wiki/` 皆無（繞過 Wiki 混入 `raw/` 或外部記憶）」。
  - **獨立重算**：使用 Python 重新計算所有 Softmax、平方誤差、Cross Entropy、Temperature（$\tau=0.5, 1.0, 2.0$）與 $\sqrt{d_k}$ 縮放數值，核對 JS 程式碼寫死之顯示值。

---

## 一、所有異常與疑點發現總表（E4 / E5 / 連動 Wiki 錯誤）

> 註：下表列出全簡報 13 頁中判定為「錯誤」之項目；完整逐頁核對明細（包含判定「未發現問題」之 Slide 2、Slide 3、Slide 9 及測驗 Q1–Q5 逐題核對）列於第二至第四節。

| 編號 | 投影片頁次與位置 | 簡報內容／元件行為 | 頁尾 Wiki 核對結果（與跨頁／raw 查證） | 判定 | 錯誤類型碼 | 嚴重度 |
|---|---|---|---|---|---|---|
| **S-01** | Slide 1（L467） | 焦慮 2：`ChatGPT、Claude、Gemini、Grok、Llama 每天推陳出新，不知哪個最好。` | 頁尾僅列 `concepts/function-mapping.md`、`sources/lecture-01-learn-ai-without-anxiety.md`。該兩頁皆未出現這 5 個模型名稱；且**全部 12 頁 Wiki 中完全沒有出現 `Claude`、`Gemini`、`Grok`**（僅出現於 `raw` L01 p.36 / L04 p.44），屬繞過 Wiki 直接混入 `raw/` 或外部記憶。 | 錯誤 | **E4** | **中** |
| **S-02** | Slide 1（L485） | 四個超能力第 3 點：`懂得為何引導有效：理解為什麼提供「正確的資訊＋清楚的指引」能改變條件機率。` | 頁尾兩頁 Wiki 僅寫「知道為什麼特定的引導（prompt）會有好處」，**完全沒有出現「正確的資訊＋清楚的指引」**（該句位於未列頁尾的 `lecture-04`、`transformer-and-self-attention`），且全部 Wiki 均無「改變條件機率」之直述。 | 錯誤 | **E4** | **中** |
| **S-03** | Slide 4（L648–649） | 3+1 架構表第 3 列 RNN 寫「把上次輸出 `h_{t-1}` 傳回與本次 `x_t` 結合」；第 4 列 Transformers 寫核心隱藏層 `Self-Attention` 與「多模態生成」 | 頁尾僅列 `concepts/neural-networks-and-learning.md`、`sources/lecture-02-neural-networks.md`。該兩頁皆未出現符號 `$h_{t-1}$`、`$x_t$`、`Self-Attention` 或「多模態生成」（分別位於 `lecture-04/05` 與 `transformer-and-self-attention`），頁尾未涵蓋。 | 錯誤 | **E4** | **低** |
| **S-04** | Slide 4（L652） | `三巨頭（Hinton、LeCun、Bengio）指出當年欠缺三大要件：複雜的軟體、大量的數據、電腦計算能力。` | 頁尾 `lecture-02`（L47）與 `neural-networks-and-learning`（L33）皆僅寫三巨頭奠基、上世紀欠缺三大要件，並未說是「三巨頭指出」（實際核對 `raw` L02 p.56 僅 Yann LeCun 一人發言框），屬簡報過度歸因改寫。 | 錯誤 | **E4** | **低** |
| **S-05** | Slide 5（L691） | `滿足「國王 − 男人 + 女人 = 皇后」` | 頁尾為 `concepts/word-embedding-and-sampling-strategies.md`、`concepts/transformer-and-self-attention.md`。該兩頁僅寫 `「國王 — 男人 vs. 皇后 — 女人」`（L34）；明確的加減等式 `國王 − 男人 + 女人 = 皇后` 僅見於未列頁尾之 `sources/lecture-04-llm-next-token-prediction.md`（L81）。 | 錯誤 | **E4** | **低** |
| **S-06** | Slide 6（L741） | 多參數偏微分括號例：`（如 L=(b_1+2w_1−w_2−3)^2 在 (1,−1,2) 化為 4w_1^2）` | 頁尾僅列 `concepts/neural-networks-and-learning.md`、`concepts/probability-entropy-and-sampling.md`。**兩頁皆完全沒有此偏微分具體例題**（該例題僅存於未列頁尾之 `sources/lecture-02-neural-networks.md` L60）。 | 錯誤 | **E4** | **中** |
| **S-07** | Slide 7（L774） | `但咖啡推薦或 LLM 猜下一個字則依機率分佈隨機抽樣` | 頁尾 `concepts/probability-entropy-and-sampling.md`（L58）僅寫「推薦系統」而未提「咖啡推薦」（「咖啡推薦」僅存於未列頁尾之 `sources/lecture-03-why-ai-differs-each-time.md` L71）。 | 錯誤 | **E4** | **低** |
| **S-08** | Slide 7（L782, L793–805, L1264） | 互動區敘述寫 `切換教材 \`p.57\` 實測溫度`，且長條圖標籤寫為 **`候選字 c (4.3)`、`候選字 b (3.4)`、`候選字 a (0.2)`**（JS 註解 L1264 亦稱 `using exact Lecture 04 p.57 numbers`） | 1. **違反簡報只讀 Wiki（E4）**：頁尾兩頁及全部 12 頁 Wiki 皆未出現「候選字 c/b/a」對應 `4.3 / 3.4 / 0.2`，簡報繞過 Wiki 直接參照 `raw` L04 p.57。<br>2. **標籤完全顛倒（E5 / 誤踩原 PDF 倒置陷阱）**：視覺核對 `raw` L04 p.53, p.54, p.57，實際對應為 **`a = 4.3`（70%）、`b = 3.4`（29%）、`c = 0.2`（1%）**；簡報誤受 `p.57` PDF 文字流倒置（`0.2, 3.4, 4.3` vs `a, b, c`）影響，把最高分 `a` 與最低分 `c` 徹底標反！ | 錯誤 | **E4 + E5** | **高** |
| **S-09** | Slide 7（L782） | HTML 正文出現未轉譯之 Markdown 反引號：`切換教材 \`p.57\` 實測溫度` | 瀏覽器直接渲染會印出字面反引號 `` `p.57` ``，屬 HTML 排版瑕疵（且不宜於簡報直接暴露 `raw` 頁碼）。 | 錯誤 | **E5** | **低** |
| **S-10** | Slide 8（L851, L855, L1295, L1302） | 互動按鈕與 JS 標題寫 `同除以 √5 ≈ 2.236`、`除以 √5 後 [1.74, 1.43, 0.45, 0.13, 0.49]`；正文寫 `第五講直覺（p.32-33）` | 頁尾僅列 `concepts/transformer-and-self-attention.md`、`sources/external-vaswani-2017-attention-is-all-you-need.md`。**該兩頁完全未出現 `√5` 或 `2.236`**（僅出現於未列頁尾之 `sources/lecture-05-sequence-memory-and-attention.md` L40；且如階段 A `W-06` 所揭露，`raw` L05 p.33 原文根本沒寫 `√5 ≈ 2.236`）。同時屬 **E4** 與連動階段 A Wiki 之 **E2** 問題。 | 錯誤 | **E4（連動 Wiki E2）** | **中** |
| **S-11** | Slide 10（L956, L969） | 案例 2 寫 `NIST 修改版`；案例 3 寫 `輸入 "炎龍老師很"，對字庫編號（帥=87, 幽=94, 有=112, 熱=174, 受=221）打分 [1.40, 0.03, 1.71, -0.73, 0.95] → Softmax 得 [30%, 7%, 40%, 4%, 19%]` | 頁尾僅列 `concepts/function-mapping.md`、`concepts/neural-networks-and-learning.md`、`concepts/transformer-and-self-attention.md`。**三頁均完全沒有出現「炎龍老師很」字庫編號、分數與 Softmax 百分比**（亦無「NIST 修改版」四字），該資料位於未列頁尾之 `sources/lecture-04`（L29–30）與 `sources/lecture-02`（L68）。 | 錯誤 | **E4** | **中** |
| **S-12** | Slide 11（L1017–1018, L1025） | 誤解 5：Balestriero, Pesenti, & LeCun (2021) 高維度空間學習本質為外插（Extrapolation） | 頁尾僅列 4 頁（`probability`、`word-embedding`、`transformer-and-self-attention`、`transformer-architecture-and-stability`），**全部未提及 Balestriero (2021) 或高維度外插**；實際來源為漏列於頁尾之 `concepts/neural-networks-and-learning.md`（L77–78）。同時，誤解 2「只是當助理用時我們不希望它作夢」亦僅見於 `sources/lecture-04`（L50）而非頁尾 4 頁。 | 錯誤 | **E4 + E5** | **中** |
| **S-13** | Slide 11（L1010） | 誤解 3 說明出現簡體字錯字：`只是把指数 e^{a/τ} 的分數差距拉近` | HTML 全文為繁體中文，唯此處混入簡體「指数」。 | 錯誤 | **E5** | **低** |
| **S-14** | Slide 12（L1072–1085, L1110） | SVG 流程圖 Node 4 含 `Word Embedding (W^T x = h)`、`Temperature`、`Top-k / Top-p`；Node 5 含 `Positional Encoding 時鐘`、`ResNet 殘差 + LayerNorm` | 頁尾僅列 4 頁，**漏列 `concepts/word-embedding-and-sampling-strategies.md` 與 `concepts/transformer-architecture-and-stability.md`**（頁尾 4 頁皆無 `W^T x = h`、Positional Encoding、ResNet、LayerNorm）；HTML 註解 L1039 亦誤寫 `connecting all 5 Concept pages`（實為 6 篇 Concept 頁）。 | 錯誤 | **E4 + E5** | **中** |
| **S-15** | Slide 12（L1093, L1100–1103） | Prompt 必殺技右卡寫「先給**陽春**方向」、「**請 AI 訪問你**：問還有哪些需要釐清的地方」、「（**先不要直接寫成品**）」、「**只要是 AI 生成的，務必自己讀過把關**」 | 頁尾 4 頁中僅 `transformer-and-self-attention.md`（L62）略提「和 AI 一起討論生成規格書／Prompt、最後人工親自審閱修改」。「請 AI 訪問你」僅在 `sources/lecture-04`（L86），而**「陽春」「先不要直接寫成品」「只要是 AI 生成的，務必自己讀過」在全部 12 頁 Wiki 中均不存在**，係直接取自 `raw` L04 p.106, p.109, p.110！ | 錯誤 | **E4** | **中** |
| **S-16** | Slide 1（L494） | Slide 1 右下角頁尾寫 `使用鍵盤 ← → 方向鍵翻頁`，與 Slide 2–13 統一之 `Slide X / 13` 格式不一致 | 雖頂部導覽列有 `1 / 13`，但投影片右下角頁碼風格未統一。 | 錯誤（輕微格式） | **E5** | **低** |

---

## 二、逐頁核對明細（Slide 1～Slide 13）

### Slide 1（L450–496）— 為什麼：封面與三大焦慮
- **頁尾來源**：`concepts/function-mapping.md`、`sources/lecture-01-learn-ai-without-anxiety.md`
- **逐項事實核對**：
  - 副標「教 AI 用你的方法做事」「用底層原理（含數學直覺）消除三大焦慮」→ 吻合 `lecture-01` L22。
  - 焦慮 1（取代焦慮、呆萌型 AI 機器人無意識不會分析、需定義輸入輸出）→ 吻合 `lecture-01` L24, L34；`function-mapping` L19。
  - 焦慮 2 列舉「ChatGPT、Claude、Gemini、Grok、Llama」→ **頁尾與全 Wiki 皆無（S-01 / E4 中）**。
  - 焦慮 3（Prompt / Context / Harness / Loop / Graph Engineering、Chat Bot、AI Agent 只是「教 AI 做事的方法」）→ 吻合 `lecture-01` L26；`function-mapping` L12。
  - 四個超能力第 1–2 點（看清限制、挑選模型）→ 吻合 `lecture-01` L28–29。
  - 四個超能力第 3 點（「正確的資訊＋清楚的指引」能改變條件機率）→ **不在頁尾兩頁 Wiki（S-02 / E4 中）**。
  - 右下角頁尾缺 `Slide 1 / 13` → **S-16 / E5 低**。

### Slide 2（L498–538）— 為什麼：生成動機與一對多平均困境
- **頁尾來源**：`concepts/function-mapping.md`、`concepts/probability-entropy-and-sampling.md`
- **本頁審查結論**：**未發現問題**。
- **實際核對項目**：
  1. 三大動機：讓電腦創作、圖靈（Alan Turing, 1950）無線打字機對話、費曼 *"What I cannot create, I do not understand."* → 完全吻合 `function-mapping` L44–47。
  2. 一對多不是函數、`"一個可愛的女孩"` 對應 $N$ 張不同照片、硬訓練得算術平均 $(\text{圖}_1+\dots+\text{圖}_N)/N$ 產生模糊「四不像」→ 完全吻合 `probability-entropy-and-sampling` L21。
  3. 兩大解決方向（潛張量 $z$ 代表天馬行空想法、輸出機率分佈再隨機抽樣）→ 完全吻合 `probability-entropy-and-sampling` L14, L22, L58–62。

### Slide 3（L540–612）— 是什麼：函數映射與張量
- **頁尾來源**：`concepts/function-mapping.md`、`sources/lecture-02-neural-networks.md`
- **本頁審查結論**：**未發現問題**。
- **實際核對項目**：
  1. 張量表（0 階純量 `x=9487`、1 階向量 `x=[9,4,8,7]` 與 784 維拉平影像、2 階矩陣 20 天×$N$ 特徵、3 階 3D 矩陣彩色 RGB）→ 完全吻合 `lecture-02` L24–25, L68 與 `function-mapping` L21。
  2. 函數映射式 $x_i \xrightarrow{f_\theta} f_\theta(x_i) = \hat{y}_i = [y_1, y_2, y_3]^T$ → 吻合 `function-mapping` L23。
  3. Softmax 公式 $(e^a/S, e^b/S, e^c/S)$、$S=e^a+e^b+e^c$、$\sum p_i=1$、條件機率 $P_\theta(y_i\mid x)=p_i$ → 吻合 `lecture-02` L28–29 與 `function-mapping` L34。
  4. 八哥辨識數值實例 `(1.9, 1.1, 0.2)` → `61% 土八哥、28% 白尾八哥、11% 家八哥` → 吻合兩頁 Wiki；Python 重算 `[61.27%, 27.53%, 11.19%]` 四捨五入即 `[61%, 28%, 11%]`。

### Slide 4（L614–661）— 是什麼：神經元與 3+1 種架構
- **頁尾來源**：`concepts/neural-networks-and-learning.md`、`sources/lecture-02-neural-networks.md`
- **逐項事實核對**：
  - 單一神經元三步驟、公式 $h=\varphi(w_1 x_1+w_2 x_2+w_3 x_3+b)$、$\theta=\{w_1,w_2,w_3,b\}$、ReLU / Sigmoid、萬用近似定理（一個隱藏層）→ 吻合兩頁 Wiki。
  - 3+1 架構表：DNN、CNN 基本說明吻合；**惟 RNN 列寫 `$h_{t-1}$`、`$x_t$` 與 Transformers 列寫 `Self-Attention`、「多模態生成」不在頁尾兩頁中（S-03 / E4 低）**。
  - 下方註解稱「三巨頭（Hinton、LeCun、Bengio）指出當年欠缺三大要件」→ 頁尾 Wiki 未說是「三巨頭指出」（**S-04 / E4 低**）。

### Slide 5（L663–701）— 是什麼：LLM 猜下一個字與 Word Embedding
- **頁尾來源**：`concepts/word-embedding-and-sampling-strategies.md`、`concepts/transformer-and-self-attention.md`
- **逐項事實核對**：
  - 「看前面一堆字，預測下一個字」、`"炎龍老師很帥"` 拆訓練對、`"今天天氣很好。"` $f_\theta(\text{"天"})=\text{"天"}/\text{"氣"}$ 一對多違反函數定義、記憶向量 $h_{t-1}$、條件機率 $P_\theta(w_i\mid x_1,\dots,x_T)$ → 吻合 `transformer-and-self-attention` L12–18 與 `word-embedding` L12。（註：「自監督學習」一詞出現在 `lecture-04` L24 與 `wiki/index.md`，頁尾兩頁寫「自動拆解為訓練樣本」。）
  - One-hot 編號（`的=1, 一=2, 我=5`）、代理任務、128 維隱藏層、Word2Vec (Mikolov et al., 2013) CBOW/Skip-Gram、權重即記憶 $W^T x=h$、Transformer 內建 Embedding 層 → 吻合 `word-embedding` L13, L23–36。
  - 等式 `國王 − 男人 + 女人 = 皇后` → 頁尾僅寫 `國王 — 男人 vs. 皇后 — 女人`，加減等式在未列頁尾之 `sources/lecture-04` L81（**S-05 / E4 低**）。

### Slide 6（L703–756）— 怎麼運作：損失函數、Cross Entropy 與梯度下降
- **頁尾來源**：`concepts/neural-networks-and-learning.md`、`concepts/probability-entropy-and-sampling.md`
- **逐項事實核對**：
  - 資訊量 $I(x)=-\log P(x)$（加州下雨）、夏農熵 $H(P)=-\sum p_i\log p_i$、交叉熵 $H(P,Q)=-\sum y_i\log\hat{y}_i=-\log\hat{y}_i$、比較表 `0.14/0.18` vs `0.36`、KL 散度 $D_{KL}(P\parallel Q)=H(P,Q)-H(P)$ 與 Soft Target `[0.7,0.2,0.1]` 差距 3 倍（`0.01` vs `0.03`）→ 吻合 `probability-entropy-and-sampling` L25–52（重算一致；MSE 實為 SSE 係沿用 Wiki 與原文）。
  - 梯度下降切線斜率、學習率 $\eta$、$w\leftarrow w-\eta(dL/dw)$、$\theta\leftarrow\theta-\eta\nabla L$、Backpropagation → 吻合 `neural-networks-and-learning` L54–61。
  - 括號內偏微分例題 `L=(b_1+2w_1−w_2−3)^2 在 (1,−1,2) 化為 4w_1^2`（重算正確）→ **不在頁尾兩頁 Wiki 中**，位於未列頁尾之 `sources/lecture-02` L60（**S-06 / E4 中**）。

### Slide 7（L758–817）— 怎麼運作：隨機抽樣與 Temperature / Top-k / Top-p
- **頁尾來源**：`concepts/probability-entropy-and-sampling.md`、`concepts/word-embedding-and-sampling-strategies.md`
- **逐項事實核對**：
  - GAN $\min_G \max_D V(D,G)$、StyleGAN 512 維 $z\to w$、AdaIN → 吻合 `probability-entropy-and-sampling` L55–57。
  - 八哥 argmax、「呆一布在」（家 15%、玩 12%、桌 7%、裝 3%）、Top-k（$k=50$、蔡炎＿必接龍）、Top-p（Nucleus Sampling, ICLR 2020, $p=0.9$, $\sum_{i=1}^N p_i>p$, $p'_k=p_k/P$）→ 吻合兩頁 Wiki。
  - 「咖啡推薦」一詞不在頁尾兩頁（位於 `sources/lecture-03` L71）→ **S-07 / E4 低**。
  - 互動元件 Temperature 模擬器：**直接引用「教材 `` `p.57` ``」（含未轉譯反引號，S-09 / E5 低），且混入 Wiki 未載之候選字代號 `c/b/a` 並將順序徹底標反為 `c(4.3) / b(3.4) / a(0.2)`（S-08 / E4 + E5 高）**；詳細重算見第三節。

### Slide 8（L819–875）— 怎麼運作：Transformer QKV 與 Scaled Dot-Product Attention
- **頁尾來源**：`concepts/transformer-and-self-attention.md`、`sources/external-vaswani-2017-attention-is-all-you-need.md`
- **逐項事實核對**：
  - RNN $O(n)$ vs Transformer $O(1)$、四步驟與列向量右乘 $Q=XW^Q, K=XW^K, V=XW^V$、$\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$、Footnote 4 變異數膨脹為 $d_k$ 與極小梯度區、第五講直覺抑制贏者通吃（$\tau=\sqrt{d_k}$）→ 吻合兩頁 Wiki。
  - 互動元件 $\sqrt{d_k}$ 切換器：未縮放與縮放之數值本身與頁尾 `transformer-and-self-attention` L44 及重算吻合；**惟按鈕與 JS 標題寫出 `√5 ≈ 2.236` 不在頁尾兩頁 Wiki 中（S-10 / E4 中，且連動階段 A `W-06` E2 錯誤）**；詳細重算見第三節。

### Slide 9（L877–930）— 怎麼運作：位置編碼、Multi-Head/Mask 與 ResNet/LayerNorm
- **頁尾來源**：`concepts/transformer-architecture-and-stability.md`、`sources/external-vaswani-2017-attention-is-all-you-need.md`
- **本頁審查結論**：**未發現問題**。
- **實際核對項目**：
  1. 位置編碼 $x_t+p_t$、$\omega_k=1/10000^{2k/d}$、$p_{2k}=\sin(\omega_k t)$、$p_{2k+1}=\cos(\omega_k t)$、單位圓時鐘（低位元快、高位元慢、$[-1,1]$）、$PE_{pos+k}$ 為 $PE_{pos}$ 線性函數與外插 → 完全吻合兩頁 Wiki。
  2. Multi-Head 與 Base 規格（$N=6, d_{\text{model}}=512, h=8, d_k=d_v=64$、Concat 乘 $W^O$）、三種 Attention（Encoder Self / Decoder Masked $-\infty$ / Decoder 中間層 $Q$ 來自 Decoder 前層、$K,V$ 來自 Encoder 輸出，含文字生圖）→ 完全吻合兩頁 Wiki（且未印出 `transformer-architecture-and-stability` L36 的錯誤合成公式 `W-07`）。
  3. ResNet 殘差連結 `LayerNorm(x + Sublayer(x))`、$z+\ell(z)\simeq f(z) \implies \ell(z)=f(z)-z$、Loss Landscape 平順、LayerNorm / RMSNorm（Llama 等，省去 $\mu$）/ DyT（Meta 最新，$\gamma\cdot\tanh(\alpha x)+\beta$）→ 完全吻合兩頁 Wiki。

### Slide 10（L932–981）— 例子：三個真實案例串聯
- **頁尾來源**：`concepts/function-mapping.md`、`concepts/neural-networks-and-learning.md`、`concepts/transformer-and-self-attention.md`
- **逐項事實核對**：
  - 案例 1（八哥三分類）：3 階張量、`[1,0,0]`、`[0.23, 0.43, 0.34]` 平方誤差和 `0.89`（重算 $0.8934\approx 0.89$）、`(1.9, 1.1, 0.2)` → `(61%, 28%, 11%)` → 吻合頁尾 Wiki。
  - 案例 2（MNIST DNN）：28×28→784 維、兩層 100 ReLU、10 維 Softmax / One-hot、SGD、learning rate、`batch_size`、`epochs` → 吻合頁尾 Wiki（惟「NIST 修改版」出自未列頁尾之 `sources/lecture-02` L68）。
  - 案例 3：《紅樓夢》300 萬參數、GPT-2 15 億、GPT-3 1,750 億參數與 4,990 億字、人類 1B vs Llama 3 15T（1.5 萬倍）→ 吻合 `transformer-and-self-attention` L57–60；**但「炎龍老師很」字庫編號 `87, 94, 112, 174, 221`、分數 `[1.40, 0.03, 1.71, -0.73, 0.95]` 與 Softmax `[30%, 7%, 40%, 4%, 19%]` 皆完全不在頁尾三頁 Wiki 中（S-11 / E4 中）**。

### Slide 11（L983–1028）— 常見誤解：五大迷思釐清
- **頁尾來源**：`concepts/probability-entropy-and-sampling.md`、`concepts/word-embedding-and-sampling-strategies.md`、`concepts/transformer-and-self-attention.md`、`concepts/transformer-architecture-and-stability.md`
- **逐項事實核對**：
  - 誤解 1（鑑別／生成同源）、誤解 3（Temperature $\tau>1$ vs $\tau<1$）、誤解 4（Decoder 中間層非 Self-Attention）→ 吻合頁尾 Wiki（誤解 3 含簡體字「指数」→ **S-13 / E5 低**）。
  - 誤解 2（Karpathy 2015 作夢機器、0% 夢境、幻覺不是 Bug）→ 大致吻合 `transformer-and-self-attention` L57（惟「只是當助理用時我們不希望它作夢」出自未列頁尾之 `sources/lecture-04` L50）。
  - 誤解 5（Balestriero, Pesenti, & LeCun 2021 高維度外插）→ **頁尾漏列 `concepts/neural-networks-and-learning.md`（S-12 / E4 + E5 中）**。

### Slide 12（L1030–1113）— 小結：全景概念串接與 Prompt 必殺技
- **頁尾來源**：`concepts/function-mapping.md`、`concepts/neural-networks-and-learning.md`、`concepts/probability-entropy-and-sampling.md`、`concepts/transformer-and-self-attention.md`
- **逐項事實核對**：
  - SVG Node 1–3 → 吻合頁尾前 3 頁。
  - SVG Node 4（`Word Embedding W^T x = h`、`Temperature`、`Top-k / Top-p`）與 Node 5（`Positional Encoding 時鐘`、`ResNet 殘差 + LayerNorm`）→ **頁尾漏列 `word-embedding-and-sampling-strategies.md` 與 `transformer-architecture-and-stability.md`，且 HTML 註解誤稱 `all 5 Concept pages`（S-14 / E4 + E5 中）**。
  - 下方 Prompt 必殺技卡：兩大重點吻合 `transformer-and-self-attention` L62；**但右卡「先給陽春方向」「先不要直接寫成品」「只要是 AI 生成的，務必自己讀過」在全部 12 頁 Wiki 中皆無記載，係直接取自 `raw` L04 p.106, p.109, p.110（S-15 / E4 中）**。

### Slide 13（L1115–1201）— 自我檢測：5 題互動小測驗
- **頁尾來源**：全部 6 篇 `concepts/*.md`
- 詳見下方第四節逐題核對；**5 題標準答案、JS 判定旗標與解析皆與 Wiki 實質一致**（僅 Q5 解析使用 `Cross-Attention` 一詞見於 `wiki/index.md` 與 `sources/lecture-05`，未出現於其所標 `concepts/transformer-architecture-and-stability.md` 正文，作輕微註記）。

---

## 三、互動元件專項審查與獨立重算

### 1. Slide 7：Temperature 模擬器（`setTau(tau)`，L780–809, L1264–1293）
- **輸入原始分數**：`[4.3, 3.4, 0.2]`
- **Python 獨立重算 vs 簡報 JS 顯示 vs Wiki（`word-embedding-and-sampling-strategies.md` L49–53）**：

| 溫度設定 | Python 精確計算 $p_i = \frac{e^{a_i/\tau}}{\sum e^{a_j/\tau}}$ | 四捨五入至整數百分比 | 簡報 JS 顯示值 | Wiki 數值 | 數值一致性 |
|---|---|---|---|---|---|
| **$\tau = 1.0$**（預設） | `[70.27%, 28.57%, 1.16%]` | `[70%, 29%, 1%]`（和 100%） | `70%, 29%, 1%` | `[0.70, 0.29, 0.01]` | **數值正確** |
| **$\tau = 2.0$**（高溫） | `[56.61%, 36.10%, 7.29%]` | `[57%, 36%, 7%]`（和 100%） | `57%, 36%, 7%` | `[0.57, 0.36, 0.07]` | **數值正確** |
| **$\tau = 0.5$**（低溫） | `[85.79%, 14.18%, 0.02%]` | `[86%, 14%, 0%]`（和 100%） | `86%, 14%, 0%` | `[0.86, 0.14, 0.00]` | **數值正確** |

- **互動元件致命錯誤（`S-08`，E4 + E5 高）**：
  - 雖然三組溫度下的機率數值計算完全正確，但三條長條圖的候選字標籤寫成：**`候選字 c (4.3)`、`候選字 b (3.4)`、`候選字 a (0.2)`**。
  - **問題一（E4）**：全部 12 頁 Wiki 從未把 `4.3, 3.4, 0.2` 標記為 `c, b, a`，簡報顯係直接查看 `raw` L04 p.57。
  - **問題二（E5）**：視覺核對 `raw` L04 p.53, p.54, p.57，實際對應是 **`a = 4.3`、`b = 3.4`、`c = 0.2`**；簡報直接掉入 PDF 文字流上下倒置陷阱，將 `a` 與 `c` 完全顛倒！

### 2. Slide 8：$\sqrt{d_k}$ 縮放切換器（`toggleDk(scaled)`，L853–866, L1295–1317）
- **輸入原始內積**：`[3.9, 3.2, 1.0, 0.3, 1.1]`
- **Python 獨立重算 vs 簡報 JS 顯示 vs Wiki（`transformer-and-self-attention.md` L44）**：

| 模式 | 計算步驟與精確值 | 四捨五入至整數百分比 | 簡報 JS 顯示值 | 頁尾 Wiki 數值 | 數值一致性 |
|---|---|---|---|---|---|
| **未縮放** | Softmax(`[3.9, 3.2, 1, 0.3, 1.1]`) = `[60.99%, 30.28%, 3.36%, 1.67%, 3.71%]` | `[61%, 30%, 3%, 2%, 4%]`（和 100%） | `61%, 30%, 3%, 2%, 4%` | `[61%, 30%, 3%, 2%, 4%]` | **完全一致** |
| **縮放後** | 除以 $\sqrt{5}\approx 2.2361$ 得精確商 `[1.7441, 1.4311, 0.4472, 0.1342, 0.4919]` → 兩位小數 `[1.74, 1.43, 0.45, 0.13, 0.49]`；Softmax 精確值 `[40.15%, 29.36%, 10.98%, 8.03%, 11.48%]`（以兩位小數算為 `[40.08%, 29.40%, 11.03%, 8.01%, 11.48%]`） | `[40%, 29%, 11%, 8%, 11%]`（和 **99%**） | `40%, 29%, 11%, 8%, 11%` | `[1.74, 1.43, 0.45, 0.13, 0.49]` 與 `[40%, 29%, 11%, 8%, 11%]` | **數值一致**（四捨五入和 99%） |

- **互動元件異常（`S-10`，E4 中，連動階段 A Wiki E2）**：
  - 按鈕文字 `同除以 √5 ≈ 2.236` 與 JS 標題 `除以 √5 後` 皆**不在頁尾標示的兩頁 Wiki 中**（僅見於 `sources/lecture-05` L40，且 `raw` L05 p.33 本身並未出現 `√5 ≈ 2.236`，屬階段 A `W-06` 延伸問題）。

---

## 四、Slide 13 自我檢測 5 題逐題核對

| 題號 | 題目重點 | JS 正解與選項 | 解析與引註 Wiki 核對 | 判定 |
|---|---|---|---|---|
| **Q1** | 同一提示詞「一個可愛的女孩」對應 100 張不同女孩照片硬訓練 $f_\theta$ 會發生什麼？ | 正解 **B**（`answerQuiz(1, true)`）：違反函數一對一/多對一，輸出 100 張照片的四不像平均 | 對照 `concepts/probability-entropy-and-sampling.md` L21–22（一對多不是函數、算術平均、四不像、需引入潛張量 $z$ 或機率抽樣）。完全吻合（題幹將 $N$ 張具體化為 100 張，不影響結論）。 | **正確** |
| **Q2** | 正解 $y=[1,0,0]$，`[0.7, 0.19, 0.11]` 與 `[0.7, 0.3, 0]` 的 Cross Entropy 關係為何？ | 正解 **A**（`answerQuiz(2, true)`）：兩者相等（皆為 $-\log 0.7 \approx 0.36$），因只看正確類別機率 | 對照 `concepts/probability-entropy-and-sampling.md` L34–36, L45–50。重算 $-\ln 0.7 = 0.3567 \approx 0.36$；MSE（平方誤差和）為 `0.14` vs `0.18`。完全吻合。 | **正確** |
| **Q3** | 希望 LLM 生成文字更固定、更一致，應如何調整 Temperature $\tau$？ | 正解 **B**（`answerQuiz(3, true)`）：調低 $\tau < 1$（如 $\tau = 0.5$），拉開高低分差距 | 對照 `concepts/word-embedding-and-sampling-strategies.md` L45–53, L72–73。重算 `[4.3, 3.4, 0.2]` 第一名由 $\tau=1$ 之 `70%` 升至 $\tau=0.5$ 之 `86%`。完全吻合。 | **正確** |
| **Q4** | Scaled Dot-Product Attention 為什麼要將 $QK^T$ 除以 $\sqrt{d_k}$？ | 正解 **A**（`answerQuiz(4, true)`）：內積變異數為 $d_k$，除以 $\sqrt{d_k}$ 把數值拉回 0 附近，避免 Softmax 贏者通吃與梯度消失 | 對照 `concepts/transformer-and-self-attention.md` L43–44（含 Vaswani 變異數為 $d_k$、極小梯度區與第五講贏者通吃直覺）。完全吻合。 | **正確** |
| **Q5** | 關於標準 Transformer 的 Encoder 與 Decoder 注意力層，何者正確？ | 正解 **B**（`answerQuiz(5, true)`）：Decoder 第一層將未來位置設為 $-\infty$（Mask 遮住），中間層 $Q$ 來自 Decoder、$K,V$ 來自 Encoder（非 Self-Attention） | 對照 `concepts/transformer-architecture-and-stability.md` L39–43, L61–62。機制完全吻合（附註：解析內用詞 `Cross-Attention` 見於 `wiki/index.md` L21 與 `sources/lecture-05` L15，未出現於 `transformer-architecture-and-stability.md` 正文，屬輕微術語跨頁）。 | **正確** |

- **自我檢測整體結論**：**5 題全部未發現事實或答案判定錯誤**；互動計分腳本 `answerQuiz()` 與 `revealAllQuiz()` 邏輯正確（可重複切換選項並即時重算總分 `0–5 / 5 題`）。

---

## 五、格式、結構與互動功能總檢（E5 檢核表）

| 檢查項目 | 檢查結果 | 說明 |
|---|---|---|
| 單一自足 HTML 檔（無外部依賴） | **通過** | 全檔僅單一 `slides/index.html`，無外部 CDN CSS/JS/字型引用，可直接以瀏覽器離線開啟。 |
| 鍵盤左右鍵翻頁 | **通過** | L1248–1262 支援 `ArrowRight`/`ArrowLeft`/`PageDown`/`PageUp`/`Home`/`End`/`Space`（註：空白鍵全域 `preventDefault()` 在焦點停留在按鈕上時會優先翻頁而非觸發按鈕，屬輕微 UX 注意事項）。 |
| 七段教學結構完整順序 | **通過** | 為什麼（1–2）→ 是什麼（3–5）→ 怎麼運作（6–9）→ 例子（10）→ 常見誤解（11）→ 小結（12）→ 自我檢測（13），結構完整。 |
| 每頁頁尾顯示來源 Wiki 頁名 | **不通過（漏列）** | 全部 13 頁皆有 `.wiki-source-badge`，但 **Slide 1, 4, 5, 6, 7, 8, 10, 11, 12 均出現頁尾未涵蓋的內容或漏列實際引用的 Wiki 頁**（詳見 `S-01`～`S-15`）。 |
| 排版與文字潔淨度 | **不通過** | Slide 7 L782 殘留 Markdown 反引號 `` `p.57` ``（`S-09`）、Slide 7 L793–805 標籤 `c/b/a` 顛倒（`S-08`）、Slide 11 L1010 簡體錯字「指数」（`S-13`）、Slide 1 L494 右下角未寫 `Slide 1 / 13`（`S-16`）。 |

---

## 六、統計彙整

| 錯誤類型碼 | 定義 | 高 | 中 | 低 | 小計 | 對應發現編號 |
|---|---|---:|---:|---:|---:|---|
| **E4** | 簡報混入頁尾所列 Wiki 以外內容（含跨頁未列頁尾、繞過 Wiki 引用 `raw/` 或外部記憶） | 1* | 7 | 4 | **12** | `S-01`～`S-08`, `S-10`～`S-12`, `S-14`, `S-15`（註：`S-08, S-12, S-14` 同時含 E5；`S-10` 連動 Wiki E2） |
| **E5** | 簡報 HTML 格式、互動元件標籤、頁尾漏列或文字瑕疵 | 1* | 2* | 3 | **6** | `S-08`*, `S-09`, `S-12`*, `S-13`, `S-14`*, `S-16` |
| **連動階段 A（E2）** | 簡報沿用 Wiki 本身之未標註反推錯誤 | 0 | 1* | 0 | **1** | `S-10`（對應 Wiki `W-06`） |
| **獨立異常項目總數（去重）** | | **1** | **8** | **7** | **16** | `S-01`～`S-16` |

- **「無法確認」項目數**：**0 件**（全部 13 頁與 2 個互動元件皆已完成 Wiki 核對與 Python 重算）。
- **未發現問題之投影片**：Slide 2、Slide 3、Slide 9、以及 Slide 13 全部 5 題自我檢測題目／答案／解析。

---

## 七、整體結論與建議退回節點（依 graph v2 條件邊）

**整體結論：階段 B（簡報）審查「不通過」，需分流退回修正。**

雖然簡報的單檔離線結構、七段教學流、Slide 2/3/9 與 5 題自我檢測皆表現良好，且兩組互動元件的 Softmax 數值計算正確，但審查發現 **1 件高嚴重度錯誤**（`S-08`：Slide 7 Temperature 模擬器繞過 Wiki 直接讀取 `raw` L04 p.57，並誤踩 PDF 倒置陷阱將 `a (4.3)` 與 `c (0.2)` 標籤完全顛倒）以及多處頁尾漏列來源或混入非 Wiki 細節（`S-01, S-02, S-06, S-10, S-11, S-12, S-14, S-15`）。依 `AGENTS.md` graph v2 條件邊，建議退回下列節點：

1. **退回節點 `B1`（處理 E4，12 件：`S-01`～`S-08`, `S-10`～`S-12`, `S-14`, `S-15`）**：
   - 重新嚴格執行「**簡報只讀 `wiki/`**」原則與頁尾可追溯性對齊：
     - **移除全部 12 頁 Wiki 中不存在的非 Wiki 內容**：`S-01`（Slide 1 移除 Claude/Gemini/Grok 或改為 Wiki 原述）、`S-02`（Slide 1 移除「改變條件機率」）、`S-08`（Slide 7 移除「教材 `p.57`」與 Wiki 未載之候選字代號 `c/b/a`，僅標分數或先待 Wiki 補齊正確 `a=4.3, b=3.4, c=0.2` 後再引用）、`S-15`（Slide 12 移除僅存於 `raw` 之「陽春」「先不要直接寫成品」「只要是 AI 生成的，務必自己讀過」，改依 Wiki 表述）。
     - **補齊各頁頁尾實際引用的 Wiki 頁名**（或收斂內容使其完全落於頁尾所列 Wiki 內）：`S-03`、`S-04`、`S-05`、`S-06`（Slide 6 補 `sources/lecture-02` 或刪除括號例題）、`S-07`、`S-11`（Slide 10 補 `sources/lecture-04`、`sources/lecture-02`）、`S-12`（Slide 11 補 `concepts/neural-networks-and-learning.md`）、`S-14`（Slide 12 補 `concepts/word-embedding-and-sampling-strategies.md` 與 `concepts/transformer-architecture-and-stability.md`）。
2. **退回節點 `B3`（處理 E5，6 件：`S-08`, `S-09`, `S-12`, `S-13`, `S-14`, `S-16`）**：
   - 修正 Slide 7 互動模擬器顛倒的標籤（`c/b/a` → 改為正確的 `a (4.3), b (3.4), c (0.2)` 或「候選字 1/2/3」以對齊 Wiki）。
   - 修正 Slide 7 L782 未轉譯 Markdown 反引號 `` `p.57` ``、Slide 11 L1010 簡體錯字「指数」→「指數」、Slide 12 L1039 註解 `5 Concept pages` → `6 Concept pages`、Slide 1 右下角頁碼格式統一為 `Slide 1 / 13`。
3. **轉入階段 A 節點 `A4b`（處理連動 Wiki 錯誤：`S-10` → Wiki `W-06`）**：
   - 先於階段 A 處理 `wiki/sources/lecture-05-sequence-memory-and-attention.md`（L40）將未出現於 `raw` p.33 的 `√5 ≈ 2.236` 改為明確的反推註記（或移除），再同步更新 Slide 8 按鈕與 JS 標題文字（如改為「同除以 $\tau = \sqrt{d_k}$（拉回 0 附近）」）。
