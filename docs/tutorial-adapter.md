# 教材算法接入：先冻结，再执行，再导入

本适配器直接调用教程独立算法的 `META` 和 `run(seed, steps, emit)`，复用工作台已有的外部锁、全人口导入、审计、报告与比较。它不会复制算法实现。只运行用户明确选择的可信本地checkout；导入Python模块会执行该模块代码。

## 比较前的实际合同

每组算法必须匹配 `family / task / metric / unit / higher_better / budget`。同为DQN或同叫return并不意味着任务、尺度和时钟相同。不同任务或预算需要分别建协议；方法资源不匹配的对照须另设计明确成本合同，不能绕过匹配检查。baseline须显式包含在算法列表。

主指标是**最后记录的value**，含义由META说明，可能是预测RMSE、累计平均奖励或内部独立冻结评价回报。适配器不再做额外评价，外层 `eval_episodes=0`；内部评价和模型计算的实际资源由 `META.budget` 声明。协议通用steps是教程run时钟，不保证等于环境交互；不能把DP sweep、prediction update或model backup默认为新交互。源哈希与META在建协议时保存，执行前拒绝漂移；Python和已登记包版本也须匹配freeze环境。

## 可运行流程

以下命令在**包含 `rlworkbench/tutorial_adapter.py` 的最新 Workbench checkout 根目录**执行；已有旧版本请先更新，并确认该文件存在。教程独立实现要求Python 3.10+；Workbench基础包虽支持3.9，这条接入流程需满足教程要求。

源码根目录可以直接用 `python3 -m ...`，无需安装包。若希望安装，先创建隔离环境再执行 `python3 -m pip install -e .`。所有阶段都用同一Python解释器；深度算法先在该环境安装教程 `examples/deep_requirements.txt`，然后再plan/freeze，避免运行时的包版本锁拒绝。

下例是可以直接使用的真实bandit ID，标准库即可运行。将教程路径替换为实际绝对路径，并确认每个输出路径尚不存在。其他算法先在教程根执行 `python3 implementations/runtime.py --list`，阅读所选文件META再建立可比组。

```bash
python3 -m rlworkbench.tutorial_adapter plan \
  --tutorial-root /absolute/path/continual-rl-tutorial \
  --ids bandit_constant_step bandit_sample_average --baseline bandit_sample_average \
  --study-id tutorial-comparison-smoke-v1 \
  --seeds 11 23 --holdout-seeds 101 211 --steps 100 \
  --failure-score -10 --out studies/tutorial-smoke-v1.json
python3 -m rlworkbench validate studies/tutorial-smoke-v1.json --external
python3 -m rlworkbench freeze studies/tutorial-smoke-v1.json --external --out studies/tutorial-smoke-v1.lock.json
python3 -m rlworkbench.tutorial_adapter run studies/tutorial-smoke-v1.lock.json \
  --tutorial-root /absolute/path/continual-rl-tutorial --out incoming/tutorial-smoke-v1
python3 -m rlworkbench import-results studies/tutorial-smoke-v1.lock.json \
  --input incoming/tutorial-smoke-v1 --out runs/tutorial-smoke-v1
python3 -m rlworkbench audit runs/tutorial-smoke-v1
python3 -m rlworkbench report runs/tutorial-smoke-v1
python3 -m rlworkbench compare runs/tutorial-smoke-v1 --candidate bandit_constant_step --baseline bandit_sample_average
```

`failure-score`是事先明确的复合分析分值；RMSE等越小越好指标需要选择足够差的高值，奖励指标通常选择低值。它不是失败算法的真实回报。这里的两个seed只检查流程，不能作效能结论。

## 保留失败与限制

每个计划job保存config、完整源码摘要、依赖版本、原始events与CSV、producer和result。普通算法异常生成failed回执并继续完整人口；已发出的前缀事件仍保留，真实未知计数写null。中断进程留下不完整目录，必须先查状态；不能覆盖重跑、也不能把未确定结束的job伪填failed。修复建立新版本/新attempt。

适配器检查记录时钟递增、有限值、完整终点、发出与返回记录一致；它不能证明环境计步、指标定义或算法忠实。依赖版本记录不是安装用的完整解析锁。当前边界是串行、小规模教学比较，没有HPO、集群调度或checkpoint恢复。关于科学验收仍参见[测试阶梯](testing.md)、[外部证据规范](external-adapters.md)与[迭代纪律](iteration.md)。
