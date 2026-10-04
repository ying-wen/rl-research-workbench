# 从手册原理到代码与工具

37 章与 8 类机制扩展均有明确映射。**人工协议、部分工具支持、所述工具已实现**描述的是支持范围，不是算法效能。所有命令只通过语法核验；带前提的命令需先准备真实数据。

[全文阅读](handbook.md) · [整体机制设计](mechanism-design.md) · [反向索引](handbook-code-index.md) · [维护说明](handbook-maintenance.md)

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
- [教程独立算法与工作台的真实接入](#extension-tutorial-adapter)
- [整体机制设计与推导桥](#extension-mechanism-design)
- [两个项目的完整生命期研究](#extension-project-lifetimes)
- [GVF、抽象、子目标与 options](#extension-prediction-abstraction-options)
- [模型、规划与完整架构](#extension-planning-architecture)
- [多智能体与持续协作](#extension-multi-agent)
- [持久学习、检索与任务内计算的分离](#extension-persistent-evidence)
- [人类与 agent 的证据驱动迭代](#extension-agent-iteration)

<a id="guide-scope"></a>

## 01 · 如何使用这份手册

**问题：** 人类研究者和 agent 应如何按当前问题选择证据层级，而不把执行成功当作科学成功？

**原则：** 先分别登记问题定义、实现一致性、机制解释、效能与持续未来价值，再选择需要通过的门。手册中的文献发现、工程经验和综合建议保留不同身份；工作流通过只证明对应记录和执行路径成立。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#guide-scope) · [交互阅读版](handbook/index.html#guide-scope)

**实践文档：** [docs/start-here.md](../docs/start-here.md) · [docs/iteration.md](../docs/iteration.md) · [docs/testing.md](../docs/testing.md) · [AGENTS.md](../AGENTS.md)

**代码职责：**

- [rlworkbench/core.py · audit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L284) — 按锁定人口核对完成、失败、缺失、无效与 claim_status；不评审机制或科学效能。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_run_and_receipts_reconcile](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L63) — 验证运行人口与原始奖励对账，并验证 smoke 报告保留 workflow_smoke_only。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench audit '{RUN_DIR}'
```

检查已完成实验的记录完整性，不据此宣告方法有效。 操作类型：`read_only`。 前提：{RUN_DIR} 为现存原生运行或已导入的结果目录，含 lock.json 与 jobs/。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [templates/iteration-log.md](../templates/iteration-log.md)

**能力缺口与结论边界：**

- 研究问题的重要性、机制成立和长期效能仍须人工或独立实验评审；audit 不认证科学结论。

<a id="guide-lineage"></a>

## 02 · 研究脉络：不同群体分别解决了什么问题

**问题：** 如何将不同研究群体的经验转化为实验设计，同时保留来源、版本和适用边界？

**原则：** 从被解决的问题组织文献：经典目标与算子、实验分布和调参、实现混杂、跨任务统计、能力基准以及持续生命期。每条经验都连接到可检查行动；不能把某篇论文中的配置或讲义建议变成跨任务普遍定律。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#guide-lineage) · [交互阅读版](handbook/index.html#guide-lineage)

**实践文档：** [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/statistics.md](../docs/statistics.md) · [docs/catalog.md](../docs/catalog.md) · [docs/project-patterns.md](../docs/project-patterns.md)

**代码职责：**

当前无直接实现；按人工研究协议执行。

**对应测试：**

当前无直接实现；按人工研究协议执行。

**模板与配置：** [docs/sources.json](../docs/sources.json) · [catalog/algorithms.json](../catalog/algorithms.json) · [catalog/environments.json](../catalog/environments.json)

**能力缺口与结论边界：**

- 当前没有自动文献真实性、版本差异或证据强度判定器；sources.json 是带时点的人工核验记录。
- 目录包含 reference_only 条目，列入来源或目录不代表已实现算法或环境。

<a id="guide-objective"></a>

## 03 · 先确定研究对象与目标函数

**问题：** 本次实验评价的是最终策略、完整学习生命期、预测误差还是给定开发预算下的可用算法？

**原则：** 先写清问题分布、指标单位、时间权重、信息权限、选择器和预算。在线累计收益必须包含探索与恢复损失；末端策略评价是另一目标。原始任务效用与训练塑形奖励分开，资源公平性对应明确的交互或计算约束。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#guide-objective) · [交互阅读版](handbook/index.html#guide-objective)

**实践文档：** [docs/protocol-reference.md](../docs/protocol-reference.md) · [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/continual.md](../docs/continual.md) · [docs/planning-and-architecture.md](../docs/planning-and-architecture.md)

**代码职责：**

- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 检查主指标、改善方向、最小效应、预算与分层 checks 的声明，并验证原生指标兼容性。
- [rlworkbench/core.py · plan](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L168) — 展开方法×环境×种子的完整人口，使预定交互预算可核对。
- [rlworkbench/contracts.py · validate_modules](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/contracts.py#L13) — 检查声明的信息权限和模块连接；不验证运行时真实信息流。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_overlap_and_budget_overrun_rejected](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L40) — 验证开发与保留种子重叠、计划超预算被拒绝。
- [tests/test_contracts.py · ContractTests.test_diagnostic_taint_cannot_be_laundered_by_middle_module](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L46) — 检查诊断特权经中间模块流向决策的声明路径会被拒绝。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/continual.json
```

检查生命期 smoke 协议字段与当前原生适配能力。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

```bash
python3 -m rlworkbench plan profiles/continual.json --summary
```

显示方法、环境、种子人口与最大交互量。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [templates/project-charter.md](../templates/project-charter.md) · [templates/module-contract.json](../templates/module-contract.json) · [profiles/continual.json](../profiles/continual.json)

**能力缺口与结论边界：**

- 自然语言目标与指标是否一致须审阅，字段合法不代表估计对象合理。
- 原生执行仅支持 mean_reward/evaluation_return；预测误差、稳态极限、通用塑形不变性和墙钟预算约束未原生实现。

<a id="guide-design"></a>

## 04 · 算法设计：从失效机制到可反驳的改进

**问题：** 如何把一次算法修改变成能够排除替代解释、可以被否定的机制实验？

**原则：** 将具体失效事件分解为竞争解释，推导修改的算子、估计器或状态，并预测中间作用与最终行为。先固定数据检查计算，再回到闭环；使用最小正反例、廉价对手和适当二因子对照，避免用单一回报增益替代机制证据。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#guide-design) · [交互阅读版](handbook/index.html#guide-design)

**实践文档：** [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/testing.md](../docs/testing.md) · [docs/iteration.md](../docs/iteration.md) · [docs/project-patterns.md](../docs/project-patterns.md)

**代码职责：**

- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 要求 implementation、mechanism、performance 三类非空检查声明；只检查存在，不执行其自然语言判据。
- [rlworkbench/core.py · next_protocol](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L392) — 根据带证据引用的明确决策创建后继草案；不决定候选是否有效。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L136) — 验证 next 不执行训练，拒绝 smoke 直接确认，确认使用保留种子并锁定选择。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/classic.json
```

检查一个示例是否分别登记实现、机制和性能目标。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [templates/module-card.md](../templates/module-card.md) · [templates/decision-record.md](../templates/decision-record.md) · [templates/decision.json](../templates/decision.json)

**能力缺口与结论边界：**

- 自动因果归因、二因子交互统计和最小反例生成未实现。
- 代码审计、方程恒等与梯度一致不自动成为回报提升证据；研究卡需记录最强替代解释和撤回条件。

<a id="stats-framework"></a>

## 05 · 统计、调参与算力：明确一次实验究竟估计什么

**问题：** 一次报告估计固定配置、完整调参流程、固定任务清单还是新任务总体的性能？

**原则：** 统计单位和不确定性层级由主张决定。固定配置的新训练种子只回答配置性能；完整选择过程的质量需要外层重复搜索，新任务泛化还需任务层抽样。先登记指标、预算和最小实际效应，再决定分析，不由已有曲线倒推问题。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-framework) · [交互阅读版](handbook/index.html#stats-framework)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/protocol-reference.md](../docs/protocol-reference.md) · [docs/iteration.md](../docs/iteration.md)

**代码职责：**

- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 要求主指标、方向、minimum_effect、预选方法与选择规则；不推断任务总体。
- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 分别在固定环境内计算已登记候选相对基线的配对差值，并输出明确局限。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_paired_statistics_constant_difference_and_direction](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L121) — 检验配对均值差的方向与常数差值区间，不检验总体代表性或区间的普遍覆盖率。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench compare '{RUN_DIR}' --candidate sarsa --baseline q_learning
```

在 classic 结构的完整结果人口中查看逐环境配对描述。 操作类型：`read_only`。 前提：{RUN_DIR} 是包含 sarsa 候选和 q_learning 登记基线的完整有效结果目录。；配对设计须事先成立；该命令不进行任务总体或选择过程推断。

**模板与配置：** [profiles/classic.json](../profiles/classic.json) · [templates/research-card.md](../templates/research-card.md)

**能力缺口与结论边界：**

- 不支持完整 HPO 过程的外层重复分析、随机任务总体推断或任务层方差分解。
- 最低两个 seed 是 schema 约束，不是统计充分性保证。

<a id="stats-randomness"></a>

## 06 · 随机单位、配对与重复：一个种子到底代表什么

**问题：** 如何区分完整训练随机性、评估回合噪声和连续生命期窗口，建立有意义的配对？

**原则：** 一次完整训练或生命期通常是独立单位；评估回合和时间窗口是内部观测。配对应共享事先定义的外生情景，并分离环境、动作和评价 RNG；相同整数种子不保证动作相关轨迹相同，也不保证方差降低。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-randomness) · [交互阅读版](handbook/index.html#stats-randomness)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/testing.md](../docs/testing.md) · [docs/protocol-reference.md](../docs/protocol-reference.md)

**代码职责：**

- [rlworkbench/engines.py · _seed](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L37) — 为教学引擎生成按命名空间派生的随机种子。
- [rlworkbench/engines.py · BanditStream.step](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L180) — 按每步所有动作的潜在噪声生成奖励，避免动作选择改变外生噪声抽取顺序。
- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 以固定环境内配对 seed 为重采样单位；不把 episode 或 checkpoint 当独立样本。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_potential_reward_noise_is_not_action_conditioned_rng](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L65) — 验证动作改变不改变下一步潜在奖励噪声的对齐。
- [tests/test_engines.py · EngineTests.test_identical_seed_reproduces_all_events](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L72) — 验证教学 bandit 在同配置和种子下复现全部事件。
- [tests/test_engines.py · EngineTests.test_eval_budget_does_not_change_training](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L135) — 验证表格示例的评价预算改变不影响训练事件和最终 Q。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench plan profiles/continual.json --summary
```

确认种子位于完整方法×环境人口层；不把阶段当新 seed。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

**模板与配置：** [profiles/continual.json](../profiles/continual.json)

**能力缺口与结论边界：**

- 通用随机流注册表、硬件逐位确定性、共享预训练的层级重采样和跨集群 RNG 恢复未实现。
- 仅按相同 seed 标签做配对不能证明外生场景有效耦合，适配器接入时需额外审计。

<a id="stats-hpo"></a>

## 07 · 超参数测试：把选择、评估与搜索成本分开

**问题：** 如何分开开发、选择和独立确认，并公平计入搜索成本？

**原则：** 冻结搜索空间、采样分布、早停、checkpoint 规则与失败处理后选择配置，再在新样本上确认。算法峰值能力与给定预算下整个选择流程的质量不同；二者需要不同外层重复。对各方法记录全部候选和失败成本，不只报告胜者。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-hpo) · [交互阅读版](handbook/index.html#stats-hpo)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/iteration.md](../docs/iteration.md) · [docs/protocol-reference.md](../docs/protocol-reference.md)

**代码职责：**

- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 当前只允许 preselected arms，并检查开发与保留种子分离以及确认选择摘要。
- [rlworkbench/core.py · freeze](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L180) — 把配置、计划和工作台源码摘要绑定到不可原地覆盖的锁文件。
- [rlworkbench/core.py · next_protocol](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L392) — 从开发决策选定方法并改用保留种子形成确认草案；不搜索超参。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_freeze_binds_config_jobs_and_source](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L48) — 验证协议、执行人口或源码漂移会使锁验证失败。
- [tests/test_workflow.py · WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L136) — 验证确认种子来自保留人口、所选配置修改会失效，smoke 不能直接升级。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench freeze '{PROTOCOL}' --out '{NEW_LOCK}'
```

在人工完成选择并审阅协议后生成新锁。 操作类型：`creates_files`。 前提：{PROTOCOL} 是已完成调参选择并通过校验的原生协议。；{NEW_LOCK} 必须不存在；正式确认还须来自 next 的合法选择来源。

```bash
python3 -m rlworkbench next '{LOCK}' --decision '{DECISION}' --study-id confirmation-v2 --out '{NEW_PROTOCOL}'
```

从开发研究与明确 confirm 决策创建待审阅确认草案。 操作类型：`creates_files`。 前提：{LOCK} 是 development 研究的有效锁，不能是 smoke。；{DECISION} 包含 parent_study_id、action=confirm、rationale、evidence、selected_arms。；{NEW_PROTOCOL} 必须不存在；新任务泛化仍需独立审查任务分布。

**模板与配置：** [templates/decision.json](../templates/decision.json) · [templates/decision-record.md](../templates/decision-record.md)

**能力缺口与结论边界：**

- 无自动 HPO、随机搜索、Hyperband、嵌套选择 bootstrap 或累计搜索成本分析器。
- 保留种子与哈希不防止人为偷看测试结果；HPO 仍需独立登记并由团队执行访问隔离。

<a id="stats-sensitivity"></a>

## 08 · 跨环境设置与超参数敏感性：峰值之外的算法品质

**问题：** 方法是否需要逐环境重调，以及所谓自动适应是否把敏感性转移到元参数？

**原则：** 同时报告共享配置与逐环境调参表现，事先固定任务权重、归一化参考和搜索范围。单变量固定其余参数与重新调优回答不同问题；关键参数交互、奖励尺度、更新率和漂移速度必须由有判别力的开发矩阵揭示。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-sensitivity) · [交互阅读版](handbook/index.html#stats-sensitivity)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md)

**代码职责：**

- [rlworkbench/core.py · plan](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L168) — 可展开人工登记的固定配置 arms×环境×种子矩阵；不会构造搜索空间、选择最优配置或计算敏感性。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_all_profiles_and_exact_population](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L24) — 仅验证预选 arms×envs×seeds 展开数量与协议一致。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench plan '{PROTOCOL}' --summary
```

核算人工登记敏感性试验的完整人口与交互预算。 操作类型：`read_only`。 前提：{PROTOCOL} 是把固定参数配置显式登记为 arms 的有效原生协议；不可将测试结果反馈为同次独立确认。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [profiles/continual.json](../profiles/continual.json)

**能力缺口与结论边界：**

- CHTB/CHS、逐环境—共享配置差值 Φ、有效超参数维度、经验 CDF 归一化和交互热图未实现。
- plan 是人口与预算展开器，不能据其成功断言搜索覆盖充分或方法易调。

<a id="stats-power"></a>

## 09 · 种子数量与统计功效：用可检测差异决定预算

**问题：** 正式重复数量如何由可检测改善和所需精度决定，而不是套用固定 seed 数？

**原则：** 先定义实际意义阈值 δ，用独立试点评估配对差值或独立组方差，并模拟实际分析在重尾、失败混合、调参层级下的表现。预算不足时收缩主张；预先规定停止，零次失败也不能推成低失败风险。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-power) · [交互阅读版](handbook/index.html#stats-power)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/iteration.md](../docs/iteration.md) · [docs/protocol-reference.md](../docs/protocol-reference.md)

**代码职责：**

- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 只检查 minimum_effect 非负、种子去重、schema 最低数量与最大交互预算；不计算功效。
- [rlworkbench/core.py · plan](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L168) — 将人工选定的样本数转换为完整人口和最大交互成本。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_invalid_fields_rejected_before_execution](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L30) — 验证非法 seed 和非有限 minimum_effect 被拒绝；不验证 seed 数足够检出效应。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench plan profiles/classic.json --summary
```

查看 smoke 预算；两次运行仅为快速通路示例，不是功效建议。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

**模板与配置：** [templates/project-charter.md](../templates/project-charter.md) · [templates/research-card.md](../templates/research-card.md)

**能力缺口与结论边界：**

- 正态/t 分布功效规划、覆盖率模拟、失败率区间、序贯检验与合法停止边界均未实现。
- 不能把 CLI 接受的两个 seed 或 bootstrap 重复次数当作独立信息量。

<a id="stats-intervals"></a>

## 10 · 区间回答不同问题：均值确定，不代表运行稳定

**问题：** 均值差的区间、运行波动和未来坏运行风险应该怎样分别报告？

**原则：** 均值置信区间刻画估计不确定性，样本标准差与分位数刻画已有运行的离散性，预测或容忍区间另有假设。增加 seed 不能消除算法波动；逐时间点区间不能冒充整条曲线同时覆盖。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-intervals) · [交互阅读版](handbook/index.html#stats-intervals)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/protocol-reference.md](../docs/protocol-reference.md)

**代码职责：**

- [rlworkbench/analysis.py · paired_interval](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L20) — 对完整配对差值有放回抽样，返回均值的 percentile bootstrap 区间；默认 95%。
- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 逐环境同时输出差值列表、均值、中位数、样本标准差和 bootstrap 区间。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_paired_statistics_constant_difference_and_direction](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L121) — 检查常数差值区间退化为常数，单对样本被拒绝，最小化指标方向正确。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench compare '{RUN_DIR}' --candidate sarsa --baseline q_learning --bootstrap 10000
```

输出固定环境内配对均值差的描述性区间。 操作类型：`read_only`。 前提：{RUN_DIR} 是 classic 结构的完整有效人口。；配对与独立训练单位已经人工核实；默认区间的小样本覆盖率可能较差。

**模板与配置：** [profiles/classic.json](../profiles/classic.json)

**能力缺口与结论边界：**

- 未实现预测区间、容忍区间、同时置信带、尾部风险或失败概率区间。
- 当前区间没有调参或多重比较校正；测试验证计算性质，不构成所有 RL 分布上的覆盖率保证。

<a id="stats-aggregate"></a>

## 11 · 跨任务聚合：同时保留分布形状与实际改善量

**问题：** 如何跨任务汇总而不让不同量纲、样本数和被隐藏的退化任务扭曲结论？

**原则：** 预先定义任务权重与归一化，并对每条运行先变换再聚合；同时保留逐任务原始表现。IQM、性能剖面和独立运行的改善概率分别回答不同问题；重采样须匹配固定任务、新任务总体或完整调参的实际层级。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-aggregate) · [交互阅读版](handbook/index.html#stats-aggregate)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/protocol-reference.md](../docs/protocol-reference.md)

**代码职责：**

- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 仅输出每个固定环境的配对差值，不合并不同环境原始回报；正差配对比例明确不是 rliable 的跨运行改善概率。
- [rlworkbench/analysis.py · markdown_report](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L66) — 按环境与方法分别报告完成/失败/缺失/无效及含失败分值的均值。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_paired_statistics_constant_difference_and_direction](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L121) — 检验逐环境方向统一；没有覆盖 IQM 或跨任务 bootstrap。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench report '{RUN_DIR}'
```

查看逐环境结果与失败人口，保留聚合前的证据。 操作类型：`read_only`。 前提：{RUN_DIR} 是已执行或导入的结果目录，包含有效锁文件。

**模板与配置：** [docs/sources.json](../docs/sources.json)

**能力缺口与结论边界：**

- IQM、任务权重、性能剖面、目标缺口、rliable 改善概率、任务层 bootstrap 尚未实现。
- 跨环境归一化参考及其估计误差需要另存并审计；当前工具不会自动生成基准总排名。

<a id="stats-comparisons"></a>

## 12 · 显著性、实际价值与多重比较

**问题：** 怎样区分统计差异、实际价值、证据不足和等价，控制分析自由度？

**原则：** 事先声明主指标、主预算、主要基线与 δ；报告差值及区间而不是只挑显著结果。多候选、多时间点与子集筛选都可能放大误报，等价需要预定界限和专门分析；CI 跨零不能证明两法相同。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-comparisons) · [交互阅读版](handbook/index.html#stats-comparisons)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/iteration.md](../docs/iteration.md)

**代码职责：**

- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 仅允许已登记基线，按 maximize/minimize 统一改善方向，输出 minimum_effect 与未校正声明。
- [rlworkbench/core.py · next_protocol](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L392) — 要求显式决策与证据引用，不根据正差或区间自动晋升。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_paired_statistics_constant_difference_and_direction](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L121) — 检验最大化/最小化的差值方向及配对摘要。
- [tests/test_workflow.py · WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L136) — 验证决策创建新草案而非自动训练或自动确认有效。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench compare '{RUN_DIR}' --candidate sarsa --baseline q_learning
```

输出一个登记候选对基线的描述，需按主比较计划解释。 操作类型：`read_only`。 前提：{RUN_DIR} 为包含登记的 q_learning 基线与 sarsa 的完整有效结果目录。；不得用多次调用后挑选的最佳区间冒充预注册主比较。

**模板与配置：** [templates/decision-record.md](../templates/decision-record.md) · [templates/decision.json](../templates/decision.json)

**能力缺口与结论边界：**

- Welch、置换、等价检验、Holm/Bonferroni、FDR 及序贯分析未实现。
- observed_positive_pair_fraction 不表示统计显著性、后验优越概率或跨运行改善概率。

<a id="stats-recipe"></a>

## 13 · 可直接执行的统计实验单

**问题：** 怎样将统计实验单落实为可重复执行、保留失败且可审计的完整证据包？

**原则：** 冻结问题、随机层级、选择规则、预算和失败效用后执行完整预定人口。区分算法失败、基础设施中断、缺失与损坏；保留原始运行及未完成状态。报告结果与限制并写下下一决定，不按幸存前缀重新定义比较人口。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#stats-recipe) · [交互阅读版](handbook/index.html#stats-recipe)

**实践文档：** [docs/protocol-reference.md](../docs/protocol-reference.md) · [docs/iteration.md](../docs/iteration.md) · [docs/statistics.md](../docs/statistics.md) · [docs/external-adapters.md](../docs/external-adapters.md)

**代码职责：**

- [rlworkbench/core.py · freeze](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L180) — 保存协议、全部计划 job、源码摘要和运行时版本。
- [rlworkbench/core.py · audit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L284) — 逐项对账完整计划人口与工件摘要，区分失败、缺失和无效。
- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 拒绝不完整或无效人口的比较；对实际算法失败使用预先登记的复合分值并标注估计对象变化。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_failed_jobs_are_kept_not_dropped](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L78) — 模拟算法失败，验证原始失败证据与预定分值保留，配对人口不缩水。
- [tests/test_workflow.py · WorkflowTests.test_missing_jobs_cannot_be_silently_scored](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L97) — 验证缺失 job 不被填成失败分数，且不能开始比较。
- [tests/test_workflow.py · WorkflowTests.test_modified_result_or_artifacts_invalidate_job](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L108) — 验证改动原始事件或结果会被标为无效。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench audit '{RUN_DIR}'
```

在分析前对齐计划与结果人口。 操作类型：`read_only`。 前提：{RUN_DIR} 为已有运行或导入结果目录。

```bash
python3 -m rlworkbench report '{RUN_DIR}' --out '{NEW_REPORT}'
```

写出保留失败、缺失与效能边界的 Markdown 报告。 操作类型：`creates_files`。 前提：{RUN_DIR} 为已有结果目录；{NEW_REPORT} 必须不存在。

**模板与配置：** [templates/iteration-log.md](../templates/iteration-log.md) · [templates/decision-record.md](../templates/decision-record.md) · [profiles/classic.json](../profiles/classic.json)

**能力缺口与结论边界：**

- 工具支持证据封装和有限配对分析，尚不生成 IQM、性能剖面、完整 HPO 成本或统计功效。
- 摘要用于检测意外漂移，不认证外部数据真实；缺失任务仍需追查，不可凭打包结果宣称实验完成。

<a id="alg-classical"></a>

## 14 · 经典强化学习：先建立可以被推翻的正确性证据

**问题：** 经典算法是否实现了声称的更新目标、终止边界与随机递推，而非仅在一个任务上涨分？

**原则：** 先用独立真值、手算轨迹、采样期望和已知反例检查算法；声明收敛或近似目标的条件。表格、线性预测、off-policy、trace 与平均奖励各有不同目标，不能用同一个 TD loss 或小任务稳定性替代全部验证。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#alg-classical) · [交互阅读版](handbook/index.html#alg-classical)

**实践文档：** [docs/testing.md](../docs/testing.md) · [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/catalog.md](../docs/catalog.md)

**代码职责：**

- [rlworkbench/engines.py · BanditLearner.update](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L167) — 实现样本均值或固定 alpha 的动作值递推。
- [rlworkbench/engines.py · td_target](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L221) — 区分 Q-learning 的 max backup 与 Sarsa 的下一采样动作，真正终止阻断 bootstrap。
- [rlworkbench/engines.py · CliffGrid.step](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L208) — 提供教学网格的悬崖非终止复位、目标终止与外部时间截断语义。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_sample_average_is_exact_empirical_average](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L41) — 以固定奖励验证在线样本均值。
- [tests/test_engines.py · EngineTests.test_constant_alpha_retains_recency](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L48) — 以手算序列验证常数步长近期加权。
- [tests/test_engines.py · EngineTests.test_external_time_limit_preserves_actual_observation_and_bootstrap](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L104) — 检查最终真实状态、Q-learning/Sarsa 不同 target 和终止遮罩。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/classic.json
```

验证 Q-learning/Sarsa 教学配置和环境语义的参数约束。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

```bash
python3 -m rlworkbench freeze profiles/classic.json --out '{NEW_LOCK}'
```

为经典 smoke 示例生成新版本锁。 操作类型：`creates_files`。 前提：{NEW_LOCK} 必须不存在；此默认配置只用于通路与边界检查。

```bash
python3 -m rlworkbench run '{LOCK}' --out '{NEW_RUN_DIR}'
```

执行已冻结经典教学人口并保留原始事件。 操作类型：`runs_smoke`。 前提：{LOCK} 由 profiles/classic.json 在当前源码与运行时下冻结。；{NEW_RUN_DIR} 必须不存在；4 条运行的默认完整交互上限为 14400。

**模板与配置：** [profiles/classic.json](../profiles/classic.json) · [profiles/continual.json](../profiles/continual.json) · [catalog/algorithms.json](../catalog/algorithms.json)

**能力缺口与结论边界：**

- 未实现独立 MRP 线性真值求解、MC、TD(λ)/true-online、GTD/TDC、重要性采样、Baird 反例或平均奖励控制。
- 教学 CliffGrid 不是对任何外部官方环境的逐步等价认证；有限测试不能证明收敛或算法效能。

<a id="alg-deep"></a>

## 15 · 现代深度强化学习：把算法与实现共同视为被测对象

**问题：** 如何把网络、优化器、采样与轨迹边界视为算法的一部分，识别实现混杂和伪增益？

**原则：** 先审计真实 transition、bootstrap 与 trace 连续性，再逐算法族检查目标、梯度和状态。机制比较、充分调参比较与资源比较分开；DQN、PPO、SAC/TD3、replay、RNN 和模型学习各自需要特定仪表，通路 smoke 不替代这些审计。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#alg-deep) · [交互阅读版](handbook/index.html#alg-deep)

**实践文档：** [docs/testing.md](../docs/testing.md) · [docs/deep-validation.md](../docs/deep-validation.md) · [docs/extension-guide.md](../docs/extension-guide.md) · [docs/algorithm-design.md](../docs/algorithm-design.md)

**代码职责：**

- [rlworkbench/engines.py · _run_ppo](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L322) — 调用可选 SB3 PPO/CartPole，按 rollout 整倍数训练，记录原始奖励并用新环境做独立冻结评价。
- [rlworkbench/engines.py · validate_job](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L43) — 检查 PPO rollout、batch 整除、预算和当前支持的参数。
- [rlworkbench/core.py · runtime](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L212) — 记录 Python 与已安装关键深度依赖的版本；不是完整可移植依赖锁。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_real_optional_ppo_budget_and_frozen_evaluation](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L195) — 可选真实 PPO 集成测试检查训练步、回合人口、评价冻结与 CPU 运行；需显式启用。
- [tests/test_engines.py · EngineTests.test_missing_optional_dependencies_fail_with_actionable_message](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L177) — 验证缺少深度依赖时给出明确错误。
- [tests/test_engines.py · EngineTests.test_unsupported_and_incomplete_configs_are_explicit_errors](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L153) — 验证不支持算法、未知配置及非法 PPO rollout/batch 约束被拒绝。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/deep.json
```

验证深度 smoke 的结构与已知能力，不保证依赖已经安装。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

```bash
python3 -m rlworkbench freeze profiles/deep.json --out '{NEW_LOCK}'
```

安装并固定深度依赖后冻结当前运行时。 操作类型：`creates_files`。 前提：先在独立 Python 环境安装 examples/deep-requirements.txt。；{NEW_LOCK} 必须不存在。

```bash
python3 -m rlworkbench run '{LOCK}' --out '{NEW_RUN_DIR}'
```

执行固定两组 PPO 参数的 CartPole 通路检查。 操作类型：`runs_smoke`。 前提：{LOCK} 由 profiles/deep.json 在相同源码和依赖环境下冻结。；{NEW_RUN_DIR} 必须不存在；默认 4 条运行交互上限 1824。；此测试不支持学习率优劣、调好 PPO 或深度算法竞争力结论。

**模板与配置：** [profiles/deep.json](../profiles/deep.json) · [examples/deep-requirements.txt](../examples/deep-requirements.txt) · [catalog/algorithms.json](../catalog/algorithms.json)

**能力缺口与结论边界：**

- DQN/Rainbow、SAC/TD3、RNN、经验回放与模型算法尚无原生执行器；当前 PPO 不是自写梯度正确性验证套件。
- 没有通用 GAE/向量 autoreset 测试、tanh 雅可比检查、完整 checkpoint 生命期恢复或跨实现效能确认。

<a id="alg-benchmarks"></a>

## 16 · 基准选择：让任务集合对应想要验证的能力

**问题：** 所选环境集合能够支持哪种能力与外推主张，哪些接口、数据和权限必须固定？

**原则：** 每项主张用可解问题、针对性压力条件和外部任务族承担不同证据角色。记录包装器、版本、观察、动作与时间单位；离线数据还需轨迹级划分、支持条件和评价权限。未见 seed、未见生成器和真实部署是不同外推层级。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#alg-benchmarks) · [交互阅读版](handbook/index.html#alg-benchmarks)

**实践文档：** [docs/catalog.md](../docs/catalog.md) · [docs/extension-guide.md](../docs/extension-guide.md) · [docs/external-adapters.md](../docs/external-adapters.md) · [docs/testing.md](../docs/testing.md)

**代码职责：**

- [rlworkbench/engines.py · validate_job](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L43) — 仅对原生教学环境与算法组合验证已知配置，未知环境显式报错。
- [rlworkbench/core.py · import_results](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L326) — 对外部生产者的完整预定人口、原始工件和来源记录做导入验证；不认证外部环境或 OPE 方法。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_unsupported_and_incomplete_configs_are_explicit_errors](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L153) — 检验环境/算法不兼容或未知配置不会静默执行。
- [tests/test_workflow.py · WorkflowTests.test_external_import_complete_bound_raw_population](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L155) — 验证外部人口完整、结果绑定锁与原始工件被保留；只验证封装。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/classic.json
```

检查实际原生环境能力，不把目录中的参考环境视作已集成。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

**模板与配置：** [catalog/environments.json](../catalog/environments.json) · [catalog/algorithms.json](../catalog/algorithms.json) · [profiles/classic.json](../profiles/classic.json) · [profiles/deep.json](../profiles/deep.json) · [profiles/continual.json](../profiles/continual.json)

**能力缺口与结论边界：**

- ALE、bsuite、Procgen、DM Control、D4RL/Minari 等目录条目不等于已安装或运行的适配器。
- 无 OPE 真值实验、IS/WIS/FQE/DR、支持性或覆盖率分析实现；环境代表性与离线数据泄漏需专门审阅。

<a id="alg-test-matrix"></a>

## 17 · 可复制测试矩阵：通过条件与证据边界一起写

**问题：** 怎样为每级测试写出独立预期、通过标准和不能证明的内容，并将其纳入迭代？

**原则：** 按单步代数、真值、采样、梯度、边界、反例、记忆和闭环归因逐层设门。容差依据精度与条件数，随机测试提前固定判据；只有通过相关实现门后才解释效能，不用扩大测试数量代替有判别力的实验。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#alg-test-matrix) · [交互阅读版](handbook/index.html#alg-test-matrix)

**实践文档：** [docs/testing.md](../docs/testing.md) · [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/iteration.md](../docs/iteration.md)

**代码职责：**

- [rlworkbench/engines.py · td_target](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L221) — 提供可独立手算的 Sarsa/Q-learning 单步边界。
- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 要求按 implementation、mechanism、performance 分层登记测试意图。
- [rlworkbench/core.py · check_measurements](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L230) — 对完成运行核对训练时域、评价人口与有限主指标。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_goal_termination_has_precedence_at_time_limit](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L114) — 验证真正目标终止与同一步时间限制重合时采用终止语义。
- [tests/test_engines.py · EngineTests.test_eval_budget_does_not_change_training](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L135) — 检验表格冻结评价隔离，而非只检查评价曲线看似合理。
- [tests/test_workflow.py · WorkflowTests.test_external_eval_cannot_be_zero_or_incomplete](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L188) — 验证外部结果不能用零评价步或不完整回合冒充完成评价。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/classic.json
```

检查示例三层验收声明与执行参数；自然语言测试并不会被自动运行。 操作类型：`read_only`。 前提：在仓库根目录运行，使用 Python 3.9+。

```bash
python3 -m rlworkbench audit '{RUN_DIR}'
```

对已运行测试/实验保留人口完整性的证据。 操作类型：`read_only`。 前提：{RUN_DIR} 是工作台已生成或导入的结果目录。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [templates/iteration-log.md](../templates/iteration-log.md) · [profiles/classic.json](../profiles/classic.json) · [profiles/deep.json](../profiles/deep.json)

**能力缺口与结论边界：**

- 完整测试矩阵中的精确求解、有限差分、true-online 等价、Baird、延迟线索 POMDP 与保存恢复套件尚未原生实现。
- 经典配方 A 与深度配方 B 是待项目化执行的方案，不因本仓库已有部分单元测试就视为完成。

<a id="crl-framing"></a>

## 18 · 持续强化学习：把整个生命期作为实验对象

**问题：** 研究的是持续运行、严格流式约束、未知变化，还是新经验长期带来的收益？

**原则：** 把完整学习器和整个生命期作为实验对象；持续、streaming、非平稳与部分可观测分别声明，不能由短程成功推断终身学习能力。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-framing) · [交互阅读版](handbook/index.html#crl-framing)

**实践文档：** [docs/continual.md](../docs/continual.md) · [docs/navigation-map.md](../docs/navigation-map.md) · [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md)

**代码职责：**

- [rlworkbench/engines.py · _run_bandit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L238) — 一个生命期只初始化一次 learner，隐藏切换只写诊断，不传任务标识。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_hidden_boundaries_and_no_lifetime_reset](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L54) — 检查 bandit 的边界不可见和无生命期重置。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/continual.json
```

核对最小持续示例的协议与原生能力。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

**模板与配置：** [profiles/continual.json](../profiles/continual.json) · [catalog/environments.json](../catalog/environments.json)

**能力缺口与结论边界：**

- 原生环境仅非平稳 bandit；不实现连续具身世界、深度可塑性或终身学习证明。

<a id="crl-objectives"></a>

## 19 · 目标、时间与被比较的系统

**问题：** 有限生命期的真实收益、折扣训练目标和资源成本分别如何定义？

**原则：** 主目标按预定完整生命期原始奖励计分；状态含权重以外的统计、记忆和优化器；只观测到前缀不能冒充完成生命期。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-objectives) · [交互阅读版](handbook/index.html#crl-objectives)

**实践文档：** [docs/continual.md](../docs/continual.md) · [docs/protocol-reference.md](../docs/protocol-reference.md)

**代码职责：**

- [rlworkbench/engines.py · _run_bandit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L238) — 每步累加实际原始奖励，最终除以注册步数。
- [rlworkbench/continual_metrics.py · summarize](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/continual_metrics.py#L12) — 区分完整生命期均值与 observed-prefix 均值。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_full_lifetime_aggregation_uses_every_raw_reward](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L80) — 核对生命期每条原始奖励都参与主指标。
- [tests/test_continual_metrics.py · ContinualMetricTests.test_full_lifetime_and_segments_include_every_raw_reward](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_continual_metrics.py#L6) — 核对阶段和全生命期奖励账本。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench plan profiles/continual.json --summary
```

展开交互预算与独立运行人口。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

**模板与配置：** [profiles/continual.json](../profiles/continual.json)

**能力缺口与结论边界：**

- 工具不强制墙钟、每步延迟和总内存上限；没有完整 learner checkpoint 保存恢复器。

<a id="crl-nonstationarity"></a>

## 20 · 先辨明变化来源，再设计对照

**问题：** 观察到的漂移来自环境外生变化、策略闭环、观测混淆还是学习器老化？

**原则：** 先分别验证固定经验流、闭环控制和外生变化；同 seed 可配对外生随机源，不能声称两个策略具有相同完整轨迹。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-nonstationarity) · [交互阅读版](handbook/index.html#crl-nonstationarity)

**实践文档：** [docs/continual.md](../docs/continual.md) · [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md) · [docs/testing.md](../docs/testing.md)

**代码职责：**

- [rlworkbench/engines.py · BanditStream.step](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L180) — 按隐藏相位生成每动作潜在奖励；每步的噪声向量与所选动作无关。
- [rlworkbench/engines.py · BanditLearner.update](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L167) — 更新仅接收动作和奖励，不能读取 phase。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_potential_reward_noise_is_not_action_conditioned_rng](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L65) — 检验动作改变不改变外生潜在奖励噪声的消费。
- [tests/test_engines.py · EngineTests.test_hidden_boundaries_and_no_lifetime_reset](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L54) — 检查隐藏边界不传 learner。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench plan profiles/continual.json --summary
```

查看静态与隐藏切换对照的完整人口。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

**模板与配置：** [profiles/continual.json](../profiles/continual.json) · [protocols/streamrate-development.json](../protocols/streamrate-development.json) · [protocols/representation-development.json](../protocols/representation-development.json)

**能力缺口与结论边界：**

- bandit 使用固定间隔循环；连续漂移、随机时长、观测变化与复杂内生漂移仍需外部适配器。

<a id="crl-benchmarks"></a>

## 21 · 基准选择：原始协议与建议变体必须分开

**问题：** 如何保留 CW20、COOM、Forager、AgarCL 的原始协议并标明本研究变体？

**原则：** 锁定版本、世界与 learner 的 reset 语义、任务权限、真实奖励账本；目录条目不能当作已完成环境集成。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-benchmarks) · [交互阅读版](handbook/index.html#crl-benchmarks)

**实践文档：** [docs/catalog.md](../docs/catalog.md) · [docs/continual.md](../docs/continual.md) · [docs/external-adapters.md](../docs/external-adapters.md)

**代码职责：**

当前无直接实现；按人工研究协议执行。

**对应测试：**

当前无直接实现；按人工研究协议执行。

**模板与配置：** [catalog/environments.json](../catalog/environments.json) · [docs/sources.json](../docs/sources.json)

**能力缺口与结论边界：**

- CW20、COOM、Forager 和 AgarCL 均为参考选型，当前未接入原生执行器。
- 奖励差值望远镜恒等、死亡补偿和自然重生需要针对所选实现逐条审计；仓库不自动验证这些语义。

<a id="crl-evaluation"></a>

## 22 · 在线主评估，冻结与回访作为诊断

**问题：** 在线收益与冻结副本、继续学习分支、旧任务回访如何互不污染？

**原则：** 持续主评估允许按协议在线更新；冻结诊断须隔离经验、随机状态及统计，权重冻结与递归状态冻结分开。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-evaluation) · [交互阅读版](handbook/index.html#crl-evaluation)

**实践文档：** [docs/continual.md](../docs/continual.md) · [docs/testing.md](../docs/testing.md) · [docs/external-adapters.md](../docs/external-adapters.md)

**代码职责：**

- [rlworkbench/engines.py · _run_bandit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L238) — 动作先于该步反馈，在线收益包含探索成本。
- [rlworkbench/engines.py · _run_tabular](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L260) — 教学表格法训练后使用独立环境和随机流评价。
- [rlworkbench/engines.py · _run_ppo](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L322) — 可选 PPO 路径在独立环境中进行冻结策略评价。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_eval_budget_does_not_change_training](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L135) — 评价预算变化不改变表格法训练事件前缀。
- [tests/test_engines.py · EngineTests.test_tabular_frozen_eval_and_episode_accounting](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L119) — 核对冻结评价与回合计数。

**模板与配置：** [profiles/continual.json](../profiles/continual.json) · [profiles/classic.json](../profiles/classic.json) · [profiles/deep.json](../profiles/deep.json)

**能力缺口与结论边界：**

- 没有持续神经学习器中期状态快照、同起点学习/冻结反事实分支或完整旧任务回访矩阵实现。
- 既有冻结隔离测试只覆盖教学表格实现，不能认证外部算法的 buffer、normalizer、hidden state 隔离。

<a id="crl-metrics"></a>

## 23 · 把收益、保留、可塑性与资源分别量化

**问题：** 生命期收益、恢复、保留、迁移、可塑性和资源怎样各自计量？

**原则：** 恢复定义固定窗口、步长、阈值和确认时刻；变化索引从零、奖励时钟从一；崩溃与行政删失分开；窗口不是独立生命期。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-metrics) · [交互阅读版](handbook/index.html#crl-metrics)

**实践文档：** [docs/continual.md](../docs/continual.md) · [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md) · [docs/protocol-reference.md](../docs/protocol-reference.md) · [docs/statistics.md](../docs/statistics.md)

**代码职责：**

- [rlworkbench/continual_metrics.py · summarize](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/continual_metrics.py#L12) — 从逐步原始奖励计算生命期/阶段统计及以前阶段基线为参照的恢复诊断。
- [rlworkbench/cli.py · main](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/cli.py#L66) — continual-metrics 筛选 train 或 training 标签的训练转移并验证 env_step 连续，排除评价事件。

**对应测试：**

- [tests/test_continual_metrics.py · ContinualMetricTests.test_confirmation_occurs_at_window_end_with_persistence](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_continual_metrics.py#L12) — 确认发生在最后一个连续合格窗口末端。
- [tests/test_continual_metrics.py · ContinualMetricTests.test_completed_nonrecovery_censoring_and_crash_are_distinct](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_continual_metrics.py#L34) — 完整未恢复、观察提前结束和崩溃分开。
- [tests/test_continual_metrics.py · ContinualMetricTests.test_scale_change_disables_recovery_claim](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_continual_metrics.py#L52) — 奖励尺度不可比时不宣称恢复。
- [tests/test_cli.py · CLITests.test_recovery_cli_checks_clock_and_completed_horizon](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_cli.py#L33) — 核对 CLI 的奖励时钟和完整时域。
- [tests/test_cli.py · CLITests.test_continual_metrics_reads_native_training_stream](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_cli.py#L56) — 真实原生 bandit 日志进入 CLI；识别 train 标签，排除评价流，核对完整奖励。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench continual-metrics '{RUN_DIR}/jobs/constant_alpha--hidden_switches--s11/events.jsonl' --changes 250,500,750,1000,1250 --window 20 --persistence 3 --tolerance 0.05 --planned-steps 1500 --end-reason completed
```

分析默认 continual profile 一条完整生命期，阈值设置仅演示。 操作类型：`read_only`。 前提：{RUN_DIR} 替换为当前代码按 profiles/continual.json 冻结并完成的运行目录；不能使用任意日志。；该默认 job 的 switch_interval=250、steps=1500，第一条变化后奖励的从零索引为 250,500,750,1000,1250；参数与注册协议一致，容差仅演示。；先确认该 job 完成；失败或提前中断须用实际终态修改参数，不能填写 completed。

**模板与配置：** [profiles/continual.json](../profiles/continual.json)

**能力缺口与结论边界：**

- 尚无自动遗忘矩阵、BWT/FWT、年龄匹配可塑性、资源曲线和多生命期生存分析。
- 恢复阈值采用旧阶段均值仅是一种已实现定义；新阶段可达性及研究意义仍需人工判定。

<a id="crl-controls"></a>

## 24 · 机制归因对照：每个对照回答一个问题

**问题：** 哪个对照能区别记忆不足、可塑性损失、学习率变化或任务特权？

**原则：** 每个 fresh/reset/frozen/oracle/replay 对照只回答预先声明的问题；完整作者方法与同基座模块消融分别命名。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-controls) · [交互阅读版](handbook/index.html#crl-controls)

**实践文档：** [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md) · [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/testing.md](../docs/testing.md) · [docs/project-patterns.md](../docs/project-patterns.md)

**代码职责：**

当前无直接实现；按人工研究协议执行。

**对应测试：**

当前无直接实现；按人工研究协议执行。

**模板与配置：** [protocols/streamrate-development.json](../protocols/streamrate-development.json) · [protocols/representation-development.json](../protocols/representation-development.json) · [templates/research-card.md](../templates/research-card.md)

**能力缺口与结论边界：**

- 两个项目中的元信用、表征、记忆与匹配资源对照是待接入方案，不在本仓库执行。
- 没有通用 fresh/reset/frozen 生成器；oracle 没有经证明的界时只能作特权诊断。

<a id="crl-tuning"></a>

## 25 · 生命期调参与版本约束

**问题：** 怎样区分独立开发生命期调参、前 k% 选择和测试未来泄漏？

**原则：** 固定选择规则与数据访问边界；开发生命期可以完整使用，不能据同一测试生命期后缀修规则；算法论文版本和实现来源一起锁定。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-tuning) · [交互阅读版](handbook/index.html#crl-tuning)

**实践文档：** [docs/continual.md](../docs/continual.md) · [docs/statistics.md](../docs/statistics.md) · [docs/iteration.md](../docs/iteration.md) · [docs/external-adapters.md](../docs/external-adapters.md)

**代码职责：**

- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 检查开发/保留 seed 不交叠，确认人口与父开发选择身份一致。
- [rlworkbench/core.py · next_protocol](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L392) — 由明确决策选择方法并使用保留 seed 建立待审确认草案。
- [rlworkbench/core.py · freeze](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L180) — 绑定注册协议、作业清单与工作台源文件摘要。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_overlap_and_budget_overrun_rejected](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L40) — 拒绝人口交叠和预算超额。
- [tests/test_workflow.py · WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L136) — 下一轮不自动运行，确认使用保留人口。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate protocols/streamrate-development.json --external
```

检查 StreamRate 开发草案结构；不代表适配可执行。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

**模板与配置：** [templates/decision.json](../templates/decision.json) · [protocols/streamrate-development.json](../protocols/streamrate-development.json)

**能力缺口与结论边界：**

- 没有自动 HPO、前缀指标访问控制或封存未来数据设施；隔离须由团队和外部系统执行。
- input_adapter_ready:false 的两个项目草案允许外部结构验证，但 freeze 被禁止；不得直接启动。

<a id="crl-recipe-a"></a>

## 26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？

**问题：** Forager 中持续适应瓶颈是状态构造还是保持可塑性？

**原则：** 把观测和变化因素、递归状态与可塑性干预分开，设置随机替换、L2 和资源匹配控制，先判机制再作独立长期确认。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-recipe-a) · [交互阅读版](handbook/index.html#crl-recipe-a)

**实践文档：** [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md) · [docs/continual.md](../docs/continual.md) · [docs/prediction-abstraction-options.md](../docs/prediction-abstraction-options.md) · [docs/algorithm-design.md](../docs/algorithm-design.md)

**代码职责：**

当前无直接实现；按人工研究协议执行。

**对应测试：**

当前无直接实现；按人工研究协议执行。

**模板与配置：** [protocols/representation-development.json](../protocols/representation-development.json) · [templates/research-card.md](../templates/research-card.md) · [templates/module-card.md](../templates/module-card.md) · [catalog/environments.json](../catalog/environments.json)

**能力缺口与结论边界：**

- 原手册配方 A 的 Forager 2×2 因子实验、CBP/ReDo 与长生命期预算均未实现或执行。
- representation-development.json 是两个当前项目的另一份开发草案，不能冒充配方 A 的直接可运行配置。

<a id="crl-recipe-b"></a>

## 27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？

**问题：** 任务序列中较少遗忘是否以学不动新任务为代价？

**原则：** 同时测完整在线收益、习得、保留和第一次/第二次访问；回访评价不回灌，任务身份和增长内存对照标明权限。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-recipe-b) · [交互阅读版](handbook/index.html#crl-recipe-b)

**实践文档：** [docs/continual.md](../docs/continual.md) · [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md) · [docs/statistics.md](../docs/statistics.md)

**代码职责：**

当前无直接实现；按人工研究协议执行。

**对应测试：**

当前无直接实现；按人工研究协议执行。

**模板与配置：** [catalog/environments.json](../catalog/environments.json) · [templates/research-card.md](../templates/research-card.md) · [docs/sources.json](../docs/sources.json)

**能力缺口与结论边界：**

- 未实现或执行 CW20/COOM 配方、P_i,j 回访矩阵和 fresh 单任务参考。
- 不能以 bandit 隐藏切换运行替代任务序列的遗忘与迁移证据。

<a id="crl-longrun"></a>

## 28 · 长期试验阶梯与最小交付包

**问题：** 短程资格测试如何逐步扩展到能暴露迟发退化的长生命期？

**原则：** 短到长沿同一锁定协议的预定阶梯运行；失败与未完成保持可见，复杂环境成功不能由简单环境代替。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#crl-longrun) · [交互阅读版](handbook/index.html#crl-longrun)

**实践文档：** [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md) · [docs/iteration.md](../docs/iteration.md) · [docs/external-adapters.md](../docs/external-adapters.md)

**代码职责：**

- [rlworkbench/core.py · check_measurements](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L230) — 完成回执必须达到注册训练时域及评价计数。
- [rlworkbench/core.py · audit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L284) — 区分完成、失败、缺失、无效，保留计划人口。
- [rlworkbench/core.py · import_results](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L326) — 导入完整外部人口并绑定原始文件。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_missing_jobs_cannot_be_silently_scored](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L97) — 未完成不能悄悄补成分值后排名。
- [tests/test_workflow.py · WorkflowTests.test_failed_jobs_are_kept_not_dropped](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L78) — 失败运行保留在比较人口内。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench plan protocols/streamrate-development.json --external --summary
```

展开项目草案的全部交互上限，未触发执行。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

**模板与配置：** [protocols/streamrate-development.json](../protocols/streamrate-development.json) · [protocols/representation-development.json](../protocols/representation-development.json)

**能力缺口与结论边界：**

- 无长程调度、checkpoint 恢复、内存/延迟监控器和自动阶段推进；预算与停止仍需外部系统落实。
- 教学 smoke 和模板预算均不构成长程效果证据。

<a id="ops-workflow"></a>

## 29 · 实验执行：从预注册到独立确认

**问题：** 如何从问题、机制、开发走到冻结执行、独立确认和下一轮决策？

**原则：** 把环境、学习器与实验控制分开；计划人口先于结果，旧协议和结果不覆盖，改动产生新版本与明确证据来源。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#ops-workflow) · [交互阅读版](handbook/index.html#ops-workflow)

**实践文档：** [docs/iteration.md](../docs/iteration.md) · [docs/start-here.md](../docs/start-here.md) · [docs/protocol-reference.md](../docs/protocol-reference.md) · [docs/external-adapters.md](../docs/external-adapters.md)

**代码职责：**

- [rlworkbench/core.py · plan](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L168) — 注册方法×环境×seed 的完整笛卡尔积。
- [rlworkbench/core.py · freeze](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L180) — 固定协议、源码摘要与作业身份。
- [rlworkbench/core.py · run](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L248) — 只在新目录运行锁定的原生计划。
- [rlworkbench/core.py · next_protocol](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L392) — 基于显式决策生成后继草案，不自动选赢家或执行。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_freeze_binds_config_jobs_and_source](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L48) — 修改配置、作业或源摘要会破坏锁身份。
- [tests/test_workflow.py · WorkflowTests.test_run_and_receipts_reconcile](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L63) — 核对计划、运行与回执对账。
- [tests/test_cli.py · CLITests.test_documented_full_path_and_budget_summary](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_cli.py#L19) — 走通 CLI 的冻结、运行、审计和报告链。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench freeze profiles/continual.json --out '{NEW_LOCK}'
```

冻结原生持续 smoke 配方；写入新锁文件。 操作类型：`creates_files`。 前提：{NEW_LOCK} 替换为不存在的 .json 路径；本命令只冻结，不运行实验。

```bash
python3 -m rlworkbench run '{LOCK}' --out '{RUN_DIR}'
```

执行已经冻结的原生教学持续 profile。 操作类型：`runs_smoke`。 前提：{LOCK} 是由当前代码冻结 profiles/continual.json 得到的文件。；{RUN_DIR} 必须为新目录；不适用于待接入的外部项目草案或长程实验。

```bash
python3 -m rlworkbench audit '{RUN_DIR}'
```

核对计划人口、终态和文件身份。 操作类型：`read_only`。 前提：{RUN_DIR} 是真实已运行目录，含 lock.json 和 jobs/。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [templates/iteration-log.md](../templates/iteration-log.md) · [templates/decision-record.md](../templates/decision-record.md)

**能力缺口与结论边界：**

- 工具不自动审查因果设计、不执行完整 HPO，也不提供集群调度、精确 checkpoint 恢复或远程真实性认证。

<a id="ops-diagnostics"></a>

## 30 · 诊断手册：症状、竞争解释与下一项实验

**问题：** 回报曲线异常时，先排查哪些可以区分的原因？

**原则：** 从奖励/时间语义到更新、经验分布、评价副作用和资源逐层定位；实现正确、机制指标和控制收益分开。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#ops-diagnostics) · [交互阅读版](handbook/index.html#ops-diagnostics)

**实践文档：** [docs/testing.md](../docs/testing.md) · [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md)

**代码职责：**

- [rlworkbench/engines.py · EventWriter.write](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L231) — 记录可追溯原始转移、计数和有限 JSON 数据。
- [rlworkbench/core.py · check_measurements](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L230) — 检查预算、终点、评价与有限指标，防止账本错误。
- [rlworkbench/continual_metrics.py · summarize](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/continual_metrics.py#L12) — 生成阶段奖励与变化后恢复诊断，不能替代机制归因。

**对应测试：**

- [tests/test_engines.py · EngineTests.test_eval_budget_does_not_change_training](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L135) — 隔离评价对训练前缀的潜在污染。
- [tests/test_workflow.py · WorkflowTests.test_modified_result_or_artifacts_invalidate_job](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L108) — 检测修改结果和原始文件。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [templates/iteration-log.md](../templates/iteration-log.md)

**能力缺口与结论边界：**

- 未内置通用梯度/KL/有效秩/dormancy/TD 误差及系统资源采集；外部 producer 必须补齐。
- 无法自动从单条回报曲线判断优化、探索、记忆或可塑性的原因。

<a id="ops-extensions"></a>

## 31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体

**问题：** 离线选择、真实系统、MARL 与 LLM 智能体应如何改变实验边界？

**原则：** 先定义被比较系统、数据与部署权限、持久状态和实际成本；团队或共享上游模型的相关性不能当独立重复。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#ops-extensions) · [交互阅读版](handbook/index.html#ops-extensions)

**实践文档：** [docs/multi-agent.md](../docs/multi-agent.md) · [docs/planning-and-architecture.md](../docs/planning-and-architecture.md) · [docs/prediction-abstraction-options.md](../docs/prediction-abstraction-options.md) · [docs/external-adapters.md](../docs/external-adapters.md) · [docs/navigation-map.md](../docs/navigation-map.md)

**代码职责：**

- [rlworkbench/contracts.py · validate_modules](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/contracts.py#L13) — 检查声明的信息流、模块引用、同事件循环和诊断信息流向。
- [rlworkbench/core.py · import_results](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L326) — 为真实外部系统接收完整人口和原始证据，不认证外部实现。

**对应测试：**

- [tests/test_contracts.py · ContractTests.test_diagnostic_taint_cannot_be_laundered_by_middle_module](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L46) — 声明的诊断信息不能经中间模块洗成行动输入。
- [tests/test_contracts.py · ContractTests.test_template_is_structurally_valid_but_only_proposed](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L76) — 结构成立与模块实现分开。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate-modules examples/designs/marl-crossplay.json
```

检查多智能体设计声明，不启动 MARL。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

```bash
python3 -m rlworkbench validate-modules examples/designs/gvf-option-ablation.json
```

检查 GVF/option 消融设计声明，不运行高层模块。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

**模板与配置：** [examples/designs/marl-crossplay.json](../examples/designs/marl-crossplay.json) · [examples/designs/gvf-option-ablation.json](../examples/designs/gvf-option-ablation.json) · [catalog/modules.json](../catalog/modules.json)

**能力缺口与结论边界：**

- 离线 OPE/Data2Online、机器人、LLM 经验学习和 MARL 不在原生执行器内；高层模块契约不是运行时信息流证明。
- 真实不可重置系统的纵向因果识别与安全执行需另设计，不能虚构独立生命期。

<a id="ops-evidence"></a>

## 32 · 如何画图、写结论和判断证据够不够

**问题：** 如何让每个结论对应合适的图、区间、反例与适用边界？

**原则：** 先报告差值、分布、失败、成本和逐任务异质性，再限定最强可支持主张；显著性或漂亮图不替代科学证据。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#ops-evidence) · [交互阅读版](handbook/index.html#ops-evidence)

**实践文档：** [docs/statistics.md](../docs/statistics.md) · [docs/iteration.md](../docs/iteration.md) · [docs/testing.md](../docs/testing.md)

**代码职责：**

- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 按固定环境和配对 seed 输出差值、区间、失败及方法边界。
- [rlworkbench/analysis.py · markdown_report](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L66) — 报告完整人口与逐方法/环境分值，明确 smoke 不证效能。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_paired_statistics_constant_difference_and_direction](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L121) — 检查配对差值和指标方向。
- [tests/test_workflow.py · WorkflowTests.test_missing_jobs_cannot_be_silently_scored](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L97) — 缺失人口不能进入完整比较。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench compare '{RUN_DIR}' --candidate constant_alpha --baseline sample_average
```

对完整 continual smoke 人口生成逐环境描述；不能宣称胜出。 操作类型：`read_only`。 前提：{RUN_DIR} 是默认 profiles/continual.json 的完整有效运行；保留失败与全部注册 seed。

```bash
python3 -m rlworkbench report '{RUN_DIR}'
```

只读输出实验人口及指标报告。 操作类型：`read_only`。 前提：{RUN_DIR} 是真实运行目录；没有 --out 时不创建报告文件。

**模板与配置：** [templates/decision-record.md](../templates/decision-record.md) · [templates/research-card.md](../templates/research-card.md)

**能力缺口与结论边界：**

- 没有自动绘图、等效/不劣检验、同时置信带或主张有效性认证。
- 现有配对 bootstrap 不校正 HPO、多重比较或任务分布抽样；正差比例不是 rliable 跨运行改善概率。

<a id="ops-checklist"></a>

## 33 · 课题组可直接使用的检查清单

**问题：** 人类和 agent 如何重复检查研究证据而不把勾选当作质量分数？

**原则：** 检查表要求给每项主张附实际证据；字段存在、进程退出成功和全部打勾都不能证明科学问题已经回答。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#ops-checklist) · [交互阅读版](handbook/index.html#ops-checklist)

**实践文档：** [docs/iteration.md](../docs/iteration.md) · [docs/testing.md](../docs/testing.md) · [docs/protocol-reference.md](../docs/protocol-reference.md)

**代码职责：**

- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 检查所声明的协议字段、预算、人口和能力，非科学设计审查。
- [rlworkbench/core.py · audit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L284) — 核对完整运行人口及文件一致性，不裁定效能。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_invalid_fields_rejected_before_execution](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L30) — 不完整结构不能进入执行。
- [tests/test_workflow.py · WorkflowTests.test_modified_result_or_artifacts_invalidate_job](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L108) — 已变更原始证据会被标为无效。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/continual.json
```

执行结构与原生能力检查。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

```bash
python3 -m rlworkbench audit '{RUN_DIR}'
```

将人口完整性作为人工科学审阅的输入。 操作类型：`read_only`。 前提：{RUN_DIR} 替换为待审真实运行目录。

**模板与配置：** [docs/research-handbook.html](../docs/research-handbook.html) · [templates/research-card.md](../templates/research-card.md) · [templates/decision-record.md](../templates/decision-record.md)

**能力缺口与结论边界：**

- HTML 勾选和导出只是本地工作辅助；自动检查不检查科学充分性、真实信息权限或因果解释。

<a id="appendix-comparators"></a>

## 34 · 补充原则：遗憾、能力泛化与压力测试

**问题：** regret 比较者、压力测试、options 和元学习的额外成本怎样声明？

**原则：** 比较者的未来信息、模型与切换权限写清；按可控轴测易中难与失效区；技能发现、规划和适应预算一起计账。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#appendix-comparators) · [交互阅读版](handbook/index.html#appendix-comparators)

**实践文档：** [docs/testing.md](../docs/testing.md) · [docs/prediction-abstraction-options.md](../docs/prediction-abstraction-options.md) · [docs/planning-and-architecture.md](../docs/planning-and-architecture.md) · [docs/continual.md](../docs/continual.md)

**代码职责：**

- [rlworkbench/engines.py · BanditStream.step](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L180) — 日志保留 selected_mean 与 optimal_mean，限于已知小型 bandit 的诊断比较者。
- [rlworkbench/contracts.py · validate_modules](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/contracts.py#L13) — 检查高层技能与规划声明的边界，不执行这些模块。

**对应测试：**

- [tests/test_contracts.py · ContractTests.test_delaying_privileged_information_does_not_make_it_legal](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L53) — 延迟的特权信息仍不能冒充合法行动输入。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate-modules examples/designs/gvf-option-ablation.json
```

核对技能/预测模块声明的依赖与权限。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

**模板与配置：** [examples/designs/gvf-option-ablation.json](../examples/designs/gvf-option-ablation.json) · [templates/module-card.md](../templates/module-card.md)

**能力缺口与结论边界：**

- 没有通用 regret 计算器或压力测试生成器；Bandit 日志的逐步最优期望不能推广为 MDP 最优控制值。
- 尚未实现 option 发现、元学习任务分布抽样及其成本统计。

<a id="appendix-templates"></a>

## 35 · 可复制模板与最小数据规范

**问题：** 怎样把空白研究模板、事件日志、逐运行汇总和机器协议对应起来？

**原则：** 原手册模板用于人工预注册与证据登记；CLI profile 是可执行协议格式，两者必须显式转换并逐字段审定，不能将 null 模板当正式实验。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#appendix-templates) · [交互阅读版](handbook/index.html#appendix-templates)

**实践文档：** [docs/protocol-reference.md](../docs/protocol-reference.md) · [docs/external-adapters.md](../docs/external-adapters.md) · [docs/extension-guide.md](../docs/extension-guide.md) · [docs/start-here.md](../docs/start-here.md)

**代码职责：**

- [rlworkbench/core.py · load](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L42) — 拒绝非有限 JSON 和重复键，避免协议解释歧义。
- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 执行协议交叉字段约束。
- [rlworkbench/engines.py · EventWriter.write](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L231) — 输出原生每转移事件；分析回到独立训练/生命期单位。
- [rlworkbench/core.py · import_results](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L326) — 外部 result/producer/原始文件一一绑定注册 job。

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_json_duplicate_keys_and_nan_rejected](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L172) — 拒绝歧义或非有限数据。
- [tests/test_workflow.py · WorkflowTests.test_external_import_complete_bound_raw_population](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L155) — 验证外部完整人口、原始文件与身份绑定。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate profiles/continual.json
```

检查一份实际可执行机器协议。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

```bash
python3 -m rlworkbench validate-modules templates/module-contract.json
```

检查一份设计契约，不将其视作算法实现。 操作类型：`read_only`。 前提：从仓库根运行，使用支持当前项目的 Python 环境。

**模板与配置：** [docs/research-handbook.html](../docs/research-handbook.html) · [schemas/protocol.schema.json](../schemas/protocol.schema.json) · [templates/research-card.md](../templates/research-card.md) · [templates/module-contract.json](../templates/module-contract.json) · [templates/decision.json](../templates/decision.json) · [examples/external-result.json](../examples/external-result.json) · [examples/external-producer.json](../examples/external-producer.json)

**能力缺口与结论边界：**

- 原手册六个下载模板保留在 HTML 内，与 JSON CLI schema 不是字节兼容的同一种格式。
- 没有自动把原 YAML/CSV 预注册模板转换成 CLI 协议或统计分析的通用迁移器。

<a id="appendix-reading"></a>

## 36 · 精读路线与术语对照

**问题：** 如何按问题读文献，再返回自己的失败和竞争解释？

**原则：** 先用实证设计明确估计对象，再补统计与实现，最后按持续目标和所选环境重写协议；术语始终附具体操作定义。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#appendix-reading) · [交互阅读版](handbook/index.html#appendix-reading)

**实践文档：** [docs/navigation-map.md](../docs/navigation-map.md) · [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/statistics.md](../docs/statistics.md) · [docs/continual.md](../docs/continual.md) · [docs/catalog.md](../docs/catalog.md)

**代码职责：**

当前无直接实现；按人工研究协议执行。

**对应测试：**

当前无直接实现；按人工研究协议执行。

**模板与配置：** [docs/research-handbook.html](../docs/research-handbook.html) · [docs/sources.json](../docs/sources.json)

**能力缺口与结论边界：**

- 阅读路线与术语是人工理解和 agent 交接入口，不是自动综述更新或算法知识完备性证明。

<a id="bibliography"></a>

## 37 · 来源登记与证据边界

**问题：** 如何把手册的原则追溯到论文、讲义、官方实现与核验范围？

**原则：** 来源记录保留版本、核验深度、贡献和边界；文献结果、作者经验、手册建议与本仓库实际运行分开。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

[阅读完整原理](handbook.md#bibliography) · [交互阅读版](handbook/index.html#bibliography)

**实践文档：** [docs/catalog.md](../docs/catalog.md) · [docs/navigation-map.md](../docs/navigation-map.md)

**代码职责：**

当前无直接实现；按人工研究协议执行。

**对应测试：**

当前无直接实现；按人工研究协议执行。

**模板与配置：** [docs/sources.json](../docs/sources.json) · [docs/research-handbook.html](../docs/research-handbook.html)

**能力缺口与结论边界：**

- 文献快照截至 2026-10-03；没有自动追踪上游论文、库版本或重新验证所有结论。
- 源文献提供方法论依据，不证明本仓库两个项目草案或高层模块已经有效。

<a id="extension-tutorial-adapter"></a>

## 教程独立算法与工作台的真实接入

**问题：** 怎样在不重写算法的条件下绑定教程源码、可比任务和完整人口？

**原则：** 先锁定任务、指标、单位、预算与源身份，再执行可信本地实现；失败与未知结束分开。

**当前支持：所述工具已实现。** 状态只描述下列子项；不表示本章全部方法已实现。

**实践文档：** [docs/tutorial-adapter.md](../docs/tutorial-adapter.md) · [docs/external-adapters.md](../docs/external-adapters.md)

**代码职责：**

- [rlworkbench/tutorial_adapter.py · make_protocol](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/tutorial_adapter.py#L42) — 从META生成同任务同指标同单位同预算的外部smoke协议，并绑定完整教程源码摘要。
- [rlworkbench/tutorial_adapter.py · produce](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/tutorial_adapter.py#L78) — 执行已锁定完整人口，保留原始记录与失败回执，交给既有外部导入。

**对应测试：**

- [tests/test_tutorial_adapter.py · TutorialAdapterTests.test_complete_population_imports_and_partial_failure_is_retained](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_tutorial_adapter.py#L32) — 成功与中途失败均进入既有导入审计，拒绝覆盖旧attempt。
- [tests/test_tutorial_adapter.py · TutorialAdapterTests.test_source_drift_rejected_before_creating_attempt](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_tutorial_adapter.py#L56) — 源码漂移在新尝试创建前拒绝。

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench import-results --help
```

查看教程生产者完成后使用的既有全人口导入命令；生产者命令详见专题文档。 操作类型：`read_only`。

**能力缺口与结论边界：**

- 教学任务不等于原论文基准复现；META内部计步与评价语义仍需科学审阅。
- 没有HPO、集群调度、完整解析依赖锁或checkpoint恢复。

<a id="extension-mechanism-design"></a>

## 整体机制设计与推导桥

**问题：** 新增机制通过什么可被反证的路径改变完整学习程序的收益？

**原则：** 依次区分外部目标、合法状态、模块目标、算子几何、信用时钟、近似实现和全生命期效能。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

**实践文档：** [docs/mechanism-design.md](../docs/mechanism-design.md) · [docs/algorithm-design.md](../docs/algorithm-design.md) · [docs/testing.md](../docs/testing.md)

**代码职责：**

- [rlworkbench/contracts.py · validate_modules](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/contracts.py#L13) — 检查声明的模块依赖与权限；不认证机制或理论
- [rlworkbench/engines.py · td_target](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L221) — 经典目标与终止语义的真实可执行参照

**对应测试：**

- [tests/test_contracts.py · ContractTests.test_diagnostic_taint_cannot_be_laundered_by_middle_module](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L46) — 特权诊断经中间模块传播的反例
- [tests/test_engines.py · EngineTests.test_external_time_limit_preserves_actual_observation_and_bootstrap](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L104) — 外部截断不冒充任务终止

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate-modules templates/module-contract.json
```

检查已有示例声明，不执行模块 操作类型：`read_only`。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [templates/module-card.md](../templates/module-card.md) · [templates/module-contract.json](../templates/module-contract.json)

**能力缺口与结论边界：**

- 没有自动推导、普遍收敛或因果识别认证
- 模块声明检查不能发现未声明的运行时信息流
- 同基座机制实验仍需研究者或外部算法适配器实现

<a id="extension-project-lifetimes"></a>

## 两个项目的完整生命期研究

**问题：** 学习控制或表征记忆修改能否在静态、变化、回访、新规则和长期成本中保持增量价值？

**原则：** 外部强方法与共同基座控制并行；隐藏变化不送入 agent；完整生命期是统计单位。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

**实践文档：** [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md) · [docs/project-patterns.md](../docs/project-patterns.md) · [docs/continual.md](../docs/continual.md) · [docs/mechanism-design.md](../docs/mechanism-design.md)

**代码职责：**

- [rlworkbench/continual_metrics.py · summarize](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/continual_metrics.py#L12) — 由原始奖励计算生命期、分段、恢复与结束类别
- [rlworkbench/core.py · validate](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L79) — 验证外部提案的协议字段与预算
- [rlworkbench/engines.py · BanditLearner](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L157) — 不接收变化标签的最小在线估计器

**对应测试：**

- [tests/test_continual_metrics.py · ContinualMetricTests.test_completed_nonrecovery_censoring_and_crash_are_distinct](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_continual_metrics.py#L34) — 区分未恢复、删失与算法失败
- [tests/test_engines.py · EngineTests.test_hidden_boundaries_and_no_lifetime_reset](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L54) — 变化不重置 learner 或暴露边界
- [tests/test_workflow.py · WorkflowTests.test_proposed_adapter_cannot_be_frozen](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L198) — 阻止未就绪适配提案冻结成可执行承诺

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate protocols/streamrate-development.json --external
```

只验证 StreamRate 开发提案结构 操作类型：`read_only`。

```bash
python3 -m rlworkbench plan protocols/representation-development.json --external --summary
```

预览表征记忆提案人口与预算，不运行 操作类型：`read_only`。

**模板与配置：** [protocols/streamrate-development.json](../protocols/streamrate-development.json) · [protocols/representation-development.json](../protocols/representation-development.json) · [profiles/continual.json](../profiles/continual.json)

**能力缺口与结论边界：**

- 两个实际项目的外部训练适配器仍未实现
- 提案尚未登记为正式实验且不构成实际结果
- 没有完整遗忘、可塑性或跨生命期生存分析后端

<a id="extension-prediction-abstraction-options"></a>

## GVF、抽象、子目标与 options

**问题：** 预测知识如何成为合法、有用且可持续维护的时间抽象能力？

**原则：** 先核问题定义与真值，再核可达性、时间边界和消费者，最后测原始控制收益与长期维护。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

**实践文档：** [docs/prediction-abstraction-options.md](../docs/prediction-abstraction-options.md) · [docs/mechanism-design.md](../docs/mechanism-design.md) · [docs/navigation-map.md](../docs/navigation-map.md)

**代码职责：**

- [rlworkbench/contracts.py · validate_modules](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/contracts.py#L13) — 验证预测与控制模块的声明结构；不是 GVF 或 option 学习器

**对应测试：**

- [tests/test_contracts.py · ContractTests.test_template_is_structurally_valid_but_only_proposed](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L76) — 模板通过结构检查仍保留 proposed 状态
- [tests/test_contracts.py · ContractTests.test_delayed_recurrent_cycle_is_allowed](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L58) — 显式延迟信息循环允许存在

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate-modules templates/module-contract.json
```

检查可扩展模块合同示例，不执行 GVF 或 option 操作类型：`read_only`。

**模板与配置：** [templates/module-card.md](../templates/module-card.md) · [catalog/modules.json](../catalog/modules.json) · [examples/designs/gvf-option-ablation.json](../examples/designs/gvf-option-ablation.json)

**能力缺口与结论边界：**

- 没有原生 GVF、option、抽象或子目标学习实现
- 设计卡不是 run 接受的实验协议
- SMDP 时间折扣与问题版本迁移须由适配器新增语义测试

<a id="extension-planning-architecture"></a>

## 模型、规划与完整架构

**问题：** 模型学习、搜索计算和模块联合适应各自贡献了什么？

**原则：** 明确数据与计算双预算；固定/在线模型与规划形成对照；原子持久状态和声明信息权限须独立核验。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

**实践文档：** [docs/planning-and-architecture.md](../docs/planning-and-architecture.md) · [docs/mechanism-design.md](../docs/mechanism-design.md) · [docs/extension-guide.md](../docs/extension-guide.md)

**代码职责：**

- [rlworkbench/contracts.py · validate_modules](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/contracts.py#L13) — 检查模块连接、即时环与诊断污染
- [rlworkbench/core.py · import_results](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L326) — 接收已锁定人口的外部证据，不验证规划本身

**对应测试：**

- [tests/test_contracts.py · ContractTests.test_algebraic_same_cycle_is_rejected](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L63) — 拒绝未声明延迟的同周期循环
- [tests/test_contracts.py · ContractTests.test_delaying_privileged_information_does_not_make_it_legal](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_contracts.py#L53) — 延迟不消除信息特权
- [tests/test_workflow.py · WorkflowTests.test_external_import_complete_bound_raw_population](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L155) — 外部结果绑定完整人口与原始证据

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench validate-modules templates/module-contract.json
```

核对示例架构的声明结构 操作类型：`read_only`。

```bash
python3 -m rlworkbench import-results --help
```

查看外部架构结果导入合同入口 操作类型：`read_only`。

**模板与配置：** [templates/module-contract.json](../templates/module-contract.json) · [catalog/modules.json](../catalog/modules.json) · [examples/external-producer.json](../examples/external-producer.json) · [examples/external-result.json](../examples/external-result.json)

**能力缺口与结论边界：**

- 没有原生世界模型、Dyna、MuZero、Dreamer 或搜索执行器
- 模型调用/节点/通信/延迟需外部生产者计量
- 未实现整个持续架构的原子快照恢复验证

<a id="extension-multi-agent"></a>

## 多智能体与持续协作

**问题：** 方法是否改善独立训练团队对新队友或对手的协作，并遵守部署信息与资源制度？

**原则：** 区分团队信用、模块信用与元信用；CTDE 权限显式；联合人口为重复单位并保留 cross-play 矩阵。

**当前支持：人工研究协议。** 状态只描述下列子项；不表示本章全部方法已实现。

**实践文档：** [docs/multi-agent.md](../docs/multi-agent.md) · [docs/planning-and-architecture.md](../docs/planning-and-architecture.md) · [docs/mechanism-design.md](../docs/mechanism-design.md) · [docs/external-adapters.md](../docs/external-adapters.md)

**代码职责：**

- [rlworkbench/core.py · import_results](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L326) — 通用外部证据容器可用于团队结果；不提供 MARL 时钟或训练
- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 可作固定任务 paired-seed 摘要；不支持交叉人口随机效应

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_external_eval_cannot_be_zero_or_incomplete](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L188) — 通用外部结果不得漏掉注册评价；不是 MARL 正确性测试

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench import-results --help
```

查看通用外部导入参数，实际 MARL 接入前仍需团队级协议 操作类型：`read_only`。

**模板与配置：** [examples/designs/marl-crossplay.json](../examples/designs/marl-crossplay.json) · [templates/module-card.md](../templates/module-card.md)

**能力缺口与结论边界：**

- 没有原生 MARL 算法、环境适配器或团队身份测试
- 没有 cross-play 聚类、交叉随机效应或 exploitability 分析
- 设计卡尚不是可执行实验协议，通用导入器不验证 CTDE 信息流

<a id="extension-persistent-evidence"></a>

## 持久学习、检索与任务内计算的分离

**问题：** 未来收益来自持久学习、已有库的检索，还是更多任务内计算？

**原则：** 用参数学习、记忆写入和检索开关分离知识来源；比较新 C 与旧 A；计入发现、维护与搜索全部成本。

**当前支持：部分工具支持。** 状态只描述下列子项；不表示本章全部方法已实现。

**实践文档：** [docs/mechanism-design.md](../docs/mechanism-design.md) · [docs/continual.md](../docs/continual.md) · [docs/continual-project-playbooks.md](../docs/continual-project-playbooks.md) · [docs/prediction-abstraction-options.md](../docs/prediction-abstraction-options.md)

**代码职责：**

- [rlworkbench/continual_metrics.py · summarize](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/continual_metrics.py#L12) — 只支持原始生命期与恢复基础诊断，不自动识别持久学习因果来源
- [rlworkbench/engines.py · _run_bandit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/engines.py#L238) — 最小在线生命期累计奖励路径

**对应测试：**

- [tests/test_continual_metrics.py · ContinualMetricTests.test_full_lifetime_and_segments_include_every_raw_reward](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_continual_metrics.py#L6) — 初期与适应期奖励不从主结果中删除
- [tests/test_engines.py · EngineTests.test_eval_budget_does_not_change_training](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_engines.py#L135) — 独立诊断评价不改变原训练轨迹

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench continual-metrics --help
```

查看生命期日志分析参数；需真实日志才产生诊断 操作类型：`read_only`。

**模板与配置：** [templates/research-card.md](../templates/research-card.md) · [templates/module-card.md](../templates/module-card.md) · [profiles/continual.json](../profiles/continual.json)

**能力缺口与结论边界：**

- 没有持久记忆开关矩阵的训练后端
- 窗口恢复不能替代迁移、保留、新规则学习或可塑性证据
- 完整架构的学习/检索/计算成本须外部登记

<a id="extension-agent-iteration"></a>

## 人类与 agent 的证据驱动迭代

**问题：** 如何让每轮结果改变下一项有边界的研究决定，而不是自动扩大训练？

**原则：** 保留、修订、确认或停止引用实际证据；继承已成立的有限结论并重检受影响假设。

**当前支持：所述工具已实现。** 状态只描述下列子项；不表示本章全部方法已实现。

**实践文档：** [AGENTS.md](../AGENTS.md) · [docs/iteration.md](../docs/iteration.md) · [docs/mechanism-design.md](../docs/mechanism-design.md) · [skills/rl-research-iteration/SKILL.md](../skills/rl-research-iteration/SKILL.md)

**代码职责：**

- [rlworkbench/core.py · next_protocol](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L392) — 依据显式决策生成不冻结且不执行的后继草案
- [rlworkbench/core.py · audit](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/core.py#L284) — 核查已登记人口、结果身份与文件摘要
- [rlworkbench/analysis.py · compare](https://github.com/ying-wen/rl-research-workbench/blob/main/rlworkbench/analysis.py#L33) — 输出固定任务配对效应摘要，供人工研究决定

**对应测试：**

- [tests/test_workflow.py · WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L136) — 后继不运行且确认使用保留种子
- [tests/test_workflow.py · WorkflowTests.test_failed_jobs_are_kept_not_dropped](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L78) — 保留失败人口
- [tests/test_workflow.py · WorkflowTests.test_missing_jobs_cannot_be_silently_scored](https://github.com/ying-wen/rl-research-workbench/blob/main/tests/test_workflow.py#L97) — 拒绝对未完整人口静默评分

**可用命令（从仓库根运行，花括号路径须替换）：**

```bash
python3 -m rlworkbench next --help
```

查看明确决策到下一研究的工具参数 操作类型：`read_only`。

**模板与配置：** [templates/iteration-log.md](../templates/iteration-log.md) · [templates/decision-record.md](../templates/decision-record.md) · [templates/decision.json](../templates/decision.json) · [templates/research-card.md](../templates/research-card.md)

**能力缺口与结论边界：**

- 不会自动证明机制、选择科学问题或批准算力
- 保留种子和哈希不能替代任务分布隔离或团队测试访问纪律
- implemented_tool 只指后继草案与审计工具，不表示整个科学迭代可以自动完成
