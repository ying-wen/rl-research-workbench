# 模块卡：<GVF / representation / abstraction / subgoal / option / planner>

- 模块 ID、版本、来源论文/代码/许可证：
- 父架构、研究卡、角色与责任人：
- 状态：design_only / implemented / computation_checked / module_evaluated / control_confirmed。
- 被解决的问题、原目标与会删去模块的结果：

## 信息、目标、时间

- 决策前可见历史；研究者专属字段与禁止使用的未来：
- 输入状态/表征的构造及是否假设 Markov：
- 目标定义与单位；经验标签来源、可得时间、评价时间：
- 参数与持久状态；更新、输出、重置的先后次序：
- 模块问题定义变化与参数学习如何区分、记录版本：

## 按模块补充

| 类别 | 必填合同 |
|---|---|
| GVF | target policy、behavior policy、cumulant、continuation、terminal payoff、多尺度单位、覆盖/离策略修正 |
| 表征/抽象 | 历史映射、合并规则、奖励/转移/价值保持主张、混淆反例、学习模型与特征的区别 |
| 子目标 | 目标集合/事件、判定器、启动分布、成功与时限、未来标签/后见重标记权限 |
| option | initiation、intra-policy、termination、中断权、实际 duration、半 MDP target、三种终止边界 |
| 规划 | primitive/option model、累计奖励/discount/终点分布、搜索预算、真实与模型交互区分 |

## 测试与对照

- 手算/真值/边界/恢复测试：
- 独立准确性、校准、可达性或组合误差指标：
- primitive / 固定 / 随机 / 学习 / oracle 对照与信息权限：
- 同容量、同经验、同计算分别控制什么：
- 与下游模块的 2×2 或更高交互；哪些交互未识别：
- 完整原始收益、成本和失败；不能支持的外推：

## 持续维护

- 问题/技能出生、删除、替换、冻结、复用规则与事件：
- ID、旧预测、trace、优化状态和 memory 的版本迁移：
- A→B→A / 新 C、隐藏变化轴、长期资源上限：
- 所有发现尝试、失败技能、维护和重学成本如何保留：
- 下一阶段出口；修订与停止条件：

参见 [GVF、抽象与 options 实践](../docs/prediction-abstraction-options.md)。
