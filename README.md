# RL Research Workbench

**供人类研究者与 AI agent 共用的强化学习实践手册和迭代工具。** 从问题、推导和可否证预测出发，把实现检查、机制诊断、完整性能实验与下一轮决策连起来。覆盖经典 RL、深度 RL 和持续 RL。

先读 [十分钟开始](docs/start-here.md)。持续强化学习项目直接进入 [持续实验原则](docs/continual.md) 和 [两个项目的生命期实验方案](docs/continual-project-playbooks.md)。它们分别处理 **StreamRate 的学习控制与元信用**、**网络表征与记忆结构**。

| 你要做什么 | 入口 | 产物 |
|---|---|---|
| 开始一个问题 | [算法设计](docs/algorithm-design.md) · [研究卡](templates/research-card.md) | 原目标、合法信息、竞争解释、可推翻条件 |
| 检验实现与机制 | [测试方法](docs/testing.md) | 手算反例、时序测试、强基线与因子对照 |
| 设计持续实验 | [CRL 手册](docs/continual.md) · [项目方案](docs/continual-project-playbooks.md) | 完整生命期、变化与回访、恢复及长期资源预算 |
| 扩展智能体能力 | [能力地图](docs/navigation-map.md) · [GVF、抽象与 options](docs/prediction-abstraction-options.md) | 预测问题、子目标、技能和抽象的逐层验证 |
| 组合完整系统 | [规划与架构](docs/planning-and-architecture.md) · [多智能体](docs/multi-agent.md) | 模块目标、资源与信息契约、整体对照和跨团队泛化 |
| 执行并分析 | [迭代流程](docs/iteration.md) · [统计手册](docs/statistics.md) | 锁定协议、完整人口、失败记录、配对分析 |
| 让 agent 接手 | [AGENTS.md](AGENTS.md) · [研究技能](skills/rl-research-iteration/SKILL.md) | 可追溯决策与短交接，不自动扩算力 |
| 接入新方法和环境 | [扩展指南](docs/extension-guide.md) · [目录](docs/catalog.md) · [外部接入](docs/external-adapters.md) | 独立适配器、版本与能力边界、原始证据 |
| 查论据 | [完整调研快照](docs/research-handbook.html) · [81 条来源记录](docs/sources.json) | 论文、讲义、实现经验与适用边界 |

## 先运行一个小实验

需要 Python 3.9+。基础示例仅使用标准库；在仓库根运行即可。推荐独立虚拟环境，工具按源码 checkout 使用。

```bash
git clone https://github.com/ying-wen/rl-research-workbench.git
cd rl-research-workbench
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m rlworkbench init --profile classic --out studies/classic.json
.venv/bin/python -m rlworkbench validate studies/classic.json
.venv/bin/python -m rlworkbench plan studies/classic.json
.venv/bin/python -m rlworkbench freeze studies/classic.json --out studies/classic.lock.json
.venv/bin/python -m rlworkbench run studies/classic.lock.json --out runs/classic
.venv/bin/python -m rlworkbench report runs/classic
.venv/bin/python -m rlworkbench compare runs/classic --candidate sarsa --baseline q_learning
```

结果目录必须是新目录。运行后保留 `lock.json`、依赖版本、每条实验的原始事件、指标及失败；`audit` 检查人口与文件摘要。失败、缺失和损坏分别报告。失败的预定分值构成复合指标，不被解释为真实回报。

| profile | 当前实际能力 | 用途边界 |
|---|---|---|
| `classic` | 自写教学 CliffGrid，Q-learning / Sarsa，独立冻结评价 | 校验终止、截断、备份目标及完整执行流程 |
| `continual` | 样本均值 / 常数步长 bandit；静态与隐藏切换对照 | 整段在线奖励、变化与回访的最小工作例 |
| `deep` | 可选 SB3 PPO / CartPole，两组固定参数，独立冻结评价 | 依赖与真实神经训练通路检查；不是 PPO 调优结果 |

三个 profile 默认都是 **smoke**。两个 seed 是快速演示配置，绝非统计充分性的建议。更复杂算法和环境在目录中标为 `reference_only`，不因为被列出就成为已实现集成。

深度示例先在自己的环境安装：

```bash
.venv/bin/python -m pip install -r examples/deep-requirements.txt
.venv/bin/python -m rlworkbench init --profile deep --out studies/deep.json
# 此后按同样的 validate → plan → freeze → run 顺序操作
```

依赖与实际验证范围见 [深度示例验证记录](docs/deep-validation.md)。环境变化后需要重新做兼容性检查。完整依赖解析结果记录在每次运行的 `runtime.json`；两个顶层固定版本不是可移植的完整依赖锁。

## 支持持续迭代的约定

1. **问题先于改动。** 每个模块有经验来源、可测目标，以及会让我们删掉它的结果。
2. **证据分层。** 方程恒等、实现正确、局部作用、完整生命期收益、跨任务泛化分别验收。
3. **先保留强对手。** 原作者完整算法、同基座移植和内部消融明确区分。
4. **开发和确认分开。** 先完成各方法开发与选择；锁定后才使用新生命期、新种子。测试集访问纪律需要团队执行，哈希不能替代隔离。
5. **失败属于人口。** 不按完成前缀排名；不删不利任务或种子；修复产生新版本和新 attempt。
6. **每轮有决定。** 继续、修改、确认或停止；`next` 根据明确决策生成新草案，不自动宣告成功或启动下一轮。

```bash
# 编辑模板，使 parent_study_id 和 evidence 指向本次实际工作
mkdir -p decisions
cp templates/decision.json decisions/classic-v1.json
.venv/bin/python -m rlworkbench next studies/classic.lock.json \
  --decision decisions/classic-v1.json --study-id classic-development-v2 \
  --out studies/classic-development-v2.json
```

`next` 的输出仍需审阅修改；新目的、足够预算、各方法调参及统计计划不能由命令替你决定。`smoke` 不允许直接升级为确认实验。

## 适合两个当前项目的扩展方式

**学习控制主线**先区分基础更新方向、critic 评价、调率、延迟信用和当前提交价值；在共同基座上做有判别力的机制实验，完整方法比较继续保留外部强基线。

**表征与记忆主线**依次检验编码、跨步记忆、步内计算、选择性共享与特殊拓扑。参数、状态存储、交互和计算对照各有职责；秩或稀疏度改善不能替代控制收益。

两者都应覆盖静态保持、隐藏变化、旧规则回访和真正新规则，并以**完整生命期原始奖励**为主结果。两个机器协议在 [protocols/](protocols/) 中明确标为待接入的开发方案；不会自动调用原项目或服务器。详见 [项目经验模式](docs/project-patterns.md)。

## GVF 到完整智能体的模块契约

GVF、多时间尺度预测、options、子目标、状态或模型抽象、世界模型、规划、记忆、学习控制、协调和整体架构都用相同问题连接：**何时获得什么信息，学习什么，如何检验，如何影响后续决策，花费多少真实资源。** 文档覆盖各自的具体测试与因子对照；[模块目录](catalog/modules.json) 保留未来接入位置。

```bash
python3 -m rlworkbench validate-modules templates/module-contract.json
```

契约检查拒绝未知模块引用、未声明的即时循环和声明为诊断信息却流向行动的路径；它不是运行时信息流证明。当前这些高层模块都是设计与协议支持，尚未作为原生算法实现。可读模板见 [模块卡](templates/module-card.md)，机器结构见 [模块契约](templates/module-contract.json)。

持续诊断可直接读取一条原始事件日志，例如默认 continual 示例中的变化任务：

```bash
# 先查看 profile 中的实际变化间隔与输出 job_id，以下参数只是说明
python3 -m rlworkbench continual-metrics runs/STUDY/jobs/JOB/events.jsonl \
  --changes 200,400,600 --window 20 --persistence 3 --tolerance 0.05 \
  --planned-steps 800 --end-reason completed
```

变化索引从零开始，奖励时钟从1开始；只能分析对应协议的实际日志。窗口不增加独立样本数，阈值可能在新任务不可达。完整字段和可执行命令见 [协议参考](docs/protocol-reference.md)。

## 验证与范围

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
# 安装可选深度依赖后
RLWORKBENCH_TEST_DEEP=1 python3 -m unittest discover -s tests -v
```

v0.1 提供有意精简的本地顺序执行器与外部结果导入规范。没有集群调度器、自动 HPO、完整 RL 算法库、自动显著性晋升或生产级远程证明。研究代码可在原框架中开发；本仓库管理可复用规范、计划、证据和决策。完整文献快照截至 2026-10-03，实践文档随迭代维护。

[贡献指南](CONTRIBUTING.md) · [版本记录](CHANGELOG.md) · [许可证](LICENSE)
