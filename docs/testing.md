# 从接口正确到控制有效的测试阶梯

每个测试声明它能支持的结论。通过导入、有限数值或 smoke 运行，只能证明对应执行路径可用。测试数量、代码覆盖率和漂亮曲线都不能代替控制收益证据。

## 所有方法先过环境合同

记录 observation/action 空间与单位、奖励原值和变换、时间尺度、动作重复、终止、截断、自动重置以及计步规则。给一条固定动作序列，手工核对环境转移和奖励。针对稀疏奖励，验证奖励确实可达；针对随机环境，验证指定外生随机性和复位可重复。

Gymnasium 的 `terminated` 与 `truncated` 不能直接合成一个万能 bootstrap mask。任务真正终止一般阻断 bootstrap；人为时间截断常需从最终有效 observation 继续 bootstrap。若终点本就是有限时域任务的一部分，还需将剩余时间纳入状态或按该目标处理。自动重置接口必须取到 terminal/final observation，不能用新回合初态替代。

## 经典 RL 的最小测试菜单

| 对象 | 具体试验 | 必须检查 |
|---|---|---|
| Bandit | 已知均值的固定/漂移臂，固定随机事件 | 更新计数、探索规则、均值估计；regret 的 oracle 定义 |
| DP/价值预测 | 2–5 状态可解 MDP、固定策略 | Bellman 残差、真值、终止边界；迭代和同步顺序 |
| TD/MC | 一条手算轨迹、零奖励、γ=0 | TD 目标、步长、终端自举；与相应参考式一致 |
| Sarsa/Q-learning | 下一动作不同于贪心动作的小例子 | on/off-policy 目标确实不同；探索覆盖与收敛假设分开 |
| 资格迹 | λ=0、延迟奖励、reset 和重复状态 | accumulating/replacing/Dutch trace 各自定义；跨边界是否清理 |
| Off-policy | 可算重要性比、行为零支持反例 | 比率截断、支持条件、偏差；不把收敛假设外失败藏掉 |
| 平均奖励 | 小型 continuing MDP 与恒定奖励平移 | 差分价值与奖励率更新；不混成折扣目标 |

对数值更新采用独立手算或参考式，别在测试中复制同一实现错误。利用零步长、关闭模块等边界检查退化到已知算法；有限差分验证可微机制时，固定随机路径并说明随机/不连续操作的限制。

## 深度算法重点审计

| 家族 | 优先检查 |
|---|---|
| DQN/Rainbow | action gather、目标网络和 stop-gradient、Double Q 选择/评估分离、n-step 跨终止、分布投影质量守恒、replay 权重 |
| PPO/Actor–Critic | rollout 时 old log-prob 固定；优势和价值目标；概率比、裁剪方向、KL、熵；GAE bootstrap 与 trace mask 分开 |
| SAC/TD3 | target 构造、双 critic、动作尺度、tanh Jacobian、温度定义、延迟更新、target smoothing 的边界 |
| RNN | 序列切分、burn-in、hidden state 来源、padding mask；reset 语义与任务一致 |
| 模型学习 | 训练/评测数据隔离、rollout 长度、模型误差随使用分布变化；真实交互和模型步分别计数 |

PPO 的 advantage 通常不沿策略 loss 回传，是否每个 epoch 重算由具体算法定义；不要将某实现惯例写成所有 PPO 的数学必需条件。episodic 环境的 hidden state 常在终止清理，continuing 重生或 meta-learning 跨 episode 记忆应按合同处理。

## 保存恢复和评价隔离

短运行分成连续执行与中途恢复两条，对比状态、奖励和参数。checkpoint 可能需要网络、优化器、目标网络、replay、归一化、日程、RNN、trace、元状态、环境与所有 RNG。不能恢复世界时，明确只能恢复 learner，不能称整条生命期精确续跑。

冻结策略的诊断评估使用独立副本，不能修改训练 RNG、归一化、buffer 或 recurrent state。在线持续评估可以合法更新，那是另一种目标，必须在协议中标注。提高评估频率后训练结果改变，是检查隔离的实用信号。

## 由低成本到正式确认

顺序为手算/边界→短轨迹→小型闭环→机制正反例→开发矩阵→新独立确认。每级先定义预期，再执行。smoke 可采用少量 seed，但其通过标准是工作流和记录完整；大规模收益结论由正式协议决定。

失败按“实现错误、已知假设外反例、算法数值失败、基础设施故障”分开。错误修复后重跑受影响门；旧结果标为无效并保留原因。假设外反例按预期出现可证明测试有判别力，不能因为它让图难看就删除。

依据：[True Online TD](https://jmlr.org/papers/v17/15-599.html)、[Gymnasium 时间限制](https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/)、[VectorEnv Autoreset](https://farama.org/Vector-Autoreset-Mode)、[PPO 37 项实现细节](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/)。算法公式与配方见[完整手册](research-handbook.html#alg-classical)。
