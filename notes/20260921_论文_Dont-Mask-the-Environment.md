# 论文阅读：Don't Mask the Environment（观测监督如何改变 RL 下的 Agent 探索）

日期：2026-09-21　阶段：论文阅读

> 论文：*Don't Mask the Environment: Observation Supervision Changes How Agents Explore Under RL*
> Juzheng Zhang 等（University of Maryland + AWS AI Labs），arXiv **2609.20715v1** [cs.LG]，2026-09-17，29 页

## 1. 一句话

Agent 轨迹的 SFT 通常只对**动作（action）token**算损失，把**环境观测（observation）token** 当成上下文 mask 掉；这篇把观测也纳入损失（记作 **ActObs**），**不加数据、不加参数、不加前向次数、不改 RL 算法**，只改 loss mask —— 结果 SFT 后两者差不多，但**接上 GRPO 之后 ActObs 明显更好**（pass@k 更高、熵保持更高）。

## 2. 它解决的问题与做法

- 轨迹形式：`ω = (x, a₁, o₁, a₂, o₂, …)`，`x` 是任务提示，`a` 是模型动作，`o` 是环境返回的终端输出。
- 标准做法（ActionSFT）：损失只落在 `A`（动作 token）上，`O`（观测 token）被 mask。
- 本文做法：损失同时落在 `A` 和 `O` 上，用权重 `θ` 控制；`θ=0` 退化为 ActionSFT，默认 `θ=1`。**prompt 仍然 mask**，分母做加权归一化保持量级。
- 直觉：预测 `o` 就是逼模型建模"这个动作会对环境造成什么后果"，等于把每条轨迹同时当成**模仿样本**和**状态转移样本**。

## 3. 主要结果

| 设置 | 结论 |
|---|---|
| SFT 之后 | 三种做法（ActionSFT / ActObs / Obs→Act）差不多 |
| 再做 GRPO（4B） | ActObs 在每个采样预算下都更好，pass@1 相对提升约 29% |
| 8B | 牺牲一点 pass@1，换更高 pass@k（pass@16 +3.4pp），解出更多不同任务（24 vs 21） |
| 跨域（aider-polyglot 225 任务） | 4B 上 pass@1 +4.2pp，说明泛化更好 |
| 机制分析 | 动作与观测的梯度**很快趋于正交**；只训动作会让"预测环境后果"的能力**退化到低于基座模型**；联合监督保住这一能力，让 GRPO 保留更多熵、离 SFT 初值更近 |
| 对照 | 把 ActionSFT 的推理温度调高到同等熵，**补不上** pass@k 的差距 |
| 规模 | Qwen3-4B/8B；50k 条终端轨迹 0.71B tokens（观测约占 45%）；GRPO 135 步、2392 个任务；评测 Terminal-Bench 2.0（89 任务）、aider-polyglot（225 任务） |

## 4. 读它需要的前置知识

### A. 必须懂（不懂就读不下去）

1. **自回归语言模型的基本训练目标**：token、下一个 token 预测、logits → softmax → 交叉熵损失。
2. **SFT 与 loss mask**：知道"SFT 就是在算 next-token 交叉熵"，以及"mask 某段 token"意味着把这些位置的损失置 0（通常在 prompt 上做）。
3. **RL 微调的基本概念**：policy、reward、advantage、KL 约束、rollout（采样）；尤其 **GRPO**——同一 prompt 采样一组回答、用组内相对分数当优势，不需要 critic。
4. **Agent 轨迹的形态**：多轮 `(action, observation)` 交错、观测是环境返回的原始输出。
5. **评测术语**：`pass@k`（采样 k 次至少一次成功的概率估计）、temperature、（策略）熵作为探索度量。

### B. 重要（不熟也能读，但读不出味道）

6. **梯度的几何直觉**：把梯度看成向量 → 内积/夹角/正交/残差分量。机制那节（以及附录）靠的就是这个。
7. **概率与期望**：条件概率 `p(o|h,a)`、期望、熵的定义。
8. **微调与 RL 的衔接**：为什么"SFT 只是 RL 的初始化"这件事重要；分布外（OOD）泛化。

### C. 可以略读/后补

- GRPO 的具体超参（学习率、批量、rollout 数）
- 数据集构造细节（Nemotron-Terminal-Corpus 的合成流程）
- 附录里的逐样本统计、完整 transcript

## 5. 怎么读（三遍法）

1. **第一遍**：标题 + 摘要 + Figure 1 + Table 1 + 结论 → 能说清"改了什么、结果如何"。
2. **第二遍**：把公式 (1) 自己写一遍 → `θ=0` 是只算动作，`θ=1` 是都算，分母按 `|A| + θ|O|` 归一化。这是全文**唯一**的技术改动，务必手推。
3. **第三遍**：机制部分（梯度正交、残差梯度、熵）→ 重点关注"为什么 SFT 的两种初始化会让后面的 GRPO 走出不同的路"。
4. 看附录的控制实验时问一句：**"是观测监督的功劳，还是仅仅多训了一遍？"**（作者用 Obs→Act 时序对照来回答。）

## 6. 我现在的差距与补法

| 缺口 | 补法 | 预计 |
|---|---|---|
| Transformer 与交叉熵 | 李沐《动手学深度学习》+ Karpathy nanoGPT 训练循环 | 1–2 周 |
| SFT / loss mask 实操 | 读 nanoGPT 的 loss 计算 + HF 的 `labels=-100` 语义 | 3 天 |
| RL 微调（PPO→GRPO） | 李宏毅 RLHF 系列视频 + GRPO 原论文 | 1 周 |
| 梯度正交那部分 | 线性代数里的内积/正交就够了，不用更深的 | 随学随用 |
| pass@k / 熵 | 概念级理解即可，配合实验结果图看 | 2 天 |

## 7. 还没搞懂的

- 为什么观测梯度与动作梯度会"快速正交"？这个现象是通用的还是这套数据特有的。
- 熵更高一定带来更好的探索吗（还是只是采样多样性变高、单次可靠性反而降）。
- 提高观测损失权重 θ 的边界在哪里（论文给了 tradeoff 趋势，但没给最优值）。
