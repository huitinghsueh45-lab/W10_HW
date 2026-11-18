# 生成式 AI 入門：從函數到 Transformer — LLM Wiki 目錄

> 本目錄由 AI 於每次 Ingest 與 Lint 通過後更新。目前共收錄 **6 篇來源摘要頁**與 **6 篇跨來源概念知識頁**（共 12 頁，全數通過 6 項 Lint 檢查）。

## 來源摘要頁（`wiki/sources/`）

- [[lecture-01-learn-ai-without-anxiety]] — 課程第一講摘要：用原理對抗三大 AI 焦慮、理解 AI 模型作為輸入到輸出的函數 $f_\theta$（八哥辨識案例）、生成式 AI 起源動機與 Colab 函數視覺化實作。
- [[lecture-02-neural-networks]] — 課程第二講摘要：張量（Tensor）與 One-hot / Softmax 表示、神經元數學模型与 3+1 種架構（DNN / CNN / RNN + Transformers）、損失函數與梯度下降法（Gradient Descent），以及 MNIST 手寫辨識實作。
- [[lecture-03-why-ai-differs-each-time]] — 課程第三講摘要：一對多平均困境與潛張量 $z$、生成對抗網路（GAN / StyleGAN / CycleGAN）、資訊量與熵（Entropy / Cross Entropy / KL Divergence），以及生成模型透過機率抽樣產生隨機性的機制。
- [[lecture-04-llm-next-token-prediction]] — 課程第四講摘要：LLM「猜下一個字」的自監督訓練與序列記憶需求、RNN 與 Transformer Self-Attention 公式、Karpathy「幻覺（作夢機器）」與資料規模、Temperature / Top-k / Top-p 選字策略，以及 Word2Vec 詞嵌入（CBOW / Skip-Gram）與 Prompt 原則。
- [[lecture-05-sequence-memory-and-attention]] — 課程第五講摘要：RNN 遞歸層數學式、Google 列向量線性組合傳統、QKV 注意力推導與除以 $\sqrt{d_k}$ 抑制贏者通吃之機制、Encoder/Decoder 三種注意力與 Mask、Positional Encoding 時鐘直覺，以及 ResNet 殘差連結與 LayerNorm / RMSNorm / DyT。
- [[external-vaswani-2017-attention-is-all-you-need]] — 外部交叉查核論文摘要（Vaswani et al., NIPS 2017）：Transformer 原論文之 $O(1)$ 平行化與路徑優勢、Scaled Dot-Product Attention 變異數 $d_k$ 縮放證明、Multi-Head Attention（$h=8, d_{\text{model}}=512$）、$-\infty$ Masking 實作與正餘弦位置編碼之相對位置線性性質。

## 概念知識頁（`wiki/concepts/`）

- [[function-mapping]] — 函數映射與 AI 模型本質：說明現代判別式與生成式 AI 皆為從張量輸入映射到數值輸出的函數 $f_\theta(x_i)=\hat{y}_i$，涵蓋八哥辨識 Softmax 機率輸出、三大 AI 焦慮與生成動機。
- [[neural-networks-and-learning]] — 神經網路與梯度下降學習機制：解析基本運算單元「神經元」公式 $h=\varphi(\sum w_i x_i + b)$、DNN 逐層張量轉換、損失函數（MSE 與 Cross Entropy）與梯度下降更新律 $\theta \leftarrow \theta - \eta \nabla L$，並以 MNIST 手寫數字辨識說明完整訓練流程。
- [[probability-entropy-and-sampling]] — 機率分佈、資訊熵與生成隨機抽樣：闡述一對多平均困境與潛張量 $z$、資訊量 $I(x)$、夏農熵 $H(P)$、交叉熵 $H(P,Q)$ 與 KL 散度 $D_{KL}$，並說明 GAN 與語言模型如何透過潛變數或 Softmax 機率抽樣讓每次輸出都不一樣。
- [[word-embedding-and-sampling-strategies]] — 詞嵌入表徵與選字抽樣策略：說明輸入端如何透過代理任務（Word2Vec CBOW / Skip-Gram）與 Embedding 層將編號轉為具語意的特徵代表向量（權重即記憶 $W^T x = h$），以及輸出端如何用 Temperature $\tau$、Top-k、Top-p（Nucleus Sampling）調控選字隨機性。
- [[transformer-and-self-attention]] — 大型語言模型與 Transformer 自注意力機制：解析為何單看前一個字違反函數定義、RNN 遞迴記憶（$O(n)$）與 Transformer 平行生成（$O(1)$）的差異、列向量 Q/K/V 線性轉換與除以 $\sqrt{d_k}$ 的 Scaled Dot-Product Attention 公式，以及 LLM 的「幻覺」創造本質與規模化奇蹟。
- [[transformer-architecture-and-stability]] — Transformer 完整架構：位置編碼、殘差連結與正規化：闡述 $(\sin(\omega_k t), \cos(\omega_k t))$ 位置編碼時鐘直覺與相對位置線性性質、Multi-Head Attention（$h=8$）與 Encoder/Decoder 三種注意力（Self / $-\infty$ Masked / Cross-Attention）、ResNet 殘差連結 $z+\ell(z)$ 與 LayerNorm / RMSNorm / DyT 正規化演進。
