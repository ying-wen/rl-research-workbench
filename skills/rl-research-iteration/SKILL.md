---
name: rl-research-iteration
description: Design, execute, analyze, or revise reinforcement learning experiments using explicit hypotheses, complete populations, and evidence-bounded decisions. Use for classical, deep, or continual RL algorithm research; not for unrequested cluster operations.
---

# 强化学习研究迭代

本技能在 RL Research Workbench checkout 中使用。用户的实际问题、预算与授权优先；定位仓库根后读 `AGENTS.md`。不要求安装全局技能，也不依赖特定 agent 平台。

## 路由

- 新想法或机制争议：读 `docs/algorithm-design.md`，按 `templates/research-card.md` 填一页卡，先找可以推翻解释的最小实验。
- 实现或性能异常：读 `docs/testing.md`，分开方程、时序、适配器和数值失效。保留原失败，修复另立版本。
- 持续学习：读 `docs/continual.md`。若涉及学习控制、表征或记忆，再读 `docs/continual-project-playbooks.md`，检查完整生命期与隐藏信息边界。
- GVF、options、子目标或抽象：读 `docs/prediction-abstraction-options.md`；规划与系统组合读 `docs/planning-and-architecture.md`；多智能体读 `docs/multi-agent.md`。只加载当前问题所需部分，使用模块卡声明输入、目标、时钟、下游作用和资源。
- 执行/统计：读 `docs/iteration.md`、`docs/statistics.md`；新增后端读 `docs/external-adapters.md`。

## 每轮输出

先说明问题与当前最强证据。区分已有结果、推导、机制诊断、候选方案和待执行实验。给出改动、对照、指标、预算、失败规则，以及继续/修改/停止条件。具体实验不必使用全部模板。

执行已有协议时先 `validate` 和 `plan`，检查预算与完整方法身份，随后 `freeze`。仅在用户授权的计算范围内 `run`；不调用隐含的服务器或已有长训。`audit` 有 missing/invalid 时不按幸存人口作比较。`compare` 只给每个固定环境的配对描述与区间，需要另审种子设计、功效、选择和多重比较。

结束写决策记录。需要下一轮时用 `next LOCK --decision FILE --study-id NEW --out FILE` 生成草案；不会自动获准启动、变成确认实验或获得科学成功标签。smoke 只验通路，不能直接升级确认。

## 不能混淆的边界

局部导数正确不等于当前提交有益；局部代理量改善不等于完整回报提高。固定表征与新表征、步内计算与跨步记忆、固定率与元调率分开控制。完整外部算法与内部消融分别命名。持续学习的旧情境回访、真正新规则学习、冻结检索和重新学习需要不同对照。

修改后检查实际文件和必要测试；文档更新不需要运行昂贵科学实验。下一次读历史日志时不要重放其命令。交付可复核文件、已完成验证、负证据与尚未完成的工作。
