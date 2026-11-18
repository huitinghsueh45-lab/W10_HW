---
title: 神經網路與梯度下降學習機制（Neural Networks & Gradient Descent）
type: concept
sources: [02神經網路的概念.pdf, 03AI為什麼每次都不一樣？.pdf]
updated: 2026-11-18
status: linted
---

# 神經網路與梯度下降學習機制（Neural Networks & Gradient Descent）

## 一、為什麼需要神經網路？
當我們將 AI 視為從輸入映射到輸出的函數學習機 $f_\theta$（參見 [[function-mapping]]）後，接下來的核心問題是：**要用什麼數學結構來建造這個函數 $f_\theta$？電腦又如何從海量資料中自動找出最佳參數 $\theta^*$？** 深度學習的核心答案就是「神經網路（Neural Networks）」搭配「梯度下降法（Gradient Descent）」`[來源: 02神經網路的概念.pdf p.28, p.30, p.74-75]`。

---

## 二、是什麼：神經元與 3+1 種神經網路架構

### 1. 基本運算單元：神經元（Neuron）
不論是哪一種深度學習網路，其最底層的基本運算單元都是**神經元（Neuron）**，且每個神經元的計算步驟完全相同 `[來源: 02神經網路的概念.pdf p.30, p.32]`：
1. **加權總和（Weighted Sum）**：接收輸入訊號 $x_1, x_2, x_3$，各自乘上代表重要程度的**權重（weights）** $w_1, w_2, w_3$ 後相加，得到總刺激 $w_1 x_1 + w_2 x_2 + w_3 x_3$ `[來源: 02神經網路的概念.pdf p.33-34]`。
2. **加上偏值（Bias）**：加上一個基準調整項 $b$，得到調整後的總刺激 $\sum_{i=1}^3 w_i x_i + b$ `[來源: 02神經網路的概念.pdf p.35]`。
3. **非線性激發函數（Activation Function, $\varphi$）**：若只有線性加總，不論疊加多少層神經元，整體依然只是線性函數；因此必須通過非線性激發函數 $\varphi$（如現代最常用的 **ReLU**，或早期的 **Sigmoid**、**Gaussian**）轉換後，才輸出訊號 $h$ `[來源: 02神經網路的概念.pdf p.36-38]`：

$$h = \varphi\left(\sum_{i=1}^3 w_i x_i + b\right), \quad \theta = \{w_1, w_2, w_3, b\}$$

### 2. 常見的 3+1 種神經網路架構
神經網路透過建立多個隱藏層（Hidden Layers）、每層放置若干個神經元來組裝函數，依神經元連結方式分為 **3+1 種主流架構** `[來源: 02神經網路的概念.pdf p.30-31, p.39]`：
- **DNN（全連結神經網路，Dense Layer）**：前一層所有輸出皆連結到下一層每一個神經元，是全面考慮的基本型 `[來源: 02神經網路的概念.pdf p.30-31, p.39, p.43]`。
- **CNN（卷積神經網路，Conv Layer）**：擅長影像與圖形辨識 `[來源: 02神經網路的概念.pdf p.30-31, p.39]`。
- **RNN（遞歸神經網路，如 LSTM、GRU）**：具備記憶結構，適合處理序列資料 `[來源: 02神經網路的概念.pdf p.30-31, p.39]`。
- **Transformers**：現代大型語言模型與生成式 AI 的核心架構 `[來源: 02神經網路的概念.pdf p.30]`。

數學上的**萬用近似定理（Universal Approximation Theorem）**證明，理論上只要「一個隱藏層」的神經網路，就能逼近任何想要學習的目標函數 `[來源: 02神經網路的概念.pdf p.52]`。而深度學習之所以在本世紀爆發（由三巨頭 Geoffrey Hinton、Yann LeCun、Yoshua Bengio 奠基），是因為終於湊齊了上世紀欠缺的三大要件：**複雜的軟體、大量的數據、電腦計算能力** `[來源: 02神經網路的概念.pdf p.53, p.55-56]`。

---

## 三、怎麼運作：從張量輸入、Softmax 到梯度下降訓練

### 1. 前向傳遞：逐層張量（Tensor）轉換與 Softmax 機率輸出
- **張量（Tensor）輸入**：輸入與輸出皆為多維數據結構——純量為 0 階 tensor、向量為 1 階 tensor、矩陣為 2 階 tensor（如過去 20 天 $\times N$ 個股價特徵）、彩色影像（R, G, B）為 3 階 tensor `[來源: 02神經網路的概念.pdf p.7-10]`。
- **逐層理解**：在 DNN 中，只需決定「幾層隱藏層」與「每層幾個神經元」；每一層都會把輸入 tensor 轉換為另一個向量，上一層的輸出即為下一層的輸入，代表電腦對輸入資料的逐層抽象理解 `[來源: 02神經網路的概念.pdf p.46, p.49-50]`。
- **Softmax 機率化**：在分類問題中，模型最後輸出的原始分數 $(a, b, c)$ 可能包含負數；透過 **Softmax** 先取自然指數 $(e^a, e^b, e^c)$ 確保為正並維持大小順序，再除以總和 $S = e^a + e^b + e^c$，即可化為總和為 1 的條件機率分佈 $P_\theta(y_i \mid \mathbf{x}) = p_i$ `[來源: 02神經網路的概念.pdf p.15-22]`：

$$\text{Softmax}(a, b, c) = \left(\frac{e^a}{S}, \frac{e^b}{S}, \frac{e^c}{S}\right), \quad S = e^a + e^b + e^c$$

### 2. 評估差距：損失函數（Loss Function）
剛初始化參數 $\theta$ 的神經網路尚未學習，預測結果如同亂猜 `[來源: 02神經網路的概念.pdf p.59-60]`。為了衡量模型預測值 $f_\theta(x_i) = \hat{y}_i$ 與訓練資料正確答案 $y_i$（常以 One-hot encoding 表示，如 $[1, 0, 0]^T$）之間的差距，我們定義**損失函數（Loss Function）** `[來源: 02神經網路的概念.pdf p.12, p.63-66, p.71-72]`：

$$L(\theta) = \frac{1}{2k} \sum_{i=1}^k \| y_i - f_\theta(x_i) \|^2$$

例如在八哥辨識中，若正確答案為 $y_1 = [1, 0, 0]^T$，而模型預測 $\hat{y}_1 = [0.23, 0.43, 0.34]^T$，則單筆平方誤差和為 $(1 - 0.23)^2 + (0 - 0.43)^2 + (0 - 0.34)^2 = 0.89$ `[來源: 02神經網路的概念.pdf p.68-69]`。而在分類與語言模型問題中，為了單純衡量模型對正確類別預測機率 $\hat{y}_i$ 的掌握度，實務上更常使用**交叉熵（Cross Entropy）** $H(P, Q) = -\sum_{i} y_i \log \hat{y}_i = -\log \hat{y}_i$ 作為損失函數（詳見 [[probability-entropy-and-sampling]]）`[來源: 03AI為什麼每次都不一樣？.pdf p.70, p.76-82]`。訓練的目的就是不斷調整參數 $\theta$，讓 $L(\theta_1) > L(\theta_2) > L(\theta_3) > \dots$，找出使誤差最小的最佳參數 $\theta^*$ `[來源: 02神經網路的概念.pdf p.73-74, p.77]`。

### 3. 參數更新：梯度下降法（Gradient Descent）
電腦如何知道要把參數往哪個方向調，才能讓損失 $L$ 變小？
1. **單參數切線斜率**：若只有一個參數 $w$，微積分的切線斜率 $L'(w) = \frac{dL}{dw}$ 指向局部極大值方向，與極小值方向相反；因此應往「減去斜率」的方向移動 `[來源: 02神經網路的概念.pdf p.80-89]`。
2. **學習率（Learning Rate, $\eta$）**：為了避免一步跨太大而「跑過頭」越過極小值，需乘上一個控制步長的小正數 $\eta$（Learning Rate），更新式為 $w \leftarrow w - \eta \frac{dL}{dw}$ `[來源: 02神經網路的概念.pdf p.91-92]`。
3. **多參數偏微分與梯度向量 $\nabla L$**：面對成千上萬個參數，數學家的做法是對每個參數「假裝只有它一個變數、其餘參數視為常數」求偏微分 $\frac{\partial L}{\partial w_i}$ `[來源: 02神經網路的概念.pdf p.93-99]`。將所有偏微分組成的向量稱為**梯度（Gradient）** $\nabla L$，則萬用參數更新公式為 `[來源: 02神經網路的概念.pdf p.100-104]`：

$$\theta \leftarrow \theta - \eta \nabla L, \quad \text{其中 } \nabla L = \begin{bmatrix} \frac{\partial L}{\partial w_1} \\ \frac{\partial L}{\partial w_2} \\ \frac{\partial L}{\partial b_1} \\ \vdots \end{bmatrix}$$

在神經網路中，這種沿網路反向計算梯度以執行梯度下降的演算法即稱為**反向傳播法（Backpropagation）** `[來源: 02神經網路的概念.pdf p.75]`。

---

## 四、實作例子：MNIST 手寫數字辨識 DNN
在 TensorFlow / Keras 中打造第一個手寫數字辨識神經網路，完整對應上述四個步驟 `[來源: 02神經網路的概念.pdf p.109-122]`：
1. **定義輸入與輸出張量**：將 MNIST 的 $28 \times 28$ 手寫數字灰階圖拉平為 **784 維向量**並做正規化（normalization）；輸出為 0～9 共 **10 個類別**的 One-hot 向量 `[來源: 02神經網路的概念.pdf p.111-114, p.118]`。
2. **架設 DNN 結構**：用 `Sequential` 串接兩層各有 **100 個神經元**、採用 **ReLU** 激發函數的全連結層（`Dense`），最後接一層 **10 維 Softmax** 輸出層 `[來源: 02神經網路的概念.pdf p.116, p.119]`。
3. **設定損失函數與最佳化器**：指定 `loss` 函數，並以 `SGD`（標準梯度下降法）設定學習率進行訓練 `[來源: 02神經網路的概念.pdf p.120]`。
4. **批次訓練與預測**：設定 `batch_size`（mini-batch 大小）與 `epochs`（訓練回合數）執行訓練，最後對測試資料執行 `predict` 驗證準確率 `[來源: 02神經網路的概念.pdf p.121-122]`。

---

## 五、常見誤解與進階觀點
- **誤解 1：「電腦認得圖片裡是家八哥」**
  - **事實**：電腦完全沒有語意意識，也不知道什麼叫「家八哥」；它只知道輸入一組數字張量後，依訓練經驗計算出第 3 個位置的數字最大（第 3 類數據）`[來源: 02神經網路的概念.pdf p.3, p.25]`。
- **誤解 2：「深度學習就只是高維度的內插法（Interpolation / Curve Fitting）」**
  - **事實**：雖然直覺上像是在訓練資料點之間做內插補足，但 Balestriero, Pesenti, & LeCun (2021) 證明，在**高維度空間**中的機器學習，幾何本質上總是**外插（Extrapolation）** `[來源: 02神經網路的概念.pdf p.106-107]`。

---

## 相關概念與來源
- 前置概念：[[function-mapping]]
- 後續概念：[[probability-entropy-and-sampling]]
- 來源摘要：[[lecture-02-neural-networks]]、[[lecture-03-why-ai-differs-each-time]]
