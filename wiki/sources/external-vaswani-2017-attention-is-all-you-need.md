---
title: Attention Is All You Need（Vaswani et al., 2017 外部交叉查核摘要）
type: source
sources: [Vaswani_2017_Attention_Is_All_You_Need.pdf]
updated: 2026-11-18
status: linted
---

# Attention Is All You Need（Vaswani et al., 2017 外部交叉查核摘要）

## 基本資訊與處理紀錄
- **原始檔案**：`raw/external/Vaswani_2017_Attention_Is_All_You_Need.pdf`（共 15 頁，未超過 60 頁，單段完整讀取）`[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.1, p.15]`。
- **論文資訊**：Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin (Google Brain / Google Research / University of Toronto), *"Attention Is All You Need"*, 31st Conference on Neural Information Processing Systems (NIPS 2017), arXiv:1706.03762v7 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.1]`。
- **專案角色**：作為本專案的**外部交叉查核節點（Cross-Verification Node）**，與第四講 `04LLM只是在猜下一個字？.pdf` 及第五講 `05AI怎麼記得前面說過什麼？.pdf` 進行公式、架構與理論依據的跨來源比對。

---

## 重點摘要

### 一、為什麼提出完全基於 Attention 的 Transformer？
1. **RNN 的循序運算瓶頸**：傳統主流序列轉換模型（如 RNN、LSTM、GRU）沿著序列位置 $t$ 逐步計算隱藏狀態 $h_t$（作為 $h_{t-1}$ 與當前輸入的函數），這種天生的循序性（inherently sequential nature）阻礙了訓練樣本內的平行化計算，在長序列時尤為嚴重 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.2]`。
2. **完全捨棄遞迴與卷積**：Transformer 是第一個完全依賴自注意力機制（Self-Attention / Intra-Attention）來計算輸入與輸出表徵、徹底摒棄 RNN 遞迴與 CNN 卷積的序列轉換模型 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.1-2]`。
3. **Table 1 三大理論優勢（複雜度、平行化、長距離依賴路徑）**：
   設序列長度為 $n$、表徵維度為 $d$、卷積核寬度為 $k$ `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6]`：
   - **Self-Attention**：每層計算複雜度為 $O(n^2 \cdot d)$（當常見句子長度 $n < d$ 時比 RNN 的 $O(n \cdot d^2)$ 更快）、最少循序操作數（Sequential Operations）為 **$O(1)$**、任意兩個位置之間的最大路徑長度（Maximum Path Length）為 **$O(1)$** `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6-7]`。
   - **Recurrent（RNN）**：每層複雜度為 $O(n \cdot d^2)$、最少循序操作數為 **$O(n)$**、最大路徑長度為 **$O(n)$** `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6]`。
   - **Convolutional（CNN）**：每層複雜度為 $O(k \cdot n \cdot d^2)$、最少循序操作數為 $O(1)$，但最大路徑長度需 $O(n/k)$（一般卷積）或 $O(\log_k(n))$（膨脹卷積）；而前向與反向訊號在網路中傳遞的路徑越短，越容易學會長距離依賴關係（long-range dependencies）`[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6-7]`。

### 二、Scaled Dot-Product Attention 與 $\frac{1}{\sqrt{d_k}}$ 縮放原理
1. **公式 (1) 定義**：輸入包含維度為 $d_k$ 的 queries 與 keys、以及維度為 $d_v$ 的 values；實務上將一組 queries 打包為矩陣 $Q$、keys 與 values 打包為矩陣 $K$ 與 $V$，輸出矩陣為 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.4]`：
   $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
2. **為什麼要除以 $\sqrt{d_k}$？（梯度消失與變異數推導）**：
   - 當 $d_k$ 較小時，加性注意力（additive attention）與內積注意力（dot-product attention）表現相近；但當 $d_k$ 較大時，未縮放的內積注意力表現變差 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.4]`。
   - **原因與 Footnote 4 證明**：若假設 $q$ 與 $k$ 的各分量為互相獨立、平均數為 $0$、變異數為 $1$ 的隨機變數，則它們的內積 $q \cdot k = \sum_{i=1}^{d_k} q_i k_i$ 的**平均數為 $0$、變異數為 $d_k$**；當 $d_k$ 很大時，內積數值量級變大，會將 Softmax 函數推入**梯度極小（extremely small gradients）**的區域，因此除以 $\sqrt{d_k}$ 可抵消此效應（使變異數回到 $1$）`[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.4]`。

### 三、Multi-Head Attention、Encoder-Decoder 與 Masking 規格
1. **Encoder 與 Decoder 堆疊結構**：
   - **Encoder**：由 $N = 6$ 個相同層堆疊而成，每層含兩個子層：(1) Multi-Head Self-Attention、(2) 位置前饋網路（Position-wise Feed-Forward Network）：$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$ `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.3, p.5]`。
   - **殘差連結與 LayerNorm**：每個子層周圍皆使用殘差連結（residual connection）後接 Layer Normalization，即子層輸出為 $\text{LayerNorm}(x + \text{Sublayer}(x))$；Base 模型所有子層與 embedding 維度皆為 $d_{\text{model}} = 512$，FFN 內層維度為 $d_{ff} = 2048$ `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.3, p.5]`。
   - **Decoder**：同樣由 $N = 6$ 個相同層堆疊，除了 Encoder 的兩個子層外，中間插入第三個子層對 Encoder 輸出執行 Multi-Head Attention `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.3]`。
2. **Multi-Head Attention 完整公式**：
   - 將 queries、keys、values 以不同的學習矩陣線性投影 $h$ 次至 $d_k, d_k, d_v$ 維度，平行執行注意力後再串接（Concat）並乘上輸出投影矩陣 $W^O$ `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.4-5]`：
     $$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)W^O, \quad \text{where } \text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$
   - Base 模型使用 **$h = 8$** 個平行注意力頭，每頭維度為 **$d_k = d_v = d_{\text{model}} / h = 64$**，總計算成本與單頭全維度注意力相當，且能讓模型同時關注不同位置、不同表徵子空間（representation subspaces）的資訊 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.5]`。
3. **三種注意力應用與 Masking 的 $-\infty$ 實作**：
   - **Encoder-Decoder Attention**：queries 來自前一層 Decoder，而 memory keys 與 values 來自 Encoder 輸出 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.5]`。
   - **Encoder Self-Attention**：$Q, K, V$ 皆來自 Encoder 前一層輸出 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.5]`。
   - **Decoder Masked Self-Attention**：為保持自回歸（auto-regressive）特性、防止向左的未來資訊洩漏，在 Scaled Dot-Product Attention 內部將 Softmax 輸入中所有對應非法未來連接的位置**設為 $-\infty$（masking out / setting to $-\infty$）**`[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.3, p.5]`。

### 四、位置編碼（Positional Encoding）與相對位置線性轉換
1. **正弦與餘弦位置編碼公式**：
   在 Encoder 與 Decoder 底層將維度同為 $d_{\text{model}}$ 的位置編碼加到輸入詞嵌入（input embeddings 乘以 $\sqrt{d_{\text{model}}}$）上 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.5-6]`：
   $$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right), \quad PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$
   其中 $pos$ 為位置、$i$ 為維度索引，波長從 $2\pi$ 到 $10000 \cdot 2\pi$ 呈幾何級數遞增 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6]`。
2. **為何選用正餘弦函數？（相對位置線性表示與外插能力）**：
   - 對於任何固定的位置偏移量 $k$，**$PE_{pos+k}$ 都可以表示為 $PE_{pos}$ 的線性函數**，作者群假設這能讓模型輕易學會根據「相對位置（relative positions）」來分配注意力 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6]`。
   - 實驗顯示正餘弦編碼與學習式位置嵌入（learned positional embeddings）分數幾乎相同（Table 3 row (E)：BLEU $25.8$ vs. $25.7$），但正餘弦版本有助於模型**外插（extrapolate）**到比訓練時更長的序列長度 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6, p.9]`。

---

## 五、與課程講義（第 4、5 講）之交叉查核對照表

| 查核主題 | 課程講義（第 4、5 講）敘述 | Vaswani et al. (2017) 原論文敘述 | 交叉查核結論 |
|---|---|---|---|
| **Scaled Dot-Product 公式** | 第 4 講 `p.31` 與第 5 講 `p.31`：$\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$（PDF 中根號為向量繪圖） | `p.4` Equation (1)：$\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$ | **完全一致**，且原論文確認根號 $\sqrt{d_k}$ 之存在。 |
| **為何除以 $\sqrt{d_k}$？** | 第 5 講 `p.31-33`：內積太大時 Softmax「贏者通吃」，除以 $\sqrt{d_k}$ 把數值拉回 0 附近（如同設溫度 $\tau=\sqrt{d_k}$） | `p.4` & Footnote 4：獨立均 0 變異 1 變數之內積變異數為 $d_k$，$d_k$ 大時內積過大推入 Softmax 極小梯度區，除以 $\sqrt{d_k}$ 將變異數壓回 1 | **直覺與理論互補一致**：講義的「贏者通吃」即對應原論文的「Softmax 飽和與梯度消失」。 |
| **列向量與矩陣右乘** | 第 4 講 `p.28`、第 5 講 `p.13, p.35`：Google 偏愛列向量，故線性轉換矩陣乘在右邊 $Q=XW^Q$ | `p.5`：$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$，其中 $W_i^Q \in \mathbb{R}^{d_{\text{model}}\times d_k}$ 確實右乘於 $Q$ | **完全一致**。 |
| **位置編碼足標與直覺** | 第 5 講 `p.46-50`：指出足標 $k$ 應從 0 開始，$\omega_k = 1/10000^{2k/d}$，並以單位圓時鐘解釋 $(\sin, \cos)$ | `p.6`：$2i$ 與 $2i+1$（$i$ 從 0 開始），並說明選用 $(\sin, \cos)$ 是因 $PE_{pos+k}$ 可表為 $PE_{pos}$ 的線性函數 | **完全一致**，單位圓旋轉矩陣正是 $PE_{pos+k}$ 為 $PE_{pos}$ 線性函數的幾何意義。 |

---

## 關聯概念頁
- [[transformer-and-self-attention]]
- [[transformer-architecture-and-stability]]
