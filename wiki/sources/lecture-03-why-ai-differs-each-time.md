---
title: 03 AI 為什麼每次都不一樣？（來源摘要）
type: source
sources: [03AI為什麼每次都不一樣？.pdf]
updated: 2026-11-19
status: linted
---

# 03 AI 為什麼每次都不一樣？（來源摘要）

## 基本資訊與分段處理紀錄
- **原始檔案**：`raw/lectures/03AI為什麼每次都不一樣？.pdf`（共 102 頁）`[來源: 03AI為什麼每次都不一樣？.pdf p.3, p.102]`。
- **分段讀取範圍**（超過 60 頁分兩段處理）：
  - **第一段（p.1–60）**：創作型 AI 的一對多平均困境與潛張量（Latent Tensor, $z$）（p.1–10）；生成對抗網路（GAN）原理、生成器 $G$ 與鑑別器 $D$ 對抗目標函數、WGAN 解決模式崩壞（p.11–33）；GAN 的高光時刻：Progressive GAN、StyleGAN（內容與風格向量 $w$、AdaIN）、Pix2Pix、CycleGAN（p.34–58）；Cross Entropy 引言（p.59–60）`[來源: 03AI為什麼每次都不一樣？.pdf p.2, p.11, p.34, p.59]`。
  - **第二段（p.61–102）**：資訊量（驚訝指數）$I(x)=-\log P(x)$、夏農熵（Shannon Entropy）$H(P)$、交叉熵（Cross Entropy）$H(P,Q)$、MSE 與 Cross Entropy 比較、KL 散度（KL Divergence）與模型蒸餾 Soft Target（p.61–90）；生成隨機性的來源（Latent $z$ 與 Softmax 機率抽樣）、語言模型猜下一個字、破除鑑別式與生成式 AI 二分迷思，以及 AI Canvas 作業設計（p.91–102）`[來源: 03AI為什麼每次都不一樣？.pdf p.61, p.91, p.99]`。

---

## 重點摘要

### 一、創作型 AI 的「一對多」困境與潛張量（Latent Tensor, $z$）
1. **一對多不是函數（平均困境）**：若我們直接將文字 `"一個可愛的女孩"` 作為函數 $f_\theta$ 的輸入，但訓練資料中同一個輸入對應多張不同的可愛女孩照片（一對多，違反單純函數一對一／多對一映射），硬去訓練神經網路會得到所有可能輸出的**平均** $\frac{1}{N}(\text{圖}_1 + \text{圖}_2 + \dots + \text{圖}_N)$，結果會變成「四不像」，失去創作意義 `[來源: 03AI為什麼每次都不一樣？.pdf p.4-8]`。
2. **引入潛張量（Latent Tensor, $z$）**：為了讓創作者機器人每次有不同創作，輸入端會放入代表「天馬行空的想法」或特徵表徵的**潛張量（Latent Tensor / Latent Vector, $z$）**（可由隨機抽樣產生，或由數據算出），再經由函數 $f_\theta$ 映射出創作作品 `[來源: 03AI為什麼每次都不一樣？.pdf p.9-10, p.92]`。

### 二、生成對抗網路（GAN）及其演進
1. **GAN 的核心架構（Goodfellow et al., NIPS 2014）**：
   - 由 Ian Goodfellow（曾與博士指導教授 Yoshua Bengio 及 Aaron Courville 合著《Deep Learning》）於 2014 年提出，Yann LeCun 於 2016 年曾讚譽對抗式訓練（GAN）是深度學習最重要的發展（*"The most important one, in my opinion, is adversarial training"*）`[來源: 03AI為什麼每次都不一樣？.pdf p.12-14]`。
   - GAN 同時訓練兩個神經網路相互對抗：**生成器（Generator, $G$）**接收潛向量 $z \sim p_z$ 生成作品，**鑑別器（Discriminator, $D$）**則判斷輸入作品是來自真實世界分佈 $x \sim p_{\text{data}}$（目標輸出 1）還是生成器的作品 $G(z) \sim p_g$（目標輸出 0）`[來源: 03AI為什麼每次都不一樣？.pdf p.18-24]`。
2. **GAN 的對抗目標函數（Minimax Loss）**：
   - 利用遞增且能把乘法變加法（$\log(a\cdot b)=\log a+\log b$）的對數函數 $\log$ `[來源: 03AI為什麼每次都不一樣？.pdf p.25-26]`：
   - **鑑別器 $D$**：希望真實資料 $D(x)$ 越接近 1 越好（即 $\mathbb{E}_{x\sim p_{\text{data}}}[\log D(x)]$ 越大越好），且生成作品 $D(G(z))$ 越接近 0 越好（即 $\mathbb{E}_{z\sim p_z}[\log(1-D(G(z)))]$ 越大越好）`[來源: 03AI為什麼每次都不一樣？.pdf p.27]`。
   - **生成器 $G$**：希望騙過鑑別器讓 $D(G(z))$ 越接近 1 越好，亦即讓 $\mathbb{E}_{z\sim p_z}[\log(1-D(G(z)))]$ 越小越好 `[來源: 03AI為什麼每次都不一樣？.pdf p.28]`。
   - 合寫為極小極大對抗目標式 `[來源: 03AI為什麼每次都不一樣？.pdf p.29]`：
     $$\min_G \max_D V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$
   - 當訓練完成時，生成分佈等於真實分佈（$p_g = p_{\text{data}}$），鑑別器 $D$ 再也無法分辨真偽 `[來源: 03AI為什麼每次都不一樣？.pdf p.30-31]`。
3. **從 WGAN、StyleGAN 到圖像轉換**：
   - **WGAN**：解決傳統 GAN 的 **Collapse（模式崩壞）**問題——即生成器不管輸入什麼 $z$ 都只生出同一張能騙過老師的圖 `[來源: 03AI為什麼每次都不一樣？.pdf p.32-33]`。
   - **Progressive GAN（Karras et al., NVIDIA, ICLR 2018）**：因為直接生 $1024\times 1024$ 高解析度圖太難，改從 $4\times 4 \to 8\times 8 \to \dots \to 1024\times 1024$ 由低解析度逐步訓練到精細解析度 `[來源: 03AI為什麼每次都不一樣？.pdf p.36-39]`。
   - **StyleGAN**：為了控制生成內容與風格，將 512 維的輸入潛向量 $z$ 先經映射網路轉為 512 維的風格向量 $w$，再經學習出的仿射轉換（affine transformation）$Aw+b$ 產生 $y=(y_s, y_b)$，透過 **AdaIN（Adaptive Instance Normalization）**注入各解析度層：`[來源: 03AI為什麼每次都不一樣？.pdf p.41-45]`
     $$\text{AdaIN}(x_i, y) = y_{s,i} \frac{x_i - \mu(x_i)}{\sigma(x_i)} + y_{b,i}$$
     其中 $w$ 就像是 prompt 一樣，在每一層不斷提醒 AI 該用什麼風格繪製，並可透過混合不同層的 $w_1, w_2$ 變換提示 `[來源: 03AI為什麼每次都不一樣？.pdf p.46-47]`。
   - **Pix2Pix（Isola, 朱俊彦等人, CVPR 2017）與 CycleGAN（朱俊彦等人, ICCV 2017）**：Pix2Pix 需成對訓練資料（同時將輸入與輸出送進鑑別器 $D$，如衛星圖變地圖、手繪線條變街景）`[來源: 03AI為什麼每次都不一樣？.pdf p.50-52]`；CycleGAN 則透過雙生成器 $(G, F)$ 與雙鑑別器 $(D_A, D_B)$ 實現**不需要配對資料**的跨領域轉換（如馬變斑馬）`[來源: 03AI為什麼每次都不一樣？.pdf p.53-55]`。GAN 曾被視為電腦創作的巔峰，直到 **Diffusion Models** 出現 `[來源: 03AI為什麼每次都不一樣？.pdf p.58]`。

### 三、資訊量、熵（Entropy）、交叉熵（Cross Entropy）與 KL 散度
1. **資訊量（驚訝指數, Information Content）**：
   - 事件 $x$ 發生機率 $P(x)$ 越低，發生時我們越驚訝、包含的資訊量越大（例如在幾乎不下雨的加州，「明天下大雨」比「明天是晴天」資訊量大得多）；定義為 `[來源: 03AI為什麼每次都不一樣？.pdf p.64-66]`：
     $$I(x) = -\log P(x)$$
2. **夏農熵（Shannon Entropy, $H(P)$）**：
   - 設機率分佈 $P = [p_1, p_2, \dots, p_n]$，其**熵（Entropy，又譯能趨疲）**定義為資訊量的期望值（平均訊息量）`[來源: 03AI為什麼每次都不一樣？.pdf p.71-74]`：
     $$H(P) = -\mathbb{E}_{x \sim P}[\log P(x)] = -\sum_{i=1}^n p_i \log p_i$$
   - 熵越大代表可能情況越複雜（常稱為「亂度」）；當只有單一確定事件（發生機率為 1）時，entropy 為 0 `[來源: 03AI為什麼每次都不一樣？.pdf p.72]`。
3. **交叉熵（Cross Entropy, $H(P, Q)$）**：
   - 用來比較真實世界機率分佈 $P=(y_1, y_2, y_3)$ 與神經網路預測機率分佈 $Q=(\hat{y}_1, \hat{y}_2, \hat{y}_3)$，公式為 `[來源: 03AI為什麼每次都不一樣？.pdf p.69, p.76-77]`：
     $$H(P, Q) = -\sum_{i=1}^3 y_i \log(\hat{y}_i)$$
   - 在分類問題中，正確答案 $y$ 為 One-hot encoding（設第 $i$ 類為正確答案 $y_i=1$，其餘為 0），此時交叉熵簡化為只看正確類別預測機率 $\hat{y}_i$ 的驚訝指數 `[來源: 03AI為什麼每次都不一樣？.pdf p.67-68, p.78-80]`：
     $$H(P, Q) = -y_i \log \hat{y}_i = -\log \hat{y}_i$$
   - 若正確答案的模型預測機率 $\hat{y}_i$ 很小，$-\log \hat{y}_i$ 就會很大，代表「正確答案你還說機率很低，就給你大扣分！」`[來源: 03AI為什麼每次都不一樣？.pdf p.68, p.80]`。
4. **為什麼分類問題用 Cross Entropy 而不用均方差（MSE）？**：
   - 在分類問題中，只要正確類別預測機率相同，兩次預測對正確答案的掌握度其實一樣好 `[來源: 03AI為什麼每次都不一樣？.pdf p.61-63]`。
   - 例如正確答案為 $y=[1, 0, 0]$，比較兩組模型輸出 $\hat{y}_a = [0.7, 0.19, 0.11]$ 與 $\hat{y}_b = [0.7, 0.3, 0]$：兩者的 **Cross Entropy 皆為 $0.36$**（只看第一類 $0.7$），但原文標為 **MSE** 的數值卻分別為 $0.14$（對應 $[0.7, 0.19, 0.11]$）與 $0.18$（對應 $[0.7, 0.3, 0]$）（同理在 `p.62` 中，$[0.6, 0.3, 0.1]$ 與 $[0.6, 0.2, 0.2]$ 的平方誤差和分別為 $0.26$ 與 $0.24$）`[來源: 03AI為什麼每次都不一樣？.pdf p.62-63, p.82]`（註：原投影片此處表頭稱「均方差 / MSE」，但實際計算式為未除以類別數 $3$、亦未乘第二講 `p.71` 之 $\frac{1}{2}$ 的**平方誤差和 SSE**）。因此分類問題使用單純在意正確答案機率的 Cross Entropy 更為合適 `[來源: 03AI為什麼每次都不一樣？.pdf p.70, p.82]`。
5. **KL 散度（KL Divergence）與知識蒸餾（Soft Target）**：
   - 當預測分佈完全等於真實分佈（$Q=P$）時，Cross Entropy 達到最小值 $H(P, P) = H(P)$，注意此最小值不一定為 0 `[來源: 03AI為什麼每次都不一樣？.pdf p.83]`。
   - 將 Cross Entropy 減去固定的真實分佈熵 $H(P)$，即為 **KL 散度（Kullback-Leibler Divergence）** `[來源: 03AI為什麼每次都不一樣？.pdf p.84-85]`：
     $$D_{KL}(P \parallel Q) = H(P, Q) - H(P)$$
     當 $Q=P$ 時，$D_{KL}(P \parallel Q) = 0$ `[來源: 03AI為什麼每次都不一樣？.pdf p.84]`。
   - **Soft Target 與模型蒸餾（Distillation）**：當真實目標不是 $[1, 0, 0]$ 這種 Hard Target，而是讓小（學生）模型學習大（老師）模型的「思路」（例如老師輸出 **Soft Target** $y=[0.7, 0.25, 0.05]$ 或 $y=[0.7, 0.2, 0.1]$）時，兩組預測 $\hat{y}_a=[0.75, 0.15, 0.1]$ 與 $\hat{y}_b=[0.6, 0.3, 0.1]$ 對目標 $y=[0.7, 0.2, 0.1]$ 的 Cross Entropy 為 $0.81$ vs. $0.83$（看似相近），但扣除 $H(P)$ 後的 **KL Divergence 為 $0.01$ vs. $0.03$（相差 3 倍！）**，因此學習 Soft Target 時應考慮 KL 散度 `[來源: 03AI為什麼每次都不一樣？.pdf p.86-90]`。

### 四、隨機性怎麼出來的？——機率抽樣與鑑別／生成同源
1. **兩種隨機性注入機制**：
   - **GAN 的隨機性**：在一開始輸入時隨機抽取潛向量 $z$ `[來源: 03AI為什麼每次都不一樣？.pdf p.92]`。
   - **Softmax 輸出的機率抽樣（Probabilistic Sampling）**：在八哥辨識中，若固定選最高分（argmax），同樣輸入必得同樣輸出（60% 土八哥、30% 白尾八哥、10% 家八哥永遠回答土八哥）`[來源: 03AI為什麼每次都不一樣？.pdf p.93]`；但若改為**依機率抽樣**（60% 機率抽土八哥、30% 抽白尾八哥、10% 抽家八哥），應用在「咖啡推薦 AI」（60% 衣索比亞日曬、30% 瓜地馬拉水洗、10% 哥斯大黎加蜜處理）或**語言模型（看前面一堆字如「呆一布在」，依 Softmax 機率分佈「家 15%、桌 7%、玩 12%、裝 3%...」抽下一個字）**，每次就會生出不一樣的回應 `[來源: 03AI為什麼每次都不一樣？.pdf p.94-96]`。
2. **破除「鑑別式 AI vs. 生成式 AI」的死背迷思**：
   - 許多「背資料學 AI」的人喜歡把 AI 硬分成鑑別式 AI（Discriminative AI）與生成式 AI（Generative AI），甚至宣稱「生成式 AI 有幻覺，所以有時要用鑑別式 AI」；但從函數學習機與 Softmax 機率分佈的原理來看，**兩者在底層原理上是完全一樣的** `[來源: 03AI為什麼每次都不一樣？.pdf p.97-98]`。

---

## 關聯概念頁
- [[function-mapping]]
- [[neural-networks-and-learning]]
- [[probability-entropy-and-sampling]]
