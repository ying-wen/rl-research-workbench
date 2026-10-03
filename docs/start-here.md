# 从一个可判定问题开始

这份实践手册用于人类研究者和研究 agent 协作改进强化学习算法。每轮产物是一个能被证据支持、修订或否定的判断。运行器帮助固定协议、执行有限矩阵、保留结果；科学判断由研究负责人和审查者完成。

首次使用先走下方闭环，再阅读与你的问题对应的专题。[整体机制设计](mechanism-design.md) 连接目标、合法信息、更新、信用与生命期证据。文献背景在 [37 章全文](handbook.md)，通过 [逐章映射](handbook-code-map.md) 找代码与工具，来源版本与核验边界在 [sources.json](sources.json)。本手册是对文献经验的操作化综合，不是已被某篇论文证明的通用最优流程。

研究预测知识、状态抽象、子目标、options 或层级规划时，使用 [GVF、抽象与 options 实践](prediction-abstraction-options.md)和[模块卡](../templates/module-card.md)，先验证各模块合同，再检验它们对整体控制的增量作用。

## 1. 选择轨道与问题

| 轨道 | 适合的首个问题 | 最小判别实验 | 升级条件 |
|---|---|---|---|
| 经典 RL | 更新式、探索、信用分配是否按预期工作？ | 可枚举小 MDP、手算轨迹、已知值函数；随后闭环控制 | 算子与边界测试通过；对预测的正例和反例均解释得通 |
| 现代深度 RL | 一个机制在函数近似和交互分布中是否仍有效？ | 固定数据诊断、共同基座干预、完整方法比较 | 环境/网络/优化语义明确；独立确认预算可承担 |
| 持续 RL | 过去的经验是否改善未来适应，代价是什么？ | 多条完整生命期、非平稳或部分可观测任务、学习/冻结/记忆对照 | 生命周期状态连续；变化与信息权限明确；长期资源可控 |

deep 是函数近似维度，continual 是学习问题与时间协议维度，两者可以交叉。严格 streaming 另约束数据访问；小 batch 或没有 replay 不足以证明持续学习。

## 2. 本地完成一次最短闭环

在仓库根目录执行。基础包只用 Python 标准库；`deep` profile 的运行依赖可选后端，先使用 `classic` 熟悉流程。

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m rlworkbench init --profile classic --out studies/demo.json
.venv/bin/python -m rlworkbench validate studies/demo.json
.venv/bin/python -m rlworkbench plan studies/demo.json
.venv/bin/python -m rlworkbench freeze studies/demo.json --out studies/demo.lock.json
.venv/bin/python -m rlworkbench run studies/demo.lock.json --out runs/demo
.venv/bin/python -m rlworkbench report runs/demo
```

先阅读生成的 study，确认方法、种子、终点和成本，再冻结。`plan` 只列计划；`freeze` 固定当前协议与被纳入的源文件身份；`run` 才产生运行证据。profile 默认预算用于检查工作流，不能据此宣布算法普遍优越。完整目录中的环境条目也不意味着已实现和测试原生适配。

随后把[研究卡](../templates/research-card.md)复制为本轮问题说明，填写预期方向、竞争解释、失败处理、独立单位、最小有意义效应。为每一轮分配新 study ID 与输出目录；已运行目录保留。不要通过覆盖配置把开发结果改称确认结果。

## 3. 人类与 agent 的分工

| 角色 | 负责决定 | 交接产物 |
|---|---|---|
| 研究负责人 | 问题、目标分布、实际价值、资源和停止边界 | [项目章程](../templates/project-charter.md)、选定的一张研究卡 |
| 设计/实现者 | 算法推导、最小改动、测试与有效配置 | 更新伪代码、改动说明、测试记录 |
| 运行者 | 按锁定矩阵执行、记录每个作业和故障 | 锁文件、完整作业清单、原始记录 |
| 独立审查者 | 竞争解释、信息泄漏、统计单位、结论强度 | [决策记录](../templates/decision-record.md)、反例和下一步 |

同一人可兼任多个角色，但应把决定写在看确认结果之前。多 agent 并行时，一人拥有公共协议，一人拥有每个运行；先划分文件与作业所有权。审查者不重复启动未知状态的同一作业。没有独立人员时，用明确的第二遍审查替代虚构的“独立审核”。

## 4. 每轮只选一个下一步

按[迭代流程](iteration.md)决定：实现错误→修复并重新验证；机制被反例推翻→修订解释或停止；区间太宽→判断新增独立样本是否值得；配置选择完成→锁定后独立确认；确认失败→保留负结果，旧确认集转为开发数据。

没有“自动晋级冠军”。分数最高只是一个观察。任何自动执行都应有明确作业数、计算上限和终止条件；agent 不因失败而无限调参，也不把运行更久当作唯一进展。

依据：[Empirical Design in RL](https://jmlr.org/papers/v25/23-0183.html)、[Spinning Up as a Deep RL Researcher](https://spinningup.openai.com/en/latest/spinningup/spinningup.html)、[RL-Glue](https://www.jmlr.org/papers/v10/tanner09a.html)。
