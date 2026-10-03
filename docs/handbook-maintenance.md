# 手册、机制与工具如何一起维护

仓库有一个完整阅读入口和两种查询方向。读者从 [37 章全文](handbook.md) 进入原理，再从 [逐章映射](handbook-code-map.md) 找实践文档、代码、测试和命令；开发者从 [文件与符号索引](handbook-code-index.md) 反查改动会影响哪些研究原则。[整体机制设计](mechanism-design.md) 将目标、信息、状态、更新、信用、预测、选项、规划与完整生命期连接起来。文献来源和机制推理不能被一组命令替代。

## 阅读与操作入口

| 需要 | 人类入口 | Agent / 终端入口 |
|---|---|---|
| 读完整原理和文献边界 | [全文 Markdown](handbook.md)；[交互 HTML](handbook/index.html) | 在 `docs/handbook.md` 搜索章节锚点 |
| 找某种机制的实验方案 | [机制设计](mechanism-design.md)、[逐章映射](handbook-code-map.md) | `python3 scripts/handbook.py find GVF --json` |
| 修改某个函数前找依据 | [反向索引](handbook-code-index.md) | `python3 scripts/handbook.py find continual_metrics.py --json` |
| 核对手册与实现是否漂移 | [映射源](traceability/) | `python3 scripts/handbook.py check` |
| 生成新的阅读入口 | 按下述步骤修改维护源 | `python3 scripts/handbook.py build` |

GitHub 直接显示 Markdown；HTML 在本地浏览器阅读。`docs/handbook/index.html` 保留全文筛选、检查清单和六种模板导出，每章末尾增加可展开的工具对应。HTML 中的实现链接指向公开的 GitHub 仓库。下载仓库后也可用全文 Markdown 的相对链接离线查阅；函数行号在线链接由生成器重新计算。

```bash
# 仓库根目录；无需安装额外依赖
python3 scripts/handbook.py find StreamRate
python3 scripts/handbook.py find rlworkbench/core.py --json
python3 scripts/handbook.py check
```

`find` 只查询，不运行实验。无匹配返回退出码 1。输出包含研究问题、原则、支持状态、代码与测试职责、操作前提和未实现部分。`check` 只解析映射中的 CLI 参数，绝不会执行记录的训练、冻结或导入命令。

## 哪些是维护源，哪些是生成物

| 文件 | 角色 | 更新方式 |
|---|---|---|
| [research-handbook.html](research-handbook.html) | 2026-10-03 原手册完整证据快照 | 保持原字节；新文献及新判断写入维护文档并标注日期 |
| [sources.json](sources.json) | 原手册 81 条来源及核验层级 | 与原快照登记保持一致；新来源在相关维护文档单独引用 |
| [chapters-core.json](traceability/chapters-core.json) | 前 17 章的原理到实现映射 | 人工评审后编辑 |
| [chapters-continual.json](traceability/chapters-continual.json) | 后 20 章的持续实验及操作映射 | 人工评审后编辑 |
| [extensions.json](traceability/extensions.json) | 整体机制、两项目、GVF/抽象/options、规划架构、MARL、持续证据及 agent 迭代 | 人工评审后编辑 |
| [mechanism-design.md](mechanism-design.md) 及各专题 `.md` | 活的研究设计、推导与实践 | 按证据修订，保留适用边界 |
| `handbook.md`、`handbook-code-map.md`、`handbook-code-index.md`、`handbook/index.html` | 完整阅读版、双向导航和交互版 | 由 `scripts/handbook.py build` 生成，不手改 |
| [index.json](traceability/index.json)、[source.json](traceability/source.json) | Agent 可读取的合并索引与来源摘要 | 生成；来源 SHA-256 可复核原文件 |
| [六种原手册模板](../templates/research-handbook/) | 从快照提取的空白研究模板 | 生成；它们不是 `rlworkbench` 的可执行协议 schema |

原理文本保留 37 章全部正文、表格、公式、伪代码及来源详情，额外的实践连接位于各章末尾。章节内的数学表达以 Unicode 文本或原 HTML 保留，Markdown 不依赖外部数学渲染服务。原始交互控件在静态 Markdown 中改为文件或 HTML 入口；浏览器中的勾选仍只保存在该浏览器。

## 增加或迭代一种机制

1. 写研究问题与可反证路径。先辨别改变的是目标、状态、更新、信用分配、选项选择还是规划计算；指向 [机制设计](mechanism-design.md) 和具体原章。
2. 实现或复用最小工具，写能区分正确与错误行为的测试。完整外部算法、共同基座和内部消融继续分别命名。
3. 在映射源登记真实 `path`、AST `symbol`、职责 `purpose`、命令 `argv`、操作类型 `mode` 和 `requires`。一个已实现函数只覆盖所述子问题；暂未实现的效能实验留在 `gaps`。
4. 若没有代码可对应，保留 `human_protocol`，代码和测试数组可空。`partial_tooling` 表示局部支持。只有明确的工具职责已经实现并有代码、测试和命令时，才使用 `implemented_tool`；它不认证整个章节的建议。
5. 新专题扩展到 `extensions.json`；原章 ID 和标题保持与快照一一对应。用新的独立方案文档承接新研究，不能默改历史快照。
6. 运行下方检查，复查 HTML、全文与索引。涉及科学机制的结论仍须独立证据；结构检查通过不等于因果解释成立。

```bash
python3 scripts/handbook.py build
python3 scripts/handbook.py check
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

CI 检查章节覆盖与顺序、标题一致性、源文件摘要、81 条来源同步、路径存在、函数和测试符号存在、CLI 参数语法，以及生成物是否过期。移动函数或增删行号后必须重新生成。普通文件中的每一行不强制写文献注释；反向索引把文件、函数职责和原理集中对应，避免散落注释失效。

这些检查发现不了研究原则是否正确、测试是否充分、命令前提是否已满足，或尚未登记的新代码。评审仍需阅读 `purpose` 和 `gaps`，并验证必要的运行行为。本次整合修复的 `train`/`training` 日志字段不一致就是例子：只有符号存在检查发现不了它，原生产生器到指标 CLI 的集成测试才能覆盖。

## 两个项目如何接入

学习控制与表征记忆项目分别沿 [完整生命期方案](continual-project-playbooks.md) 和 [机制设计](mechanism-design.md) 确定比较对象，再适配 [外部结果规范](external-adapters.md)。当前开发协议仍为未接入状态；结构验证可用，不能冻结并执行原项目。保持原实验和历史运行不变，在新的适配器与研究版本中登记真实算法身份、信息权限、资源、完整生命期和失败人口。

未来 GVF、options、抽象、规划、子目标、整体架构与多智能体遵循同一路径：先有模块职责与时序契约，再有局部诊断，最后有完整系统的增量效能对照。当前模块契约工具检查声明结构与信息路径；它没有运行这些高层算法。

本次全文整合、公式保留、CLI 回归及桌面/手机浏览器验收见 [2026-10-03 整合验证记录](validation-integration-2026-10-03.json)。后续修改应新增带时点的验证记录，不能把这份历史验收当成新代码的通过证明。
