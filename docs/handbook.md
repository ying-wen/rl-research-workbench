# 强化学习实验与算法测试手册：完整阅读版

原手册 37 章全文，保留表格、公式、来源及证据边界。此文件由原始 HTML 与逐章映射生成；请修改原理快照以外的维护源，见 [维护说明](handbook-maintenance.md)。

[整体机制设计](mechanism-design.md) · [逐章代码与工具](handbook-code-map.md) · [代码反查原理](handbook-code-index.md) · [交互 HTML](handbook/index.html) · [原始快照](research-handbook.html)

HTML 提供全文筛选、浏览器本地勾选与导出。下列静态检查表不会自动保存状态；空白研究模板与可执行 CLI 协议分开。

- [01 · 如何使用这份手册](#guide-scope)
- [02 · 研究脉络：不同群体分别解决了什么问题](#guide-lineage)
- [03 · 先确定研究对象与目标函数](#guide-objective)
- [04 · 算法设计：从失效机制到可反驳的改进](#guide-design)
- [05 · 统计、调参与算力：明确一次实验究竟估计什么](#stats-framework)
- [06 · 随机单位、配对与重复：一个种子到底代表什么](#stats-randomness)
- [07 · 超参数测试：把选择、评估与搜索成本分开](#stats-hpo)
- [08 · 跨环境设置与超参数敏感性：峰值之外的算法品质](#stats-sensitivity)
- [09 · 种子数量与统计功效：用可检测差异决定预算](#stats-power)
- [10 · 区间回答不同问题：均值确定，不代表运行稳定](#stats-intervals)
- [11 · 跨任务聚合：同时保留分布形状与实际改善量](#stats-aggregate)
- [12 · 显著性、实际价值与多重比较](#stats-comparisons)
- [13 · 可直接执行的统计实验单](#stats-recipe)
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](#alg-classical)
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](#alg-deep)
- [16 · 基准选择：让任务集合对应想要验证的能力](#alg-benchmarks)
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](#alg-test-matrix)
- [18 · 持续强化学习：把整个生命期作为实验对象](#crl-framing)
- [19 · 目标、时间与被比较的系统](#crl-objectives)
- [20 · 先辨明变化来源，再设计对照](#crl-nonstationarity)
- [21 · 基准选择：原始协议与建议变体必须分开](#crl-benchmarks)
- [22 · 在线主评估，冻结与回访作为诊断](#crl-evaluation)
- [23 · 把收益、保留、可塑性与资源分别量化](#crl-metrics)
- [24 · 机制归因对照：每个对照回答一个问题](#crl-controls)
- [25 · 生命期调参与版本约束](#crl-tuning)
- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](#crl-recipe-a)
- [27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？](#crl-recipe-b)
- [28 · 长期试验阶梯与最小交付包](#crl-longrun)
- [29 · 实验执行：从预注册到独立确认](#ops-workflow)
- [30 · 诊断手册：症状、竞争解释与下一项实验](#ops-diagnostics)
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](#ops-extensions)
- [32 · 如何画图、写结论和判断证据够不够](#ops-evidence)
- [33 · 课题组可直接使用的检查清单](#ops-checklist)
- [34 · 补充原则：遗憾、能力泛化与压力测试](#appendix-comparators)
- [35 · 可复制模板与最小数据规范](#appendix-templates)
- [36 · 精读路线与术语对照](#appendix-reading)
- [37 · 来源登记与证据边界](#bibliography)

<a id="guide-scope"></a>


## 01 · 如何使用这份手册



可靠的强化学习研究，必须同时回答四件事：问题定义是否正确，算法是否按定义实现，性能差异是否可信，产生差异的机制是否被识别。持续强化学习还必须回答：过去的经验，是否在有限资源下持续改善未来的预测与控制。



本手册面向研究生、算法研究者、实验负责人及评审者。经典强化学习涵盖表格与线性函数逼近、预测与控制、同策略与异策略、回合制与持续任务；现代深度强化学习涵盖价值方法、策略梯度、actor–critic、模型学习、离线学习与泛化；持续强化学习涵盖长期交互、变化环境、遗忘、可塑性、状态构造与资源约束。多智能体、机器人和大模型智能体作为扩展边界讨论，不能用一个通用清单替代各领域的完整评测规范。



调研截至 **2026 年 10 月 3 日**。以 Adam White 的讲座为入口，沿参考文献、后续工作和独立研究群体扩展至教材、原始论文、作者讲义及官方实现文档。采用主题驱动的综合调研，**不声称完成所有数据库的穷尽检索或正式系统综述**。优先使用出版方、作者及官方代码来源；核心争议追溯全文，版本差异单独标注。没有运行本文所列算法训练，配方与预算都是待执行方案。


**三种证据身份。**“文献发现”是来源报告的结果；“经验建议”是作者讲义或工程文档中的实践意见；“手册建议”是本报告的综合设计，包括示例预算、验收门槛和模板。经验与建议都不能自动升级为定理、社区共识或已验证效果。


| 你的当前任务 | 阅读顺序 | 应产出的证据 |
| --- | --- | --- |
| 实现经典算法 | 目标定义 → 算法测试分册 → 最小配方 → 运行记录 | 可手算轨迹、精确真值、期望更新与边界行为 |
| 提出深度 RL 新算法 | 算法设计 → 实现审计 → 统计与调参 → 深度 RL 配方 | 机制预测、强基线、等预算比较、完整消融与独立确认 |
| 研究持续智能体 | 目标定义 → 持续 RL 分册 → 隔离评估 → 生命周期配方 | 在线收益、未来适应、保留与迁移、长期资源曲线 |
| 评审或复现实验 | 结论与证据对应表 → 协议 → 来源与版本 → 检查清单 | 可以重算的原始结果，以及明确不能支持的结论 |

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#guide-scope)。 入口：[start-here](../docs/start-here.md) · [iteration](../docs/iteration.md) · [testing](../docs/testing.md)

<a id="guide-lineage"></a>


## 02 · 研究脉络：不同群体分别解决了什么问题



强化学习实验方法论并非某一实验室的一套规则。下面按照研究问题组织脉络；各分册继续给出公式、实施方法和边界。一个有效的实验设计通常需要把这些视角组合使用。



| 研究脉络与代表作者 | 贡献所在 | 转化为实验行动 |
| --- | --- | --- |
| Sutton、Barto 及经典随机逼近研究 | 明确预测/控制目标、更新算子、访问与收敛条件 | 先建立精确或可分析的基准，再检验近似与闭环性能；定理前提与实验设定逐条对应 |
| [Adam White 讲座](https://deeprlcourse.github.io/assets/guests/adam_white.pdf)；Patterson、Neumann、Martha White、Adam White | 把实验看作关于完整学习系统的科学推断；统筹运行分布、基线、超参及研究者偏差 | 先写要估计的量，再决定重复、统计量和调参协议 |
| [Schulman 2017 讲义](https://sites.google.com/view/deep-rl-bootcamp/lectures)；[Achiam 2018](https://spinningup.openai.com/en/latest/spinningup/spinningup.html) | 从小问题启动、观察学习过程、调好基线、持续消融与回归验证 | 建立小型诊断问题集，检查状态访问、价值拟合、策略变化和失败样本 |
| [Islam 等 2017](https://arxiv.org/abs/1708.04133)；[Henderson 等 2018](https://ojs.aaai.org/index.php/AAAI/article/view/11694) | 揭示随机性、实现与超参导致的复现差异 | 公开每次独立训练的结果，不把不同代码和包装器下的数字直接拼表 |
| Colas、Sigaud、Oudeyer；Jordan、Chandak、Thomas 等 | 功效、统计比较，以及“算法加调参过程”的评价 | 区分固定配置与选择过程；按目标效应及误差要求规划重复次数 |
| Agarwal、Schwarzer、Castro、Courville、Bellemare | 跨任务聚合、不确定性、IQM、性能分布与改进概率 | 同时报告聚合、逐任务结果与分布，不让一个排名遮蔽退化任务 |
| [Chan、Fishman、Canny、Korattikara、Guadarrama](https://arxiv.org/abs/1912.05663) | 把可靠性拆为时间波动、训练间差异和下尾风险 | 平均成绩以外，记录崩溃概率、坏运行和训练中的性能下跌 |
| Engstrom、Ilyas、Madry 等；Andrychowicz 等 | 识别策略梯度中实现选择与算法机制的混杂 | 统一实现骨架做机制比较，再用独立实现检查结论可迁移性 |
| [Huang、Dossa、Raffin、Kanervisto、Wang](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/)；[SB3 团队](https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html) | 把代码谱系、包装器和 PPO 实现细节变得可检查 | 引用 commit 和实际配置；把张量形状、终止处理、动作变换写成具体测试 |
| Machado、Bellemare 等的 ALE；Osband 等的 bsuite；Cobbe 等的 Procgen | 分别强调协议可比性、能力诊断和未见环境泛化 | 一个基准只承担它能测的能力；从已见游戏成绩推到未见任务必须另做实验 |
| [Obando Ceron、Castro](https://proceedings.mlr.press/v139/ceron21a.html) | 小规模实验仍可产生关于算法组件的科学洞见 | 把廉价机制实验用作研究主干之一，再验证向复杂环境的外推 |
| Eimer、Lindauer、Raileanu；Adkins、Bowling、White | 调参方法、开发集过拟合与超参敏感性的评价 | 报告搜索分布和成本，检测“容易调”是否只是选择了有利的搜索范围 |
| [Dulac-Arnold 等](https://arxiv.org/abs/2003.11881)；[Wang 等](https://openreview.net/forum?id=AiOUi3440V)；[Coblin 等](https://arxiv.org/abs/2608.11349) | 真实环境约束与不能在线反复调参时的模型辅助选择 | 计算部署前成本，并单独检验模型选择排名能否转移到真实数据或交互 |
| [Gorsane 等](https://proceedings.neurips.cc/paper_files/paper/2022/hash/249f73e01f0a2bb6c8d971b565f159a7-Abstract-Conference.html) | 把单智能体经验扩展到合作 MARL 的报告与比较协议 | 把一次联合训练作为统计单位，固定地图、队伍规模及评估对手 |
| Sutton 等的 Alberta Plan；Dohare 等；Sokar 等；Wołczyk 等；Khetarpal 等；持续环境研究群体 | 将适应、遗忘、可塑性、状态构造与生命周期纳入研究对象 | 保留一个学习者的完整生命史，用长期在线结果及受控诊断共同支撑结论 |




### 对入口讲座的准确理解



White 的课件先讨论实验目的，再以复现案例说明少量运行、基线调参及未记载实现的风险，继而讨论分布与超参，最后讨论 calibration models。其“更多重复”不是统一规定某个种子数；水处理部分也不能直接当成通用自主控制成功。出处为原课件第 5–7、13–17、25–38、40–60 页（按 PDF 的 1 起始页码）。这里读取的是课件，未把未获取的完整视频转录当作证据。



### 经验的边界和相互张力



早期实用讲义推荐标准化、增加采样、监控熵与 KL，这些是排错起点。它们不是“熵必须越大越好”“KL 越小算法越好”或“所有任务都必须减去奖励均值”的定律。Schulman 用 1/(1−γ) 描述折扣的时间尺度，也不意味着这个长度以外的奖励被硬截断。Achiam 的研究入门建议强调强性能基线；本手册进一步区分机制发现、理论反例、负结果与性能提升——有价值的科学贡献不必都成为排行榜第一。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#guide-lineage)。 入口：[algorithm-design](../docs/algorithm-design.md) · [statistics](../docs/statistics.md) · [catalog](../docs/catalog.md)

<a id="guide-objective"></a>


## 03 · 先确定研究对象与目标函数



算法名不足以定义实验。把一个实验写成 `问题分布 × 环境与包装器 × 学习算法 × 实现 × 超参选择器 × 资源预算 × 评估规则`。其中任意一项改变，都可能改变结论所指的对象。下面的形式化与协议是本手册的综合建议。



| 目标 | 可估计的量 | 需要隔离的混杂 |
| --- | --- | --- |
| 部署一个固定策略 | J(π)=E\[Σ γᵗRₜ₊₁\] 或未折扣回合回报、成功率 | 训练随机性与策略评估随机性；选择 checkpoint 的规则 |
| 学习过程的价值 | J<sub>life,T</sub>(A)=E\[Σ<sub>t=0…T−1</sub> Rₜ₊₁\]；均值为 J/T | 探索损失、启动成本、恢复期均计入；不能只取最好后缀 |
| 持续任务稳态控制 | ρ(π)=lim<sub>T→∞</sub>E\[Σ Rₜ₊₁\]/T，在极限存在等条件下 | 有限时域经验均值不是稳态极限证明；非平稳环境也不必有此极限 |
| 预测学习 | E<sub>s∼d</sub>\[(v̂(s)−v<sup>π</sup>(s))²\]，以及明确投影权重下的 MSPBE 等 | d、目标策略、cumulant 和 γ；MC 目标噪声与估计误差 |
| 泛化 | E<sub>M∼P<sub>test</sub></sub>\[J(A,M)\] | 未见 seed、未见地图、未见动力学、未见任务家族不是同一级别 |
| 低成本可用性 | 给定总开发/部署预算后所选算法的未来收益 | 所有候选、调参失败、评估和搜索计算都可能属于成本 |




**例：**方法 A 在前半程损失严重、最后得分很高；方法 B 较早学会且之后略低。固定末端策略评价可能支持 A，累计在线回报可能支持 B。二者没有统计矛盾，回答的是不同问题。平均回合回报还会因策略改变回合长度而改变权重：它不等于每个环境时间步的平均奖励。



### 算法与环境之间的信息边界



在时刻 t，行动只允许依赖已获得的历史 Hₜ=(O₀,A₀,R₁,…,Oₜ) 及预先允许的知识。任务标识、真实状态、未来变化时间、离线最优动作、额外训练标签、环境模型查询、奖励函数内部变量，都必须列明是否可访问。训练期特权信息可以是合法设定，但必须公开，并为基线匹配权限。



状态表示 xₜ=f(Hₜ) 与环境真实状态 Sₜ 要分开。给某个方法真实状态，而其他方法仅见局部像素，测到的可能是信息优势。若研究的是部分可观测条件下的记忆，必须保持观测接口一致，并为“充分状态 oracle”另列诊断曲线。



### 奖励、评价指标和任务效用应分别记载



训练可以用裁剪、缩放、内在奖励或塑形奖励；主评估仍应报告原始任务回报及实际成功/失败指标。奖励升高而目标行为没有改善，需要检查奖励漏洞。正比例缩放在无额外约束的纯回报目标下保留策略排序，但会改变梯度、优化器和熵正则的相对尺度；逐步加常数在可变长度回合中可能改变偏好。



```text
R′(s,a,s′)=R(s,a,s′)+γΦ(s′)−Φ(s)
```



[Ng、Harada、Russell（1999）](https://people.eecs.berkeley.edu/~russell/papers/icml99-shaping.pdf)给出 potential-based shaping 的策略不变性条件。实践中要匹配折扣与边界条件；有限回合的末端势函数若处理错误，残余项仍会改变目标。报告中同时给原始奖励与塑形奖励的定义，不能把改任务当作算法改进。



### “更公平”必须对应资源问题



同样环境步数支持样本效率比较，同样墙钟时间支持特定硬件下的速度比较，同样梯度步数支持部分优化比较；三者通常无法同时相等。回放比例、批量大小、并行环境数、模型滚动、规划次数和决策频率都会改变资源。主分析预先选一个约束，补充其他坐标下的收益—成本曲线，而不是强行宣布一种归一化永远公平。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#guide-objective)。 入口：[protocol-reference](../docs/protocol-reference.md) · [algorithm-design](../docs/algorithm-design.md) · [continual](../docs/continual.md)

<a id="guide-design"></a>


## 04 · 算法设计：从失效机制到可反驳的改进



以下流程吸收经典 RL 的算子分析、[Schulman 的小问题与消融经验](https://sites.google.com/view/deep-rl-bootcamp/lectures)、[Ilyas 等对策略梯度内部环节的诊断](https://arxiv.org/abs/1811.02553)及实现比较研究。它是一套研究流程建议，不是任何单篇论文原样提出的标准。



1. **精确定义症状。**“不稳定”要改写成可观测事件：值函数数值发散、回报短时下降、训练间双峰分布、更新后 KL 突增、变化后无法恢复，或长期性能衰退。
2. **给出竞争解释。**至少区分环境错误、数据覆盖不足、估计偏差、优化失败、表示能力、奖励尺度、探索与信用分配。不要先认定自己擅长的模块就是原因。
3. **构造最小反例与正例。**一个任务刻意放大该机制，另一个去掉该机制。写出在何种条件下新方法应该有效、无效甚至更差。
4. **推导修改的对象。**目标函数、更新估计器、预条件矩阵、采样分布、状态表示、探索策略、回放规则分别是什么；是否引入偏差、新的超参或额外信息。
5. **写出中介预测。**例如“减少估值偏差后改善动作选择”，应同时预测偏差和控制收益。只测最终回报无法确认因果链。
6. **先用固定数据检验计算，再回到交互。**固定经验序列适于验证估计器与更新；闭环对照才能评估策略改变后产生的数据分布、探索和长期收益。
7. **去除替代解释。**匹配参数量、更新次数、数据可见性及调参预算；比较廉价替代品，例如单纯降学习率、加宽网络或增大批量。
8. **独立确认与外推。**锁定算法后，用未参与开发的种子和任务复核；报告失败家族。机制成立不等于普遍性能优势。



### 示例：过估计假设如何成为完整实验



```text
若 Q̂(a)=Q(a)+εₐ 且 E[εₐ]=0，
E[maxₐ Q̂(a)] ≥ maxₐ E[Q̂(a)] = maxₐ Q(a)。
```



这个由 max 的凸性得到的关系指出一种过估计来源，却没有证明某个深度算法必然失败，也没有保证双估计器永远更好。要设计实验：先控制动作数、噪声和估计器相关性，检查偏差随条件改变；再检查动作排序；最后在闭环比较回报、欠估计与样本效率。若新算法收益来自额外网络容量或更少更新，应由匹配对照揭示。相关机制背景见 [van Hasselt 等对 deadly triad 的实证分析](https://arxiv.org/abs/1812.02648)，以及算法分册的 Double Q / TD3 原始论文。



### 六类设计问题及对应证据



| 改动对象 | 应提出的机制问题 | 关键对照与诊断 |
| --- | --- | --- |
| 状态表示与记忆 | 历史中的什么信息影响未来预测和控制？ | 同观测的无记忆模型、等容量模型、充分状态 oracle；延迟/混淆状态探针 |
| 探索与数据收集 | 是否更快访问有用状态，而不只是更随机？ | 奖励发现率、覆盖、首次成功时间；固定行为数据与闭环分别比较 |
| 信用分配 | 奖励延迟、噪声或干扰如何改变更新质量？ | 受控延迟链、无关干扰特征、有限差分、trace 截断和 λ=0 边界 |
| 自举与价值估计 | 误差来自目标噪声、偏差还是分布不匹配？ | 精确值、MC 参考、目标网络频率、异策略程度；偏差与回报分开报告 |
| 优化与模块耦合 | 预条件或步长改变了大小、方向还是时序？ | 等更新范数对照、actor/critic 分别冻结、共享/分离表示、优化状态匹配 |
| 持续适应与可塑性 | 过去学习导致的新知识获取障碍是否被缓解？ | 年龄匹配/经验匹配探针、fresh agent、重置状态消融、相同资源下长期适应 |




### 消融不应只有“拿掉一个组件”



两组件 X、Y 应至少比较基线、仅 X、仅 Y、X+Y。交互项可定义为 Δ<sub>XY</sub>=J<sub>XY</sub>−J<sub>X</sub>−J<sub>Y</sub>+J<sub>0</sub>；其大小依赖评价尺度，需给不确定性。固定超参的消融回答“在原配置附近拿掉组件会怎样”；给每个消融重新调参回答“该算法族去掉组件后最佳可达到什么”。两者都可用，但不得混称。



“额外模块”最好再加入参数量匹配、计算量匹配、随机/打乱信号、简单常数策略、oracle 五类中的适用对照。信号打乱可能改变时间相关性和数值分布，必须说明它破坏了什么。oracle 提供额外信息，通常是诊断参考；未证明时，不叫理论上界。



### 如何对待没有提升的结果



算法实现通过、更新等式验证或梯度误差降到机器精度，只说明计算一致。若回报提升不确定，就保留“机制计算正确但效益未确立”的结论。相反，在确认实现与统计能力后发现理论预期不适用于深度闭环，也可以形成有价值的负结果。不要删掉退化任务、崩溃运行或不支持故事的消融。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#guide-design)。 入口：[algorithm-design](../docs/algorithm-design.md) · [testing](../docs/testing.md) · [iteration](../docs/iteration.md)

<a id="stats-framework"></a>


## 05 · 统计、调参与算力：明确一次实验究竟估计什么



本章综合实证 RL、稳健统计、AutoML 与工程复现研究，提出可执行的手册规则；规则是针对研究工作流的综合建议，不能当作所有论文一致认可的标准。核心文献已核对正式出版页，并阅读全文中的相关方法、实验及局限部分。



Adam White 的课程把统计比较、调参、跨任务聚合分别连接到 Colas、Jordan、Agarwal 等人的工作，因而起点本身就是多条研究路线的汇合。[White，课程课件](https://deeprlcourse.github.io/assets/guests/adam_white.pdf)强调先提出有资源回答的问题；[Patterson 等，2024](https://jmlr.org/papers/v25/23-0183.html)则系统讨论性能分布、参数选择、比较与环境设计。两者最值得继承的是“结论必须匹配实验问题”，而非把某种图表或种子数变成合格证。



<a id="stats-estimands"></a>

### 1. 在运行前写下估计对象



设算法为 A，配置为 h，环境为 e，完整训练随机性为 ξ，预算为 T；单次训练产生轨迹，再按预先固定的规则得到标量 X(A,h,e,ξ;T)。统计对象至少分为以下四种，不能混报：



| 问题 | 估计对象 | 需要独立变化的层级 |
| --- | --- | --- |
| 这个明确配置能否可靠运行？ | μ(h,e)=E<sub>ξ</sub>\[X(A,h,e,ξ;T)\] | 完整训练运行；评估回合是其内部观测 |
| 给定调参流程和预算后可达到什么表现？ | Ψ(B)=E<sub>D<sub>tune</sub>,ξ<sub>HPO</sub></sub>\[μ(ĥ<sub>B</sub>,e)\] | 重复整个调参流程，再独立测试所选配置 |
| 固定任务集上整体如何？ | θ<sub>suite</sub>=Σ<sub>e</sub>w<sub>e</sub>μ(h,e) | 固定环境中的运行；w<sub>e</sub>预先给定 |
| 新环境或新持续流上能否泛化？ | θ<sub>pop</sub>=E<sub>e∼P</sub>E<sub>ξ</sub>\[X\] | 独立抽取环境、流或任务序列，再抽训练随机性 |




固定 h 的测试均值并不估计未知的最优配置；在已调过的任务上换新种子，也不等于泛化到新任务。[Jordan 等，2020，§3–5](https://proceedings.mlr.press/v119/jordan20a.html)把参数选择规则纳入完整算法定义，并考虑归一化和聚合产生的不确定性；其目标偏向可直接使用的算法，和“充分调参后的峰值能力”是不同问题。



**手册建议：**论文主张应能改写为“A 的完整实现，在 P、T、B 下，相比 B 的预先指定主指标至少改善 δ；结论针对固定任务集／新任务分布”。如果 P 只是人为收集的一组游戏，写清“在该任务集上”，不要用统计区间把代表性问题藏起来。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-framework)。 入口：[statistics](../docs/statistics.md) · [protocol-reference](../docs/protocol-reference.md) · [iteration](../docs/iteration.md)

<a id="stats-randomness"></a>


## 06 · 随机单位、配对与重复：一个种子到底代表什么



最常见的伪重复是把一个训练所得策略的 100 个测试回合当作 100 个算法样本。它们主要刻画同一策略的执行噪声；不同初始化、探索路径、回放内容导致的训练间变化仍只有一个样本。[Henderson 等，2018](https://ojs.aaai.org/index.php/AAAI/article/download/11694/11553)通过连续控制实验显示，随机性、网络设置、奖励缩放与代码库都可能改变比较结果；该证据不意味着所有任务的方差结构完全相同。



用独立的随机数生成器分别控制环境、初始化、动作采样、回放采样、数据顺序、任务生成及 HPO 搜索，并记录派生规则。评估调用不得消耗训练 RNG 或修改训练的归一化统计。硬件非确定性应作为实现条件记录；固定整数种子不等于逐位确定复现。



配对设计应让 A、B 面对同一条外生情景，例如相同扰动表、任务序列、初始状态或预先生成的数据流。若 D<sub>i</sub>=X<sub>A,i</sub>−X<sub>B,i</sub>，则 Var(D)=Var(X<sub>A</sub>)+Var(X<sub>B</sub>)−2Cov(X<sub>A</sub>,X<sub>B</sub>)；正相关才带来方差降低。算法耗用随机数的顺序不同，仅令 seed=42 并不保证情景相同。配对规则须在看到结果前固定，不能事后挑最有利的匹配。参见[NIST，两样本比较](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm)。



持续 RL 中，一条跨越全部阶段的训练流通常是独立单位，阶段不是独立样本。共享预训练模型的多个微调任务还具有共同上游随机性；若要对“重新预训练后再适配”的流程作推断，应重采样或重复预训练层级。预算只允许一个预训练模型时，可报告“条件于该模型”的结果，不能虚构上游独立重复。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-randomness)。 入口：[statistics](../docs/statistics.md) · [testing](../docs/testing.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="stats-hpo"></a>


## 07 · 超参数测试：把选择、评估与搜索成本分开



### 2. 三层数据纪律



[Eimer、Lindauer 与 Raileanu，2023，§4–6](https://proceedings.mlr.press/v202/eimer23a.html)展示了对调参种子的过拟合，并比较自动 HPO 与常见人工搜索；其可迁移经验是明确搜索空间、预算、目标及独立测试种子，而不是照搬文中某个小种子数。手册采用如下三层流程：



1. **开发层：**查错、画诊断图、确定候选模块；探索次数、曾尝试的方法和环境都进入研究日志。
2. **选择层：**冻结搜索空间 H、采样分布 q(h)、HPO 方法、预算 B、种子集合、checkpoint 选择与失败处理规则。仅在该层选 ĥ。
3. **确认层：**锁实现与 ĥ，在从未参与选择的运行上评估。若目标是新任务迁移，还要隔离任务或流生成规则；改变方法后原确认集转为开发证据。



单阶段挑最好均值有赢家偏差：E\[max<sub>h</sub>X̄<sub>h</sub>\]≥max<sub>h</sub>E\[X̄<sub>h</sub>\]。独立复测消除“使用同一噪声既选择又报分”的偏差，但得到的是所选配置的性能。要评估 Ψ(B)，外层必须重复选择过程；可对完整 sweep 数据做重采样近似，但小样本无法恢复未出现的失败模式，简单对最大值 bootstrap 也不会自动提供无偏最优值估计。这是对[Patterson 等，2024，§3.2](https://jmlr.org/papers/v25/23-0183.html)选择不确定性讨论的执行层区分。



### 3. 搜索公平性与成本



相同配置数量、相同环境步数、相同 GPU 小时分别回答不同问题。建议主比较固定一种与应用相关的预算，另报三维成本：环境交互、计算时间与人工开发。计入全部失败候选、早停、评估、元优化和预训练；复用公开配置要给出处与先验调参范围。算法“只需一个学习率”不等于零调参：网络宽度、归一化、更新比、截断阈值、初始值也可能是设计自由度。



[Bergstra 与 Bengio，2012](https://www.jmlr.org/papers/v13/bergstra12a.html)给出随机搜索的理论和实验证据，适合作为多维搜索的基线；其原始实验不是 RL，不能推成所有 RL 问题上必优。学习率通常按对数尺度采样，但尺度和边界本身必须公开。[Li 等，2018，Hyperband](https://www.jmlr.org/papers/v18/16-558.html)通过早停和资源分配提高搜索效率。用于 RL 前，应在开发集验证短预算排名能否预测长预算表现，否则容易淘汰探索慢、后期才稳定的配置；持续学习的短前缀尤其不能代表长期适应。



报告“搜索预算—独立测试性能”曲线：每个预算点重新执行同一选择规则，测试数据只用于画最终曲线。自动调参和自适应超参数是完整算法的一部分；其元参数、重启和群体规模仍计成本。[Parker-Holder 等，2022](https://jair.org/index.php/jair/article/view/13596)的 AutoRL 综述提供元学习、演化及配置方法的地图，不能替代针对具体流水线的独立测试。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-hpo)。 入口：[statistics](../docs/statistics.md) · [iteration](../docs/iteration.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="stats-sensitivity"></a>


## 08 · 跨环境设置与超参数敏感性：峰值之外的算法品质



[Patterson 等，2024，CHS／现行 CHTB，§4](https://rlj.cs.umass.edu/2024/papers/Paper330.html)在多个环境上选择一个共享配置，再用新运行复测。现行官方题名为 *Cross-environment Hyperparameter Tuning for Reinforcement Learning*；早期 CHS 名称仍见于摘要。共享配置的选择可写为 ĥ=argmax<sub>h</sub>Σ<sub>e</sub>w<sub>e</sub>X̄<sub>e,h</sub>（先作合理归一化）。若使用非线性经验 CDF，应先逐运行变换，再求均值，即 E\[F<sub>e</sub>(X)\]；它不等于 F<sub>e</sub>(E\[X\])。这是跨任务一致性的测试；若选择和报告使用同一环境集，它并不是环境外泛化测试。



[Adkins、Bowling 与 White，2024，§3、§5–6](https://papers.nips.cc/paper_files/paper/2024/hash/e1cadf5f02cc524b59c208728c73f91c-Abstract-Conference.html)进一步定义逐环境调参与共享设置的差值。令 Γ(e,h) 为期望性能的可比尺度：



```text
Φ = Σ_{e}w_{e} max_{h} Γ(e,h) − max_{h} Σ_{e}w_{e}Γ(e,h) ≥ 0.
```



Φ 衡量对逐环境调参的依赖；有效超参数维度衡量为达到规定比例的跨环境平均逐环境调参峰值，至少要释放多少个坐标逐环境调整，其余坐标锁在最佳共享配置。论文采用的 95% 是可调整阈值。搜索范围、网格密度、任务组成、归一化都会改变结果，因此不能把 Φ 当作算法脱离情境的常数。



**手册扩展：**同时画共享配置分数、逐环境调参分数和预算曲线；给学习率×更新比等关键二维交互图。单变量扫描要说明其余参数锁定或重新调优：前者测试固定系统的干预效应，后者测试剩余系统可补偿后的最佳表现。对自适应方法，增加奖励尺度、观测尺度、数据速率和漂移速度变化，才能检查“自动适应”是否只是把敏感性移到元参数。



归一化须固定参考：随机／人类参考差接近零时，线性归一化会放大噪声；经验 CDF 依赖参与算法和参数池，加入新算法可改变旧分数。保存原始单位、参考值及生成数据；跨版本比较时重新使用同一参考。用当次所有结果决定归一化常数时，其估计误差也应进入不确定性传播，或明确区间条件于该参考。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-sensitivity)。 入口：[statistics](../docs/statistics.md) · [algorithm-design](../docs/algorithm-design.md) · [continual-project-playbooks](../docs/continual-project-playbooks.md)

<a id="stats-power"></a>


## 09 · 种子数量与统计功效：用可检测差异决定预算



[Colas、Sigaud 与 Oudeyer，2019，§4–6](https://arxiv.org/abs/1904.06979)比较了偏态、多峰和真实 RL 性能分布上的检验，说明小样本既可能误报也可能漏报。其“约 20 个样本识别大效应”等结论依赖实验分布、效应量及检验，不能当成 RL 的统一门槛。均值作为期望值的估计并不要求原始数据是高斯分布；真正需要检查的是所用推断方法的假设与有限样本表现。



先定义有实际意义的最小改善 δ，再用独立先导实验估计方差。双侧 α、功效 1−β、近似正态且等样本数的两独立组，每组所需运行数近似为：



```text
n ≈ (z_{1−α/2}+z_{1−β})²(σ_{A}²+σ_{B}²)/δ²；若 σ_{A}=σ_{B}=σ，则 n≈2(z_{1−α/2}+z_{1−β})²/d²，d=δ/σ。
```



由[NIST 样本量公式](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm)应用于两组均值差推得：α=0.05、功效 0.8 时，d=1 约需每组 16 次，d=0.5 约需 63 次；这是大样本规划近似，小样本 t 临界值通常使需求增加。配对情形明确使用 n<sub>pairs</sub>≈(z<sub>1−α/2</sub>+z<sub>1−β</sub>)²σ<sub>D</sub>²/δ²，不再有两独立组的系数 2；n 计配对数。重尾、多峰、失败混合及嵌套调参应模拟完整分析过程的覆盖率和检出率，不能仅塞入一个 pooled SD。



本手册不规定“统一 3／5／10 个种子”。有限预算先缩小确认问题、减少次要方法或增加廉价诊断，而不是把几次昂贵运行包装成高精度结论。分阶段增加样本应预先确定阶段及停止规则；看到 p 刚好小于 0.05 就停止会改变错误率。探索后再确认时，使用新样本。



没有观察到失败也不等于可靠：独立运行 n 次、零失败，二项模型下一侧 95% 失败概率上界为 1−0.05<sup>1/n</sup>。n=10、30、100 时分别约为 25.9%、9.5%、3.0%。这是直接由“零次失败”的概率 (1−p)<sup>n</sup> 反解所得；任务依赖、分布变化及相关运行会破坏该模型。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-power)。 入口：[statistics](../docs/statistics.md) · [iteration](../docs/iteration.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="stats-intervals"></a>


## 10 · 区间回答不同问题：均值确定，不代表运行稳定



| 表达 | 含义 | 误读风险 |
| --- | --- | --- |
| 标准差、经验分位数、全部运行散点 | 已观测运行的分散程度 | 不是总体参数的 95% 置信区间 |
| 均值差的置信区间 | 重复抽样程序对固定总体差值的覆盖性质 | 不是“下一次运行落入此区间的概率” |
| 预测区间 | 规定模型下单个未来观测的范围 | 不等于覆盖某个比例总体的保证 |
| (1−α,p) 容忍区间 | 以置信度 1−α，至少覆盖总体 p 的比例 | 不能直接把样本 5%–95% 分位数叫 95% 置信容忍区间 |




[NIST，容忍区间](https://www.itl.nist.gov/div898/handbook/prc/section2/prc263.htm)区分总体参数与总体成员的范围。可写为 P<sub>D</sub>{P<sub>X</sub>(L(D)≤X≤U(D))≥p}≥1−α。增加运行数会缩小均值的不确定性，却不会消除算法实际运行的波动。对连续 IID 数据，以样本最小值和最大值为区间，覆盖总体比例 p 的置信度为 1−np<sup>n−1</sup>+(n−1)p<sup>n</sup>；p=0.9 时，n=46 才约达 95.2%。参见[NIST，分布无关极值区间](https://www.itl.nist.gov/div898/handbook/prc/section2/prc264.htm)。这个例子说明尾部可靠性往往比平均值更耗样本，并非建议所有实验统一运行 46 次。



建议每个确认实验至少输出主效应及区间、全部运行或经验分布、失败率及其区间；仅展示平滑平均曲线不足以判断多峰性。注明平滑窗口、先平滑再聚合还是先聚合再平滑、区间是逐时间点还是同时覆盖全曲线。跨时间的 95% 逐点带不能解释为整条轨迹 95% 同时覆盖。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-intervals)。 入口：[statistics](../docs/statistics.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="stats-aggregate"></a>


## 11 · 跨任务聚合：同时保留分布形状与实际改善量



[Agarwal 等，2021，§4](https://proceedings.neurips.cc/paper/2021/file/f514cec81cb148559cf475e7426eed5e-Paper.pdf)提出在少量重复的多任务基准中结合分层 bootstrap、IQM、性能分布及改善概率。其论据针对特定数据和覆盖率实验；不能据此宣称“bootstrap 可以修复任意三个种子”。特别是单任务尾部，未被采到的模式不会因重复重采样而出现。



设 M 个任务、任务 m 有 N<sub>m</sub> 次运行，归一化分数为 x<sub>m,n</sub>。应先明确任务权重 w<sub>m</sub>≥0、Σw<sub>m</sub>=1，等权时 w<sub>m</sub>=1/M；不同任务运行数不同时，直接摊平数据会让样本较多的任务占更大权重。建议使用下列互补指标，而不是看结果后选择最有利者：



| 指标 | 定义 | 用途与边界 |
| --- | --- | --- |
| 任务加权均值（等权为特例） | Σ<sub>m</sub>w<sub>m</sub>N<sub>m</sub><sup>−1</sup>Σ<sub>n</sub>x<sub>m,n</sub> | 保留改善幅度；易受高分任务和归一化尺度影响 |
| IQM | 按既定任务权重组成的混合分布中去除上下各 25% 质量后的均值 | 均值与中位数间的稳健折中；尾部失败须另报 |
| 性能剖面 | P̂(τ)=Σ<sub>m</sub>w<sub>m</sub>N<sub>m</sub><sup>−1</sup>Σ<sub>n</sub>1\[x<sub>m,n</sub>&gt;τ\] | 呈现超过不同阈值的运行比例；交叉曲线提示取舍 |
| 平均改善概率 | Σ<sub>m</sub>w<sub>m</sub>{Pr(X<sub>A,m</sub>&gt;X<sub>B,m</sub>)+½Pr(X<sub>A,m</sub>=X<sub>B,m</sub>)} | 随机任务上独立运行的胜出概率；不表示效应幅度或“算法真正更好”的后验概率 |
| 目标缺口 | Σ<sub>m</sub>w<sub>m</sub>E\[(τ−X<sub>m</sub>)<sub>+</sub>\] | 只累计目标以下的不足；τ 应具有实际含义 |




这些定义可与[rliable 官方实现](https://github.com/google-research/rliable/blob/master/rliable/metrics.py)核对：标准矩阵输入是“运行×任务”；IQM 对所有分数做 25% trimmed mean，默认各任务运行数相同；库的 median 是“各任务均值的中位数”，不是所有运行混合后的中位数；改善概率实现按 Mann–Whitney U 处理相等值。库截至本次核验已于 2025-10-15 归档，复现时锁定版本及依赖，不能把库调用本身当作统计有效性的证明。



**执行规则：**固定任务集时，在每个任务内部有放回抽取完整运行，保持任务权重，每次重算主指标；95% percentile 区间取重采样统计量的 2.5% 和 97.5% 分位数。要比较 A−B，应直接构建差值分布；若设计配对，则共同抽取配对索引。研究新任务总体时，另需外层抽取独立任务／任务家族；研究完整调参流程时，重采样过程还须包含选择。重采样整条学习曲线可以保留时间依赖，而把 checkpoint 独立抽样会破坏它。更多 bootstrap 次数只能减少重采样的数值误差，不能增加真实实验信息。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-aggregate)。 入口：[statistics](../docs/statistics.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="stats-comparisons"></a>


## 12 · 显著性、实际价值与多重比较



优先报告差值 Δ̂、区间和事先定义的 δ。未拒绝“零差异”只表示证据不足；若主张两法在实践上等价，应定义等价界限并使用等价检验或相应区间准则。若区间同时允许大幅正效应与负效应，应写“尚不能区分”，不能写“性能相同”。



独立组均值比较可用 Welch 统计量 T=(X̄<sub>A</sub>−X̄<sub>B</sub>)/√(s<sub>A</sub>²/n<sub>A</sub>+s<sub>B</sub>²/n<sub>B</sub>)，自由度按 Welch–Satterthwaite 公式计算；它不要求两组方差相同，但不能保证极少样本、极端偏态下可靠。配对比较分析 D<sub>i</sub>。置换检验需要相应零假设下标签可交换；“两组均值相等”不自动保证异方差样本可任意置换。秩检验也不是均值检验的无假设替代。基础公式见[NIST](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm)，RL 分布下的经验比较见[Colas 等，2019](https://arxiv.org/abs/1904.06979)。



将 m 个检验组成一个预先定义的家族。Bonferroni 使用 α/m；[Holm，1979](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf)的逐步校正通常更有功效。若各检验独立且各自错误率为 α，至少一次误报概率是 1−(1−α)<sup>m</sup>，不是严格等于 mα；后者是一般的并合上界。大量探索问题可报告 [Benjamini–Hochberg，1995](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1995.tb02031.x)的 FDR 控制，但其原始保证针对独立统计量，相关检验应核对依赖条件；不能把探索后赢家当作预先假设。时间点、种子、任务子集、归一化方法和备选指标的选择同样构成分析自由度，不能只对最终表格几行做校正。



一套简洁的确认协议是：一个主指标、一个主预算、一个主要基线、一组预先声明的机制预测；次要指标用于解释。避免强制排出全部算法的线性名次：不确定区间、性能剖面交叉与任务异质性常常支持“各有条件优势”。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-comparisons)。 入口：[statistics](../docs/statistics.md) · [iteration](../docs/iteration.md)

<a id="stats-recipe"></a>


## 13 · 可直接执行的统计实验单



1. **冻结问题：**填写算法完整版本、环境／流分布、部署预算、主指标、实用差异 δ、确认与探索边界。
2. **登记随机层级：**列出任务、预训练、训练、评估回合与 HPO 种子；指定独立单位、是否配对及外生随机流。
3. **冻结选择器：**登记搜索空间和采样尺度、调参预算、评分窗口、checkpoint 规则、早停和 NaN／崩溃处理；基线同等执行。
4. **做预算规划：**用先导分布评估主效应区间宽度、功效及尾部失败概率；算力不足时缩小确认主张。
5. **执行独立确认：**固定后在新运行上测试；新任务主张需新任务，流程主张需重做整个选择过程。
6. **保留失败：**工程中断与算法发散分开记录。工程重跑仅依预定规则；算法失败不得只删掉再平均。缺失不是零分，零分也不是缺失；失败怎样映射成任务效用必须预先定义。
7. **输出证据包：**原始逐运行结果、差值及区间、分布／失败率、跨任务 IQM 与性能剖面、共享与逐环境调参对比、总计算成本和可重现分析脚本。
8. **限制结论：**分别写明统计不确定性、测试任务的代表性、搜索预算不足和未验证长期尾部；发布否定与不确定结果。



这些步骤同时适用于表格与线性 RL、现代深度 RL 和持续 RL；变化的是随机单位、时间指标及外推范围。经典小环境可以用大量重复检验估计器与机制，深度基准需要成本可承受的分层估计，持续学习必须保留完整流与前史依赖。三者都不能用一个漂亮的总分取代问题定义。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#stats-recipe)。 入口：[protocol-reference](../docs/protocol-reference.md) · [iteration](../docs/iteration.md) · [statistics](../docs/statistics.md)

<a id="alg-classical"></a>


算法正确性与研究设计 · 本节测试矩阵和配方为综合建议，尚未执行



## 14 · 经典强化学习：先建立可以被推翻的正确性证据



一个实现能提高回报，只说明某个程序在某个任务上有用；要确认它实现了所声称的算法，还需要独立真值、逐步更新和反例。建议按“接口语义 → 单步代数 → 采样期望 → 有限路径等价 → 长程行为 → 外部任务”逐级推进。教材提供问题与算法定义；下面的测试组合是本手册的工程与研究建议，不是教材规定的统一认证标准。[\[A01 Sutton–Barto 教材作者目录\]](https://people.cs.umass.edu/~barto/pubs-Barto.html)



<a id="alg-oracle"></a>

### 1. 真值必须独立于被测实现



在有限折扣 MDP 中，直接从转移表构造 P<sub>π</sub>、r<sub>π</sub>，解线性方程 (I−γP<sub>π</sub>)v=r<sub>π</sub>。不要把被测 TD 函数调用很多次当作真值。控制任务可枚举确定性策略或独立实现动态规划，检查 Bellman 最优残差；只有 γ&lt;1 的相应范数下，才能使用折扣算子的收缩误差界。γ=1 的回合任务需要适当终止条件，不能直接套同一逆矩阵或误差界。



最小回归问题可用 s₀→s₁→终止，奖励依次为 0、1，γ=0.9，因此 v=(0.9,1)。再加入随机转移、重复访问、并列最优动作、不可达状态、动作相关奖励和负奖励。每次只增加一个困难。用状态置换检验实现不依赖编号；在固定策略折扣预测中，检验奖励乘常数后的值缩放。涉及优化器、截断或自适应步长时，不要擅自要求整条学习轨迹也保持缩放等价。



线性预测必须区分逼近目标。令 v=Φw，D 为已声明的采样状态权重，A=ΦᵀD(I−γP<sub>π</sub>)Φ、b=ΦᵀDr<sub>π</sub>，TD 固定点在可解条件下满足 Aw=b；它通常不是最小均方值误差解，也不等同于最小均方 Bellman 误差解。对 GTD 类方法另算 MSPBE=(b−Aw)ᵀC⁻¹(b−Aw)，C=ΦᵀDΦ；奇异情形必须另述约束或广义逆。梯度 TD 的价值在于明确目标与稳定条件，不能把“TD loss 降低”当作这些目标都改善。[\[A02 GTD2/TDC 原论文\]](https://icml.cc/2009/papers/546.pdf)



<a id="alg-tabular"></a>

### 2. 按算法族选择最小反证



- **Bandit：**固定奖励表验证样本均值与常数步长递推；全相同估值时检查随机打破平局；ε-greedy 中“随机选动作”通常包括贪心动作，不能把最优动作概率误写成 1−ε。分别记录平均奖励、最优动作率、伪遗憾；非平稳试验把均值漂移与观测噪声分开设种子。
- **DP / MC：**同步 DP 与原地 DP 的中间轨迹可不同，固定点应匹配；MC 用一条重复访问状态的确定性轨迹区分 first-visit 与 every-visit，并验证终止奖励计入一次、回报下标无偏移。训练数据与真值估计样本不能共用后再宣称独立验证。
- **TD / Sarsa / Q-learning：**手算同一 transition 的三个 target，专门选择“采样下一动作不是贪心动作”的情况；Expected Sarsa 明确对哪个策略取期望。Q-learning 在固定 ε 下学最优动作值与 Sarsa 学含探索行为的动作值并非同一目标，不能要求曲线重合。
- **Eligibility traces：**λ=0 应退化到对应一步法；构造重复特征轨迹区分 accumulating 与 replacing trace。冻结权重的离线 forward view 与传统 trace 对照，在线随时更新权重时不要误要求传统 TD(λ) 与在线 forward view 精确相等。true-online 方法应和其匹配的在线 forward view 逐时刻比较，并覆盖非二值特征。[\[A03 true-online TD\]](https://jmlr.org/papers/v17/15-599.html)
- **Off-policy：**在能枚举动作的两动作 MDP 检查 ρ=π(a|s)/b(a|s)，验证 E<sub>b</sub>\[ρf\]=E<sub>π</sub>\[f\] 的适用条件、时间下标和乘积范围。令 b=π 时应退化；故意去掉行为支持时应报告不可识别。普通与加权重要性采样的有限样本偏差、方差不同，不应要求二者每批相等。
- **Actor–critic：**先令 critic 为精确 v<sup>π</sup>，再换成学习 critic。小 MDP 可从 J(θ)=μᵀ(I−γP<sub>θ</sub>)⁻¹r<sub>θ</sub>做中心有限差分，对照完整期望策略梯度；检查折扣访问权重、baseline 的动作独立性以及 actor 梯度是否误流入 critic target。最后才测 actor 与 critic 耦合。
- **Average reward：**先用不可约有限马尔可夫链解稳态分布 d，得到 r̄=dᵀr，再解 (I−P)v=r−r̄1 并指定一个值偏移规范。分别检查 r̄、差分价值与策略；不同 offset 的差分值不一定是错误。随后用 Access-Control 类持续任务检查饱和、拒绝动作和资源约束；不能用“γ非常接近1”自动替代平均奖励目标。[\[A04 Wan–Naik–Sutton\]](https://proceedings.mlr.press/v139/wan21a.html)



**收敛前提也要作为测试输入。**表格法应列出访问覆盖、步长是否满足随机逼近条件、策略是否固定或满足对应控制条件；线性 TD 应列出特征秩、采样分布和 on/off-policy；双时间尺度法应说明两组步长。有限样本稳定不是收敛证明，常数步长跟踪也不要求误差最终归零。保留 Baird 七状态反例：按原协议复现普通 off-policy TD 的发散，同时测稳定算法。若所有算法都“稳定”，优先排查隐藏裁剪、错误的行为分布或零初始化，而不是删去反例。[\[A02\]](https://icml.cc/2009/papers/546.pdf)



**有限差分不能选错被检验的函数。**半梯度 TD 有意将下一状态的值视为常量；若有限差分时同时扰动 target，就在检查另一个算法。先缓存 target 并冻结随机数，再比较自动微分与数值差分；要检查完整 Bellman residual 梯度则另设测试。随机转移下，平方期望 Bellman 误差与单样本平方 TD 误差也不同，后者不能直接充当前者的无偏梯度 oracle。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#alg-classical)。 入口：[testing](../docs/testing.md) · [algorithm-design](../docs/algorithm-design.md) · [catalog](../docs/catalog.md)

<a id="alg-deep"></a>


## 15 · 现代深度强化学习：把算法与实现共同视为被测对象



几条独立研究线索共同改变了测试对象的边界：Engstrom 等揭示代码中的优化、归一化与初始化会改变 PPO/TRPO 的比较；Andrychowicz 等在统一实现中系统调查超过 50 种选择；Fujimoto 等从 actor–critic 的估计误差推导出 TD3 的修正机制；Obando-Ceron 与 Castro 用小任务重新检查 Rainbow 的组成。它们支持“机制 → 可控干预 → 诊断 → 行为后果”的研究路径，但各自实验范围不能推出一个跨任务永远最优的配置。[\[A05\]](https://arxiv.org/abs/2005.12729) [\[A06\]](https://arxiv.org/abs/2006.05990) [\[A07\]](https://proceedings.mlr.press/v80/fujimoto18a.html) [\[A08\]](https://proceedings.mlr.press/v139/ceron21a.html)



<a id="alg-boundaries"></a>

### 3. 先通过轨迹边界测试，再看学习曲线



`terminated` 表示任务定义内的终止；`truncated` 表示外部截断。对继续任务目标，一步 target 通常为 r+γ(1−terminated)V(s′)：外部时间截断仍从最后真实观察 bootstrap。若时间预算本身是任务目标，则有限时域结束可属于真正终止，剩余时间也必须纳入 Markov 状态定义。不能仅凭“有时间上限”决定 mask。[\[A09\]](https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/)



**两个 mask 不可混成一个。**价值 bootstrap 可以跨外部截断估计未观测的未来，但针对独立回合目标，GAE/trace 的样本递推不能穿过 reset 拼接下一回合。跨回合 meta-RL 或持续世界重生则应按其上层目标另定连续性。用 `bootstrap_mask=1−terminated` 计算最后真实状态的 TD residual；用单独的连续性 mask 阻断跨回合递推。n-step 遇终止后尾项归零；遇截断时从最后真实状态取尾值，并用实际累积步数的 γ 幂。rollout 因批大小结束但环境未 reset 时，价值可 bootstrap，RNN 状态通常继续保留。



```text
# 概念伪代码：先把 autoreset 返回值恢复成每条真实 transition
delta[t] = reward[t] + gamma * (1 - terminated[t]) * V(real_next_obs[t]) - V(obs[t])
continues[t] = same_episode(t, t + 1) and next_transition_is_in_rollout(t)
adv[t] = delta[t] + gamma * lam * continues[t] * adv[t + 1]
# rollout 末端 adv 的递推尾项为 0；delta 内仍包含允许的价值 bootstrap。
# 独立 episodic 目标且无跨回合记忆权限时，reset 清 hidden state；仅 batch 切分时保留。
# meta-RL/持续世界重生是否保留状态，按其明确的上层任务边界决定。
```



Gymnasium v1.1 起支持 next-step、same-step、disabled 三种 autoreset；当前 same-step 示例把真实末状态放在 `info["final_obs"]`，较早版本使用过 `final_observation`。必须固定版本并读取 `metadata["autoreset_mode"]`：same-step 防止把 reset 观察存成 s′，next-step 防止把只负责 reset 的调用当成有效训练 transition。用两个长度不同的子环境验证向量化批次与串行轨迹一致。[\[A10 官方接口说明\]](https://farama.org/Vector-Autoreset-Mode)



<a id="alg-family"></a>

### 4. 每个算法族必须有自己的诊断仪表



- **DQN / Double DQN / Rainbow：**关闭探索、冻结网络，逐项比对 target；Double DQN 应由在线网络选动作、target 网络评价。检查 target 更新频率按环境步还是梯度步计数，且 target 不参与反向传播。分布价值（distributional RL）检查投影后概率和为1、端点与单原子边界；PER 检查抽样频率、重要性权重及重复索引更新；多步回报检查边界。逐组件删除消融之外，再做关键组件二因子实验，例如 n-step×replay ratio，否则组合效应会被归错。[\[A11 Rainbow\]](https://arxiv.org/abs/1710.02298)
- **PPO：**保存 rollout 当时的 old log-prob；第一轮未更新时 ratio 应近于1。手造正负 advantage，检查 clipped surrogate 的分支和梯度方向；actor 梯度计算须将 advantage 视为常量，old 行为策略概率固定；是否跨 epoch 重算 advantage 应明确规定并单独测试。记录 KL、clip fraction、熵、价值拟合与梯度范数。PPO clipping 不保证每个 ratio 或 KL 都被硬性限制，因此“所有 ratio 必须在区间内”不是正确测试。记录动作裁剪或变换前后哪个随机变量用于 log-prob。[\[A05\]](https://arxiv.org/pdf/2005.12729)
- **SAC / TD3：**SAC 检查 tanh 变换的密度雅可比、动作缩放、log-prob 对动作维求和、重参数化梯度以及熵项符号；自动温度调整要用“熵偏低时温度增加”的受控输入检查。检查 twin critics 是否意外共享全部参数或 target。TD3 分别开关 clipped double-Q、延迟 actor 更新、target smoothing；同步测真实 rollout return 与估计 Q 的偏差，而非仅比较最终分数。[\[A12 SAC\]](https://proceedings.mlr.press/v80/haarnoja18b.html) [\[A13 实现说明\]](https://spinningup.openai.com/en/latest/algorithms/sac.html) [\[A07\]](https://proceedings.mlr.press/v80/fujimoto18a.html)
- **Replay / normalization：**写入序列号与 episode ID，检验 n-step/序列不越过边界；独立冻结策略诊断的数据不进主训练 buffer，也不更新主归一化统计；在线持续评估中的合法适应照常进行，但不得使用未来数据或让诊断副本回流；恢复 checkpoint 必须包含优化器、target、归一化、随机状态和所需 buffer。容量与 replay ratio 是不同变量；分别扫描，记录样本年龄与每条数据使用次数。经验回放研究表明其效应依赖算法，因此不要把“容量更大”或“更新更多”写成一般规律。[\[A14\]](https://proceedings.mlr.press/v119/fedus20a.html)
- **Recurrent RL：**用有可控记忆长度的 POMDP 检查 hidden state 的重置、传递、detach、burn-in 与 padding mask。批内置换序列后答案应随序列一起置换；一次完整前向与分段前向在相同参数、连续 hidden state 下应一致。旧 replay hidden state 与新网络可能不一致，需测存储状态、零状态加 burn-in 等方案；R2D2 的直接启示是监测参数滞后与状态陈旧。[\[A15\]](https://willdabney.com/publication/r2d2/)
- **Model-based RL：**分离动力学拟合、模型使用与最终控制：比较真实模型、学习模型、无模型三条路径，扫描 rollout 长度和每步规划预算；在当前策略访问分布上评估多步预测、终止预测和回报偏差。漂亮的重建图与低一步 MSE 不保证模型能支持规划。MBPO 对短模型 rollout 的研究提供一种可验证机制，而非“短 rollout 总优”的定律。[\[A16\]](https://proceedings.neurips.cc/paper/2019/hash/5faf461eff3099671ad63c6f3f094f7f-Abstract.html)



<a id="alg-fairness"></a>

### 5. 公平比较要回答三种不同问题



**机制比较：**共享实现，只改变目标机制；保持网络、wrapper、数据、优化器设置相同，并允许说明必要差异。**最佳算法比较：**给各方法同等且公开的调参预算，允许各自合理配置；不要只精调新方法。**资源比较：**分别给出固定真实交互量和固定总算力的结果。报告环境步、原始帧、梯度更新、batch size、数据复用、模型生成步、推理规划预算、墙钟时间及硬件；相同环境步不代表相同计算。Henderson 等提醒深度 RL 对随机性和实现选择敏感；据此应保留每个训练种子和失败运行，而不是把一次最佳 checkpoint 当算法水平。[\[A17\]](https://arxiv.org/abs/1709.06560)

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#alg-deep)。 入口：[testing](../docs/testing.md) · [deep-validation](../docs/deep-validation.md) · [extension-guide](../docs/extension-guide.md)

<a id="alg-benchmarks"></a>


## 16 · 基准选择：让任务集合对应想要验证的能力



| 基准 | 适用问题 | 必须固定的协议 | 不能单独支撑的结论 |
| --- | --- | --- | --- |
| 可解 MDP / bsuite [\[A18\]](https://github.com/google-deepmind/bsuite) | 探索、记忆、泛化等可分解能力及机制反例 | 任务参数、难度、种子与能力分项 | 小任务通过不代表视觉控制或部署可靠 |
| ALE / Atari [\[A19\]](https://arxiv.org/abs/1709.06009) | 视觉离散控制、多游戏适用性 | sticky action 概率、frameskip、原始帧预算、life loss、起始方式、奖励裁剪和评估终止 | 确定性轨迹记忆不等于鲁棒决策；不同协议的榜单不可直接拼接 |
| Procgen [\[A20\]](https://proceedings.mlr.press/v119/cobbe20a.html) | 训练关卡到未见关卡的程序化泛化 | train/test level seeds、训练关卡数、难度、视觉输入与模型容量 | 同一生成器的未见关卡不等于任意分布外泛化，也不自动是持续学习 |
| DM Control [\[A21\]](https://arxiv.org/abs/1801.00690) | 连续控制、状态或像素输入、动力学学习 | 物理引擎、task 版本、control timestep、action repeat、观察形式和时域 | 仿真稳定和高回报不保证真实机器人安全或跨动力学迁移 |
| D4RL / Minari [\[A22\]](https://arxiv.org/abs/2004.07219) [\[A23\]](https://minari.farama.org/datasets/D4RL/index.html) | 固定数据、混合行为与覆盖不足下的离线学习 | dataset ID、版本/哈希、超时标签、轨迹划分、归一化分数参考值；迁移数据重新核对 | 标准化分数不等于真实风险；不同数据版本或环境迁移不能视为相同试验 |




建议每项主张配置一个可解例子、一个针对性压力测试、一个外部任务族。任务集应包含预期有效、预期无效及可能变差的条件；任务选择在观察主要结果之前确定。禁止把“在固定任务不断重启训练”改名为持续强化学习；后者需独立的状态保留和时间协议。



<a id="alg-offline"></a>

### 6. 离线学习与 OPE：评估权限是问题定义的一部分



固定数据协议必须公开：能否调用模拟器选超参数、能否使用额外演示、奖励标签或在线微调。若使用环境回报筛选模型，应报告该交互预算；这与只凭离线数据选择部署策略的难度不同。划分优先以整条轨迹、采集主体或时间块为单位，避免相邻 transition 泄漏；拟合预处理、行为模型和 OPE nuisance models 的数据边界也要记录。



在可解 MDP 上，把真实策略值作为 OPE 真值，联合比较 IS/WIS、模型法或 FQE、doubly robust；覆盖从充分到不足，策略偏离从小到大，时域从短到长。记录偏差、RMSE、置信区间覆盖率与策略排序错误；权重有效样本量 ESS=(Σw)²/Σw² 只是诊断，不能证明支持充分或区间校准。Doubly robust 的性质依赖其假设，不能理解为任意两个错误模型相加仍可信。[\[A24 Jiang–Li\]](https://proceedings.mlr.press/v48/jiang16.html)



当目标策略在行为数据零支持区域选动作时，单靠该数据通常无法识别其真实回报；报告“不可识别/证据不足”，不要凭低 Bellman loss 补出部署保证。真实部署还需要符合具体应用的风险约束、干预成本与监控方案；离线榜单和 OPE 分数只能提供其中部分证据。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#alg-benchmarks)。 入口：[catalog](../docs/catalog.md) · [extension-guide](../docs/extension-guide.md) · [external-adapters](../docs/external-adapters.md)

<a id="alg-test-matrix"></a>


## 17 · 可复制测试矩阵：通过条件与证据边界一起写



以下容差仅为建议起点。确定性 FP64 代数测试可从绝对误差 10⁻¹⁰、相对误差 10⁻⁸ 起步，再按条件数、规模和精度设定；随机测试应事先固定样本量与误差判据，不能运行到碰巧通过为止。



| 目的 | 最小问题 | 方法 | 通过判据 | 不能证明什么 |
| --- | --- | --- | --- | --- |
| 单步更新正确 | 两状态两动作，固定 transition | 独立标量手算；记录更新前后全部状态 | 参数增量及辅助变量逐项一致 | 长程稳定和回报收益 |
| 目标真值匹配 | 5–20 状态 MRP | 线性求解、DP 与采样学习分离 | 残差及目标误差按预定预算下降；允许常数步长误差地板 | 非线性控制的收敛 |
| 采样估计正确 | 可枚举行为与目标策略 | 精确求和与多次独立采样均值对照 | 差异在预设 Monte Carlo 误差范围；无系统漂移 | 小方差、良好覆盖或控制有效 |
| 梯度正确 | 小软最大策略、固定 batch | 自动微分、中心差分、多个 ε；固定随机噪声 | 避开不可微点后相对误差符合精度；冻结量一致 | 半梯度等于完整目标梯度 |
| 轨迹等价 | 含重复特征的短 episode | true-online 与对应 forward view | 每一步 w 与预测一致 | 新算法优于传统 TD |
| 边界语义 | 真正终止、外部截断、批末切分、向量 reset 各一例 | 手算 n-step/GAE，逐 transition 审计 | 尾值来自真实末状态，递推不跨 reset | 高维感知正确 |
| 反例保真 | Baird 与充分覆盖的稳定问题成对 | 原协议重现并扫描步长 | 已知失效机制出现；稳定算法按其条件表现 | 普遍稳定性定理 |
| 记忆可用 | 延迟线索 POMDP | 打乱 history、消融 hidden、扫描延迟 | 完整记忆能用线索，移除线索/历史后按预期退化 | 长时域通用智能 |
| 归因可信 | 简化环境+外部任务族 | 机制开关、二因子交互、资源匹配 | 主要预测方向与指标一致；负结果如实保留 | 未测试任务上的因果普遍性 |
| 复现完整 | 短运行中途保存/恢复 | 连续运行与恢复后轨迹对照；独立机器复跑 | 确定性配置逐步一致；非确定性配置统计结果相容 | 部署性能或算法优越性 |




<a id="alg-recipe-one"></a>

### 配方 A：一个新的 TD / trace / 步长算法如何进入正式实验



1. **登记主张：**写明要改善的是预测速度、稳定范围、跟踪误差还是资源消耗；固定目标值、时间预算、特征和采样分布。不要把四种目标混成“更好”。
2. **验证实现：**通过单步、λ=0、采样期望和有限路径测试；若含 meta-gradient，对完整计算图做有限差分，并另测截断近似的偏差。保留零步长、固定步长与 oracle 辅助量控制。
3. **先导诊断：**开发集使用随机 MRP、Random Walk、非二值特征和 Baird。扫描步长×trace 参数，画误差与发散区域；由先导方差决定正式重复数及最小关注效应，而非固定迷信“5个seed”。
4. **锁定算法与超参后验证：**在未参与调参的 MRP 参数/种子上比较，增加非平稳奖励或转移变化检验跟踪；分别报告早期误差、稳态误差、变化后恢复、计算和内存。
5. **升级门槛：**实现正确但性能无优势仍是有效结果；只有预设性能证据成立后才扩大任务。局部等价或反例修复只能支撑相应机制主张。



<a id="alg-recipe-two"></a>

### 配方 B：一个新的深度 actor–critic 组件如何排除伪增益



1. **冻结基线：**选择有版本记录的 PPO、SAC 或 TD3；用同一环境 wrapper 与日志定义复现合理性能范围，不能要求精确命中论文一个数字。
2. **分解假设：**例如“降低 Q 过估计会提高回报”，同时登记 Q 偏差、critic误差、策略动作分布和任务回报；用真值可估计的小连续控制问题先检查中间环节。
3. **建立四组：**基线、新组件、仅增加相同计算量、关键机制打乱/关闭控制；必要时加组件×归一化或组件×replay ratio 的交互。无效控制也要检查其是否改变目标或数据分布。
4. **三轴比较：**在同交互、同计算、同调参预算下分别评价；开发任务选配置，留出任务/种子验证。像素版与状态版、短与长时域各承担一个明确外推问题。
5. **发布证据：**逐运行曲线、失败率、最终固定窗口结果、学习面积及区间；提供完整配置、依赖版本、数据和 checkpoint 元信息。收益若只在一个 wrapper、奖励缩放或预算下存在，应将条件写入结论。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#alg-test-matrix)。 入口：[testing](../docs/testing.md) · [algorithm-design](../docs/algorithm-design.md) · [iteration](../docs/iteration.md)

<a id="crl-framing"></a>


## 18 · 持续强化学习：把整个生命期作为实验对象



持续强化学习的核心问题是：一个资源有限的智能体，在不断行动、承担探索代价并改变自身经验分布的过程中，能否持续获得收益、保留有用知识并学会新东西？实验对象应包括策略、价值函数、状态构造、优化器、记忆以及它们的更新规则。只比较若干训练终点的冻结策略，回答不了这个问题。



[Alberta Plan（2022，固定原版）](https://arxiv.org/pdf/2208.11173v1)把有限计算下的持续感知、行动与在线奖励最大化作为研究方向，并主张从能隔离核心困难的简单问题逐步构造系统；它是研究路线，不是算法有效性的证据。[Abel 等（NeurIPS 2023）](https://arxiv.org/abs/2307.11046)则把持续学习形式化为不会停止的隐式搜索，并讨论最优智能体仍必须继续学习的情形。这给实验提出一个要求：说明为何持续学习在当前问题中有用，而不能仅凭训练时间长或环境名字带“continual”完成论证。



| 术语 | 实验中必须说明什么 | 不能自动推出什么 |
| --- | --- | --- |
| Continuing，无限时域 | 没有任务自然终点，奖励随时间累计；死亡、重生与恢复属于世界动力学还是人为重置？ | 稳定环境可能存在足够好的固定策略；无限时域不必然要求参数永远更新。 |
| Continual，持续学习 | 何种变化或容量限制使持续适应有价值；哪些知识随生命期保留？ | 有限实验不能证明所有最佳智能体永远必须学习，只能检验有限时域假设。 |
| Streaming，流式更新 | 本手册严格轨道：单条经验流，当前转移到达后更新，不保存原始历史样本供再次训练；允许固定大小的递归状态与资格迹。 | 无 replay 不等于无 episodic reset；固定内存也不等于无 replay。 |
| Nonstationary，非平稳 | 奖励、转移、观测映射、对手策略中究竟哪一项变化；变化对谁可见？ | 观测分布变化不一定意味着完整状态上的转移核随时间变化。 |
| Sequential / multi-task | 任务依次还是混合出现；身份、边界、任务数是否给定？ | 任务序列是持续学习的一类实验，不能代表全部无边界交互。 |
| Partially observable | 缺失信息能否通过历史推断；记忆长度、隐藏状态与历史访问权限。 | 部分可观测本身不证明参数学习不可停止；固定的递归策略仍可利用记忆。 |




建议将“严格单流、无外部重置、固定学习器资源”作为一条明确命名的研究轨道，而不是强加给所有持续学习论文的唯一合法定义。任务增量、有限 replay、扩展网络、并行采样也可以研究，但结论必须携带这些条件。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-framing)。 入口：[continual](../docs/continual.md) · [navigation-map](../docs/navigation-map.md) · [continual-project-playbooks](../docs/continual-project-playbooks.md)

<a id="crl-objectives"></a>


## 19 · 目标、时间与被比较的系统



令环境完整状态为 X<sub>t</sub>，观测为 O<sub>t</sub>，智能体递归状态为 Z<sub>t</sub>，所有可学习参数与统计量为 Θ<sub>t</sub>。建议把接口写为：



```text
Z_{t} = f_{Θₜ}(Z_{t−1}, O_{t}, A_{t−1}, R_{t})；A_{t} ∼ π_{Θₜ}(· | Z_{t})；Θ_{t+1} = U(Θ_{t}, Z_{t}, A_{t}, R_{t+1}, O_{t+1})。
```



这里的 Θ 不仅是神经网络权重，还包括步长状态、动量、目标网络、奖励和观测归一化、神经元效用、任务推断器、模型与记忆索引。只保存权重的 checkpoint 通常不能恢复同一个持续学习器。



本手册建议以有限生命期真实获得的未裁剪奖励为主要 estimand：



```text
J_{T}(A) = E[Σ_{t=0}^{T−1} R_{t+1}]；ρ̂_{T} = (1/T) Σ_{t=0}^{T−1} R_{t+1}；ρ̂_{w}(t) = (1/w) Σ_{u=t−w+1}^{t} R_{u}。
```



预注册一个主要时域 T，辅以多个递增时域的累计收益和分段奖励率。滚动曲线用于定位退化，不能把高度相关窗口当独立样本。若目标是长期平均奖励，可写 ρ(A)=liminf<sub>T→∞</sub>E\[ΣR\]/T；有限试验只能估计有限时域代理。若使用折扣目标，应解释 γ 对有效关注时域的影响，并区分“算法内部用折扣 critic”与“部署目标按整个生命期奖励率计分”。不因算法实现方便而更换问题目标。



同时计入动作决策延迟、学习耗时、环境交互步数和墙钟时间。环境会在计算期间继续变化时，等待更新本身也是行动后果；仿真暂停等待 learner 的实验不能直接支持实时控制结论。模型规划步、离线预训练、试错搜索、人工调参、诊断评估均分别记账，报告其是否包含在部署资源上限内。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-objectives)。 入口：[continual](../docs/continual.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="crl-nonstationarity"></a>


## 20 · 先辨明变化来源，再设计对照



[Khetarpal、Riemer、Rish、Precup（JAIR 2022）](https://jair.org/index.php/jair/article/view/13673)以非平稳性的范围和来源组织持续 RL 的形式化、方法与评估，为下面区分环境变化与学习者数据分布变化提供综述入口；具体测试规则仍是本手册的综合建议。



外生变化是实验者或外界改变奖励、摩擦、观测映射或对手策略；可以预先生成变化日程并隐藏于 agent。内生变化来自策略学习、探索、物体消耗、控制对象生长或与其他实体互动，后续经验取决于此前行为。完整状态中的稳定规则也可能产生学习器看来不断变化的数据。将两者都称为“非平稳”时，须注明所指层次。



推荐用三种分离实验：固定数据流的预测试验隔离更新机制；固定环境但允许策略变化的控制试验检验自诱导分布漂移；加入独立外生变化日程的试验检验跟踪与恢复。固定数据流上的优势只支持预测或优化机制，不自动支持闭环控制收益。相同 seed 也不保证两个 agent 看到相同数据，因为不同动作会改变世界；能够配对的是初始化、外生随机过程或任务顺序，不是凭空相同的整条轨迹。



外生变化至少覆盖突然切换、缓慢漂移、复现旧情境及新情境；变化频率、幅度、周期可预测性与观测可见性应分开操纵。固定周期可能被时钟或递归状态识别；若声称适应“未知变化”，测试中应使用未见过的间隔或幅度，并检查输入是否泄漏了 task ID、边界标记、重置信号和计步器。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-nonstationarity)。 入口：[continual](../docs/continual.md) · [continual-project-playbooks](../docs/continual-project-playbooks.md) · [testing](../docs/testing.md)

<a id="crl-benchmarks"></a>


## 21 · 基准选择：原始协议与建议变体必须分开



| 来源及原始设定 | 适合回答的问题 | 解释边界与建议补充 |
| --- | --- | --- |
| [Continual World，2021](https://papers.nips.cc/paper/2021/file/ef8446f35513a8d6aa2308357a268a7e-Paper.pdf)：Meta-World 操纵任务；CW20 是 CW10 顺序重复两遍，每段 1M 交互步；原协议使用任务边界与独立输出头。[代码](https://github.com/awarelab/continual_world) | 受控任务序列中的保留、重学、前向迁移；低维状态下较易进行机制实验。 | 不是无任务身份的单一世界，也不是连续漂移基准。隐藏边界、共享头或更换 Meta-World 版本都是新变体，须单独命名并重新建立基线。 |
| [COOM，NeurIPS 2023](https://github.com/TTomilin/COOM)：ViZDoom 上的视觉任务序列；官方明确定位 task-incremental，任务边界清楚，含 8 类场景。 | 具身第一人称视觉下的遗忘与迁移，以及存储开销。 | 保留原版任务、纹理、动作映射和评测脚本；不得把任务增量结果写成 task-free 成果。全历史记忆可作诊断，但增长内存的优势应单列。 |
| [Jelly Bean World，ICLR 2020](https://arxiv.org/abs/2002.06306)：可配置、非 episodic 的程序生成网格世界，支持局部视觉与气味等感知。[代码](https://github.com/eaplatanios/jelly-bean-world) | 空间探索、历史依赖与永续交互。 | 论文提供的是可构造不同问题的 testbed。具体奖励日程、物品分布及感知模式才定义实验；监测地图探索带来的环境内存增长。 |
| [Forager，RLJ 2026](https://rlj.cs.umass.edu/2026/papers/Paper39.pdf)：有限环面、可变视野与可配置物体/奖励；环境内存不随生命期无限增长。[原始实现](https://github.com/andnp/forager) | 低成本隔离部分可观测、状态构造与持续适应。 | 有限环面不能称作真正无限地图；环境固定内存也不保证 learner 固定内存。官方 start()/step() 接口没有终止信号，Gym 适配不能偷偷添加周期 reset。 |
| [AgarCL，2025／2026-v3](https://arxiv.org/html/2505.18347v3)：非 episodic、局部像素观察与混合动作；质量改变速度和视野；被吞噬后重生而世界继续；当前其他细胞由手工策略控制。[基线代码](https://github.com/AgarCL/AgarCL-Benchmark) | 复杂交互下的持续控制与探索，以及学习器所经历的内生变化。 | 不是多个智能体同时学习的实验。区分 episodic mini-games、continual mini-games、完整默认世界及增密简化世界；不能互换其成绩。 |




两项证据提醒我们不要把持续学习缩成“保护旧权重”：[Forager 的受控实验](https://arxiv.org/html/2605.01131v1)强调状态构造的作用；[AgarCL v3](https://arxiv.org/html/2505.18347v3)在所测设置中发现仅加入 Shrink and Perturb、ReDo 或 Continual Backprop 的改善有限。两者都不证明这些方法在其他条件下无效，而是说明可塑性、记忆、探索和控制必须分开检查。版本注：Forager 早期文本中关于 AgarCL 尚未测试持续学习方法的表述，不能覆盖 AgarCL 2026-08 的更新。



奖励审计尤其重要。例如，如果某配置严格使用质量差 R<sub>t</sub>=m<sub>t</sub>−m<sub>t−1</sub>，则总和会望远镜消去为末质量减初质量；任意固定或随机停止时刻，只要每步都是该差值，等式仍成立；只有额外补偿、裁剪、另行定义的死亡/终止奖励，或未计入的重生质量跳变等才可能改变账本。应对所固定的 AgarCL 实现逐项验证奖励账本，不仅抄论文中的简写，也不能直接将质量、累计回报与长期增长率互称。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-benchmarks)。 入口：[catalog](../docs/catalog.md) · [continual](../docs/continual.md) · [external-adapters](../docs/external-adapters.md)

<a id="crl-evaluation"></a>


## 22 · 在线主评估，冻结与回访作为诊断



本手册推荐 prequential 主评估：用更新前可获得的信息选择动作，环境返回结果，先记录真实收益，再进行由该信息触发的学习。奖励来自实际行为策略，探索损失包含其中。预测任务则先给预测、后接收目标并计算误差，再更新；如果目标依赖未来，应把评分时点和目标可用时点分开记录。不得用未来完整轨迹提前归一化当前输入。



1. **主生命期不中断。**从出生到 T 只初始化一次世界与 agent；日志按预注册窗口汇总，人工恢复、进程崩溃、死亡和资源超限全部留下事件记录。世界自然重生与人为重置分开统计。
2. **冻结诊断从副本开始。**在预定 t<sub>f</sub>复制 agent 与可复制的世界状态，比较继续学习和冻结参数的未来轨迹。冻结网络权重时，通常仍允许递归状态按新观察演化；另外做“所有适应统计均冻结”变体，以识别归一化或记忆自身带来的适应。明确停止了哪类更新。
3. **不可复制就使用独立、匹配的生命期。**不要在真实在线世界交替开启/关闭学习后，把两个不同历史段当同一起点反事实。可报告这样的干预，但必须承认顺序混杂。
4. **旧任务回访矩阵单列。**若仿真支持独立评测环境，记录任务 i 训练后在任务 j 的无学习得分 P<sub>i,j</sub>。这些副环境的交互不能回灌主 learner，也不能让其改变主 RNG、归一化统计、hidden state 或 buffer。
5. **无可复现旧任务时承认不可辨识。**单条真实世界轨迹不能直接测全部过去任务的遗忘。可用自然复现情境的恢复曲线、固定诊断集上的预测误差或限定分布的行为探针，但不得将其冒充完整遗忘矩阵。



冻结以后变差支持“在该分支时段继续适应有益”，不证明参数更新永远必要。冻结不变差可能意味着已学得稳健策略、环境不再挑战它、测试时段太短或策略原本就失败。先确保学习器达到非平凡水平，再做冻结检验；否则“冻结没有影响”常常只说明没学会。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-evaluation)。 入口：[continual](../docs/continual.md) · [testing](../docs/testing.md) · [external-adapters](../docs/external-adapters.md)

<a id="crl-metrics"></a>


## 23 · 把收益、保留、可塑性与资源分别量化



| 指标 | 建议定义 | 主要陷阱 |
| --- | --- | --- |
| 生命期收益 | 累计真实奖励与按等长时间段的奖励率；另报末段、最低段及失败概率。 | 总均值可能掩盖晚年崩溃；末段均值可能隐藏漫长探索成本。 |
| 遗忘 | 在任务可回访时 F<sub>j</sub>=P<sub>j,j</sub>−P<sub>K,j</sub>；另报峰值到终点版本时要换名并说明。 | 从未学好的任务可有“零遗忘”；峰值估计有选择偏差；不同任务奖励必须有明确尺度。 |
| 后向迁移 | BWT=(1/(K−1))Σ<sub>j&lt;K</sub>(P<sub>K,j</sub>−P<sub>j,j</sub>)。 | 与上述遗忘定义符号相反；不能一边用峰值遗忘一边宣称严格互为相反数。 |
| 前向迁移 | 在任务 i 的等预算适应区间，以 ΔAUC<sub>i</sub>=AUC<sub>history,i</sub>−AUC<sub>fresh,i</sub> 对比从零学习。 | 零样本进入成绩与学习速度是两个量；fresh 必须匹配架构、预算和初始环境条件。 |
| 恢复时间 | 变化后首次达到预注册阈值并连续保持 L 个窗口的延迟；固定窗口宽、步长及记首次达标还是确认时刻。观察期结束仍未恢复记右删失；同时报截止 H 的恢复率。 | 不能丢弃未恢复运行再算平均。崩溃/资源耗尽应列失败或竞争事件，不自动视为非信息性删失；新情境最优值变化时，不能直接用旧分数作阈值。 |
| 可塑性 | 不同年龄 checkpoint 面对匹配新挑战的适应曲线，相对 fresh 的 ΔAUC、学习斜率与最终可达表现。 | 不是旧任务记忆；探针任务太容易或只训练输出层，无法代表整体可塑性。 |
| 表示诊断 | 固定探针与当前访问分布分别测 dormant 比例、有效秩、激活/权重/梯度范数、TD 误差及更新幅度。 | 秩高、神经元活跃或误差小都是机制线索；不是行为收益证据，且受采样分布影响。 |
| 资源与持续性 | 参数、优化器、迹、hidden state、replay、模型、任务掩码总字节；每步耗时分位数；OOM/NaN/停机率；内存对时间斜率。 | 仅固定网络参数不能说明固定总内存；只报平均吞吐会隐藏长尾动作延迟。 |




上表是统一报告建议。若复现 [Continual World](https://papers.nips.cc/paper/2021/file/ef8446f35513a8d6aa2308357a268a7e-Paper.pdf)，还应保留其原始前向迁移归一化定义 (AUC−AUC<sub>fresh</sub>)/(1−AUC<sub>fresh</sub>)，并注明它基于成功率；分母近零时不稳定，不宜直接推广到任意奖励。



统计独立单位是完整 lifetime，而不是每个窗口、任务段、episode 或神经元。种子同时影响初始化、探索和环境生成；若外生日程作为独立随机因素，应跨日程和运行分层汇总。先用探索性 pilot 估计预注册主指标差值的方差和最小有意义差异，再确定确认实验的运行数。不存在所有持续 RL 都适用的“5／10／30 个 seed”。不能事后只给赢家增加运行数，也不能把同一 checkpoint 分出的多条副本当新的独立训练运行。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-metrics)。 入口：[continual](../docs/continual.md) · [continual-project-playbooks](../docs/continual-project-playbooks.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="crl-controls"></a>


## 24 · 机制归因对照：每个对照回答一个问题



| 对照 | 可解释问题 | 必须匹配与声明 |
| --- | --- | --- |
| Fresh | 老 learner 对新挑战是否比未学习过的同架构 learner 更能学？ | 相同新挑战起点或匹配起点分布；新数据预算相等；fresh 的初始化、buffer 和归一化状态重新开始。 |
| Reset | 具体旧状态是否妨碍学习？ | 分别重置优化器、输出头、全部权重、buffer，避免一次清空所有状态后把收益归给单一机制。环境不随网络 reset 自动重置。 |
| Frozen | 继续更新在此后是否有价值？ | 相同分支点；权重冻结、统计冻结、状态冻结分别命名；保留固定 recurrent policy 的正常状态演化。 |
| Oracle | 当前观测、记忆、探索或目标推断中哪一项构成瓶颈？ | 逐项加入完整状态、真实任务身份或规划模型。称作特权诊断；只有参照值具有经证明的上界保证（例如同条件下的最优值）才称上界。 |
| Task-aware | 任务身份与边界提供多少帮助？ | 把已知边界、已知身份、二者均知分开；不能把有特权方法放在无标签公平排名中。 |
| Replay | 改进来自经验保留还是更新结构？ | 固定字节容量、采样分布、更新次数和数据年龄；全历史 replay 是增长资源诊断，不能归入严格 streaming 轨道。 |
| 随机替换／等量扰动 | 按效用选择特征是否优于单纯注入新随机性？ | 相同替换数、成熟期、计算量；明确入边、出边和相关优化器状态的处理。 |
| 状态构造 | 性能不足是否源于观测别名和记忆不足？ | 前馈、history stack、递归结构、特权全状态逐层比较；同时报告参数与每步计算两种预算。 |




[Abbas 等（2023）](https://proceedings.mlr.press/v232/abbas23a/abbas23a.pdf)用循环 Atari 和重置 learner 的参照检验重学能力，说明“保留旧知识”与“仍能学回去”不同；其 CReLU 实验也处理了激活维度与参数容量的差异。[Dohare 等（Nature 2024）](https://www.nature.com/articles/s41586-024-07711-7)的 Continual Backprop 持续替换低效用单元；原 RL 实验同时使用 L2，复现时不能省去这一条件。[ReDo（ICML 2023）](https://proceedings.mlr.press/v202/sokar23a.html)针对 dormant 神经元循环再利用。三者提供可测试机制，而不是“激活更健康就必然回报更高”的通用定理。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-controls)。 入口：[continual-project-playbooks](../docs/continual-project-playbooks.md) · [algorithm-design](../docs/algorithm-design.md) · [testing](../docs/testing.md)

<a id="crl-tuning"></a>


## 25 · 生命期调参与版本约束



[Mesbahi 等（ICML 2025）](https://proceedings.mlr.press/v267/mesbahi25a.html)指出，用部署全生命期表现挑超参数会削弱持续学习研究所要检验的未知未来假设。其工作延续了 [K-percent evaluation](https://arxiv.org/abs/2404.02113)：限制可用于选择超参数的早期数据。其百分比是实验协议参数，不是通用正确常数。



建议将可接触的数据分成开发生命期、选择期和锁定后的确认生命期。搜索器只能读取允许时间段的指标；晚期成绩不能用于调步长、选归一化、换模型大小、决定哪个 checkpoint 对外发布。若允许在线 meta-learning，它应作为算法的一部分，只根据过去信息行动，自己的状态与计算也计入预算。用待评分的同一部署生命期后缀挑配置，是使用测试未来的诊断，不能与受限选择协议混为一个排名。若完整时域调参发生在独立开发生命期，随后测试封存的新生命期，则可以是有效泛化协议；它使用更丰富的开发信息，应与严格前缀选择轨道分开，但不自动等于未来泄漏。



还要防止“论文标题相同，算法已变”：[Streaming Deep RL 2024-v1](https://arxiv.org/html/2410.14606v1)的 stream-x 使用 ObGD 等组件；[2026-09-21 的 v3](https://arxiv.org/html/2410.14606v3)引入逐坐标 StreamingOptimizer 并扩展评测。其更新形式为 v<sub>t</sub>=max(βv<sub>t−1</sub>,|u<sub>t</sub>|)，Δθ<sub>t</sub>=αu<sub>t</sub>/(v<sub>t</sub>+ε)，对有限增量有逐坐标幅度界。更新有界不证明累计参数、价值函数或回报稳定；无 replay 的成功也不自动证明无限生命期有效。使用[作者代码](https://github.com/mohmdelsayed/streaming-drl)时固定分支、commit 和论文版本，分别标记旧版复现与新版比较。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-tuning)。 入口：[continual](../docs/continual.md) · [statistics](../docs/statistics.md) · [iteration](../docs/iteration.md)

<a id="crl-recipe-a"></a>


## 26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？



**研究假设。**在固定计算与记忆下，局部观测使部分失败源于状态别名；仅保持表示可塑性未必足够。预注册主要问题：递归状态与可塑性干预是否分别改善后期在线奖励率，二者是否存在交互作用。



**基准与操纵。**先复现所固定 Forager 版本的一个 switching 任务，保留其原始奖励、布局和观测设定，确认实现与论文趋势相容。随后另命名“手册建议变体”：同一地图做 2×2 条件——固定／隐藏变化奖励、较大／较小视野；日程由独立环境 RNG 生成。固定周期只用于开发，确认期使用事先封存的变化间隔分布。地图、日程和 seed 清单生成后锁定，不看结果再挑“有效”的变化。



**方法与对照。**在同一基算法上做前馈／递归 × 原始更新／一种可塑性干预四组。若用 CBP，保留其需要的 L2 条件并另做 L2 单独组；若用 ReDo，则做相同替换数量的随机替换组。配备随机策略、固定启发式、允许全局状态的特权参照，以及新挑战上的 fresh 和中期 frozen 分支。递归模型既给参数匹配结果，也给每步计算匹配结果；显式限制 history stack、BPTT 序列、replay 总字节。若要声称严格 streaming，选择不存原始历史样本的递归更新；含 BPTT 缓冲的组按有限缓存轨道报告。



**建议预算。**以下为本手册的起始方案，不是社区标准或论文原始配置：开发先跑 10<sup>5</sup> 步检查奖励与状态，再用 10<sup>6</sup> 步估计运行时间和主指标方差；确认生命期设为 10<sup>7</sup> 步，并预注册 1M、3M、10M 的分段结果。开发选择只允许读取前 10% 的指标；10% 仅是这个方案的取值，可在研究开始前根据用途调整。每种算法给相同的候选配置数与总开发交互预算，报告实际消耗。确认运行数由 pilot 方差、最小有意义改善和资源上限确定，整个矩阵同时执行；精度不足时如实报告。



**指标。**主指标为后 90% 生命期平均原始奖励；同时保留全生命期收益、变化后恢复曲线、最低窗口收益、按区域访问率、长期远离奖励区域的时间、诊断探针上的可塑性和内存/延迟曲线。按独立 lifetime 估计四组主效应与交互差的区间，不从成千上万个时间窗口虚增样本数。



**失败与证伪。**若优势仅在全状态可见时出现，不支持“解决记忆瓶颈”；若随机替换同样好，不支持特定效用选择机制；若扩大前馈模型后优势消失，只能主张给定资源下的优势；若晚期收益不升而 dormant 指标改善，行为主假设失败。若所有方法接近随机，先把探索、奖励频率或可学性做诊断，不能将整体失败直接归因于塑性丧失。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-recipe-a)。 入口：[continual-project-playbooks](../docs/continual-project-playbooks.md) · [continual](../docs/continual.md) · [prediction-abstraction-options](../docs/prediction-abstraction-options.md)

<a id="crl-recipe-b"></a>


## 27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？



**研究假设。**一种保护旧知识的算法可能降低遗忘，却降低新任务学习速度；应检验其在有限存储与计算预算下是否改善生命期总收益，而不只报告末尾平均成功率。



**基准与版本。**使用原版 CW20：CW10 重复两遍，每段 1M 步，合计 20M 步；固定 Meta-World、MuJoCo、任务顺序、输出头、每段处理规则和评测脚本。先在官方短任务三元组上开发，最后回到原版完整序列；另预注册若干任务顺序作为泛化测试，标为本手册扩展。视觉扩展可在 COOM 再测，但作为新的证据层，不能把不同基准的归一化分数直接拼成生命期奖励。



**方法与对照。**至少包含：顺序 fine-tuning、所研究的保留机制、同算法 fresh 单任务参照、固定容量 replay、已知身份多头版本；全历史 replay 与多任务同时训练作为资源／访问特权诊断。各方法拥有同等开发总预算。若保留机制需要 task boundary，而研究目标是无边界，应单独加上边界推断模块并核算其错误与开销，不直接借用真实边界。



**预算与执行。**20M 是原 CW20 的交互预算；以下是建议增加的审查设计：确认前锁定所有超参数与序列；每个任务段结束生成独立评测副本，回访全部已见任务并记录 P<sub>i,j</sub>；额外评测数据不进入训练。评测 episode 数按预定置信精度与预算上限选择，训练 lifetime 数按主差值方差选择，二者分开。开发规模、评测间隔、重复顺序数量属于本研究的预注册参数，不声称原论文要求。



**指标与证伪。**同时展示遗忘矩阵、第一次和第二次访问的 AUC、相对 fresh 的前向迁移、旧任务后向迁移、在线收益、任务头／掩码／buffer 内存及延迟。若遗忘下降但总收益和适应 AUC 下降，结论应为保留—适应权衡，不是全面更优；若第二次访问低于 fresh，需要区分输出头初始化、buffer 清空、探索状态和特征塑性。依次恢复这些组件做诊断，避免把整个 agent reset 后的改善归给“神经网络老化”。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-recipe-b)。 入口：[continual](../docs/continual.md) · [continual-project-playbooks](../docs/continual-project-playbooks.md) · [statistics](../docs/statistics.md)

<a id="crl-longrun"></a>


## 28 · 长期试验阶梯与最小交付包



建议按四级推进，且每一级都设置可停止的失败条件。一级用人工可核对的非平稳 bandit、小型 MDP 或预测流验证时序、迹、bootstrap、终止与归一化；二级用 Forager 等轻量环境分别增加部分可观测、变化、有限记忆；三级用 CW20／COOM 做跨任务保留与迁移；四级进入 AgarCL 完整世界或真实持续控制。四级失败不抹去前面已经支持的窄结论，也不能由一级成功直接宣布解决持续学习。



从短到长应延长同一个已锁定协议，而不是每延长一段就重新调参。可按 T、3T、10T 等几何阶梯暴露容量饱和与迟发退化；具体倍数是建议，不是理论保证。除环境步数外，按已经历的变化次数、旧情境复现次数与状态空间覆盖分层报告，防止“运行很久但没有遇到新问题”。正式确认前记录哪些失败会触发停止：数值非有限、资源超限、环境协议错误、不可恢复世界状态；算法失败应保留为结果，实施错误修复后应重新运行相关确认实验并公开修正。



AgarCL 建议先通过 episodic mini-game 的动作与奖励检查，再进入 continual mini-game，最后完整世界；这是一条本手册建议的开发阶梯。mini-game 可学而持续版本失败时，应检查偏离食物区域后的重新发现、观测尺度与生存行为，而不是默认增加训练步数即可解决。完整世界运行前先测实际吞吐与资源开销，避免用若干分钟 toy 试验的速度估计整个研究预算。



交付包至少应包含：论文/仓库版本与环境配置；任务或变化生成器及封存清单；所有方法与调参搜索空间；完整 learner state 的 checkpoint 定义；逐步计数与分段未裁剪奖励；每个 lifetime 的失败事件；主指标的每运行数值；评测副本与主轨迹隔离说明；所有资源账本；支持、未支持和未完成的假设清单。允许压缩日志，但不允许只保存好看的平滑曲线与最佳运行。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#crl-longrun)。 入口：[continual-project-playbooks](../docs/continual-project-playbooks.md) · [iteration](../docs/iteration.md) · [external-adapters](../docs/external-adapters.md)

<a id="ops-workflow"></a>


## 29 · 实验执行：从预注册到独立确认



本节给出可直接用于课题组的工作流程。探索阶段可以改变假设、代码与分析；确认阶段必须锁定这些选择。修改不是错误，隐藏修改才会使证据难以解释。开发中已反复查看的结果，不再是独立测试结果。



| 阶段 | 做什么 | 进入下一阶段的条件 | 保留的文件 |
| --- | --- | --- | --- |
| 问题与协议 | 定义主张、估计量、最小有意义效应、预算、任务分布与信息权限 | 任何成员均能说明什么结果会否定假设 | 预注册协议、任务清单、选择规则 |
| 环境与更新审计 | 手算轨迹、奖励/动作可视化、终止语义、参考实现、检查点恢复 | 明确的边界与数值测试通过；已知反例按预期失败 | 测试记录、依赖版本、最小复现 |
| 试点 | 估计运行成本、变异、失败模式，确认预算内可回答的问题 | 确定独立单位、样本量规划和正式资源上限 | 试点原始记录及与正式数据的隔离声明 |
| 探索性开发 | 调参、机制对照、负例与小规模消融 | 冻结算法、实现、超参选择过程和主分析 | 所有候选、搜索空间、开发任务使用记录 |
| 确认 | 新种子/隐藏任务或新生命周期；自动执行，预设失败处理 | 达到预设精度/样本计划，或如实报告预算不足 | 不可覆盖的 run manifest、原始事件、失败记录 |
| 解释与交付 | 重算图表，核查异质性、退化、资源成本和适用范围 | 每个结论能定位到表、图或测试；他人可以从原始结果重算 | 分析程序、环境锁定文件、结论—证据表 |




### 把环境、智能体与实验控制分离


[Tanner 与 Adam White 的 RL-Glue（JMLR 2009）](https://www.jmlr.org/papers/v10/tanner09a.html)通过最小化、跨语言接口促进环境和算法共享。今天采用什么框架可以不同，但实验控制器应独立掌管随机分配、预算、日志与评估；环境定义反馈，agent 根据允许的信息学习。避免把方法专属预处理藏进公共环境，也避免让环境直接读取算法内部状态改变难度。


### 不要让“自动化”自动制造偏差



作业队列应在查看结果之前生成；随机或分块交错运行方法，降低机器负载、环境版本或真实时间变化与方法标签的混杂。记录每个计划 run 的身份和终态。提前终止、NaN、OOM、环境故障都不能悄悄变成缺失值后被平均函数忽略。



将失败分为算法失败、预算超限、可独立归因的基础设施失败。基础设施重跑应保留原记录、重跑原因和关联 ID，并应用于所有方法。算法崩溃则按预注册的可解释规则进入主分析，同时单列失败率。任务回报无自然下界时，不能随意填零；可以预定义部署效用/失败代价，或给有界敏感性分析与条件于成功运行的辅助分析。不同做法回答不同问题。



### checkpoint 不只是网络权重



恢复状态可能包括优化器动量、目标网络、回放缓冲区及索引、归一化统计、探索/学习率日程、RNN 隐状态、资格迹、元学习状态、环境状态、任务调度器及各随机数流。做“连续运行 vs 中途保存后恢复”的短前缀对照；不支持环境精确恢复时明确实验边界，不声称逐步一致。



确定性执行帮助调试，但不能取代独立重复。硬件或并行归约导致位级差异时，保留依赖、设备与确定性选项，并用统计可复现性评价。相同 seed 数字也不保证两个算法经历相同随机事件；不同动作或调用顺序可能消费不同数量的随机数。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#ops-workflow)。 入口：[iteration](../docs/iteration.md) · [start-here](../docs/start-here.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="ops-diagnostics"></a>


## 30 · 诊断手册：症状、竞争解释与下一项实验



下面是本手册的排错建议。每项首先缩小问题范围，不保证某种修复必然有效。观察到健康指标变化，只能作为中间证据；最终仍要检验任务目标。



| 症状 | 优先排查 | 最小验证 | 容易误下的结论 |
| --- | --- | --- | --- |
| 回报始终等于随机策略 | 奖励触发、动作映射、梯度是否实际更新、探索能否到达奖励 | 手工策略/随机轨迹、参数差值、无噪声单步任务、稠密奖励诊断变体 | 直接认定网络容量不足 |
| loss 下降但控制没有改善 | 采样分布改变、自举目标移动、错奖励、critic 对 actor 常访问区域失真 | 固定状态集精确/MC 评估；同初始状态比较动作与实际结果 | 把更小 TD loss 当作更好策略 |
| Q 值暴涨 | 奖励尺度、γ、bootstrap mask、目标梯度、离策略覆盖、动作外推 | 折扣 γ&lt;1 时由奖励界检查值尺度；平均奖励差分值须另固定 offset；关闭自举/换同策略数据/固定目标逐项隔离 | 只加裁剪就说明理论问题解决 |
| 少数种子极好，其余失败 | 探索/初始化双峰、成功阈值、超参选择偏差 | 单次运行轨迹与分布、首次奖励时间、预设新种子确认 | 中位数掩盖灾难尾部，或展示最好种子 |
| PPO 训练后突然倒退 | 更新步数、KL、旧策略概率、优势/价值目标、动作概率密度 | 冻结 rollout 重算 ratio；初始 ratio≈1；逐 epoch 记录 KL 与回报诊断 | 认为裁剪天然保证单调改进 |
| 长回合比短回合差 | 信用距离、状态混淆、截断处理、RNN 重置、折扣目标 | 逐级增加延迟/长度，保持其他难度不变 | 把短回合成功当作长程信用问题已解 |
| 评估频率一改，训练曲线也变 | 共用 RNG、归一化更新、环境共享、评估数据回流、墙钟调度 | 有/无评估的训练前缀对照；哈希检查完整学习者状态 | 把评估当作天然无副作用操作 |
| 任务重现时学不会 | 遗忘、低可塑性、优化器状态、探索衰减、表征漂移 | 冻结测旧能力；重新学习曲线；仅重置优化器/仅重置部分参数的配对对照 | 把遗忘与可塑性损失当作同一现象 |
| 在线适应很强但耗时越来越长 | 回放/记忆/模型/搜索树增长及检索开销 | 总内存和决策延迟随生命长度的曲线；固定资源版本 | 有限任务列表表现好即满足终身资源约束 |
| 新方法只在一套代码上有效 | 实现交互、默认超参、隐藏预处理或任务选择 | 最小共同实现、第二实现、相同候选预算 | 把实现特定优势写成算法普遍优势 |




### 统一日志的四层



**任务层：**原始奖励、成功/失败、时间、约束、状态访问与变化事件。**学习层：**损失、价值/目标分布、梯度和更新范数、KL、熵、回放年龄、重要性权重及有效样本量。**持续性层：**学习年龄、重访/新任务表现、表示活动、预测误差、资源使用。**系统层：**环境步、agent 决策、原始帧、梯度步、批量、设备、墙钟、异常和版本。所有派生图都应能追溯到这些字段。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#ops-diagnostics)。 入口：[testing](../docs/testing.md) · [algorithm-design](../docs/algorithm-design.md) · [continual-project-playbooks](../docs/continual-project-playbooks.md)

<a id="ops-extensions"></a>


## 31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体



### 离线策略选择与 Data2Online 不是同一个问题



[Paine 等（2020）](https://arxiv.org/abs/2007.09055)关注仅凭离线数据选择训练好的策略；[Wang 等（TMLR 2022）](https://openreview.net/forum?id=AiOUi3440V)研究用 calibration model 选择随后要在线学习的算法配置。后一种对象是整条学习轨迹，而不是固定 π 的一次 OPE。



```text
λ̂ = arg max_{λ∈Λ} J_{model}(A_{λ})；
真正需要验证的是 J_{env}(A_{λ̂})，以及相对可达到配置的选择损失。
```



手册建议把数据按真实时间或主体分块：模型训练、选择验证、最终外推彼此区分。模型的单步预测误差、长滚动稳定性、超参排名保真和所选配置真实效用分别测量；某个指标改善不自动推出其余指标改善。对日志未覆盖动作的推断要明确外推假设，模拟器滚动次数不能冒充额外真实数据。



[Coblin、Wang、Martha White、Adam White（2026）](https://arxiv.org/html/2608.11349v1)把此路线用于水处理传感器 nexting，arXiv 页面标注已被 RLC 2026 接收。研究对象是被动预测，未展示智能体自主操纵工厂。长滚动与部分超参趋势有支持，但扩大数据后的泛化效果不一致；使用部署期样本挑起始状态属于 oracle-like 诊断。手册因此不把这项结果概括为“离线模型已解决真实控制调参”。



### 机器人与工业系统



[Dulac-Arnold 等（2019）](https://arxiv.org/abs/1904.12901)及其[后续实证研究](https://arxiv.org/abs/2003.11881)强调延迟、限制、非平稳等真实条件。对应的实验应逐个控制传感器噪声、动作延迟、执行频率、约束与人工介入，再组合压力测试。人工重置、示范采集、预训练数据、事故恢复和安全控制器都计入成本与能力归属。



对一个无法重置的真实系统，不能虚构大量独立 lifetime。可在时间块、设备或站点层面设计比较，考虑残留效应与环境变化；反复随机切换学习者可能破坏各自的学习史，普通 A/B 解释未必适用。无独立复制时，把结论限定为案例与时间序列证据，结合可控模拟实验验证机制。离线日志重放也无法评估本来未执行动作的真实后果。



### 多智能体



[Gorsane 等（NeurIPS 2022）](https://proceedings.neurips.cc/paper_files/paper/2022/hash/249f73e01f0a2bb6c8d971b565f159a7-Abstract-Conference.html)对合作 MARL 评估的分析支持完整报告与统一协议。其具体推荐服务于特定评价目标；例如给 on-policy 更多交互或选择最好 checkpoint，不能直接搬到“同交互预算”与“在线生命周期”问题。



一次联合训练产生相关的多个智能体，不能把队员当作独立种子。明确集中训练可见信息与分散执行权限，计数全队总环境交互、消息、计算与参数量。合作任务报告整体成功及个体差异；对抗/自博弈增加冻结对手池、交叉对战矩阵及对未见对手的泛化。循环克制存在时，单一 Elo 或自博弈胜率不能完整代表能力。对手同时学习造成的非平稳，应与外部环境漂移区分。



### 大模型、搜索与记忆型智能体



这里给出从上述原则推导的扩展协议，不声称是已统一的 LLM-RL 标准。先定义智能体边界：基座权重、上下文、长期记忆、技能库、检索器、规划器、外层代码或提示词优化各自何时改变。冻结网络但写入长期记忆的系统仍可能学习；仅增加同一任务内搜索量则不足以证明跨任务持续改进。



比较固定模型、固定模型+搜索、经验记忆、在线参数更新及组合；匹配可访问工具、环境交互、生成 token、推理时计算和持久存储。评价训练/适应流程时，以独立流程运行为外层、测试问题为内层；评价给定冻结模型的新任务表现时，独立抽取的任务或任务家族可作为统计单位，结论条件于该模型。分离训练/开发/确认任务，检查公开题目污染、奖励模型过优化和验证器漏洞。使用任务完成的外部验证，不能仅以自评、自报成功或代理奖励作为能力证据。



验证持续学习可安排：经验阶段 → 未见表面形式下的未来任务 → 规则变化后的纠错阶段。保留已学内容，再比较是否继续更新；清空记忆是机制消融，不能作为所有学习者都必须通过的判据。外层搜索了多少版本、人工修改多少轮，应与单个部署智能体自己的经验收益分开报告。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#ops-extensions)。 入口：[multi-agent](../docs/multi-agent.md) · [planning-and-architecture](../docs/planning-and-architecture.md) · [prediction-abstraction-options](../docs/prediction-abstraction-options.md)

<a id="ops-evidence"></a>


## 32 · 如何画图、写结论和判断证据够不够



下面不是要求每篇论文都产生十几张图，而是要求主张有对应证据。优先选择少而明确的主图，完整诊断与逐任务结果放附录。按 [Chan 等的可靠性视角](https://arxiv.org/abs/1912.05663)，训练期间风险与固定策略风险应分别讨论。



| 主张 | 最低限度的对应证据 | 仍不能推出 |
| --- | --- | --- |
| 实现正确 | 可解例子、更新恒等式/有限差分、边界测试、参考实现比较 | 学习有效、稳定或优于基线 |
| 样本效率更高 | 同交互定义及预算下的学习曲线和预定 AUC/阈值时间；完整失败记录 | 计算更省、总开发成本更低 |
| 总体性能更好 | 预定任务权重、差值区间、分布、逐任务结果和独立确认 | 每个任务都更好、任意未知环境更好 |
| 某机制带来提升 | 受控干预、机制量变化、匹配对照、预测的正例/负例 | 单张相关性散点图即可证明因果 |
| 更容易调参 | 公开搜索分布、相同调参预算、选择过程的独立重复、敏感性曲线 | 参数数量少就一定更容易 |
| 适应变化更快 | 匹配历史和变化条件，在线适应损失、恢复时间与未恢复比例 | 仅旧任务保持好即更可塑 |
| 持续学习能力增强 | 可复制环境的独立长生命，或明确受限的真实纵向证据；按主张报告未来收益、适应、保留/迁移及资源 | 一个有限序列已经代表无界终身学习 |
| 真实系统可部署 | 真实权限与成本下的独立结果、延迟/约束/人工干预记录 | 模拟分数或被动预测等于自主控制成功 |




### 建议的图组



1. **主目标图：**横轴明确为环境步/原始帧/秒；纵轴是预定主指标，标明实际 n、区间类型与平滑方式。
2. **运行分布图：**单次运行点、ECDF/性能剖面或分位数；在存在失败双峰时尤其必要。
3. **逐任务差异：**差值及区间，配聚合指标；不能只用胜场数忽略退化幅度。
4. **机制与消融：**中介量、交互项、简单替代方案和失败条件；图轴与主张直接对应。
5. **调参与成本：**搜索预算—所得性能、敏感性、计算/内存/延迟；持续任务另画生命周期资源曲线。



保留原始曲线；平滑窗口以环境时间定义，不能对不同速度方法用不同平滑强度。学习曲线每点区间不是整条曲线的同时置信带，也不能在每个时刻都做未校正显著性检验。多重比较与连续窥视应预先控制，或把分析标为探索性。



### 推荐结论写法



> 在预注册的任务集、信息权限与资源预算下，方法 A 相对基线 B 的主指标差异为 Δ，区间为 \[L,U\]。收益主要出现于……，在……条件下没有优势/存在退化。机制实验支持……，但尚不能区分……。结论仅覆盖本次配置选择与任务范围。



若区间横跨有意义的正负效应，写“现有证据不足以确定差异”，不要写“两者一样好”。需要等效或不劣结论时，预先定义容忍界限并设计相应分析。若测得统计差异但小于实际重要性阈值，应直接说明。优秀论文的标准是问题重要、证据清晰且可复核，不能由显著性、图像美观或一项基准排名代替。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#ops-evidence)。 入口：[statistics](../docs/statistics.md) · [iteration](../docs/iteration.md) · [testing](../docs/testing.md)

<a id="ops-checklist"></a>


## 33 · 课题组可直接使用的检查清单



勾选状态仅保存在当前浏览器；下方按钮可导出检查结果。它是执行辅助，不是研究质量评分器。未经适用性判断的“全部打勾”没有科学意义。



<a id="checklist"></a>

- [ ] 主张、主估计量、任务范围和反证条件已写清。

- [ ] 训练目标、评估目标、奖励变换与时间单位一致或已解释差异。

- [ ] 观测、任务标识、模型查询、预训练和特权信息已披露。

- [ ] 环境版本、包装器顺序、termination/truncation/autoreset 已核查。

- [ ] 更新、梯度、边界与检查点恢复通过有意义的测试。

- [ ] 基线实现可靠，搜索预算和配置来源完整。

- [ ] 开发、选择和确认数据/种子/生命周期的关系明确。

- [ ] 独立统计单位、样本量依据、最小有意义效应与停止规则明确。

- [ ] 所有计划运行均有终态，失败和重跑按预定规则记录。

- [ ] 区间、重采样单位、任务权重、配对结构和多重比较正确。

- [ ] 机制消融含适用的匹配对照、负例与简单替代方案。

- [ ] 冻结诊断不回流经验，必要时验证不改变在线训练前缀。

- [ ] 持续学习保留生命周期、变化规则、资源和迟发失败证据。

- [ ] 环境交互、调参、训练、评估、规划与记忆成本可重算。

- [ ] 负结果、退化任务、不可识别机制及推广边界已保留。

- [ ] 所有主图可由原始记录重建；代码和数据身份可核验。




[导出检查结果 JSON](handbook/index.html#ops-checklist)


### 最容易误用的十二句话



| 常见说法 | 应改写为 |
| --- | --- |
| 大家都用 3/5/10 seeds，所以足够 | 重复次数服务于目标效应、变异与可接受误差。 |
| 多测一千个 episodes 就相当于更多训练种子 | 它减少固定策略评估噪声，不能替代独立训练。 |
| 95% 阴影很窄，所以每次运行都可靠 | 均值的不确定性与单次运行分布是不同量。 |
| IQM 更稳健，所以只报 IQM | 它会减弱尾部贡献；风险任务还要单列失败与下尾。 |
| 同样环境步数就绝对公平 | 这里只匹配样本预算，还需披露计算与调参差异。 |
| 使用最新算法就是强基线 | 强基线需要匹配任务、实现和调参，简单方法也应认真比较。 |
| 无 replay 就是持续学习 | 它描述经验使用方式，不足以说明长期适应和资源能力。 |
| 冻结评估总是正确的唯一主指标 | 固定策略能力与在线学习生命周期各有自己的主目标。 |
| 有效秩更高或死神经元更少，就证明学习更好 | 这些是诊断指标，需要未来任务和控制收益验证。 |
| 最好 checkpoint 更高就是算法更好 | 需把选择过程与额外评估纳入协议，避免测试集选峰值。 |
| 不显著就是没有作用 | 可能效应小，也可能统计能力不足；检查区间与精度。 |
| 通过测试就完成了论文实验 | 计算正确性、机制支持、性能与推广是不同证据层次。 |

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#ops-checklist)。 入口：[iteration](../docs/iteration.md) · [testing](../docs/testing.md) · [protocol-reference](../docs/protocol-reference.md)

<a id="appendix-comparators"></a>


## 34 · 补充原则：遗憾、能力泛化与压力测试



### 遗憾必须说明比较者



以非平稳 bandit 为例，已知各动作时变期望收益 μₜ(a) 时，可以定义动态伪遗憾 Σₜ\[maxₐμₜ(a)−μₜ(Aₜ)\]。这比较的是每时刻都知道最佳动作的 oracle；它往往比最佳固定动作强得多。在未知真实环境中，μₜ 本身通常不可观测。一般 MDP 的动作还改变未来状态，因此不能把“在学习者访问到的每个状态选即时奖励最大动作”当作正确的最优控制比较者。



手册建议优先报告实际可测的在线收益；若另报 regret，写清静态/动态策略类、初始分布、未来信息权限、模型权限、可达性、是否允许策略切换，以及 oracle 值如何计算。与某个训练得很好的基线之差，应叫相对该基线的收益差，除非已经建立其与理论 regret 的关系。



### 压力测试应是因素设计



| 轴 | 可控变化 | 需要固定或同时记录 |
| --- | --- | --- |
| 信用分配 | 奖励延迟、有效决策间隔、无关转移数 | 最优策略、奖励密度与终止目标是否随之改变 |
| 探索 | 奖励稀疏度、分支数、不可逆状态、随机干扰 | oracle 可达性、行为覆盖和首次成功时间 |
| 状态构造 | 视野、观测混淆、记忆需求、传感器延迟 | 是否存在足够历史可恢复的状态；信息丢失是否不可逆 |
| 稳健性 | 观测噪声、动作扰动、动力学变化、攻击预算 | 威胁模型与权限；自然扰动和对抗扰动分别报告 |
| 函数逼近 | 容量、特征相关性、无关输入、共享表示 | 初始化、优化预算、数据分布、表示误差与控制误差 |
| 持续变化 | 变化频率、幅度、可预测性、重复结构 | 资源上限、任务提示、运行年龄、过去经验量 |




每条压力轴至少测容易、中等和预期失效区域，并呈现失效边界。不要只取能让方法排名最高的强度。鲁棒性对某一噪声分布成立，不推出对未见攻击或动力学成立；防御方法应在统一扰动权限与完整失败运行下比较。表示敏感性也可以作为诊断，但不能自动等同于任务失败概率。



### 层次 RL 与元学习的额外账本



学习 options/技能时，分别核算发现技能的数据、奖励、特权标记、技能库大小及高层规划预算；比较等计算的原始动作策略与随机/人工技能参照。技能访问频率高不等于技能有用，应检查移除或替换对未来控制的影响。元 RL 以任务分布为研究对象：任务必须在合适层级划分，适应期数据计成本，跨 episode 的隐状态是否保留取决于元任务边界。通过状态递归适应与通过参数更新适应都可能合法，需明确所比较的机制。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#appendix-comparators)。 入口：[testing](../docs/testing.md) · [prediction-abstraction-options](../docs/prediction-abstraction-options.md) · [planning-and-architecture](../docs/planning-and-architecture.md)

<a id="appendix-templates"></a>


## 35 · 可复制模板与最小数据规范



以下文件为空白模板，填写并审定之后才能运行正式实验。它们与本文的四份完整实验配方配套使用；模板中的 null 表示待填写，不能当作可直接提交的正式协议。下载内容也内嵌于本 HTML，单独保存页面后仍可导出。




- [实验预注册协议 YAML](../templates/research-handbook/experiment-protocol.yaml)


- [单次运行记录 JSON](../templates/research-handbook/run-manifest.json)


- [逐运行主指标 CSV](../templates/research-handbook/run-results.csv)


- [失败与重跑登记 CSV](../templates/research-handbook/failure-register.csv)


- [结论—证据对应 CSV](../templates/research-handbook/claim-evidence.csv)


- [事件日志字段 JSON](../templates/research-handbook/event-log-schema.json)




### 原则：先汇总到正确的独立单位，再聚合



```text
for each pre-registered independent training run or lifetime:
    load its complete original event log and manifest
    validate expected horizon, environment version, units, and terminal status
    compute the primary score using the locked endpoint/window/AUC rule
    keep failure status; apply only the predeclared utility mapping
    retain one score per task/run and all subsidiary diagnostic records

for each bootstrap replicate (fixed task suite example):
    resample complete runs inside each task
    preserve declared A/B pairing and any shared upstream learner
    keep the predeclared task weights
    recompute the primary aggregate and A-minus-B difference

report effect interval, run distribution, failure rate, task-level effects,
       tuning costs, deployment costs, and unsupported claims
# New-task population claims require the appropriate outer task sampling.
# Adaptive HPO procedure claims require outer selection-process repetition.
# This is analysis pseudocode, not a supplied or validated statistics library.
```



### 数据表的推荐粒度



**事件表：**一次真实环境转移或明确汇总窗口一行，包含 run、task/phase、所有步计数、真实奖励、终止/截断、墙钟和异常。**评估表：**每个训练 run、checkpoint、独立评估 episode 一行，并标明 frozen/online。**主结果表：**每个任务、算法配置、独立训练 run 一个主指标；来源日志和计算规则哈希可追溯。**搜索表：**每个候选配置每次试验一行，含未完成与失败候选。



不能把同一数据重复导出到多个文件后当作独立重复。主结果表不应把 episode 与训练 run 混在同一列。若一个 agent 顺序经历多任务，各阶段共享同一 lifetime ID；若一个预训练 checkpoint 分叉出多个适应分支，同时保留 parent ID，分析时保持这一相关结构。



### 建议的论文附录顺序



1. 完整问题和任务生成规则；信息与预算权限。
2. 算法伪代码、梯度阻断、更新时序、初始化及所有日程。
3. 实现与环境版本、包装器、硬件、可恢复状态。
4. 所有搜索空间、选择流程与确认划分。
5. 主指标和统计方法，失败/缺失/多重比较规则。
6. 逐任务与逐运行结果，消融、负结果、资源曲线。
7. 复现步骤、数据身份、分析脚本入口和证据边界。

> **本章实践连接：部分工具支持。** [文档、函数、测试、命令与缺口](handbook-code-map.md#appendix-templates)。 入口：[protocol-reference](../docs/protocol-reference.md) · [external-adapters](../docs/external-adapters.md) · [extension-guide](../docs/extension-guide.md)

<a id="appendix-reading"></a>


## 36 · 精读路线与术语对照



建议按研究问题精读，不按论文影响力堆叠。第一轮读 White 课件、Patterson 的实验指南及 Schulman 实践讲义，写出自己的协议；第二轮读 Henderson、Colas、Jordan、Agarwal，完成统计与调参设计；第三轮读 Engstrom、Andrychowicz、TD3、Rainbow/Replay 复查研究，建立机制测试；第四轮读 Alberta Plan、持续学习定义、可塑性研究与所选环境原论文，改写生命周期协议；第五轮回到自己的全部失败运行，检查文献中的解释是否真的适用。



| 术语 | 本手册用法 |
| --- | --- |
| Estimand／估计对象 | 实验试图估计的总体量，包括其任务分布、配置与预算条件。 |
| Independent run／独立运行 | 从完整规定的初始随机性生成的训练或学习过程；不是同一策略的多次回放。 |
| Replication／重复 | 必须说明是新随机运行、重跑代码、独立实现，还是新任务复核，避免含糊使用。 |
| Mechanism／机制 | 连接方法改动与行为结果的可干预因果解释，而不是一个相关诊断量。 |
| Ablation／消融 | 对组件或信息实施受控干预；超参是否重调决定它回答的问题。 |
| Prequential／先测后学 | 按真实时间顺序先行动或预测、再接收结果并学习；未来信息不提前进入。 |
| Frozen evaluation／冻结评估 | 评估指定冻结范围下的能力；状态演化、记忆写入、统计更新必须分别规定。 |
| Plasticity／可塑性 | 根据新经验进一步学习的能力；与已有知识是否被遗忘是不同问题。 |
| Forward transfer／前向迁移 | 过去经验改善新任务起点或学习速度；二者的操作定义应分开。 |
| Oracle／特权参照 | 能获得被测方法不可用信息的诊断系统；没有上界保证时不叫上界。 |
| Streaming／流式 | 经验到达即处理的更新约束；是否允许样本缓存、回放与并行须明确。 |
| Lifetime／生命期 | 携带完整学习历史的一次持续运行，通常是持续 RL 的外层统计单位。 |




阅读文献时，始终追问：作者测的是哪种对象、哪些随机性被重复、哪些选择看过测试结果、失败如何处理、结论跨越了多少未经检验的条件。对手册本身也使用同样标准。

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#appendix-reading)。 入口：[navigation-map](../docs/navigation-map.md) · [algorithm-design](../docs/algorithm-design.md) · [statistics](../docs/statistics.md)

<a id="bibliography"></a>

## 37 · 来源登记与证据边界


共 81 条来源记录，包含论文、不同版本、官方代码、讲义与统计文档；不是同等数量的独立论文，也不表示每一项都已全文通读。每项列出核验深度；关键论点在正文就近链接。相同论文在不同分册的记录保留原 ID，便于对应。


[下载完整来源 JSON](sources.json)

| ID / 年份 | 原始来源与核验 | 用途 | 证据边界 |
| --- | --- | --- | --- |
| **S01**<br>2024 | [Empirical Design in Reinforcement Learning](https://jmlr.org/papers/v25/23-0183.html)JMLR 25(318):1–63<br>核验范围<br>2026-10-03；正式出版页与63页PDF；§2、§3.2、§4、附录C重点核验<br> | 性能分布、区间、选择偏差、完整比较流程 | 教程示例不能推成统一种子数；重采样最大值不自动无偏 |
| **S02**<br>2024 | [Cross-environment Hyperparameter Tuning for Reinforcement Learning](https://rlj.cs.umass.edu/2024/papers/Paper330.html)RLJ 5:2298–2319; RLC 2024<br>核验范围<br>2026-10-03；正式出版页与22页现行PDF；§4–6<br> | 跨环境共享配置选择与复测，CHS/CHTB | 当前题名与早期CHS别称有差别；同一任务集上复测不是新任务泛化 |
| **S03**<br>2024 | [A Method for Evaluating Hyperparameter Sensitivity in Reinforcement Learning](https://papers.nips.cc/paper_files/paper/2024/hash/e1cadf5f02cc524b59c208728c73f91c-Abstract-Conference.html)NeurIPS 2024 main conference<br>核验范围<br>2026-10-03；正式出版页与23页PDF；式(1)(2)(4)、§6<br> | 逐环境调参和共享配置的敏感性差值、有效超参数维度 | 结果依赖环境分布、归一化、搜索范围与粒度；不泛化为所有归一化技巧都增加敏感性 |
| **S04**<br>2020 | [Evaluating the Performance of Reinforcement Learning Algorithms](https://proceedings.mlr.press/v119/jordan20a.html)ICML 2020; PMLR 119:4962–4973<br>核验范围<br>2026-10-03；正式出版页与12页PDF；§3–5<br> | 完整算法定义、性能百分位、聚合不确定性传播PBP | 面向可用性与少环境专用调参；不等于充分调参的峰值能力 |
| **S05**<br>2021 | [Deep Reinforcement Learning at the Edge of the Statistical Precipice](https://proceedings.neurips.cc/paper/2021/file/f514cec81cb148559cf475e7426eed5e-Paper.pdf)NeurIPS 2021<br>核验范围<br>2026-10-03；官方全文；§4、图6–10及方法核验<br> | 分层bootstrap、IQM、性能剖面、目标缺口和改善概率 | 经验覆盖率限定于所研究分布；少样本尾部不能靠bootstrap恢复 |
| **S06**<br>2021 | [rliable: official evaluation library](https://github.com/google-research/rliable)官方开源实现<br>核验范围<br>2026-10-03；核对README、metrics.py及归档标记：2025-10-15 archived<br> | 核对运行×任务矩阵、IQM、median和Mann–Whitney ties处理 | 归档只读；锁版本与依赖；调用库不代替设计假设 |
| **S07**<br>2019 | [A Hitchhiker's Guide to Statistical Comparisons of Reinforcement Learning Algorithms](https://arxiv.org/abs/1904.06979)公开预印本；相关workshop版本<br>核验范围<br>2026-10-03；arXiv记录与23页PDF全文；§4–6及附录功效表<br> | RL分布下检验、样本量和效应量模拟 | 不照抄其过强表述；均值估计无需原始高斯，FWER不是严格线性；固定N结论限定于模拟 |
| **S08**<br>2018 | [Deep Reinforcement Learning that Matters](https://ojs.aaai.org/index.php/AAAI/article/download/11694/11553)AAAI 2018；预印本2017<br>核验范围<br>2026-10-03；AAAI官方PDF与作者稿；实验分析核验<br> | 随机性、实现差别、超参数和报告方式改变比较 | 早期连续控制案例；不能外推全部任务的定量效应 |
| **S09**<br>2023 | [Hyperparameters in Reinforcement Learning and How To Tune Them](https://proceedings.mlr.press/v202/eimer23a.html)ICML 2023; PMLR 202:9104–9149<br>核验范围<br>2026-10-03；正式出版页与46页PDF；§4–6重点核验<br> | 独立调参/测试种子、自动HPO、搜索成本与公平协议 | 自动HPO优势受空间和预算影响；不能照搬样本数 |
| **S10**<br>2012 | [Random Search for Hyper-Parameter Optimization](https://www.jmlr.org/papers/v13/bergstra12a.html)JMLR 13(10):281–305<br>核验范围<br>2026-10-03；正式出版元数据和摘要核验；未阅读全文<br> | 随机搜索作为多维HPO基线 | 原始实证不是RL，不声称所有RL问题优于网格 |
| **S11**<br>2018 | [Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization](https://www.jmlr.org/papers/v18/16-558.html)JMLR 18(185):1–52<br>核验范围<br>2026-10-03；正式出版元数据与摘要核验；未阅读全文<br> | 多保真、提前停止与资源分配 | RL长短预算排名可能不一致；不声称已有RL通用保证 |
| **S12**<br>2022 | [Automated Reinforcement Learning (AutoRL): A Survey and Open Problems](https://jair.org/index.php/jair/article/view/13596)JAIR 74:517–568<br>核验范围<br>2026-10-03；正式出版页、DOI、日期和摘要核验；本章仅作扩展阅读<br> | AutoRL方法地图与元优化视角 | 未把综述当成新效能实验 |
| **S13**<br>n.d. | [NIST/SEMATECH e-Handbook: Sample sizes required](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm)统计技术手册<br>核验范围<br>2026-10-03；页面公式与已知/未知方差条件核验<br> | 效应量、错误率、功效与样本量关系 | 正态近似仅用于规划；两独立组公式是将均值差方差代入的推导 |
| **S14**<br>n.d. | [NIST/SEMATECH e-Handbook: Two-Sample t-Test for Equal Means](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm)统计技术手册<br>核验范围<br>2026-10-03；页面定义、配对与Welch公式核验<br> | 独立和配对比较及不等方差处理 | 原始RL数据的适用性需单独检查；不等同等价检验 |
| **S15**<br>n.d. | [NIST/SEMATECH e-Handbook: Tolerance intervals for a normal distribution](https://www.itl.nist.gov/div898/handbook/prc/section2/prc263.htm)统计技术手册<br>核验范围<br>2026-10-03；置信区间和容忍区间定义核验<br> | 总体参数与总体覆盖比例的区别 | 参数法要求相应分布假设；本章不用正态法处理任意RL分布 |
| **S16**<br>n.d. | [NIST/SEMATECH e-Handbook: Tolerance intervals based on the largest and smallest observations](https://www.itl.nist.gov/div898/handbook/prc/section2/prc264.htm)统计技术手册<br>核验范围<br>2026-10-03；极值容忍区间公式核验；n=46,p=0.9数值独立计算<br> | 分布无关容忍区间与样本量限制 | 连续IID；不适用于相关时间点冒充独立样本 |
| **S17**<br>n.d. | [Adam White — Deep RL Course guest lecture and slides](https://deeprlcourse.github.io/guests/adam_white/)课程页面和79页课件<br>核验范围<br>2026-10-03；课程页与课件全文提取核验；未观看视频<br> | 引出Colas、Jordan、Agarwal及实证设计路线 | 精确讲授日期未核实；不引用页面职务为当前事实 |
| **S18**<br>1979 | [A Simple Sequentially Rejective Multiple Test Procedure](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf)Scandinavian Journal of Statistics 6(2):65–70<br>核验范围<br>2026-10-03；大学托管原论文PDF与元数据核验<br> | Holm逐步家族错误率控制 | 要求每个零假设p值有效；不修复选择性报告 |
| **S19**<br>1995 | [Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1995.tb02031.x)JRSS Series B 57(1):289–300<br>核验范围<br>2026-10-03；出版社摘要与元数据核验<br> | FDR作为探索多重比较目标 | 原论文保证针对独立统计量；相关RL比较需检查依赖条件 |
| **A01**<br>2018 | [Reinforcement Learning: An Introduction, Second Edition — author publication record](https://people.cs.umass.edu/~barto/pubs-Barto.html)author bibliography and textbook pointer<br>核验范围<br>作者目录已核对；incompleteideas官方PDF本次抓取失败，未声称重读全书<br> | 经典RL问题与算法定义入口；测试流程为独立综合建议 | 教材定义不构成具体实现验证；官方PDF抓取失败 |
| **A02**<br>2009 | [Fast Gradient-Descent Methods for Temporal-Difference Learning with Linear Function Approximation](https://icml.cc/2009/papers/546.pdf)conference paper<br>核验范围<br>全文可访问；核对目标函数区别、线性条件及Baird实验<br> | MSPBE、GTD2/TDC与off-policy反例 | 线性逼近与论文假设下的结论不能自动推广到深度控制 |
| **A03**<br>2016 | [True Online Temporal-Difference Learning](https://jmlr.org/papers/v17/15-599.html)journal paper<br>核验范围<br>期刊元数据、摘要及PDF可访问<br> | 匹配在线forward view的精确等价与trace测试 | 必须比较匹配的forward view，不能泛化为任意传统TD等价 |
| **A04**<br>2021 | [Learning and Planning in Average-Reward Markov Decision Processes](https://proceedings.mlr.press/v139/wan21a.html)conference paper<br>核验范围<br>PMLR出版页与摘要已核对<br> | 平均奖励、差分价值、参考状态及Access-Control测试入口 | 收敛条件需按算法及论文定理检查，不能套用任意深度实现 |
| **A05**<br>2020 | [Implementation Matters in Deep Policy Gradients: A Case Study on PPO and TRPO](https://arxiv.org/abs/2005.12729)conference paper<br>核验范围<br>arXiv与ICLR2020 PDF全文可访问；核对优化组件、消融和KL诊断<br> | 实现选择影响算法行为与进步归因 | 论文任务和实现范围有限，不能导出通用最优配置 |
| **A06**<br>2021 | [What Matters for On-Policy Deep Actor-Critic Methods? A Large-Scale Study](https://openreview.net/forum?id=nIAxjsniDzg)conference paper; preprint 2020<br>核验范围<br>摘要及48页PDF可访问；核对八组实验与超过50种选择；正式ICLR 2021题名与Google Research出版页已核实；早期arXiv题名What Matters In On-Policy Reinforcement Learning?<br> | 统一实现中系统研究架构、归一化、优势估计和训练选择 | 主要为五个连续控制任务，经验建议存在协议边界 |
| **A07**<br>2018 | [Addressing Function Approximation Error in Actor-Critic Methods](https://proceedings.mlr.press/v80/fujimoto18a.html)conference paper<br>核验范围<br>PMLR出版页与PDF可访问<br> | 估计误差引出TD3的双critic、延迟更新和target smoothing机制 | 偏差降低与回报提升需分别测量，不能只凭机制名称归因 |
| **A08**<br>2021 | [Revisiting Rainbow: Promoting more insightful and inclusive deep reinforcement learning research](https://proceedings.mlr.press/v139/ceron21a.html)conference paper<br>核验范围<br>PMLR出版页与PDF可访问<br> | 小任务能够承担机制比较和低成本科学研究 | 小任务结论仍需有针对性的外部验证 |
| **A09**<br>2026 | [Handling Time Limits — Gymnasium Documentation](https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/)official documentation; accessed 2026-10-03<br>核验范围<br>全文读取并核对termination/truncation与bootstrap语义<br> | 环境边界与价值target | 外部截断规则不能代替任务自身有限时域定义 |
| **A10**<br>2025 | [Deep Dive: VectorEnv Autoreset](https://farama.org/Vector-Autoreset-Mode)official documentation<br>核验范围<br>官方2025-02-20说明全文已读取<br> | Gymnasium v1.1三种autoreset及final\_obs字段 | 依赖库版本与wrapper支持；旧版字段不同 |
| **A11**<br>2018 | [Rainbow: Combining Improvements in Deep Reinforcement Learning](https://arxiv.org/abs/1710.02298)conference paper; preprint 2017<br>核验范围<br>arXiv标题与作者论文入口已核对<br> | 组合型DQN组件与消融背景 | 本手册逐项测试矩阵为综合建议，未复跑原论文 |
| **A12**<br>2018 | [Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor](https://proceedings.mlr.press/v80/haarnoja18b.html)conference paper<br>核验范围<br>PMLR出版页与摘要已核对<br> | 最大熵随机actor–critic算法来源 | 不同SAC版本的value network与温度更新需分清 |
| **A13**<br>2018 | [Soft Actor-Critic — Spinning Up documentation](https://spinningup.openai.com/en/latest/algorithms/sac.html)official implementation documentation<br>核验范围<br>公式及actor密度变换说明已读取<br> | tanh密度修正、重参数化与双Q实现检查 | 实现文档使用较旧Gym API；不能照抄其环境接口到当前版本 |
| **A14**<br>2020 | [Revisiting Fundamentals of Experience Replay](https://proceedings.mlr.press/v119/fedus20a.html)conference paper<br>核验范围<br>PMLR页与19页PDF可访问<br> | 区分buffer容量与replay ratio并控制数据复用 | 效应依赖算法和评估范围，不代表越大或越多总是更好 |
| **A15**<br>2019 | [Recurrent Experience Replay in Distributed Reinforcement Learning](https://willdabney.com/publication/r2d2/)author publication page for ICLR paper<br>核验范围<br>作者页和OpenReview索引摘要已核对；OpenReview直开受验证页影响<br> | 参数滞后、表示漂移与recurrent state staleness | 本手册的hidden-state测试是综合建议，未复跑R2D2 |
| **A16**<br>2019 | [When to Trust Your Model: Model-Based Policy Optimization](https://proceedings.neurips.cc/paper/2019/hash/5faf461eff3099671ad63c6f3f094f7f-Abstract.html)conference paper<br>核验范围<br>NeurIPS官方出版页与摘要已核对<br> | 模型偏差与短模型rollout的可检验机制 | 理论与实际算法有近似差距，短rollout不是普遍定律 |
| **A17**<br>2018 | [Deep Reinforcement Learning that Matters](https://arxiv.org/abs/1709.06560)conference paper; preprint 2017<br>核验范围<br>arXiv原论文摘要与出版信息已核对<br> | 随机性、实现差异与实验报告标准化 | 不能仅凭该论文决定任何新研究的seed数量 |
| **A18**<br>2020 | [Behaviour Suite for Reinforcement Learning](https://github.com/google-deepmind/bsuite)official code and paper<br>核验范围<br>官方代码库及arXiv论文摘要已核对<br> | 针对核心能力的可解释共享实验 | 小规模能力测试不等于高维部署性能 |
| **A19**<br>2018 | [Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents](https://arxiv.org/abs/1709.06009)journal paper; preprint 2017<br>核验范围<br>原论文摘要及作者机构出版页已核对<br> | sticky actions与ALE评估协议 | 不同预处理、life-loss和交互单位会改变问题 |
| **A20**<br>2020 | [Leveraging Procedural Generation to Benchmark Reinforcement Learning](https://proceedings.mlr.press/v119/cobbe20a.html)conference paper<br>核验范围<br>PMLR官方页及训练代码入口已核对<br> | Procgen程序化关卡、样本效率与泛化 | 同生成器泛化不能覆盖任意分布外条件 |
| **A21**<br>2018 | [DeepMind Control Suite](https://arxiv.org/abs/1801.00690)technical paper<br>核验范围<br>作者arXiv原文入口与摘要已读取<br> | 结构标准化的连续控制任务 | 状态/像素、控制频率、模拟器版本都必须固定 |
| **A22**<br>2020 | [D4RL: Datasets for Deep Data-Driven Reinforcement Learning](https://arxiv.org/abs/2004.07219)benchmark paper<br>核验范围<br>作者arXiv摘要已读取<br> | 固定数据、混合策略、演示和覆盖等离线问题 | 数据分数不提供真实部署保证 |
| **A23**<br>2026 | [D4RL — Minari Documentation](https://minari.farama.org/datasets/D4RL/index.html)official dataset documentation; accessed 2026-10-03<br>核验范围<br>当前官方数据集目录已读取<br> | D4RL在Minari中的重现数据及版本记录入口 | reproduction不意味着与旧D4RL字节一致，应核对迁移差异 |
| **A24**<br>2016 | [Doubly Robust Off-policy Value Evaluation for Reinforcement Learning](https://proceedings.mlr.press/v48/jiang16.html)conference paper<br>核验范围<br>PMLR官方出版页与摘要已读取<br> | 序列决策OPE、方差与双重稳健估计的假设边界 | 不自动解决支持缺失、未知行为机制或部署风险 |
| **C01**<br>2022 | [The Alberta Plan for AI Research (v1)](https://arxiv.org/pdf/2208.11173v1)research-vision<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 固定2022原版；持续感知行动、有限计算、由简单问题逐步构建预测与控制体系。 | 路线图与研究立场，不是效能证据；核验日期2026-10-03。未采用未定版本HTML重定向的不同标题。 |
| **C02**<br>2023 | [A Definition of Continual Reinforcement Learning](https://arxiv.org/abs/2307.11046)paper<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 持续学习的形式化：隐式搜索不停歇，最佳智能体仍为持续学习智能体；NeurIPS 2023正式论文页面同时核验。 | 理论定义不能由有限生命期实验直接证明；不将所有POMDP或长训练都称为严格CRL。 |
| **C03**<br>2021 | [Continual World: A Robotic Benchmark For Continual Reinforcement Learning](https://papers.nips.cc/paper/2021/file/ef8446f35513a8d6aa2308357a268a7e-Paper.pdf)paper<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | CW20=CW10重复两次；每段1M步；已知任务边界、分任务输出头；前向迁移AUC和遗忘定义。 | 低维Meta-World序列；不是task-free、无reset或连续漂移基准。原始Meta-World v1不能无说明替换成新版。 |
| **C04**<br>2021 | [awarelab/continual\_world official repository](https://github.com/awarelab/continual_world)repository<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | README核验20段每段1M步及single/cl/multi-task入口。 | 本次未安装运行；复现需要锁定commit、旧MuJoCo/Meta-World依赖。 |
| **C05**<br>2023 | [COOM: A Game Benchmark for Continual Reinforcement Learning — official repository](https://github.com/TTomilin/COOM)paper-and-repository<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 官方说明task-incremental、明确任务边界、8类ViZDoom场景；Average Performance/Forgetting/Forward Transfer及Perfect Memory资源限制。 | README含hyintell旧地址；本次以实际可访问TTomilin仓库为入口；未执行基准。 |
| **C06**<br>2020 | [Jelly Bean World: A Testbed for Never-Ending Learning](https://arxiv.org/abs/2002.06306)paper<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | ICLR 2020；程序生成的非episodic开放网格世界、可配置任务、多模态局部感知。 | testbed不是单一固定协议；具体奖励变化及物品参数必须说明。 |
| **C07**<br>2020 | [eaplatanios/jelly-bean-world official repository](https://github.com/eaplatanios/jelly-bean-world)repository<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 官方环境实现入口与never-ending learning说明。 | 本次只核验仓库和文档，未验证当前依赖可运行性；长时地图内存需实际测量。 |
| **C08**<br>2026 | [Forager: a lightweight testbed for continual learning with partial observability in RL — RLJ 2026](https://rlj.cs.umass.edu/2026/papers/Paper39.pdf)paper<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 从Adam White官方2026发表列表点击获取的24页RLJ PDF；持续、局部观测、固定环境内存与状态构造实验。 | 首次读取成功，后续PDF检索部分请求超时；细节交叉核验arXiv 2605.01131v1。不是纯预印本状态。 |
| **C09**<br>2026 | [Forager arXiv v1 full text](https://arxiv.org/html/2605.01131v1)paper-version<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 环面、可配置FOV/物品/奖励；冻结诊断；状态构造和可塑性干预的受控结果；10%-percent选择协议。 | 2026-05-01版本对AgarCL未测试持续方法的描述已被AgarCL v3更新；不引用为现状结论。实验配方是手册建议而非原论文协议。 |
| **C10**<br>2026 | [andnp/forager environment implementation](https://github.com/andnp/forager)repository<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | README核验ForagerEnv/ForagerConfig、start()/step()、无termination信号、观测模式和物体再生接口。 | 此原始实现不是同名2024通用ABM Foragax；本次未执行，不保证与RLJ全部实验配置一一对应。 |
| **C11**<br>2026 | [The Cell Must Go On: Agar.io for Continual Reinforcement Learning (v3)](https://arxiv.org/html/2505.18347v3)paper-version<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | v1发布2025-05-23，v3为2026-08-08；区分完整世界、episodic/continual mini-games及简化世界；世界不随死亡reset；手工bot；CBP/ReDo等有限改善。 | 未把所有配置失败表述为任何方法都不能学习；奖励差、衰减及死亡处理需核对实现；原式不可替代实际奖励账本。 |
| **C12**<br>2026 | [AgarCL/AgarCL-Benchmark official baselines](https://github.com/AgarCL/AgarCL-Benchmark)repository<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 训练入口与continual env\_type=1配置、DQN/PPO/SAC基线、mini-game区分。 | README seed=3..12为范围表达，不能默认当shell有效参数；本手册未直接给出未测试训练命令。 |
| **C13**<br>2024 | [Loss of plasticity in deep continual learning](https://www.nature.com/articles/s41586-024-07711-7)paper<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | Nature 632:768–774；区分可塑性丧失与遗忘；Continual Backprop低效用单元替换；RL PPO实验与L2配合。 | 论文特定监督与RL设置中的结果不能作为所有持续任务的有效性保证。 |
| **C14**<br>2024 | [shibhansh/loss-of-plasticity official implementation](https://github.com/shibhansh/loss-of-plasticity)repository<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 作者发布的Loss of Plasticity展示与Continual Backprop实现入口。 | 本次未执行；入边、出边、optimizer状态处理应在具体实现commit逐项审计。 |
| **C15**<br>2023 | [The Dormant Neuron Phenomenon in Deep Reinforcement Learning](https://proceedings.mlr.press/v202/sokar23a.html)paper<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | ICML 2023 ReDo，循环再利用dormant神经元以改善表达利用和学习。 | dormancy降低与回报改善要分别报告；不能把机制指标当持续RL解决证据。 |
| **C16**<br>2023 | [Loss of Plasticity in Continual Deep Reinforcement Learning](https://proceedings.mlr.press/v232/abbas23a/abbas23a.pdf)paper<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | CoLLAs 2023；循环Atari、fresh/reset对照、重学能力及CReLU容量控制。 | 能重学与能保留是不同结论；循环episodic游戏不等同单一无reset世界。 |
| **C17**<br>2024 | [Streaming Deep Reinforcement Learning Finally Works (2024 v1)](https://arxiv.org/html/2410.14606v1)paper-version<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 原始stream-x、资格迹、归一化、SparseInit与ObGD；严格单样本无replay更新问题。 | 原文含episodic任务与trace reset；不能将streaming等同于无reset持续控制；公式与v3不同。 |
| **C18**<br>2026 | [Streaming Deep Reinforcement Learning Finally Works (2026 v3)](https://arxiv.org/html/2410.14606v3)paper-version<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 提交历史核验2026-09-21；StreamingOptimizer逐坐标leaky-max规范化；扩展算法与实验。 | arXiv版本更新不等于新的peer-reviewed结论；位移有界不是长期价值或收益稳定证明；HTML部分指数排版错误，正文仅采用明确核实主公式。 |
| **C19**<br>2024 | [mohmdelsayed/streaming-drl official implementation](https://github.com/mohmdelsayed/streaming-drl)repository<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | 作者streaming-drl实现，README明确无experience replay、target networks或batch updates。 | 必须固定分支与论文版本；本次未安装执行，README可能对应旧版。 |
| **C20**<br>2025 | [Position: Lifetime tuning is incompatible with continual reinforcement learning](https://proceedings.mlr.press/v267/mesbahi25a.html)position-paper<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | ICML 2025 Adam/Martha White团队，论证与实验展示全生命周期调参会改变持续学习结论，建议限制可用于调参的早期时域。 | 位置论文及有限设置实验；k值不是社区统一标准，受限搜索总预算仍需报告。 |
| **C21**<br>2024 | [K-percent Evaluation for Lifelong RL](https://arxiv.org/abs/2404.02113)paper-version<br>核验范围<br>已访问原始来源；具体版本和核验内容见贡献/边界字段<br> | Lifetime tuning系列早期稿，明确只用k百分比实验数据选择超参数。 | 与2025正式位置论文相关版本，不应当作完全独立的重复实证证据。 |
| **R01**<br>2017 | [The Nuts and Bolts of Deep RL Research — John Schulman](https://drive.google.com/file/d/0BxXI_RttTZAhc2ZsblNvUHhGZDA/view?resourcekey=0-8WDMtE-O_gmlo1ppKR_ENw)Berkeley Deep RL Bootcamp 作者讲义<br>核验范围<br>2017-08-26版本；经官方课程页定位并下载PDF、读取全文<br> | 小任务、诊断、基线、消融和开发经验 | 历史工程经验；特定超参不是当前统一推荐；个人站点下载失败后使用课程原链接 |
| **R02**<br>2018 | [Spinning Up as a Deep RL Researcher — Joshua Achiam](https://spinningup.openai.com/en/latest/spinningup/spinningup.html)作者实践指南<br>核验范围<br>官方页面全文<br> | 问题选择与研究开发流程、强基线 | 历史文档；正文将性能主张与机制/负结果贡献分开 |
| **R03**<br>2017 | [Reproducibility of Benchmarked Deep Reinforcement Learning Tasks for Continuous Control](https://arxiv.org/abs/1708.04133)原始研究公开稿<br>核验范围<br>原始摘要与元数据<br> | 代码、超参与连续控制复现差异 | 未据摘要抽取具体实验数值 |
| **R04**<br>2020 | [Measuring the Reliability of Reinforcement Learning Algorithms](https://arxiv.org/abs/1912.05663)ICLR 2020；arXiv v2<br>核验范围<br>原始摘要、状态及论文定义入口<br> | 训练期间和固定策略的变异与风险 | 本手册诊断表是综合设计，未冒称原文指标全集 |
| **R05**<br>2022 | [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/)ICLR Blog Track；作者实现研究<br>核验范围<br>全文结构、代码谱系与核心细节段落<br> | 复现须固定具体实现谱系及环境细节 | 与论文消融证据区分；不沿用其少种子数作为标准 |
| **R06**<br>accessed 2026 | [Reinforcement Learning Tips and Tricks — Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html)官方工程文档<br>核验范围<br>当前页面；2026-10-03<br> | 开发排错、环境、归一化与评估 | 会更新的工程建议；确定性策略选择及独立评估不直接覆盖持续在线目标 |
| **R07**<br>2020 | [A Closer Look at Deep Policy Gradients](https://arxiv.org/abs/1811.02553)ICLR 2020；arXiv v4<br>核验范围<br>原始论文摘要及作者方法解读<br> | 把梯度估计、价值预测和优化目标与真实回报分开诊断 | 实证结论限定于其所测算法和任务；手册不声称普遍失败 |
| **R08**<br>2018 | [Deep Reinforcement Learning and the Deadly Triad](https://arxiv.org/abs/1812.02648)原始研究公开稿<br>核验范围<br>原始摘要与研究范围<br> | 经典发散机制与深度Q学习实践之间的差异 | 并非所有自举/异策略/函数逼近组合都会发散 |
| **R09**<br>1999 | [Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping](https://people.eecs.berkeley.edu/~russell/papers/icml99-shaping.pdf)ICML 1999；作者论文<br>核验范围<br>作者PDF与摘要/变换形式<br> | potential-based shaping 的策略不变性 | 需满足问题、折扣与边界条件；不推出实现轨迹相同 |
| **R10**<br>2019 | [Challenges of Real-World Reinforcement Learning](https://arxiv.org/abs/1904.12901)原始研究公开稿<br>核验范围<br>原始摘要与问题划分<br> | 现实部署的约束和评价维度 | 研究问题地图，不是部署认证 |
| **R11**<br>2020 | [An Empirical Investigation of the Challenges of Real-World Reinforcement Learning](https://arxiv.org/abs/2003.11881)原始研究公开稿<br>核验范围<br>原始摘要、官方基准仓库说明<br> | 控制延迟、噪声、限制等因素的实验路线 | 仿真挑战测试不等于真实部署已验证 |
| **R12**<br>2022 | [No More Pesky Hyperparameters: Offline Hyperparameter Tuning for RL](https://openreview.net/forum?id=AiOUi3440V)TMLR 2022<br>核验范围<br>原始PDF正文、模型与选择算法<br> | Data2Online 与 calibration model | 模拟器内学习轨迹的选择；对未覆盖分布有外推限制 |
| **R13**<br>2026 | [Dynamics Models for Offline Hyperparameter Selection in Real-World RL](https://arxiv.org/html/2608.11349v1)arXiv v1；摘要页标注RLC 2026接收<br>核验范围<br>全文§1–4和限制；2026-08-11版本<br> | 工业传感器nexting的模型辅助调参及分布漂移检验 | 被动预测，不是自主工厂控制；长期模型泛化效果混合、含oracle-like诊断 |
| **R14**<br>2020 | [Hyperparameter Selection for Offline Reinforcement Learning](https://arxiv.org/abs/2007.09055)原始研究公开稿<br>核验范围<br>原始摘要与定义<br> | 仅凭离线数据选择固定策略 | 不同于评估随后继续学习的Data2Online系统 |
| **R15**<br>2022 | [Towards a Standardised Performance Evaluation Protocol for Cooperative MARL](https://proceedings.neurips.cc/paper_files/paper/2022/hash/249f73e01f0a2bb6c8d971b565f159a7-Abstract-Conference.html)NeurIPS 2022<br>核验范围<br>正式出版页及全文§3–4<br> | 合作MARL报告、聚合与复现 | 推荐的预算比和checkpoint规则取决于目标；不直接替代持续在线指标 |
| **R16**<br>2009 | [RL-Glue: Language-Independent Software for Reinforcement-Learning Experiments](https://www.jmlr.org/papers/v10/tanner09a.html)JMLR 10(74):2133–2136<br>核验范围<br>正式出版摘要与元数据<br> | 实验控制、环境与智能体的接口隔离及共享 | 历史软件设计；不要求使用旧运行时 |
| **R17**<br>2022 | [Towards Continual Reinforcement Learning: A Review and Perspectives](https://jair.org/index.php/jair/article/view/13673)JAIR 75:1401–1476<br>核验范围<br>正式出版摘要、元数据与原始公开稿摘要<br> | 持续RL问题形式化、非平稳范围与驱动来源 | 综述地图；未把综述当作新机制效能证据 |

> **本章实践连接：人工研究协议。** [文档、函数、测试、命令与缺口](handbook-code-map.md#bibliography)。 入口：[catalog](../docs/catalog.md) · [navigation-map](../docs/navigation-map.md)
