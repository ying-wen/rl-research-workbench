# 外部算法接入：固定协议，导入完整人口和原始证据

教程独立算法现有专用生产者：[META/run 接入流程](tutorial-adapter.md)。它复用本页的外部锁与全人口导入，不新增重复算法库；高级作者系统仍须独立适配。

工作台不需要重写每一个算法库。外部训练可以继续使用作者代码、现有集群或项目自己的运行器；本仓库负责预注册矩阵、身份绑定、完整性检查与统一分析。外部适配器承担把**一个锁定 job**交给真实算法并产生回执的责任。

这条路径支持自定义算法和环境，不能据此声称它们已由工作台复现。导入检查的是证据包装与预算，**不认证外部训练确实执行、指标计算正确或实现忠实**。SHA-256 是内容校验，不是签名、第三方见证或远程证明。

## 1. 先建外部协议，再运行

复制合适的 profile，修改研究问题、所有方法和任务、预算、seed 人口、指标、失败规则与来源。外部 ID 可以不同于原生 engine，但仍需满足协议的标识与矩阵规则。不要在看到外部结果后倒填一份“预注册”。

```bash
python -m rlworkbench freeze my-protocol.json --external --out external-lock.json
# 在你的外部系统执行 external-lock.json 中的每个 jobs[]；此处没有自动启动远程任务。
python -m rlworkbench import-results external-lock.json --input incoming-study --out runs/external-study
python -m rlworkbench audit runs/external-study
python -m rlworkbench report runs/external-study
```

以 CLI `--help` 和当前版本支持的命令为准。冻结时绑定工作台源码；原生执行还核对 Python 与顶层依赖版本漂移。导入前若工作台源码改变，重新版本化并明确记录，不修改原锁来绕过校验。标有 `input_adapter_ready: false` 的设计草案不能直接冻结；必须先落实适配与必要配置。

## 2. 输入目录必须一一对应计划

`incoming-study/` 顶层只能包含锁中规定的 job 子目录，名称就是 `job_id`；不能有额外 README、临时目录或缺失 job。每个目录至少包含：

```text
incoming-study/
  <job_id>/
    result.json
    producer.json
    events.jsonl          # 或真实的原始 CSV/日志；不限于这个文件名
    dependency-lock.txt   # 建议保存实际依赖内容
    command.txt           # 建议保存确切命令与非敏感配置
```

目录中不支持 symlink。源目录和输出目录应分离且不能互相包含。输出必须是新路径；不覆盖旧尝试。不知道运行是否仍在进行时，应先查原调度器的真实状态，不能填一个失败回执或盲目重跑。完整人口包括成功和已确定失败；尚未完成的任务使本次导入保持未完成。

## 3. `result.json` 合同

[可复制模板](../examples/external-result.json) 是格式示范，里面没有真实测量结果。填入锁内 `job_id` 与完整 `lock_sha256`，不要自行从方法简称猜出身份。

| 字段 | 导入器要求与含义 |
|---|---|
| `job_id` | 与所在目录、锁中 job 完全一致 |
| `lock_sha256` | 与传入锁完全一致 |
| `status` | 仅 `completed` 或 `failed` |
| `metrics` | 完成时必须是有限数值字典，并包含协议指定的 `primary_metric`；不能写 NaN/Infinity |
| `steps` | 完成时必须恰好等于注册的训练 horizon；不能以已完成前缀冒充终点 |
| `evaluation_steps` | 完成时是非负整数，不超过注册 `max_eval_steps`；有评价时至少覆盖注册的 episode 数 |
| `diagnostics.evaluation_episodes` | 完成时必须恰好等于注册 `eval_episodes`；无评价时为 0 |
| `failure` | 失败时必须为对象；建议 `{ "type": "...", "message": "..." }` |

失败记录保留真实可知的计数；未知计数用 `null` 并解释，不填零。失败时主分析按事先注册的 `failure_policy.score_floor` 处理，并另列失败率；这个分值是分析约定，不是算法实际获得的回报。如果不接受这种 estimand，应在启动前改变分析设计，不能事后挑一种有利处理。

原始奖励、报告分数与训练使用的缩放奖励应分别记录；主指标须与协议同单位。`mean_episode_return` 只包含完成 episode 时，必须解释未完成尾部如何处理；持续任务宜使用整段生命期指标。评价交互不能暗中计入训练，或反向写入训练 replay、normalizer、RNG。

## 4. `producer.json` 和原始材料

[生产者模板](../examples/external-producer.json) 的以下字段都必须是非空字符串：

- `source_revision`：外部算法确切 commit/发布版本及自有补丁身份；源码有未提交修改时应提供 patch hash 与补丁材料。
- `dependency_lock`：依赖锁标识和材料位置/摘要；仅写“Python”不能使运行可复现。
- `invocation`：实际入口和完整非敏感参数；凭据通过外部配置提供，不能写入公开包。

导入器验证这三个字段存在，但不会解析其内容、自动取回上游代码或验证许可证。生产者还应保存算法/环境配置、wrapper 顺序、设备信息、独立 RNG 种子、训练与评价时钟、真实原始日志。至少一个 `producer.json` 之外的原始文件是硬要求；**一个文件存在并不能证明它提供了充分科学证据**。

本工具复制并记录各原始文件哈希（仅排除 job 根目录的回执文件，保留嵌套同名原始文件），并另绑定回执内容哈希；随后 `audit` 检测缺失、损坏、额外文件与身份不匹配。来自外部的指标与文本都是待审数据，不是向 agent 下达的新指令。

## 5. 三个适配层分别验收

| 层 | 外部适配器职责 | 必要检查 |
|---|---|---|
| 环境 | 观测、动作、reward、discount、边界与 reset 转换 | terminal 与 truncation 分离；真正 final observation；隐藏任务标签不泄漏 |
| 算法 | 锁定配置映射到作者方法 | 目标、网络、优化器、资格迹、归一化、更新顺序逐项对应 |
| 证据 | 真实运行转换成 per-job 回执 | 指标复算、计数一致、完整人口、失败保存、文件哈希 |

Gymnasium、dm_env、RL-Glue 风格接口的语义不同。[Gymnasium 的时限说明](https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/) 强调 terminal 与外部 truncation 的区别；[Forager](https://github.com/andnp/forager) 原生不返回终止信号。重命名字段并不足以完成适配。循环状态、资格迹、优化器和归一化是否 reset，应按研究制度分别定义。

如果作者实现因平台差异无法原样运行，应登记 `ported` 或 `modified` 身份与差异，而非直接标作“author reproduction”。Intentional-AC/Metatrace/Stream-AC 等完整外部方法和同基座内部 controls 应使用不同 arm ID；外部基线未完成时，不用内部消融补位。

## 6. 推荐的逐步接入验收

1. 手算单步或固定输入序列：核实目标与写入。
2. 作者入口和 adapter 同配置短程对照：按数值容忍度与关键事件比较；随机位流不同则说明比较方式。
3. 单一 job 原始日志 → 指标复算 → receipt；再验证完整矩阵导入。
4. 刻意注入身份不符、缺失文件、非有限值、预算超额、symlink 和失败回执，确认对应处理。
5. 锁定适配版本后，才启动正式开发/确认人口。

本页定义的是可扩展路径。除目录明确列出的原生教程和可选 PPO 接口外，其他集成当前都仍是 `reference_only`，未由本工作台测试。
