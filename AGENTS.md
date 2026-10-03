# Agent 工作入口

目标是帮助研究者回答可判定的 RL 问题并改进算法。根据当前请求选择所需层级，不为形式完整而扩大任务。

## 开始

1. 读 `README.md`、实际项目的当前状态与用户授权范围。历史报告只是带时点证据，运行状态需重新核实。
2. 新方向先填 `templates/research-card.md`；持续学习读 `docs/continual.md` 和 `docs/continual-project-playbooks.md`。
3. 理论或机制改动读 `docs/algorithm-design.md`、`docs/testing.md`；统计读 `docs/statistics.md`。
4. 如需执行，按 `docs/iteration.md` 选小型机制实验或完整效能实验。调用 `python -m rlworkbench --help` 确认当前命令。
5. 涉及GVF、options、子目标、抽象、规划或多智能体，先读 `docs/navigation-map.md`，再路由到对应手册；补 `templates/module-card.md` 和机器契约。通过结构验证不代表模块已实现或整体架构有效。
6. 整体机制思路读 `docs/mechanism-design.md`；原调研 37 章全文在 `docs/handbook.md`。修改代码前运行 `python3 scripts/handbook.py find 文件名或机制名 --json`，按 `purpose` 和 `gaps` 了解它实际承接的原则、测试和能力边界。完整文件反查在 `docs/handbook-code-index.md`。

## 维护原理到工具的对应

按 `docs/handbook-maintenance.md` 编辑专题文档与 `docs/traceability/chapters-*.json` / `extensions.json`。原始 `docs/research-handbook.html` 是不可覆盖的证据快照；全文阅读版和双向索引为生成物。函数移动、新工具接入或测试重命名后，运行 `python3 scripts/handbook.py build` 和 `python3 scripts/handbook.py check`，并检查受影响的职责与缺口，不能只修到路径存在。CLI 语法通过不表示命令前提已满足，也不会自动运行任何命令。

## 研究纪律

- 写明真实目标、agent 到达此刻可见的信息、可测目标、近似偏差、主改动和撤回条件。研究者的真实相位、未来分支或最优参数不可默默成为策略输入。
- 完整作者方法、同基座移植、内部消融分开；记录基础写入、率函数、目标、信用递推和事件顺序。
- 实现测试、机制诊断和回报收益分别报告。样本是训练运行/生命期；窗口、episode 和条件分叉通常不是新的训练 seed。
- 负结果、失败及原比较人口保留。未知或中断状态先查证，不重复启动同一个 attempt。
- 正式协议、运行源和结果禁止原地覆盖。新改动建新版本；`run` 默认拒绝已有输出目录。摘要检测意外漂移，不提供对恶意篡改的认证。
- 评价模式明确：在线持续评价允许按协议学习；冻结诊断隔离参数、buffer、归一化与随机状态。不要把所有评价都强行冻结。
- 独立开发生命期上的完整调参可以合法；查看正式测试生命期的未来表现后修规则不能再声称同一次独立确认。
- 先有预算再运行。文档中的计划不授权访问服务器或启动长训；沿用用户已给的授权，不重复求确认。

## 合作与交接

并行时明确文件所有者和实验操作者；只读审查与代码改动分开。每轮交付：修改与原因、实际执行及证据、最强反例、未解决问题、下一决定。用 `templates/iteration-log.md` 记录，不把增加代码或测试数量作为科学进步。

可直接使用仓库技能 `skills/rl-research-iteration/SKILL.md`。技能不依赖 Codex 专有工具；其他 agent 可按同样文件和 CLI 操作。
