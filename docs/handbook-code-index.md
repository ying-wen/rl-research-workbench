# 从代码、测试与协议反查手册

修改一个文件前，先查看它承接哪些原理、验证哪些子问题。索引覆盖映射中实际引用的文件；没有引用的实现仍须补登记，不能由本工具自动判断完备性。

[全文](handbook.md) · [逐章映射](handbook-code-map.md) · [机制设计](mechanism-design.md)

```bash
python3 scripts/handbook.py find rlworkbench/continual_metrics.py --json
python3 scripts/handbook.py find GVF
python3 scripts/handbook.py check
```

## AGENTS.md

[打开文件](../AGENTS.md)

- [01 · 如何使用这份手册](handbook-code-map.md#guide-scope) · `docs`
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `docs`

## catalog/algorithms.json

[打开文件](../catalog/algorithms.json)

- [02 · 研究脉络：不同群体分别解决了什么问题](handbook-code-map.md#guide-lineage) · `assets`
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `assets`
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `assets`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `assets`

## catalog/environments.json

[打开文件](../catalog/environments.json)

- [02 · 研究脉络：不同群体分别解决了什么问题](handbook-code-map.md#guide-lineage) · `assets`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `assets`
- [18 · 持续强化学习：把整个生命期作为实验对象](handbook-code-map.md#crl-framing) · `assets`
- [21 · 基准选择：原始协议与建议变体必须分开](handbook-code-map.md#crl-benchmarks) · `assets`
- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](handbook-code-map.md#crl-recipe-a) · `assets`
- [27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？](handbook-code-map.md#crl-recipe-b) · `assets`

## catalog/modules.json

[打开文件](../catalog/modules.json)

- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `assets`
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `assets`
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `assets`

## docs/algorithm-design.md

[打开文件](../docs/algorithm-design.md)

- [02 · 研究脉络：不同群体分别解决了什么问题](handbook-code-map.md#guide-lineage) · `docs`
- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `docs`
- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `docs`
- [08 · 跨环境设置与超参数敏感性：峰值之外的算法品质](handbook-code-map.md#stats-sensitivity) · `docs`
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `docs`
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `docs`
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `docs`
- [24 · 机制归因对照：每个对照回答一个问题](handbook-code-map.md#crl-controls) · `docs`
- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](handbook-code-map.md#crl-recipe-a) · `docs`
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `docs`
- [36 · 精读路线与术语对照](handbook-code-map.md#appendix-reading) · `docs`
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `docs`

## docs/catalog.md

[打开文件](../docs/catalog.md)

- [02 · 研究脉络：不同群体分别解决了什么问题](handbook-code-map.md#guide-lineage) · `docs`
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `docs`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `docs`
- [21 · 基准选择：原始协议与建议变体必须分开](handbook-code-map.md#crl-benchmarks) · `docs`
- [36 · 精读路线与术语对照](handbook-code-map.md#appendix-reading) · `docs`
- [37 · 来源登记与证据边界](handbook-code-map.md#bibliography) · `docs`

## docs/continual-project-playbooks.md

[打开文件](../docs/continual-project-playbooks.md)

- [08 · 跨环境设置与超参数敏感性：峰值之外的算法品质](handbook-code-map.md#stats-sensitivity) · `docs`
- [18 · 持续强化学习：把整个生命期作为实验对象](handbook-code-map.md#crl-framing) · `docs`
- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `docs`
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `docs`
- [24 · 机制归因对照：每个对照回答一个问题](handbook-code-map.md#crl-controls) · `docs`
- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](handbook-code-map.md#crl-recipe-a) · `docs`
- [27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？](handbook-code-map.md#crl-recipe-b) · `docs`
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `docs`
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `docs`
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `docs`
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `docs`

## docs/continual.md

[打开文件](../docs/continual.md)

- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `docs`
- [18 · 持续强化学习：把整个生命期作为实验对象](handbook-code-map.md#crl-framing) · `docs`
- [19 · 目标、时间与被比较的系统](handbook-code-map.md#crl-objectives) · `docs`
- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `docs`
- [21 · 基准选择：原始协议与建议变体必须分开](handbook-code-map.md#crl-benchmarks) · `docs`
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `docs`
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `docs`
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `docs`
- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](handbook-code-map.md#crl-recipe-a) · `docs`
- [27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？](handbook-code-map.md#crl-recipe-b) · `docs`
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `docs`
- [36 · 精读路线与术语对照](handbook-code-map.md#appendix-reading) · `docs`
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `docs`
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `docs`

## docs/deep-validation.md

[打开文件](../docs/deep-validation.md)

- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `docs`

## docs/extension-guide.md

[打开文件](../docs/extension-guide.md)

- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `docs`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `docs`
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `docs`
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `docs`

## docs/external-adapters.md

[打开文件](../docs/external-adapters.md)

- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `docs`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `docs`
- [21 · 基准选择：原始协议与建议变体必须分开](handbook-code-map.md#crl-benchmarks) · `docs`
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `docs`
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `docs`
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `docs`
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `docs`
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `docs`
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `docs`
- [教程独立算法与工作台的真实接入](handbook-code-map.md#extension-tutorial-adapter) · `docs`
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `docs`

## docs/iteration.md

[打开文件](../docs/iteration.md)

- [01 · 如何使用这份手册](handbook-code-map.md#guide-scope) · `docs`
- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `docs`
- [05 · 统计、调参与算力：明确一次实验究竟估计什么](handbook-code-map.md#stats-framework) · `docs`
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `docs`
- [09 · 种子数量与统计功效：用可检测差异决定预算](handbook-code-map.md#stats-power) · `docs`
- [12 · 显著性、实际价值与多重比较](handbook-code-map.md#stats-comparisons) · `docs`
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `docs`
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `docs`
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `docs`
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `docs`
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `docs`
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `docs`
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `docs`
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `docs`

## docs/mechanism-design.md

[打开文件](../docs/mechanism-design.md)

- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `docs`
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `docs`
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `docs`
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `docs`
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `docs`
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `docs`
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `docs`

## docs/multi-agent.md

[打开文件](../docs/multi-agent.md)

- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `docs`
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `docs`

## docs/navigation-map.md

[打开文件](../docs/navigation-map.md)

- [18 · 持续强化学习：把整个生命期作为实验对象](handbook-code-map.md#crl-framing) · `docs`
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `docs`
- [36 · 精读路线与术语对照](handbook-code-map.md#appendix-reading) · `docs`
- [37 · 来源登记与证据边界](handbook-code-map.md#bibliography) · `docs`
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `docs`

## docs/planning-and-architecture.md

[打开文件](../docs/planning-and-architecture.md)

- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `docs`
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `docs`
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `docs`
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `docs`
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `docs`

## docs/prediction-abstraction-options.md

[打开文件](../docs/prediction-abstraction-options.md)

- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](handbook-code-map.md#crl-recipe-a) · `docs`
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `docs`
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `docs`
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `docs`
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `docs`

## docs/project-patterns.md

[打开文件](../docs/project-patterns.md)

- [02 · 研究脉络：不同群体分别解决了什么问题](handbook-code-map.md#guide-lineage) · `docs`
- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `docs`
- [24 · 机制归因对照：每个对照回答一个问题](handbook-code-map.md#crl-controls) · `docs`
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `docs`

## docs/protocol-reference.md

[打开文件](../docs/protocol-reference.md)

- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `docs`
- [05 · 统计、调参与算力：明确一次实验究竟估计什么](handbook-code-map.md#stats-framework) · `docs`
- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `docs`
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `docs`
- [09 · 种子数量与统计功效：用可检测差异决定预算](handbook-code-map.md#stats-power) · `docs`
- [10 · 区间回答不同问题：均值确定，不代表运行稳定](handbook-code-map.md#stats-intervals) · `docs`
- [11 · 跨任务聚合：同时保留分布形状与实际改善量](handbook-code-map.md#stats-aggregate) · `docs`
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `docs`
- [19 · 目标、时间与被比较的系统](handbook-code-map.md#crl-objectives) · `docs`
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `docs`
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `docs`
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `docs`
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `docs`

## docs/research-handbook.html

[打开文件](../docs/research-handbook.html)

- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `assets`
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `assets`
- [36 · 精读路线与术语对照](handbook-code-map.md#appendix-reading) · `assets`
- [37 · 来源登记与证据边界](handbook-code-map.md#bibliography) · `assets`

## docs/sources.json

[打开文件](../docs/sources.json)

- [02 · 研究脉络：不同群体分别解决了什么问题](handbook-code-map.md#guide-lineage) · `assets`
- [11 · 跨任务聚合：同时保留分布形状与实际改善量](handbook-code-map.md#stats-aggregate) · `assets`
- [21 · 基准选择：原始协议与建议变体必须分开](handbook-code-map.md#crl-benchmarks) · `assets`
- [27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？](handbook-code-map.md#crl-recipe-b) · `assets`
- [36 · 精读路线与术语对照](handbook-code-map.md#appendix-reading) · `assets`
- [37 · 来源登记与证据边界](handbook-code-map.md#bibliography) · `assets`

## docs/start-here.md

[打开文件](../docs/start-here.md)

- [01 · 如何使用这份手册](handbook-code-map.md#guide-scope) · `docs`
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `docs`
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `docs`

## docs/statistics.md

[打开文件](../docs/statistics.md)

- [02 · 研究脉络：不同群体分别解决了什么问题](handbook-code-map.md#guide-lineage) · `docs`
- [05 · 统计、调参与算力：明确一次实验究竟估计什么](handbook-code-map.md#stats-framework) · `docs`
- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `docs`
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `docs`
- [08 · 跨环境设置与超参数敏感性：峰值之外的算法品质](handbook-code-map.md#stats-sensitivity) · `docs`
- [09 · 种子数量与统计功效：用可检测差异决定预算](handbook-code-map.md#stats-power) · `docs`
- [10 · 区间回答不同问题：均值确定，不代表运行稳定](handbook-code-map.md#stats-intervals) · `docs`
- [11 · 跨任务聚合：同时保留分布形状与实际改善量](handbook-code-map.md#stats-aggregate) · `docs`
- [12 · 显著性、实际价值与多重比较](handbook-code-map.md#stats-comparisons) · `docs`
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `docs`
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `docs`
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `docs`
- [27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？](handbook-code-map.md#crl-recipe-b) · `docs`
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `docs`
- [36 · 精读路线与术语对照](handbook-code-map.md#appendix-reading) · `docs`

## docs/testing.md

[打开文件](../docs/testing.md)

- [01 · 如何使用这份手册](handbook-code-map.md#guide-scope) · `docs`
- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `docs`
- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `docs`
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `docs`
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `docs`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `docs`
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `docs`
- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `docs`
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `docs`
- [24 · 机制归因对照：每个对照回答一个问题](handbook-code-map.md#crl-controls) · `docs`
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `docs`
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `docs`
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `docs`
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `docs`
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `docs`

## docs/tutorial-adapter.md

[打开文件](../docs/tutorial-adapter.md)

- [教程独立算法与工作台的真实接入](handbook-code-map.md#extension-tutorial-adapter) · `docs`

## examples/deep-requirements.txt

[打开文件](../examples/deep-requirements.txt)

- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `assets`

## examples/designs/gvf-option-ablation.json

[打开文件](../examples/designs/gvf-option-ablation.json)

- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `assets`
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `assets`
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `assets`

## examples/designs/marl-crossplay.json

[打开文件](../examples/designs/marl-crossplay.json)

- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `assets`
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `assets`

## examples/external-producer.json

[打开文件](../examples/external-producer.json)

- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `assets`
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `assets`

## examples/external-result.json

[打开文件](../examples/external-result.json)

- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `assets`
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `assets`

## profiles/classic.json

[打开文件](../profiles/classic.json)

- [05 · 统计、调参与算力：明确一次实验究竟估计什么](handbook-code-map.md#stats-framework) · `assets`
- [10 · 区间回答不同问题：均值确定，不代表运行稳定](handbook-code-map.md#stats-intervals) · `assets`
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `assets`
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `assets`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `assets`
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `assets`
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `assets`

## profiles/continual.json

[打开文件](../profiles/continual.json)

- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `assets`
- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `assets`
- [08 · 跨环境设置与超参数敏感性：峰值之外的算法品质](handbook-code-map.md#stats-sensitivity) · `assets`
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `assets`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `assets`
- [18 · 持续强化学习：把整个生命期作为实验对象](handbook-code-map.md#crl-framing) · `assets`
- [19 · 目标、时间与被比较的系统](handbook-code-map.md#crl-objectives) · `assets`
- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `assets`
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `assets`
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `assets`
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `assets`
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `assets`

## profiles/deep.json

[打开文件](../profiles/deep.json)

- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `assets`
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `assets`
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `assets`
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `assets`

## protocols/representation-development.json

[打开文件](../protocols/representation-development.json)

- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `assets`
- [24 · 机制归因对照：每个对照回答一个问题](handbook-code-map.md#crl-controls) · `assets`
- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](handbook-code-map.md#crl-recipe-a) · `assets`
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `assets`
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `assets`

## protocols/streamrate-development.json

[打开文件](../protocols/streamrate-development.json)

- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `assets`
- [24 · 机制归因对照：每个对照回答一个问题](handbook-code-map.md#crl-controls) · `assets`
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `assets`
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `assets`
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `assets`

## rlworkbench/analysis.py

[打开文件](../rlworkbench/analysis.py)

- [05 · 统计、调参与算力：明确一次实验究竟估计什么](handbook-code-map.md#stats-framework) · `code` · `compare` — 分别在固定环境内计算已登记候选相对基线的配对差值，并输出明确局限。
- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `code` · `compare` — 以固定环境内配对 seed 为重采样单位；不把 episode 或 checkpoint 当独立样本。
- [10 · 区间回答不同问题：均值确定，不代表运行稳定](handbook-code-map.md#stats-intervals) · `code` · `paired_interval` — 对完整配对差值有放回抽样，返回均值的 percentile bootstrap 区间；默认 95%。
- [10 · 区间回答不同问题：均值确定，不代表运行稳定](handbook-code-map.md#stats-intervals) · `code` · `compare` — 逐环境同时输出差值列表、均值、中位数、样本标准差和 bootstrap 区间。
- [11 · 跨任务聚合：同时保留分布形状与实际改善量](handbook-code-map.md#stats-aggregate) · `code` · `compare` — 仅输出每个固定环境的配对差值，不合并不同环境原始回报；正差配对比例明确不是 rliable 的跨运行改善概率。
- [11 · 跨任务聚合：同时保留分布形状与实际改善量](handbook-code-map.md#stats-aggregate) · `code` · `markdown_report` — 按环境与方法分别报告完成/失败/缺失/无效及含失败分值的均值。
- [12 · 显著性、实际价值与多重比较](handbook-code-map.md#stats-comparisons) · `code` · `compare` — 仅允许已登记基线，按 maximize/minimize 统一改善方向，输出 minimum_effect 与未校正声明。
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `code` · `compare` — 拒绝不完整或无效人口的比较；对实际算法失败使用预先登记的复合分值并标注估计对象变化。
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `code` · `compare` — 按固定环境和配对 seed 输出差值、区间、失败及方法边界。
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `code` · `markdown_report` — 报告完整人口与逐方法/环境分值，明确 smoke 不证效能。
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `code` · `compare` — 可作固定任务 paired-seed 摘要；不支持交叉人口随机效应
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `code` · `compare` — 输出固定任务配对效应摘要，供人工研究决定

## rlworkbench/cli.py

[打开文件](../rlworkbench/cli.py)

- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `code` · `main` — continual-metrics 筛选 train 或 training 标签的训练转移并验证 env_step 连续，排除评价事件。

## rlworkbench/continual_metrics.py

[打开文件](../rlworkbench/continual_metrics.py)

- [19 · 目标、时间与被比较的系统](handbook-code-map.md#crl-objectives) · `code` · `summarize` — 区分完整生命期均值与 observed-prefix 均值。
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `code` · `summarize` — 从逐步原始奖励计算生命期/阶段统计及以前阶段基线为参照的恢复诊断。
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `code` · `summarize` — 生成阶段奖励与变化后恢复诊断，不能替代机制归因。
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `code` · `summarize` — 由原始奖励计算生命期、分段、恢复与结束类别
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `code` · `summarize` — 只支持原始生命期与恢复基础诊断，不自动识别持久学习因果来源

## rlworkbench/contracts.py

[打开文件](../rlworkbench/contracts.py)

- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `code` · `validate_modules` — 检查声明的信息权限和模块连接；不验证运行时真实信息流。
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `code` · `validate_modules` — 检查声明的信息流、模块引用、同事件循环和诊断信息流向。
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `code` · `validate_modules` — 检查高层技能与规划声明的边界，不执行这些模块。
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `code` · `validate_modules` — 检查声明的模块依赖与权限；不认证机制或理论
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `code` · `validate_modules` — 验证预测与控制模块的声明结构；不是 GVF 或 option 学习器
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `code` · `validate_modules` — 检查模块连接、即时环与诊断污染

## rlworkbench/core.py

[打开文件](../rlworkbench/core.py)

- [01 · 如何使用这份手册](handbook-code-map.md#guide-scope) · `code` · `audit` — 按锁定人口核对完成、失败、缺失、无效与 claim_status；不评审机制或科学效能。
- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `code` · `validate` — 检查主指标、改善方向、最小效应、预算与分层 checks 的声明，并验证原生指标兼容性。
- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `code` · `plan` — 展开方法×环境×种子的完整人口，使预定交互预算可核对。
- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `code` · `validate` — 要求 implementation、mechanism、performance 三类非空检查声明；只检查存在，不执行其自然语言判据。
- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `code` · `next_protocol` — 根据带证据引用的明确决策创建后继草案；不决定候选是否有效。
- [05 · 统计、调参与算力：明确一次实验究竟估计什么](handbook-code-map.md#stats-framework) · `code` · `validate` — 要求主指标、方向、minimum_effect、预选方法与选择规则；不推断任务总体。
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `code` · `validate` — 当前只允许 preselected arms，并检查开发与保留种子分离以及确认选择摘要。
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `code` · `freeze` — 把配置、计划和工作台源码摘要绑定到不可原地覆盖的锁文件。
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `code` · `next_protocol` — 从开发决策选定方法并改用保留种子形成确认草案；不搜索超参。
- [08 · 跨环境设置与超参数敏感性：峰值之外的算法品质](handbook-code-map.md#stats-sensitivity) · `code` · `plan` — 可展开人工登记的固定配置 arms×环境×种子矩阵；不会构造搜索空间、选择最优配置或计算敏感性。
- [09 · 种子数量与统计功效：用可检测差异决定预算](handbook-code-map.md#stats-power) · `code` · `validate` — 只检查 minimum_effect 非负、种子去重、schema 最低数量与最大交互预算；不计算功效。
- [09 · 种子数量与统计功效：用可检测差异决定预算](handbook-code-map.md#stats-power) · `code` · `plan` — 将人工选定的样本数转换为完整人口和最大交互成本。
- [12 · 显著性、实际价值与多重比较](handbook-code-map.md#stats-comparisons) · `code` · `next_protocol` — 要求显式决策与证据引用，不根据正差或区间自动晋升。
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `code` · `freeze` — 保存协议、全部计划 job、源码摘要和运行时版本。
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `code` · `audit` — 逐项对账完整计划人口与工件摘要，区分失败、缺失和无效。
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `code` · `runtime` — 记录 Python 与已安装关键深度依赖的版本；不是完整可移植依赖锁。
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `code` · `import_results` — 对外部生产者的完整预定人口、原始工件和来源记录做导入验证；不认证外部环境或 OPE 方法。
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `code` · `validate` — 要求按 implementation、mechanism、performance 分层登记测试意图。
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `code` · `check_measurements` — 对完成运行核对训练时域、评价人口与有限主指标。
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `code` · `validate` — 检查开发/保留 seed 不交叠，确认人口与父开发选择身份一致。
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `code` · `next_protocol` — 由明确决策选择方法并使用保留 seed 建立待审确认草案。
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `code` · `freeze` — 绑定注册协议、作业清单与工作台源文件摘要。
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `code` · `check_measurements` — 完成回执必须达到注册训练时域及评价计数。
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `code` · `audit` — 区分完成、失败、缺失、无效，保留计划人口。
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `code` · `import_results` — 导入完整外部人口并绑定原始文件。
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `code` · `plan` — 注册方法×环境×seed 的完整笛卡尔积。
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `code` · `freeze` — 固定协议、源码摘要与作业身份。
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `code` · `run` — 只在新目录运行锁定的原生计划。
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `code` · `next_protocol` — 基于显式决策生成后继草案，不自动选赢家或执行。
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `code` · `check_measurements` — 检查预算、终点、评价与有限指标，防止账本错误。
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `code` · `import_results` — 为真实外部系统接收完整人口和原始证据，不认证外部实现。
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `code` · `validate` — 检查所声明的协议字段、预算、人口和能力，非科学设计审查。
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `code` · `audit` — 核对完整运行人口及文件一致性，不裁定效能。
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `code` · `load` — 拒绝非有限 JSON 和重复键，避免协议解释歧义。
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `code` · `validate` — 执行协议交叉字段约束。
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `code` · `import_results` — 外部 result/producer/原始文件一一绑定注册 job。
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `code` · `validate` — 验证外部提案的协议字段与预算
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `code` · `import_results` — 接收已锁定人口的外部证据，不验证规划本身
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `code` · `import_results` — 通用外部证据容器可用于团队结果；不提供 MARL 时钟或训练
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `code` · `next_protocol` — 依据显式决策生成不冻结且不执行的后继草案
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `code` · `audit` — 核查已登记人口、结果身份与文件摘要

## rlworkbench/engines.py

[打开文件](../rlworkbench/engines.py)

- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `code` · `_seed` — 为教学引擎生成按命名空间派生的随机种子。
- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `code` · `BanditStream.step` — 按每步所有动作的潜在噪声生成奖励，避免动作选择改变外生噪声抽取顺序。
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `code` · `BanditLearner.update` — 实现样本均值或固定 alpha 的动作值递推。
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `code` · `td_target` — 区分 Q-learning 的 max backup 与 Sarsa 的下一采样动作，真正终止阻断 bootstrap。
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `code` · `CliffGrid.step` — 提供教学网格的悬崖非终止复位、目标终止与外部时间截断语义。
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `code` · `_run_ppo` — 调用可选 SB3 PPO/CartPole，按 rollout 整倍数训练，记录原始奖励并用新环境做独立冻结评价。
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `code` · `validate_job` — 检查 PPO rollout、batch 整除、预算和当前支持的参数。
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `code` · `validate_job` — 仅对原生教学环境与算法组合验证已知配置，未知环境显式报错。
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `code` · `td_target` — 提供可独立手算的 Sarsa/Q-learning 单步边界。
- [18 · 持续强化学习：把整个生命期作为实验对象](handbook-code-map.md#crl-framing) · `code` · `_run_bandit` — 一个生命期只初始化一次 learner，隐藏切换只写诊断，不传任务标识。
- [19 · 目标、时间与被比较的系统](handbook-code-map.md#crl-objectives) · `code` · `_run_bandit` — 每步累加实际原始奖励，最终除以注册步数。
- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `code` · `BanditStream.step` — 按隐藏相位生成每动作潜在奖励；每步的噪声向量与所选动作无关。
- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `code` · `BanditLearner.update` — 更新仅接收动作和奖励，不能读取 phase。
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `code` · `_run_bandit` — 动作先于该步反馈，在线收益包含探索成本。
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `code` · `_run_tabular` — 教学表格法训练后使用独立环境和随机流评价。
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `code` · `_run_ppo` — 可选 PPO 路径在独立环境中进行冻结策略评价。
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `code` · `EventWriter.write` — 记录可追溯原始转移、计数和有限 JSON 数据。
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `code` · `BanditStream.step` — 日志保留 selected_mean 与 optimal_mean，限于已知小型 bandit 的诊断比较者。
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `code` · `EventWriter.write` — 输出原生每转移事件；分析回到独立训练/生命期单位。
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `code` · `td_target` — 经典目标与终止语义的真实可执行参照
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `code` · `BanditLearner` — 不接收变化标签的最小在线估计器
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `code` · `_run_bandit` — 最小在线生命期累计奖励路径

## rlworkbench/tutorial_adapter.py

[打开文件](../rlworkbench/tutorial_adapter.py)

- [教程独立算法与工作台的真实接入](handbook-code-map.md#extension-tutorial-adapter) · `code` · `make_protocol` — 从META生成同任务同指标同单位同预算的外部smoke协议，并绑定完整教程源码摘要。
- [教程独立算法与工作台的真实接入](handbook-code-map.md#extension-tutorial-adapter) · `code` · `produce` — 执行已锁定完整人口，保留原始记录与失败回执，交给既有外部导入。

## schemas/protocol.schema.json

[打开文件](../schemas/protocol.schema.json)

- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `assets`

## skills/rl-research-iteration/SKILL.md

[打开文件](../skills/rl-research-iteration/SKILL.md)

- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `docs`

## templates/decision-record.md

[打开文件](../templates/decision-record.md)

- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `assets`
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `assets`
- [12 · 显著性、实际价值与多重比较](handbook-code-map.md#stats-comparisons) · `assets`
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `assets`
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `assets`
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `assets`
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `assets`
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `assets`

## templates/decision.json

[打开文件](../templates/decision.json)

- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `assets`
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `assets`
- [12 · 显著性、实际价值与多重比较](handbook-code-map.md#stats-comparisons) · `assets`
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `assets`
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `assets`
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `assets`

## templates/iteration-log.md

[打开文件](../templates/iteration-log.md)

- [01 · 如何使用这份手册](handbook-code-map.md#guide-scope) · `assets`
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `assets`
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `assets`
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `assets`
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `assets`
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `assets`

## templates/module-card.md

[打开文件](../templates/module-card.md)

- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `assets`
- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](handbook-code-map.md#crl-recipe-a) · `assets`
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `assets`
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `assets`
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `assets`
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `assets`
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `assets`

## templates/module-contract.json

[打开文件](../templates/module-contract.json)

- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `assets`
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `assets`
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `assets`
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `assets`

## templates/project-charter.md

[打开文件](../templates/project-charter.md)

- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `assets`
- [09 · 种子数量与统计功效：用可检测差异决定预算](handbook-code-map.md#stats-power) · `assets`

## templates/research-card.md

[打开文件](../templates/research-card.md)

- [01 · 如何使用这份手册](handbook-code-map.md#guide-scope) · `assets`
- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `assets`
- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `assets`
- [05 · 统计、调参与算力：明确一次实验究竟估计什么](handbook-code-map.md#stats-framework) · `assets`
- [08 · 跨环境设置与超参数敏感性：峰值之外的算法品质](handbook-code-map.md#stats-sensitivity) · `assets`
- [09 · 种子数量与统计功效：用可检测差异决定预算](handbook-code-map.md#stats-power) · `assets`
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `assets`
- [24 · 机制归因对照：每个对照回答一个问题](handbook-code-map.md#crl-controls) · `assets`
- [26 · 实验配方 A：持续适应的瓶颈究竟是可塑性还是状态构造？](handbook-code-map.md#crl-recipe-a) · `assets`
- [27 · 实验配方 B：任务序列中“少遗忘”是否换来了“学不动”？](handbook-code-map.md#crl-recipe-b) · `assets`
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `assets`
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `assets`
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `assets`
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `assets`
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `assets`
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `assets`
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `assets`
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `assets`

## tests/test_cli.py

[打开文件](../tests/test_cli.py)

- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `tests` · `CLITests.test_recovery_cli_checks_clock_and_completed_horizon` — 核对 CLI 的奖励时钟和完整时域。
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `tests` · `CLITests.test_continual_metrics_reads_native_training_stream` — 真实原生 bandit 日志进入 CLI；识别 train 标签，排除评价流，核对完整奖励。
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `tests` · `CLITests.test_documented_full_path_and_budget_summary` — 走通 CLI 的冻结、运行、审计和报告链。

## tests/test_continual_metrics.py

[打开文件](../tests/test_continual_metrics.py)

- [19 · 目标、时间与被比较的系统](handbook-code-map.md#crl-objectives) · `tests` · `ContinualMetricTests.test_full_lifetime_and_segments_include_every_raw_reward` — 核对阶段和全生命期奖励账本。
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `tests` · `ContinualMetricTests.test_confirmation_occurs_at_window_end_with_persistence` — 确认发生在最后一个连续合格窗口末端。
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `tests` · `ContinualMetricTests.test_completed_nonrecovery_censoring_and_crash_are_distinct` — 完整未恢复、观察提前结束和崩溃分开。
- [23 · 把收益、保留、可塑性与资源分别量化](handbook-code-map.md#crl-metrics) · `tests` · `ContinualMetricTests.test_scale_change_disables_recovery_claim` — 奖励尺度不可比时不宣称恢复。
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `tests` · `ContinualMetricTests.test_completed_nonrecovery_censoring_and_crash_are_distinct` — 区分未恢复、删失与算法失败
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `tests` · `ContinualMetricTests.test_full_lifetime_and_segments_include_every_raw_reward` — 初期与适应期奖励不从主结果中删除

## tests/test_contracts.py

[打开文件](../tests/test_contracts.py)

- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `tests` · `ContractTests.test_diagnostic_taint_cannot_be_laundered_by_middle_module` — 检查诊断特权经中间模块流向决策的声明路径会被拒绝。
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `tests` · `ContractTests.test_diagnostic_taint_cannot_be_laundered_by_middle_module` — 声明的诊断信息不能经中间模块洗成行动输入。
- [31 · 扩展场景：离线选择、真实系统、多智能体与大模型智能体](handbook-code-map.md#ops-extensions) · `tests` · `ContractTests.test_template_is_structurally_valid_but_only_proposed` — 结构成立与模块实现分开。
- [34 · 补充原则：遗憾、能力泛化与压力测试](handbook-code-map.md#appendix-comparators) · `tests` · `ContractTests.test_delaying_privileged_information_does_not_make_it_legal` — 延迟的特权信息仍不能冒充合法行动输入。
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `tests` · `ContractTests.test_diagnostic_taint_cannot_be_laundered_by_middle_module` — 特权诊断经中间模块传播的反例
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `tests` · `ContractTests.test_template_is_structurally_valid_but_only_proposed` — 模板通过结构检查仍保留 proposed 状态
- [GVF、抽象、子目标与 options](handbook-code-map.md#extension-prediction-abstraction-options) · `tests` · `ContractTests.test_delayed_recurrent_cycle_is_allowed` — 显式延迟信息循环允许存在
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `tests` · `ContractTests.test_algebraic_same_cycle_is_rejected` — 拒绝未声明延迟的同周期循环
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `tests` · `ContractTests.test_delaying_privileged_information_does_not_make_it_legal` — 延迟不消除信息特权

## tests/test_engines.py

[打开文件](../tests/test_engines.py)

- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `tests` · `EngineTests.test_potential_reward_noise_is_not_action_conditioned_rng` — 验证动作改变不改变下一步潜在奖励噪声的对齐。
- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `tests` · `EngineTests.test_identical_seed_reproduces_all_events` — 验证教学 bandit 在同配置和种子下复现全部事件。
- [06 · 随机单位、配对与重复：一个种子到底代表什么](handbook-code-map.md#stats-randomness) · `tests` · `EngineTests.test_eval_budget_does_not_change_training` — 验证表格示例的评价预算改变不影响训练事件和最终 Q。
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `tests` · `EngineTests.test_sample_average_is_exact_empirical_average` — 以固定奖励验证在线样本均值。
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `tests` · `EngineTests.test_constant_alpha_retains_recency` — 以手算序列验证常数步长近期加权。
- [14 · 经典强化学习：先建立可以被推翻的正确性证据](handbook-code-map.md#alg-classical) · `tests` · `EngineTests.test_external_time_limit_preserves_actual_observation_and_bootstrap` — 检查最终真实状态、Q-learning/Sarsa 不同 target 和终止遮罩。
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `tests` · `EngineTests.test_real_optional_ppo_budget_and_frozen_evaluation` — 可选真实 PPO 集成测试检查训练步、回合人口、评价冻结与 CPU 运行；需显式启用。
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `tests` · `EngineTests.test_missing_optional_dependencies_fail_with_actionable_message` — 验证缺少深度依赖时给出明确错误。
- [15 · 现代深度强化学习：把算法与实现共同视为被测对象](handbook-code-map.md#alg-deep) · `tests` · `EngineTests.test_unsupported_and_incomplete_configs_are_explicit_errors` — 验证不支持算法、未知配置及非法 PPO rollout/batch 约束被拒绝。
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `tests` · `EngineTests.test_unsupported_and_incomplete_configs_are_explicit_errors` — 检验环境/算法不兼容或未知配置不会静默执行。
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `tests` · `EngineTests.test_goal_termination_has_precedence_at_time_limit` — 验证真正目标终止与同一步时间限制重合时采用终止语义。
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `tests` · `EngineTests.test_eval_budget_does_not_change_training` — 检验表格冻结评价隔离，而非只检查评价曲线看似合理。
- [18 · 持续强化学习：把整个生命期作为实验对象](handbook-code-map.md#crl-framing) · `tests` · `EngineTests.test_hidden_boundaries_and_no_lifetime_reset` — 检查 bandit 的边界不可见和无生命期重置。
- [19 · 目标、时间与被比较的系统](handbook-code-map.md#crl-objectives) · `tests` · `EngineTests.test_full_lifetime_aggregation_uses_every_raw_reward` — 核对生命期每条原始奖励都参与主指标。
- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `tests` · `EngineTests.test_potential_reward_noise_is_not_action_conditioned_rng` — 检验动作改变不改变外生潜在奖励噪声的消费。
- [20 · 先辨明变化来源，再设计对照](handbook-code-map.md#crl-nonstationarity) · `tests` · `EngineTests.test_hidden_boundaries_and_no_lifetime_reset` — 检查隐藏边界不传 learner。
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `tests` · `EngineTests.test_eval_budget_does_not_change_training` — 评价预算变化不改变表格法训练事件前缀。
- [22 · 在线主评估，冻结与回访作为诊断](handbook-code-map.md#crl-evaluation) · `tests` · `EngineTests.test_tabular_frozen_eval_and_episode_accounting` — 核对冻结评价与回合计数。
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `tests` · `EngineTests.test_eval_budget_does_not_change_training` — 隔离评价对训练前缀的潜在污染。
- [整体机制设计与推导桥](handbook-code-map.md#extension-mechanism-design) · `tests` · `EngineTests.test_external_time_limit_preserves_actual_observation_and_bootstrap` — 外部截断不冒充任务终止
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `tests` · `EngineTests.test_hidden_boundaries_and_no_lifetime_reset` — 变化不重置 learner 或暴露边界
- [持久学习、检索与任务内计算的分离](handbook-code-map.md#extension-persistent-evidence) · `tests` · `EngineTests.test_eval_budget_does_not_change_training` — 独立诊断评价不改变原训练轨迹

## tests/test_tutorial_adapter.py

[打开文件](../tests/test_tutorial_adapter.py)

- [教程独立算法与工作台的真实接入](handbook-code-map.md#extension-tutorial-adapter) · `tests` · `TutorialAdapterTests.test_complete_population_imports_and_partial_failure_is_retained` — 成功与中途失败均进入既有导入审计，拒绝覆盖旧attempt。
- [教程独立算法与工作台的真实接入](handbook-code-map.md#extension-tutorial-adapter) · `tests` · `TutorialAdapterTests.test_source_drift_rejected_before_creating_attempt` — 源码漂移在新尝试创建前拒绝。

## tests/test_workflow.py

[打开文件](../tests/test_workflow.py)

- [01 · 如何使用这份手册](handbook-code-map.md#guide-scope) · `tests` · `WorkflowTests.test_run_and_receipts_reconcile` — 验证运行人口与原始奖励对账，并验证 smoke 报告保留 workflow_smoke_only。
- [03 · 先确定研究对象与目标函数](handbook-code-map.md#guide-objective) · `tests` · `WorkflowTests.test_overlap_and_budget_overrun_rejected` — 验证开发与保留种子重叠、计划超预算被拒绝。
- [04 · 算法设计：从失效机制到可反驳的改进](handbook-code-map.md#guide-design) · `tests` · `WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds` — 验证 next 不执行训练，拒绝 smoke 直接确认，确认使用保留种子并锁定选择。
- [05 · 统计、调参与算力：明确一次实验究竟估计什么](handbook-code-map.md#stats-framework) · `tests` · `WorkflowTests.test_paired_statistics_constant_difference_and_direction` — 检验配对均值差的方向与常数差值区间，不检验总体代表性或区间的普遍覆盖率。
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `tests` · `WorkflowTests.test_freeze_binds_config_jobs_and_source` — 验证协议、执行人口或源码漂移会使锁验证失败。
- [07 · 超参数测试：把选择、评估与搜索成本分开](handbook-code-map.md#stats-hpo) · `tests` · `WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds` — 验证确认种子来自保留人口、所选配置修改会失效，smoke 不能直接升级。
- [08 · 跨环境设置与超参数敏感性：峰值之外的算法品质](handbook-code-map.md#stats-sensitivity) · `tests` · `WorkflowTests.test_all_profiles_and_exact_population` — 仅验证预选 arms×envs×seeds 展开数量与协议一致。
- [09 · 种子数量与统计功效：用可检测差异决定预算](handbook-code-map.md#stats-power) · `tests` · `WorkflowTests.test_invalid_fields_rejected_before_execution` — 验证非法 seed 和非有限 minimum_effect 被拒绝；不验证 seed 数足够检出效应。
- [10 · 区间回答不同问题：均值确定，不代表运行稳定](handbook-code-map.md#stats-intervals) · `tests` · `WorkflowTests.test_paired_statistics_constant_difference_and_direction` — 检查常数差值区间退化为常数，单对样本被拒绝，最小化指标方向正确。
- [11 · 跨任务聚合：同时保留分布形状与实际改善量](handbook-code-map.md#stats-aggregate) · `tests` · `WorkflowTests.test_paired_statistics_constant_difference_and_direction` — 检验逐环境方向统一；没有覆盖 IQM 或跨任务 bootstrap。
- [12 · 显著性、实际价值与多重比较](handbook-code-map.md#stats-comparisons) · `tests` · `WorkflowTests.test_paired_statistics_constant_difference_and_direction` — 检验最大化/最小化的差值方向及配对摘要。
- [12 · 显著性、实际价值与多重比较](handbook-code-map.md#stats-comparisons) · `tests` · `WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds` — 验证决策创建新草案而非自动训练或自动确认有效。
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `tests` · `WorkflowTests.test_failed_jobs_are_kept_not_dropped` — 模拟算法失败，验证原始失败证据与预定分值保留，配对人口不缩水。
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `tests` · `WorkflowTests.test_missing_jobs_cannot_be_silently_scored` — 验证缺失 job 不被填成失败分数，且不能开始比较。
- [13 · 可直接执行的统计实验单](handbook-code-map.md#stats-recipe) · `tests` · `WorkflowTests.test_modified_result_or_artifacts_invalidate_job` — 验证改动原始事件或结果会被标为无效。
- [16 · 基准选择：让任务集合对应想要验证的能力](handbook-code-map.md#alg-benchmarks) · `tests` · `WorkflowTests.test_external_import_complete_bound_raw_population` — 验证外部人口完整、结果绑定锁与原始工件被保留；只验证封装。
- [17 · 可复制测试矩阵：通过条件与证据边界一起写](handbook-code-map.md#alg-test-matrix) · `tests` · `WorkflowTests.test_external_eval_cannot_be_zero_or_incomplete` — 验证外部结果不能用零评价步或不完整回合冒充完成评价。
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `tests` · `WorkflowTests.test_overlap_and_budget_overrun_rejected` — 拒绝人口交叠和预算超额。
- [25 · 生命期调参与版本约束](handbook-code-map.md#crl-tuning) · `tests` · `WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds` — 下一轮不自动运行，确认使用保留人口。
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `tests` · `WorkflowTests.test_missing_jobs_cannot_be_silently_scored` — 未完成不能悄悄补成分值后排名。
- [28 · 长期试验阶梯与最小交付包](handbook-code-map.md#crl-longrun) · `tests` · `WorkflowTests.test_failed_jobs_are_kept_not_dropped` — 失败运行保留在比较人口内。
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `tests` · `WorkflowTests.test_freeze_binds_config_jobs_and_source` — 修改配置、作业或源摘要会破坏锁身份。
- [29 · 实验执行：从预注册到独立确认](handbook-code-map.md#ops-workflow) · `tests` · `WorkflowTests.test_run_and_receipts_reconcile` — 核对计划、运行与回执对账。
- [30 · 诊断手册：症状、竞争解释与下一项实验](handbook-code-map.md#ops-diagnostics) · `tests` · `WorkflowTests.test_modified_result_or_artifacts_invalidate_job` — 检测修改结果和原始文件。
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `tests` · `WorkflowTests.test_paired_statistics_constant_difference_and_direction` — 检查配对差值和指标方向。
- [32 · 如何画图、写结论和判断证据够不够](handbook-code-map.md#ops-evidence) · `tests` · `WorkflowTests.test_missing_jobs_cannot_be_silently_scored` — 缺失人口不能进入完整比较。
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `tests` · `WorkflowTests.test_invalid_fields_rejected_before_execution` — 不完整结构不能进入执行。
- [33 · 课题组可直接使用的检查清单](handbook-code-map.md#ops-checklist) · `tests` · `WorkflowTests.test_modified_result_or_artifacts_invalidate_job` — 已变更原始证据会被标为无效。
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `tests` · `WorkflowTests.test_json_duplicate_keys_and_nan_rejected` — 拒绝歧义或非有限数据。
- [35 · 可复制模板与最小数据规范](handbook-code-map.md#appendix-templates) · `tests` · `WorkflowTests.test_external_import_complete_bound_raw_population` — 验证外部完整人口、原始文件与身份绑定。
- [两个项目的完整生命期研究](handbook-code-map.md#extension-project-lifetimes) · `tests` · `WorkflowTests.test_proposed_adapter_cannot_be_frozen` — 阻止未就绪适配提案冻结成可执行承诺
- [模型、规划与完整架构](handbook-code-map.md#extension-planning-architecture) · `tests` · `WorkflowTests.test_external_import_complete_bound_raw_population` — 外部结果绑定完整人口与原始证据
- [多智能体与持续协作](handbook-code-map.md#extension-multi-agent) · `tests` · `WorkflowTests.test_external_eval_cannot_be_zero_or_incomplete` — 通用外部结果不得漏掉注册评价；不是 MARL 正确性测试
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `tests` · `WorkflowTests.test_next_never_runs_and_confirmation_uses_reserved_seeds` — 后继不运行且确认使用保留种子
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `tests` · `WorkflowTests.test_failed_jobs_are_kept_not_dropped` — 保留失败人口
- [人类与 agent 的证据驱动迭代](handbook-code-map.md#extension-agent-iteration) · `tests` · `WorkflowTests.test_missing_jobs_cannot_be_silently_scored` — 拒绝对未完整人口静默评分
