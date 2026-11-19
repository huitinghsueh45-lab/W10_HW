---
title: 大型語言模型與 Transformer 自注意力機制（LLM & Self-Attention）
type: concept
sources: [04LLM只是在猜下一個字？.pdf, 05AI怎麼記得前面說過什麼？.pdf, Vaswani_2017_Attention_Is_All_You_Need.pdf]
updated: 2026-11-19
status: linted
---

# 大型語言模型與 Transformer 自注意力機制（LLM & Self-Attention）

## 一、為什麼「只看前一個字」無法成為語言模型？
現代大型語言模型（LLM）的核心任務其實只有一件：**「看前面的一堆字，預測下一個字（Next-Token Prediction）」**`[來源: 04LLM只是在猜下一個字？.pdf p.8, p.13, p.20]`。這種設計最大的好處是全世界所有現成句子都能直接拆解為訓練樣本（例如 `"炎龍老師很帥"` 可自動拆為 `(炎)→龍`、`(龍)→老`、`(老)→師` 等）`[來源: 04LLM只是在猜下一個字？.pdf p.9]`。

然而，如果模型真的「只輸入前一個字 $x_t$」去預測下一個字 $x_{t+1}$，馬上就會撞上數學矛盾：以 `"今天天氣很好。"` 為例，模型會同時遇到 `[來源: 04LLM只是在猜下一個字？.pdf p.10]`：
- $f_\theta(\text{“天”}) = \text{“天”}$（第一個「天」後面是「天」）`[來源: 04LLM只是在猜下一個字？.pdf p.10]`
- $f_\theta(\text{“天”}) = \text{“氣”}$（第二個「天」後面是「氣」）`[來源: 04LLM只是在猜下一個字？.pdf p.10]`

同一個輸入對應不同輸出（一對多），**這根本不是函數！**`[來源: 04LLM只是在猜下一個字？.pdf p.10]` 因此，語言模型必須是**「有記憶的」神經網路**：將前面所有字 $x_1, x_2, \dots, x_{t-1}$ 的上下文記憶融合成向量 $h_{t-1}$，計算條件機率分佈 $P_\theta(w_i \mid x_1, x_2, \dots, x_T)$，再不斷將新生成的字接回尾端一路接龍下去 `[來源: 04LLM只是在猜下一個字？.pdf p.11, p.13-15, p.64]`。

---

## 二、是什麼：從 RNN 遞迴記憶到 Transformer 平行自注意力

在深度學習的 3+1 種架構中（參見 [[neural-networks-and-learning]]），處理序列記憶的主角曾經是 **RNN（遞歸神經網路）**，而現代 LLM 的基石則是 Google 提出的 **Transformer（變形金剛）**`[來源: 04LLM只是在猜下一個字？.pdf p.12, p.23]`：

| 比較維度 | RNN（遞歸神經網路） | Transformer（變形金剛） |
|---|---|---|
| **記憶傳遞方式** | 將上一個時間點的記憶向量（hidden state）$h_{t-1}$ 傳回並與目前輸入 $x_t$ 一起加權送入神經元，如 $h^1_t = \sigma(w^x_{11}x^1_t + w^x_{21}x^2_t + w^h_{11}h^1_{t-1} + w^h_{21}h^2_{t-1} + b_1)$ `[來源: 04LLM只是在猜下一個字？.pdf p.24-25]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.4-5]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.2]` | 徹底捨棄遞迴與卷積，完全透過 **Self-Attention（自注意力機制）** 直接讓序列中每個字與其他所有字計算關聯並融合記憶 `[來源: 04LLM只是在猜下一個字？.pdf p.27-29]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.16, p.27-30]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.1-2]` |
| **運算效率與平行化** | **遞迴型運算（最少循序操作數 $O(n)$）**：必須等 $h_t$ 算完才能算 $h_{t+1}$，無法對整句序列平行計算；每層複雜度 $O(n \cdot d^2)$ `[來源: 04LLM只是在猜下一個字？.pdf p.26]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.2, p.6]` | **一次平行生成（最少循序操作數 $O(1)$）**：整段輸入 $x_1, \dots, x_T$ 透過矩陣乘法一次同時生成所有位置的記憶 $h_1, \dots, h_T$；每層複雜度 $O(n^2 \cdot d)$ `[來源: 04LLM只是在猜下一個字？.pdf p.27, p.30-31]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.27, p.35]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6]` |
| **長距離依賴路徑長度** | 最大路徑長度為 **$O(n)$**，距離越遠訊號越難傳遞 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6]` | 任意兩位置間最大路徑長度為常數 **$O(1)$**，更容易學習長距離語意依賴 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.6]` |

---

## 三、怎麼運作：Q, K, V 與 Scaled Dot-Product Attention

Transformer 的 **Self-Attention** 完全由線性轉換與矩陣乘法構成，分為四個核心步驟 `[來源: 04LLM只是在猜下一個字？.pdf p.28-31]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.17-35]`：

1. **線性轉換產生 Q, K, V 三個特徵代表向量（列向量矩陣乘法）**：
   對序列中每個字的詞嵌入向量 $x_t$（Google 慣用**列向量**表示，因此依矩陣「先列後行」規則，線性轉換矩陣乘在右方），乘上學習而來的權重矩陣，一次算出所有位置的 **Query ($Q = X W^Q$)**、**Key ($K = X W^K$)**、**Value ($V = X W^V$)** `[來源: 04LLM只是在猜下一個字？.pdf p.28]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.10-14, p.34-35]`。
2. **內積計算 Attention 強度 $e_j$**：
   要合成第 $i$ 個位置的記憶向量 $h_i$（大家輪流當 query $q_i$），拿它的查詢向量 $q_i$ 與序列中每個位置的索引向量 $k_j$ 做內積，算出相關強度 $a(q_i, k_j) = \langle q_i, k_j \rangle = q_i k_j^T = e_j$（寫成矩陣乘法即 $q_i K^T = [e_1, e_2, \dots, e_T]$）`[來源: 04LLM只是在猜下一個字？.pdf p.29-30]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.21-23, p.29]`。
3. **除以 $\sqrt{d_k}$ 並經 Softmax 正規化為注意力權重 $\alpha_j$**：
   - **統計與梯度解釋（Vaswani et al., 2017）**：若 $q$ 與 $k$ 的各分量為獨立、平均數 $0$、變異數 $1$ 的隨機變數，則內積 $q \cdot k = \sum_{i=1}^{d_k} q_i k_i$ 的平均數為 $0$、**變異數會膨脹為 $d_k$**；當 $d_k$ 較大時，內積數值變得極大，會將 Softmax 推入**梯度極小（extremely small gradients）**的飽和區域 `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.4]`。
   - **教學直覺與數值例子（第五講）**：Softmax 具有「贏者通吃」特性，當內積數值偏大時會讓最高分權重過度極端（例如分數 `[3.9, 3.2, 1, 0.3, 1.1]` 直接做 Softmax 會變成 `[61%, 30%, 3%, 2%, 4%]`）；因此先同除以 Key 向量維度平方根 $\tau = \sqrt{d_k}$ 將數字拉回 0 附近（使變異數回到 $1$，分數變為 `[1.74, 1.43, 0.45, 0.13, 0.49]`，Softmax 後成為較均衡的 `[40%, 29%, 11%, 8%, 11%]`），得到總和為 1 的權重係數 $\alpha_1, \alpha_2, \dots, \alpha_T$ `[來源: 04LLM只是在猜下一個字？.pdf p.29-31]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.24, p.31-33]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.4]`。
4. **Value 向量的加權線性組合**：
   以權重 $\alpha_j$ 對各位置的內容向量 $v_j$ 加權平均（即列向量線性組合 $\alpha V$），得到融合上下文後的輸出向量 $h_i = \alpha_1 v_1 + \alpha_2 v_2 + \dots + \alpha_T v_T$ `[來源: 04LLM只是在猜下一個字？.pdf p.29]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.20, p.25]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.3-4]`。

將所有位置的運算合併為單一矩陣公式，即為著名的 **Scaled Dot-Product Attention** `[來源: 04LLM只是在猜下一個字？.pdf p.31]` `[來源: 05AI怎麼記得前面說過什麼？.pdf p.31]` `[來源: Vaswani_2017_Attention_Is_All_You_Need.pdf p.4]`：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

---

## 四、例子與規模化奇蹟：為什麼「只猜下一個字」卻無所不知？

1. **從字元接龍到「作夢的機器」**：
   Andrej Karpathy (2015) 曾展示僅靠「猜下一個字」就能讓模型寫出假的代數幾何論文、莎士比亞劇本或《紅樓夢》續集（如輸入 `"自孫悟空從石頭中蹦出來之後..."`，模型便用紅樓夢文風把孫悟空與賈政、鳳姐、劉姥姥寫在一起）`[來源: 04LLM只是在猜下一個字？.pdf p.33-37]`。Karpathy 指出，LLM 生成的內容本質上都是**「幻覺（hallucinated）」**——搜尋引擎是 0% 的夢境但不會創造，而 LLM 是「作夢的機器」，幻覺不是 Bug，而是 LLM 具創造力的核心特點 `[來源: 04LLM只是在猜下一個字？.pdf p.38-40]`。
2. **驚人的參數量與閱讀資料規模**：
   - 課堂《紅樓夢》生成器約 **300 萬**參數 $\to$ GPT-2 達 **15 億**參數 $\to$ GPT-3 高達 **1,750 億**參數 `[來源: 04LLM只是在猜下一個字？.pdf p.42-43]`。
   - 人類一生所有閱讀量約為 **1B（10 億字）**量級；而 GPT-3 精讀了約 **4,990 億字**，**Llama 3** 更使用了 **15T（15 兆）**量級的訓練資料，相當於人類一生閱讀量的 **1.5 萬倍** `[來源: 04LLM只是在猜下一個字？.pdf p.44-45]`。因為幾乎讀遍了人類文明的各種文本模式，這個「很會接話的呆萌機器人」才能對答如流 `[來源: 04LLM只是在猜下一個字？.pdf p.20, p.45]`。
3. **如何指揮這台接話機器（Prompt 與 Context Engineering）**：
   正因為 LLM 不知道你腦中的背景、只是順著上下文接話，寫好 Prompt 只有兩個核心原則：**「正確的資訊」**（把背景資料、條件給齊）＋**「清楚的指引」**（把任務目標、輸出格式、受眾講明白），並可透過「和 AI 一起討論生成規格書／Prompt、最後人工親自審閱修改」來達成最佳效果 `[來源: 04LLM只是在猜下一個字？.pdf p.21, p.100-101, p.105-111]`。

---

## 相關概念與來源
- 前置概念：[[function-mapping]]、[[neural-networks-and-learning]]、[[probability-entropy-and-sampling]]、[[word-embedding-and-sampling-strategies]]
- 後續概念：[[transformer-architecture-and-stability]]
- 來源摘要：[[lecture-04-llm-next-token-prediction]]、[[lecture-05-sequence-memory-and-attention]]、[[external-vaswani-2017-attention-is-all-you-need]]
