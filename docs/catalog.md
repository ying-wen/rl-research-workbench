# 算法与环境目录：先查执行状态，再选扩展目标

目录覆盖经典 RL、深度 RL 和持续 RL，目的是给人和 agent 一个有来源、有边界的选型入口。**目录收录不等于工作台已经支持执行。** 机器入口是 [algorithms.json](../catalog/algorithms.json) 和 [environments.json](../catalog/environments.json)。初版分别收录 28 个算法/干预条目和 20 个环境/环境族/数据条目；另有 10 类高层模块的设计目录。

## 当前可执行范围

| 类型 | 精确 ID | 作用 |
|---|---|---|
| 原生教程算法 | `epsilon_greedy_sample_average`、`epsilon_greedy_constant_alpha` | Bandit 估值、探索和变化后追踪 |
| 原生教程算法 | `tabular_q_learning`、`tabular_sarsa` | 表格控制、on/off-policy 目标差异 |
| 原生教程环境 | `stationary_bandit`、`switching_bandit`、`cliff_grid` | 小成本检查完整研究工作流 |
| 可选适配 | `sb3_ppo` + `CartPole-v1` | 通过 SB3 展示深度 RL 的接入与预算记录 |

`profiles/deep.json` 是短程接口示范，显式使用 100 步 episode 上限；它不同于通常的 CartPole-v1 500 步设置。它的运行回报不能和其他 episode 上限下的成绩直接比较。更多 SB3 算法或任意 Gymnasium ID 不因库本身支持就自动成为本工作台支持范围。

环境族、数据集与单任务不是同一种目录对象。例如 `gymnasium_control` 需要进一步选择确切 ID；`minari_datasets` 还需要确切数据集版本、哈希和收集协议。

## 状态字段的含义

- `builtin_tutorial`：工作台自有的小型教学实现，有明确支持组合。不是原作者源码复现，也不表示已完成算法效能基准。
- `optional_adapter`：仓库提供接入代码，需要额外依赖。可用性取决于该发布版的依赖与检查结果；这不是所有任务的兼容认证。
- `reference_only`：仅提供文献/上游入口、协议要求与风险边界。**本工作台未实现、未运行、未验证该集成。** 通过外部结果导入可以保存其证据，但导入通过不改变此状态。

运行身份与科学证据另见具体锁文件、运行回执及报告。不要根据论文名、目录存在或安装成功，将状态自动提升为“已复现”。

## 如何选择下一组方法和任务

| 要回答的问题 | 便宜的先行诊断 | 随后的外部研究对象 |
|---|---|---|
| 更新式、terminal、trace 是否正确 | 表格 MDP、随机游走、cliff grid | 对应算法族任务；GTD 用离策略反例 |
| 探索与奖励尺度是否鲁棒 | stationary/switching bandit、bsuite | ALE、Procgen；训练与测试水平分开 |
| 深度控制增益来自哪里 | CartPole 接口检查、低维控制 | DQN/Rainbow、PPO、SAC、TD3 的原生任务 |
| 更多规划算力是否有价值 | 小型已知模型、相同观测下的计算对照 | DreamerV3、TD-MPC2；真实/想象交互分开 |
| 流式学习规则是否改进 | 小型非平稳预测/控制 | Stream-AC、Metatrace、Intentional-AC |
| 持久记忆和适应是否有价值 | 隐藏切换、延迟线索、回访设计 | Forager、AgarCL 与合适的循环基线 |
| 跨任务保留和迁移是否改进 | 明确任务顺序的短序列 | Continual World、COOM；登记边界/任务 ID 权限 |
| 离线数据是否足够 | 已知行为策略的小数据集 | CQL + 锁定的 Minari 数据；在线选择成本单列 |

不同制度的算法仍可以比较，但结论应同时呈现制度差异。例如 replay 算法可作为资源允许条件下的性能参照，不能据此直接判断严格 streaming 约束内谁更优。任务序列评测不能替代单一持续世界中无边界的长期评测。

## 扩展一个目录条目的步骤

1. 选择稳定且唯一的 `id`。新版本如果改变算法含义，登记版本身份，不悄悄替换旧运行中的方法。
2. 填入所有必填字段，并使用原论文、作者仓库或官方文档作为 URL。`upstream_url` 是查找入口，**不是版本锁**。
3. 默认 `implementation_status = reference_only`。先写适配合同、支持矩阵和测试计划，再开发代码。
4. 明确接口语义：观测与动作空间、reward 单位、discount、terminated/truncated、final observation、reset 与状态持久性。
5. 对每个算法列出真实目标、写入方向、率函数、资格/信用递推、预处理、所有随机源与计算时钟。
6. 做手算/差分或作者实现对照、RNG 和评价隔离、预算、失败保存测试；再做小型端到端运行。不要用这些检查代替性能比较。
7. 添加新 profile 与外部 adapter 或原生 engine，记录测试范围。审核通过后才提升目录状态；在原有支持范围以外仍视为未验证。

没有上游许可证或再分发授权时，保留链接和用户自行获取的路径方案；本仓库许可证不覆盖第三方代码、ROM、数据或论文。本文目录不复制任何上游源码。

## 机器字段合同

两个 JSON 文件各包含 `schema_version`（字符串 `"1.0"`）、`kind`、`updated_on`、`scope` 和 `items`。这与研究协议的整数 `schema_version: 1` 是两个独立合同。

每个条目至少包括：

| 字段 | 约束 |
|---|---|
| `id` | 文件内唯一的稳定字符串；执行 ID 还须被对应 engine/adapter 接受 |
| `name` | 人类可读方法/任务名，不混淆移植与原方法 |
| `track` | `classic`、`deep`、`continual` 之一；只是导航分类，不限制跨领域使用 |
| `implementation_status` | 上述三个枚举之一 |
| `upstream_url` | 上游实现或官方说明入口 |
| `citation_url` | 支持方法/任务身份的主要来源 |
| `version_pin_required` | 初版全部为 `true`；研究运行必须另记录确切源码、依赖和任务版本 |
| `protocol_requirements` | 该条目必须声明的实验设计事项 |
| `caveats` | 证据、制度、实现或许可边界 |

供 agent 查询可运行目录的标准库示例：

```python
import json
from pathlib import Path
for path in Path("catalog").glob("*.json"):
    registry = json.loads(path.read_text())
    for item in registry["items"]:
        if item["implementation_status"] != "reference_only":
            print(path.stem, item["id"], item["implementation_status"])
```

## 特别容易漂移的来源

2026-10-03 核对时，[Stream-X 作者仓库](https://github.com/mohmdelsayed/streaming-drl) 已明确区分 2024 与 2026 分支。使用者必须锁定 exact commit 和对应论文版本；分支名本身会移动。[Forager](https://github.com/andnp/forager) 的原生接口是不终止的 `start/step`；加入 episodic wrapper 应视为明确的实验改动。[COOM](https://github.com/TTomilin/COOM) 明确是 task-incremental 设计；其边界信息不能免费迁移到 task-free 假设。

运行前重新核对所使用版本的来源和许可证。目录中的日期表示条目整理时点，不能代替你这次运行的版本与依赖锁。
