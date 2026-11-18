---
title: Transformer 完整架構：位置編碼、殘差連結與正規化（Positional Encoding, Residual & Norm）
type: concept
sources: [05AI怎麼記得前面說過什麼？.pdf, Vaswani_2017_Attention_Is_All_You_Need.pdf]
updated: 2026-11-18
status: linted
---

# Transformer 完整架構：位置編碼、殘差連結與正規化

## 一、為什麼只有 Self-Attention 還不夠組成 Transformer？
雖然 **Self-Attention（自注意力機制）**讓模型擺脫了 RNN 逐字遞迴的瓶頸、能夠一次平行處理整段序列（參見 [[transformer-and-self-attention]]），但若只有單純的 Self-Attention，模型仍會面臨三個關鍵問題 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.36, p.42, p.52]`：
1. **喪失先後順序感**：平行做內積時，「狗咬人」與「人咬狗」的字向量集合相同，模型不知道誰前誰後 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.42]`。
2. **單一注意力視角有限，且生成時不能偷看未來答案**：只算一組 Q, K, V 只能捕捉一種關聯，且在 Decoder 生成下一個字時，不能讓模型偷看後面還沒生出來的字 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.36-40]`。
3. **網路疊深後難以訓練與收斂**：當層數變深，損失函數地形會變得極度崎嶇，數值也容易發散 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.52, p.58]`。

為了解決這三大問題，Transformer 引入了**位置編碼（Positional Encoding）**、**多頭與遮罩注意力（Multi-Head & Masked Attention）**，以及**殘差連結（Residual Connection）與正規化（LayerNorm / RMSNorm）**`[來源: 05AI怎麼記得前面說過什麼？.pdf p.36-64]`。

---

## 二、是什麼與怎麼運作：三大核心架構組件

### 1. 位置編碼（Positional Encoding）：快慢不同的單位圓時鐘
為了讓平行運算的 Transformer 知道每個字的位置 $t$，我們在輸入的詞嵌入向量 $x_t$ 上直接加上一個同為 $d$ 維的**位置向量 $p_t$**（即 $x_t + p_t$）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.42, p.45]`。
- **奇幻進位系統的設計條件**：觀察十進位制（如 `9487`，低位數變化頻率最快、高位數週期最長頻率最低），我們希望位置編碼具備：(1) **連續函數**、(2) **有週期性**、(3) **數值不要太大**（以免蓋過原本的 word embedding $x_t$），因此自然選用介於 $[-1, 1]$ 的 $\sin$ 與 $\cos$ 函數 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.43-44]`。
- **數學公式**：將 $d$ 維位置向量 $p_t = [p_0, p_1, \dots, p_{d-1}]$ 兩兩一組配對相同頻率 $\omega_k$（足標 $k$ 從 $0$ 開始，頻率隨維度增加而變慢 $\omega_0 > \omega_1 > \dots$）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.46-48]`：

$$\omega_k = \frac{1}{10000^{2k/d}}, \quad \begin{cases} p_{2k} = \sin(\omega_k \cdot t) \\ p_{2k+1} = \cos(\omega_k \cdot t) \end{cases}$$

- **為什麼同時需要 $\sin$ 與 $\cos$？（時鐘直覺與相對位置線性轉換）**：
  - **幾何時鐘直覺（第五講）**：每一組 $(\sin(\omega_k t), \cos(\omega_k t))$ 剛好構成**單位圓上的一點**，當 $t=0$ 時指向 $(0, 1)$（一般時鐘的 12 點方向），隨位置 $t$ 增加則沿順時鐘方向旋轉；低位元（$k$ 小）就像轉得快的秒針／分針，高位元（$k$ 大）就像轉得慢的時針 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.49-50]`。
  - **代數相對位置性質（Vaswani et al., 2017）**：對於任何固定的位置偏移量 $k$，**$PE_{pos+k}$ 都可以表示為 $PE_{pos}$ 的線性函數**，這讓模型能輕易學會根據「相對位置（relative positions）」分配注意力，並外插到比訓練時更長的序列長度 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6]`。

### 2. Multi-Head Attention 與 Encoder / Decoder 的三種注意力機制
- **多頭注意力（Multi-Head Attention）**：字與字之間的關聯不只一種（如語法關聯、指代關聯、語意關聯），若只用單一注意力頭做平均會抑制不同子空間的資訊；因此將 $Q, K, V$ 以不同學習矩陣投影 $h$ 次（原版 Base 模型設 $d_{\text{model}}=512$、平行頭數 **$h=8$**、每頭維度 **$d_k = d_v = d_{\text{model}}/h = 64$**），平行計算後再串接（Concat）並乘上輸出投影矩陣 $W^O$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.36]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.4-5]`：
  $$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)W^O, \quad \text{where } \text{head}_n = \text{Attention}(X W^Q_n, X W^K_n, X W^V_n)$$
- **Encoder 與 Decoder 中的三種 Attention 角色**（原版 Base 模型 Encoder 與 Decoder 各堆疊 **$N=6$ 層**，每層另含內層維度 $d_{ff}=2048$ 的前饋網路 $\text{FFN}(x)=\max(0, xW_1+b_1)W_2+b_2$）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.37-40, p.67]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.3, p.5]`：

| 所在位置 | 注意力層名稱 | $Q, K, V$ 的來源 | 核心功能與特性 |
|---|---|---|---|
| **Encoder 底層** | Multi-Head (Self) Attention | $Q, K, V$ 全部由 Encoder 輸入向量**自家生產** | 雙向理解整段輸入序列的所有上下文關聯 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.37, p.39]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.5]` |
| **Decoder 第一層** | **Masked** Multi-Head (Self) Attention | $Q, K, V$ 全部由 Decoder 輸入向量**自家生產** | 將尚未生成的未來位置在 Softmax 輸入前**設為 $-\infty$（Mask 遮住）**，確保預測下一個字時保持自回歸（auto-regressive）特性、不偷看未來答案 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.37, p.40]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.3, p.5]` |
| **Decoder 中間層**（及跨模態混入） | Multi-Head Attention（**非 Self-Attention**） | **$Q$ 來自 Decoder 前一層輸出**；**$K, V$ 來自 Encoder 輸出** | 讓生成端根據查詢 $Q$ 去檢索輸入端（或文字生圖中的文字矩陣 $\chi$）的先備知識 $K, V$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.38, p.67]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.5]` |

### 3. 深層穩定雙引擎：ResNet 殘差連結與正規化（LayerNorm $\to$ RMSNorm $\to$ DyT）
1. **ResNet 殘差連結（Residual / Skip Connection）**：
   - 在原版 Transformer 中，每個子層（Sub-layer）周圍都加上殘差連結並接上 Layer Normalization，輸出寫為 $\text{LayerNorm}(x + \text{Sublayer}(x))$ `[來源: 05AI怎麼記得前面說過什麼？.pdf p.52]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.3]`。
   - 若直接要求某層網路硬學出目標函數 $\ell(z) \simeq f(z)$，當層數很深時極難訓練；ResNet 將架構改為把輸入 $z$ 直接跳接加上去：`[來源: 05AI怎麼記得前面說過什麼？.pdf p.53-56]`
     $$z + \ell(z) \simeq f(z) \implies \ell(z) = f(z) - z$$
   - 這使該層只需要學習**「之前還沒學到的殘差」**；若前一層輸出 $z$ 已接近目標，該層 $\ell(z)$ 幾乎不需費力調整，大幅平滑了損失函數地形（Loss Landscape，Li et al., NeurIPS 2018）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.56-58]`。
2. **正規化技術的演進**：
   - **Layer Normalization（原版 Transformer 採用）**：對單一字向量 $x = (x_1, \dots, x_n)$ 計算平均 $\mu = \frac{1}{n}\sum_{i=1}^n x_i$ 與標準差 $\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^n (x_i - \mu)^2}$，標準化並以學習參數 $\gamma, \beta$ 縮放平移 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.60-62]`：
     $$\hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta$$
   - **RMSNorm（Llama 等現代開源 LLM 採用）**：省去計算平均值 $\mu$，直接除以均方根 $\text{RMS}(x) = \sqrt{\frac{1}{n}\sum_{i=1}^n x_i^2}$：`[來源: 05AI怎麼記得前面說過什麼？.pdf p.64]`
     $$\text{RMSNorm}(x) = \frac{x}{\text{RMS}(x)} \cdot \gamma$$
   - **Dynamic Tanh（DyT，Meta 最新提出）**：甚至移除標準差除法，改以 $\text{DyT}(x) = \gamma \cdot \tanh(\alpha x) + \beta$ 實現穩定訓練 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.65]`。

---

## 三、常見誤解
- **誤解 1：「Transformer 裡面每一層的 Attention 都是 Self-Attention（自注意力）」**
  - **事實**：在標準 Encoder-Decoder Transformer 中，Decoder 中間那層並不是 Self-Attention！它的 Query ($Q$) 來自 Decoder 前一層，但 Key ($K$) 與 Value ($V$) 來自 Encoder 的輸出（在跨模態文字生圖中，也是用圖像潛變數當 $Q$、文字特徵當 $K, V$）`[來源: 05AI怎麼記得前面說過什麼？.pdf p.38, p.67]`。
- **誤解 2：「位置編碼（Positional Encoding）只是在每個字後面串接一個代表第幾個字的整數 $1, 2, 3, \dots$」**
  - **事實**：若直接放整數 $1, 2, \dots, T$，句子越長數值越大，會嚴重破壞原本的詞嵌入向量；因此原版 Transformer 採用與詞向量同維度 $d$、由不同頻率 $\omega_k = 1/10000^{2k/d}$ 的 $(\sin(\omega_k t), \cos(\omega_k t))$ 所組成的有界週期向量，直接加在詞嵌入向量上 `[來源: 05AI怎麼記得前面說過什麼？.pdf p.42-50]`。

---

## 相關概念與來源
- 前置概念：[[transformer-and-self-attention]]、[[word-embedding-and-sampling-strategies]]
- 來源摘要：[[lecture-05-sequence-memory-and-attention]]、[[external-vaswani-2017-attention-is-all-you-need]]
