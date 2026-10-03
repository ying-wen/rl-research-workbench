# 一次完整实验：比较之前，先检查证据

本例使用仓库原生的 CliffGrid、Q-learning 与 Sarsa。目的是学会使用工作台。默认只有两个训练种子，每个方法训练 3000 步。这不是判断两个算法孰优孰劣的实验。

## 1. 先明确问题与预算

在仓库根运行以下命令。需要 Python 3.9+，这个例子不需要第三方依赖。`studies/walkthrough*` 和 `runs/walkthrough` 必须尚不存在。重复操作时使用新名称。

```bash
python3 -m rlworkbench init --profile classic --out studies/walkthrough.json
python3 -m rlworkbench validate studies/walkthrough.json
python3 -m rlworkbench plan studies/walkthrough.json --summary
```

打开生成的 JSON。先核对五件事：

1. `purpose` 是 `smoke`。本次运行检查工作流，不确认效果。
2. 两个算法使用各自正确的备份目标。Sarsa 使用下一个采样动作；Q-learning 使用动作价值的最大值。
3. 两个种子、两个方法、一个环境，共四个训练运行。六个评价 episode 不会把独立训练样本数变成十二。
4. 每个运行最多有 3000 次训练交互和 600 次评价交互。矩阵上限是 14400 次环境交互。
5. 主指标是冻结评价回报。训练时的探索行为与评价策略不是同一个对象。

`plan` 只列出计划，不启动训练。如果改变问题、预算或方法，先修改草案，再检查。不要修改已经执行过的锁文件。

## 2. 锁定、执行、审计

```bash
python3 -m rlworkbench freeze studies/walkthrough.json --out studies/walkthrough.lock.json
python3 -m rlworkbench run studies/walkthrough.lock.json --out runs/walkthrough
python3 -m rlworkbench audit runs/walkthrough
```

审计输出应覆盖四个预定作业。检查 `completed`、`failed`、`missing` 和 `invalid`，不要只查看成功作业。`population_complete` 表示预定人口已被交代，不表示每个算法正确，也不表示假设成立。

查看以下文件，理解每份证据的职责：

| 文件 | 用它回答什么 | 不能用它证明什么 |
|---|---|---|
| `lock.json` | 原先计划比较谁，预算和源文件身份是什么？ | 计划是否科学充分 |
| `runtime.json` | 这次执行使用哪些实际依赖与运行时？ | 在其他机器必然逐位一致 |
| `jobs/` 中的逐步事件 | 每步发生了什么，训练和评价是否分开？ | 这些时间点是独立训练样本 |
| 作业终态与摘要 | 哪些完成、失败或损坏，摘要能否重算？ | 某个方法普遍优越 |

环境目标终止时不再 bootstrap。训练脚本的时间截断未必终止所定义的任务。这个区别应先通过微型更新测试，再通过完整轨迹核对。

## 3. 生成报告并正确解读比较

```bash
python3 -m rlworkbench report runs/walkthrough
python3 -m rlworkbench compare runs/walkthrough --candidate sarsa --baseline q_learning --bootstrap 2000
```

`report` 输出 Markdown。`compare` 输出 JSON。比较单位是同一环境中按训练 seed 配对的运行。正值表示 candidate 相对于 baseline 改善；这是经过指标方向处理后的差值。

两对数据可能恰好具有相同差值。此时经验 bootstrap 区间会退化成一个点。这不是没有统计不确定性。增加 bootstrap 次数只会更精确地重采样这两对数据，不会创造新的训练运行。

同样，不要因为 Q-learning 的这次冻结评价更好，就推断它在探索期间更安全。训练损失、训练回报、冻结评价和风险是不同的测量对象。要比较风险，需要事先规定风险指标及相应实验。

## 4. 写下一决定

先检查实现。如果 target、截断或评价隔离错误，修复并建立新版本。如果实现正确但两条曲线不同，先提出竞争解释：探索是否相同，评价是否关闭探索，预算是否足够，是否比较了不同策略。

接着填 [研究卡](../templates/research-card.md) 与 [决策记录](../templates/decision-record.md)。决定可以是增加诊断、调整开发设计、在新种子上独立确认，或者停止。工具不会把一次 smoke 运行自动升级成确认实验。

## 5. 换成持续问题时，改变什么？

`continual` profile 改用静态与隐藏切换 bandit。主指标包括整个生命期的在线奖励。变化时不重置学习器，也不把真实相位交给 agent。它可用于检查样本均值与常数步长的跟踪差异；不能用于证明神经网络保持可塑性。

要引入 GVF、options 或新的深度智能体，先查看 [当前支持矩阵](catalog.md)。未接入的方法需要外部适配器或新的原生实现。写出模块契约不等于模块已经能运行。

下一步：[实验设计](algorithm-design.md) · [测试方法](testing.md) · [统计分析](statistics.md) · [实用化路线](practical-roadmap.md)。
