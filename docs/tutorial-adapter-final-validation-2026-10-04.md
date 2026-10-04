# 最终教程源码接入验证 · 2026-10-04

在最终教程源码冻结后，使用 `/opt/homebrew/bin/python3.13`（Python 3.13.5）完成真实CLI流程：plan → validate external → freeze external → adapter run → import-results → audit → report → compare。系统默认python3为3.9.6，所以没有使用不满足教程Python3.10+要求的默认解释器；全过程同一解释器、未中途改变依赖。

注册 `bandit_constant_step / bandit_sample_average`，seeds=11,23、holdout=101,211（未运行），每job=100环境步、共400环境交互，failure score=-1。最终结果4/4 completed、failed=0、missing=0、invalid=0、extra jobs为空、population_complete=true。最终累计平均奖励固定步长0.70/0.76，样本均值0.70/0.75；报告与bootstrap=100的配对比较读取完整人口，均保持workflow_smoke_only。差值0.005不构成算法优势证据。

本地可复核材料位于Workbench根目录：

- `studies/tutorial-final-bandit-adapter-20261004-v2.json`
- `studies/tutorial-final-bandit-adapter-20261004-v2.lock.json`
- `incoming/tutorial-final-bandit-adapter-20261004-v2/`：每job的原始events/CSV/config/dependencies/producer/result
- `runs/tutorial-final-bandit-adapter-20261004-v2/`：已导入完整人口、锁、哈希与回执
- `runs/tutorial-final-bandit-adapter-20261004-v2/report.md`

lock SHA256为 `1cd032a5080db4bfe4a588ca235e2d363c5f29ed2b870902c5feff77a63b4f55`。运行后再次核对锁内65份教程Python源码摘要与最终checkout一致。旧尝试与旧验收没有覆盖。

Workbench全回归74项通过，1项可选SB3训练跳过；手册检查37章/8扩展通过；repository检查通过。这里检验的是最新教程adapter的实际接入与全人口证据，不认证所有教学方法效果、原论文重训或远端发布状态。
