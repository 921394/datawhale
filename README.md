# 国内 A 股量化学习与回测

这是一个面向初学者的量化交易学习记录。当前目标很明确：**先做 A 股本地回测，不连接真实账户**。

## 从这里开始

1. [A 股本地回测流程](docs/a-share-backtest.md)：从行情文件到第一个可复现回测。
2. [A 股量化完整工作流](docs/a-share-workflow.md)：现成策略、框架选择和进阶自研路径。
3. [从文档到可运行项目](docs/next-stage-plan.md)：当前缺口、最小项目和入门到进阶路线。
4. [开源代码与免费资源](docs/open-source-and-free-resources.md)：数据源、框架、现成策略和社区成品。
5. [量化赚钱的方式](docs/quant-profit-models.md)：Beta、因子、套利、执行和非交易收入。
6. [策略设计思想与收益来源](docs/strategy-design-and-counterparties.md)：按市场假设、收益来源和交易对手分析策略。
7. [网站与源码中的现成策略](docs/strategy-examples-by-source.md)：按类别记录公开网站和开源仓库中的策略示例，并标注收录状态。
8. [AI 辅助学习与开发](docs/ai-assisted-learning.md)：可直接复制给 AI 的提示词和检查清单。
9. [开源量化框架调查](docs/framework-survey.md)：了解不同框架的边界，再决定是否使用。
10. [小盘股热点与补涨策略调查](docs/small-cap-hot-theme-strategy.md)：分析小市值基线、新闻热点补涨逻辑和可验证路径。

## 推荐的 AI 协作角色

当前项目还处于文档和最小回测准备阶段，不需要启用全部角色。按任务选择下面的角色即可：

| 角色 | Agent 名称 | 适用任务 |
| --- | --- | --- |
| 投资研究员 | `Investment Researcher` / `finance-investment-researcher` | 分析 A 股策略假设、收益来源、交易对手和资料 |
| 数据工程师 | `Data Engineer` / `engineering-data-engineer` | 设计行情 CSV 清洗、字段统一、复权和数据质量检查 |
| 统计学家 | `Statistician` | 检查未来数据泄漏、样本外验证和统计结论 |
| 财务分析师 | `Financial Analyst` / `finance-financial-analyst` | 估算手续费、滑点、换手率和收益结构 |
| 代码审查员 | `Code Reviewer` / `engineering-code-reviewer` | 回测代码完成后检查交易逻辑、边界条件和安全风险 |
| 技术写作者 | `Technical Writer` / `engineering-technical-writer` | 维护本 README 和 `docs/` 文档，保持结构、术语和示例一致 |

推荐顺序：投资研究员 -> 数据工程师 -> 统计学家 -> 代码审查员。技术写作者贯穿文档维护，不参与交易决策。

## 当前技术路线

```text
A股规则与数据
    -> Python 数据处理
    -> 简单规则策略
    -> 含手续费/滑点的本地回测
    -> 样本外验证
    -> 仿真交易
    -> 券商接口与合规确认
```

第一阶段只需要 Python、`pandas`、`numpy`、`matplotlib` 和一份合规取得的历史行情数据。不要一开始搭建微服务、做高频交易或训练复杂模型。

## 当前下一步

先不连接真实账户，也不急着写复杂代码；用一份本地 A 股日线 CSV、一个简单策略和 pandas 完成可重复的最小回测，再逐步增加交易规则、组合管理和仿真交易。

## 国内 A 股的关键事实

- 交易规则、申报单位、交易时段、停牌和回转交易以交易所最新规则为准。
- A 股实盘接口不是通用的 Python API，通常需要券商开通特定接口和权限。
- 程序化交易涉及报告、监控和风控要求，实盘前必须向券商确认。

## 文档原则

AI 可以帮助解释概念、生成最小代码、分析报错和审查逻辑；但每段代码都必须自己运行，并检查时间对齐、未来数据泄漏、交易成本和异常处理。
