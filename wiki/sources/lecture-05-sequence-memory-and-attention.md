---
title: 05 AI 怎麼記得前面說過什麼？（來源摘要）
type: source
sources: [05AI怎麼記得前面說過什麼？.pdf]
updated: 2026-11-18
status: linted
---

# 05 AI 怎麼記得前面說過什麼？（來源摘要）

## 基本資訊與分段處理紀錄
- **原始檔案**：`raw/lectures/05AI怎麼記得前面說過什麼？.pdf`（共 86 頁）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.3, p.86]`。
- **分段讀取範圍**（超過 60 頁分兩段處理）：
  - **第一段（p.1–60）**：RNN 遞歸層數學原理與矩陣表示（p.1–8）；線性代數 101（先列後行、內積、Google 偏愛列向量與列向量線性組合）（p.9–14）；QKV 注意力機制推導、Self-Attention、除以 $\sqrt{d_k}$ 抑制 Softmax 贏者通吃、Multi-Head Attention、Encoder vs. Decoder 與 Masked Self-Attention（p.15–40）；位置編碼（Positional Encoding）與單位圓時鐘直覺（p.41–50）；ResNet 殘差連結與 Layer Normalization（p.51–60）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.2, p.9, p.15, p.41, p.51]`。
  - **第二段（p.61–86）**：LayerNorm 向量廣播運算、RMSNorm（Llama 等採用）與 Dynamic Tanh（DyT，Meta 提出）（p.61–65）；跨模態資訊混入（文字生圖 Cross-Attention）（p.66–67）；Vibe Coding 實作單一 HTML 互動網頁與 GitHub Pages 部署流程（p.68–86）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.61, p.68]`。

---

## 重點摘要

### 一、RNN 遞歸層原理與線性代數基礎
1. **RNN 遞歸層的數學式**：
   - 以具有 2 個輸入 $(x^1_t, x^2_t)$、2 個 RNN 神經元的遞歸層為例：它看起來像全連結層，但差別在於**上次 RNN 層的輸出（hidden states）$h_{t-1} = [h^1_{t-1}, h^2_{t-1}]^T$ 還會再傳回來**，連同本次正常輸入 $x_t = [x^1_t, x^2_t]^T$ 一起決定本次輸出 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.3-6]`。
   - 第 1 號 RNN 神經元的輸出公式為 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.5]`：
     $$h^1_t = \sigma\left(w^x_{11} x^1_t + w^x_{21} x^2_t + w^h_{11} h^1_{t-1} + w^h_{21} h^2_{t-1} + b_1\right)$$
   - 若寫成矩陣乘法，可利用 $(W_X)^T \cdot x_t$ 與 $(W_H)^T \cdot h_{t-1}$ 同時算出兩個 RNN 神經元的輸入與記憶加權和 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.6-8]`。
2. **線性代數 101：為什麼 Google 把矩陣乘在右邊？**：
   - 矩陣核心口訣是**「先列後行」**：$m \times n$ 矩陣有 $m$ 列（橫）、$n$ 行（直）；若 $C=AB$，則 $c_{ij}$ 是 $A$ 的第 $i$ 列與 $B$ 的第 $j$ 行的**內積（dot product）** $\langle u, v \rangle = u v^T = \sum_{k=1}^p a_k b_k$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.10-12]`。
   - 一般線性代數習慣以行向量為中心寫成 $Ax$，但 **Google 極度偏愛列向量（與內積）**，當列向量 $x = [x_1, x_2, \dots, x_m]$ 乘在矩陣 $A$ 左方（$x A$）時，結果 $x_1 a_1 + x_2 a_2 + \dots + x_m a_m$ 正好是由 $x$ 向量的各分量對 $A$ 矩陣的**列向量做線性組合** `[來源: 05AI怎麼記得前面說過什麼？.pdf p.13-14]`。

### 二、QKV 注意力機制、$\sqrt{d_k}$ 縮放與多頭注意力
1. **從單一 Query 到 Self-Attention 矩陣公式**：
   - 2017 年 Google 發表 *"Attention Is All You Need"*（Vaswani et al., NIPS 2017）提出 Transformer 架構以取代 RNN `[來源: 05AI怎麼記得前面說過什麼？.pdf p.16]`。
   - 給定一段先備知識 $x_1, \dots, x_T$（每個 $x_t$ 皆產生特徵代表向量 $k_t, v_t$），當一個問題（query）$q$ 進來時，想找出最適合 $q$ 的代表向量 $h = \alpha_1 v_1 + \alpha_2 v_2 + \dots + \alpha_T v_T$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.17-20]`。
   - **計算步驟**：以內積計算相關強度 $a(q, k_t) = \langle q, k_t \rangle = q k_t^T = e_t$（將所有 $k_t, v_t$ 以列向量排成矩陣 $K, V$，則強度可一次算完：$q K^T = [e_1, e_2, \dots, e_T]$），再經 Softmax 得到權重係數 $\text{softmax}(q \cdot K^T) = [\alpha_1, \alpha_2, \dots, \alpha_T]$，最後乘上 $V$ 即完成對 $V$ 列向量的線性組合 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.21-26]`：
     $$\text{Attention}(q, K, V) = \text{softmax}(q \cdot K^T)V$$
   - **Self-Attention（大家輪流當 $q$）**：每個 $x_t$ 除了產生 $k_t, v_t$ 外也產生自己的 $q_t$（由列向量矩陣乘法一次算出：$Q = X W^Q, K = X W^K, V = X W^V$），將所有 $q_i$ 排成矩陣 $Q$，即可一次平行算出所有位置的記憶輸出 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.27-30, p.34-35]`。
2. **為什麼要除以 $\sqrt{d_k}$？（抑制 Softmax 贏者通吃）**：
   - Google 發現直接用內積 $\text{softmax}(QK^T)V$ 效果不如預期，主因是當數值偏大時，**Softmax 的「贏者通吃」特性會讓最高分權重比合理比例高出太多** `[來源: 05AI怎麼記得前面說過什麼？.pdf p.31]`。
   - **數值實例**：原始分數 `[3.9, 3.2, 1, 0.3, 1.1]`（前兩名感覺只差一點），直接經 Softmax 卻變成 `[61%, 30%, 3%, 2%, 4%]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.32]`；若同除以 $\tau = \sqrt{d_k} = \sqrt{5} \approx 2.236$ 將數字拉回 0 附近，分數變為 `[1.74, 1.43, 0.45, 0.13, 0.49]`，經 Softmax 後即成為較平緩合理的 `[40%, 29%, 11%, 8%, 11%]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.33]`。
   - 因此加入縮放因子 $\sqrt{d_k}$（其中 $d_k = \text{dim}(k_i)$，本質上就如同設定溫度超參數 $\tau = \sqrt{d_k}$）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.31, p.33]`：
     $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
3. **Multi-Head Attention 與 Encoder / Decoder 的三種注意力**：
   - **多頭注意力（Multi-Head Attention）**：注意力沒理由只有一種，因此可定義第 $n$ 個注意力頭為 $\text{Attention}(X W^Q_n, X W^K_n, X W^V_n)$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.36]`。
   - **Encoder 與 Decoder 的設計差異**：Transformer 輸入有幾個字/詞向量，輸出就有幾個 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.39]`：
     1. **Encoder 的 Multi-Head (Self) Attention**：由輸入向量自家生產 $q, k, v$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.37]`。
     2. **Decoder 第一層的 Masked Multi-Head (Self) Attention**：同樣自家生產 $q, k, v$，但**一開始還沒有出現的未來輸入會被 Mask 遮住** `[來源: 05AI怎麼記得前面說過什麼？.pdf p.37, p.40]`。
     3. **Decoder 中間層的 Multi-Head Attention（唯一不是 Self-Attention 的一層）**：其 $q$ 來自 Decoder 前一層的輸出，而 $k, v$ 則來自 Encoder 的輸出 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.38]`。（同理，在文字生圖等跨模態 AI 中，可用隨機產生的想法 $Z$ 作為 $Q$，並用代表文字意思的矩陣 $\chi$ 產生 $K, V$，藉此把文字意涵混入圖像生成 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.66-67]`。）

### 三、位置編碼（Positional Encoding）與時鐘直覺
1. **為什麼需要位置編碼？**：RNN 是真的逐字讀取，而 Transformer 為了平行化一次做完 Self-Attention，本身沒有考慮每個字的先後順序，因此必須把位置資訊 $p_t$ 加到原本的 word embedding $x_t$ 上（$x_t + p_t$）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.42, p.45]`。
2. **奇幻進位系統與 $(\sin, \cos)$ 時鐘**：
   - 觀察十進位數（如 `9487`，在向量中低位數寫在前面如 `[7, 8, 4, 9]`），位數越低變化頻率越高（頻率 $1$），位數越高週期越長、頻率越低（頻率 $1/10, 1/100, 1/1000$）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.43, p.45]`。
   - 為了找一個連續、有週期性、且數值不大（介於 $[-1, 1]$ 以免蓋過原 embedding）的通用進位系統，原論文將位置向量 $p_t = [p_0, p_1, \dots, p_{d-1}]$ 兩兩一組設為同頻率 $\omega_k$（要求 $\omega_0 > \omega_1 > \dots$，越往後頻率越慢）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.44, p.46-47]`：
     $$\omega_k = \frac{1}{10000^{2k/d}}, \quad p_i = \begin{cases} \sin(\omega_k \cdot t), & \text{當 } i = 2k \\ \cos(\omega_k \cdot t), & \text{當 } i = 2k+1 \end{cases}$$
   - **為什麼同時要 $\sin$ 與 $\cos$？**：每一組 $(\sin(\omega_k t), \cos(\omega_k t))$ 剛好是單位圓上的一點，可想成**時鐘指針上的一個點**（當 $t=0$ 時指向 $(0, 1)$ 即一般時鐘 12 點方向，且隨 $t$ 增加呈順時鐘旋轉）；低位元的時鐘轉得快、高位元的時鐘轉得慢 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.48-50]`。

### 四、讓 Transformer 更深更穩的技術：ResNet 殘差連結與 Normalization
1. **ResNet 殘差連結（Residual Connection）**：
   - 原版 Transformer 大量使用了 ResNet 型的設計：將原本希望某層直接學會目標 $f(z)$（即 $\ell(z) \simeq f(z)$），改為輸出 **$z + \ell(z) \simeq f(z)$** `[來源: 05AI怎麼記得前面說過什麼？.pdf p.52-56]`。
   - 這代表該層神經網路**只需要學習「之前還沒學到的殘差」** $\ell(z) = f(z) - z$；若前面的 $z$ 已經很接近正確答案 $f(z)$，後面 $\ell(z)$ 就不太需要再學什麼 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.56-57]`。
   - Li et al. (NeurIPS 2018) *"Visualizing the Loss Landscape of Neural Nets"* 顯示，加入 skip connection 後，損失函數地形會從極度崎嶇變得非常平順好走 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.58]`。
2. **從 Layer Normalization 到 RMSNorm 與 DyT**：
   - **Layer Normalization（原版 Transformer 採用）**：對單一樣本向量 $x=(x_1, \dots, x_n)$ 計算平均值 $\mu = \frac{1}{n}\sum_{i=1}^n x_i$ 與標準差 $\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^n (x_i - \mu)^2}$，標準化為 $\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}}$（$\epsilon$ 預防除以 0），再以學習而來的向量 $\gamma, \beta$ 調整為 $y_i = \gamma \hat{x}_i + \beta$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.60-62]`。（相較之下，Batch Normalization 則是跨樣本 $x_1, \dots, x_m$ 計算平均與標準差 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.59]`。）
   - **RMSNorm（Llama 等現代 LLM 採用）**：省略平均值 $\mu$，只算均方根 $\text{RMS}(x) = \sqrt{\frac{1}{n}\sum_{i=1}^n x_i^2}$，並計算 $\text{RMSNorm}(x) = \frac{x}{\text{RMS}(x)} \cdot \gamma$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.64]`。
   - **Dynamic Tanh（DyT，Meta 提出）**：主張不需做 Normalization，直接以 $\text{DyT}(x) = \gamma \cdot \tanh(\alpha x) + \beta$（其中純量 $\alpha$ 初值可設為 $0.5$，$\gamma, \beta$ 為學習來的向量）取代 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.65]`。

### 五、Vibe Coding 單一檔案互動網頁實作
- 互動網頁由三種技術組成：**HTML**（決定內容）、**CSS**（決定排版、字型、顏色）、**JavaScript**（讓網頁能互動），且可寫在**單一檔案的 `index.html`** 中，直接拉進瀏覽器即可執行，或上傳至 GitHub 透過 GitHub Pages（`https://你的帳號.github.io/repo名稱/`）發布 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.69-70, p.76-85]`。

---

## 關聯概念頁
- [[transformer-and-self-attention]]
- [[transformer-architecture-and-stability]]
