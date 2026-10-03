# 协议与命令参考

本页定义 v0.1 实际支持的接口；研究设计判断仍在实践手册中。结构 schema 位于 [`protocol.schema.json`](../schemas/protocol.schema.json)，CLI 还检查交叉字段、预算、能力、种子隔离和模块连接。

## 协议字段

| 字段 | 含义与约束 |
|---|---|
| `study_id` | 新版本的安全字符串身份，不能拿旧 ID 覆盖已有运行 |
| `track` | classic / deep / continual；MARL等能力通过模块、外部环境与设计说明登记 |
| `purpose` | smoke / development / confirmation；smoke 只检验执行通路 |
| `question`, `hypothesis` | 问题、竞争解释和可推翻的预测 |
| `primary_metric`, `direction`, `minimum_effect` | 指标、正负方向、预定实际意义阈值；不自动执行显著性晋升 |
| `seeds`, `holdout_seeds` | 当前完整人口及保留人口，两者不交叠；最少2只是示例解析约束 |
| `arms`, `envs` | 算法和环境的身份、后端名及实际配置；展开为全笛卡尔积 |
| `budget` | 每条训练步数、评价回合、评价步数上限、全部人口的交互上限 |
| `selection` | 预先指定配置及选择规则；首版不提供自动HPO；确认通过父开发与决策摘要绑定方法、环境和保留种子 |
| `failure_policy` | 预先声明的失败复合分值；同时必须保留失败原因、时间与失败率 |
| `checks` | 实现、机制、性能三层各自需要的证据；字段存在不代表检查已通过 |
| `provenance` | 公开原始来源；完整版本/依赖/命令由 producer 或原生运行记录提供 |
| `input_adapter_ready` | false 的设计草案可以验证结构，但不能 freeze |
| `modules` | 可选高层模块声明；仅外部架构，当前内置教学引擎不会执行它 |

`steps` 必须在每个项目登记明确计数单位。原生单环境例为真实环境转移；MARL接入应选择联合转移，并在原始记录另保留各agent动作数。模拟步、梯度步、option终止次数不能偷换成真实交互步。除交互硬预算外，内存、规划、模型训练和墙钟需外部producer另行限额与记录。

## 命令与状态

```text
init --profile classic|deep|continual --out PROTOCOL
validate PROTOCOL [--external]
plan PROTOCOL [--external] [--summary]
freeze PROTOCOL --out LOCK [--external]
run LOCK --out NEW_DIRECTORY
import-results LOCK --input EXTERNAL_DIRECTORY --out NEW_DIRECTORY
audit RUN_DIRECTORY
report RUN_DIRECTORY [--out NEW_REPORT]
compare RUN_DIRECTORY --candidate ARM --baseline ARM [--bootstrap N]
next LOCK --decision DECISION --study-id NEW_ID --out NEW_PROTOCOL
validate-modules CONTRACT
continual-metrics EVENTS --changes INDICES --window W --planned-steps T
```

`plan --summary` 只显示人口和预算；去掉后显示每条job。生成文件默认拒绝覆盖。CLI错误退出码2，运行或审计存在失败/未完成人口退出码1，符合该命令检查的结果退出码0；退出0不是科学结论。

`freeze` 绑定协议、完整job清单、核心代码、测试文件及pyproject摘要；记录Python与四种可选顶层依赖版本。`run` 检查当前源码与这些版本是否一致。它不是完整容器或传递依赖锁，平台/BLAS/驱动仍会影响结果；研究级外部执行须另交依赖锁与平台资格。

job回执状态为completed或failed；尚无回执为missing，格式或哈希异常为invalid。缺失不能填失败分值。完整回执要求训练达到注册终点、评价预算与回合匹配、指标有限。原始文件列表与内容摘要需一致，源文件和结果摘要检测意外修改，不提供数字签名或远程真实性证明。

中断不会自动重试。先判断已有attempt的真实状态；需要恢复或重跑时，记录原因、重新登记独立attempt、保留原失败，并说明分析如何处理这两个attempt。首版没有checkpoint恢复调度器。

## 比较的精确含义

`compare` 使用同一固定环境、同一seed标签下的candidate−baseline差；最小化时反转符号。输出均值、样本标准差、中位数及按seed配对的95% percentile bootstrap区间。区间算法固定分析seed=0，默认10000次重采样。记录正差比例，但它不是rliable的跨独立运行改善概率。

任何missing/invalid/额外job都会拒绝比较；failed按预声明分值进入复合终点并单独计数。配对是否科学有效需审阅随机源设计；同一seed不保证同轨迹。首版不自动修正调参、多重比较、任务抽样，也不将小样本bootstrap视为充分精度证明。

## 持续指标

`continual-metrics` 接受一条标准`events.jsonl`，读取`type=transition, stream=train`（原生格式），也兼容外部生产者的`stream=training`；评价流不计入在线收益。要求env_step从1连续。`--changes`表示第一条新阶段奖励的从零索引；例如200意味着第201条转移起变化。`--baseline-window`默认等于window；`--persistence`默认1；`--tolerance`为绝对奖励容差；`--direction`默认maximize。

`--end-reason completed|censored|crash` 必须来自真实终态；提前结束不得写completed。`--different-reward-scale`禁用基于前一阶段数值阈值的恢复主张。输出完整或前缀生命期统计、阶段原始奖励及恢复状态；崩溃和普通右删失分开。不同生命期的聚合、生存分析和回访因果判别另行设计。

## 模块检查的限制

模块信息流由用户声明，检查器只检查这个声明。将未来信息错误标成agent信息不会被自动发现。通过结构检查后仍需事件级可见性审计、隔离评价、断链/滞后对照以及整个闭环实验。延迟环允许跨步记忆；同事件即时环需给出实际求解/调度语义，不能只画箭头。
