# 网站与源码中的现成策略清单

这一页专门记录从公开网站、官方文档和开源仓库找到的具体策略示例。它们适合学习和复现，不代表已经证明能在 A 股实盘赚钱。

## 总览矩阵

| 策略类别 | 设计思想是否已记录 | 具体来源/代码是否已记录 | 当前状态 |
| --- | --- | --- | --- |
| 买入并持有 / Beta | 是 | RQAlpha 示例 | 已收录，可直接入门 |
| 双均线 / 黄金交叉 | 是 | RQAlpha、VectorBT | 已收录，可直接入门 |
| 海龟 / 突破趋势 | 是 | RQAlpha 示例 | 已收录，可直接入门 |
| 时间序列动量 | 是 | AQR 研究 | 已收录，有研究来源，需自行实现 |
| 短期反转 / 均值回归 | 是 | De Bondt-Thaler 研究 | 已收录，有研究来源，需自行实现 |
| 配对交易 | 是 | NBER 配对交易研究 | 已收录，有研究来源，需自行实现 |
| 价值 / 质量 / 规模因子 | 是 | Qlib 因子工作流 | 已收录，具体 A 股案例仍需补充 |
| Alpha158 / Alpha360 / 机器学习 | 是 | Qlib benchmarks | 已收录，属于模型工作流，不是现成实盘策略 |
| ETF 轮动 | 是 | 社区 ETF 轮动仓库 | 已收录，社区代码，需独立复核 |
| 指数调仓 / 被动资金流 | 是 | 指数权重调整研究 | 已收录，有研究来源，需自行实现 |
| 财报 / 分红 / 停复牌事件 | 只做过概念说明 | 暂无完整策略源码 | 待补充 |
| 可转债策略 | 是 | 社区筛选/定价仓库 | 已收录，社区代码，需独立复核 |
| ETF 申赎套利 | 是 | FCA、Fed、BIS 研究 | 已收录，研究来源，无 A 股个人可运行代码 |
| 期权波动率 / Delta 对冲 | 是 | 波动率风险溢价研究 | 已收录理论，未收录可运行案例 |
| Carry / 期限结构 | 是 | AQR Carry 研究、FuturesBacktest 文档 | 已收录，非 A 股入门方向 |
| 做市 / 订单簿 | 是 | 市场微观结构研究 | 已收录理论，未收录可运行案例 |
| VWAP / TWAP 执行 | 是 | vn.py 文档和执行应用 | 已收录，偏执行工程 |
| 新闻 / 情绪 / 另类数据 | 是 | FinBERT 模型仓库 | 已收录模型组件，未收录 A 股完整策略 |
| 风险平价 / 资产配置 | 只做过概念说明 | VectorBT 组合优化示例 | 已收录工具，完整策略仍需补充 |
| 强化学习交易 | 是 | Qlib RL 示例 | 已收录入口，不建议入门使用 |

### 状态说明

- **已收录，可直接入门：**已有公开代码或完整官方示例，可以先跑通。
- **已收录，有研究来源：**有论文或研究页面，但通常需要自己实现和验证。
- **已收录理论，未收录可运行案例：**解释过收益来源，但还没有完整可执行代码。
- **待补充：**目前只在其他文档中提到名称或概念，没有独立来源和案例。

## 1. 入门基准类

### 买入并持有

- **来源：** [RQAlpha 策略示例](https://github.com/ricequant/rqalpha/blob/master/docs/source/intro/examples.rst)
- **思想：** 第一天买入后一直持有，用来建立最简单的收益基准。
- **类别：** Beta/基准
- **适合阶段：** 入门
- **A 股注意：** 必须加入复权、分红和交易成本；不能只看价格曲线。

这是所有策略都应该比较的基准。如果复杂策略不能稳定超过基准，复杂度可能没有意义。

## 2. 趋势和动量类

### 黄金交叉 / 双均线

- **来源：** [RQAlpha Golden Cross 示例](https://github.com/ricequant/rqalpha/blob/master/docs/source/intro/examples.rst)
- **来源：** [VectorBT 官方资源](https://github.com/polakowo/vectorbt/blob/master/docs/docs/getting-started/resources.md)
- **思想：** 短期均线向上穿过长期均线时买入，反向穿越时退出。
- **类别：** 趋势跟踪
- **适合阶段：** 入门
- **A 股注意：** 信号通常在收盘后产生，成交应放到下一个可交易时点；要处理涨跌停、停牌和 T+1。

### 海龟交易系统

- **来源：** [RQAlpha 策略示例](https://github.com/ricequant/rqalpha/blob/master/docs/source/intro/examples.rst)
- **思想：** 突破过去一段时间的价格区间后入场，并用波动率和止损管理仓位。
- **类别：** 趋势/突破
- **适合阶段：** 入门后
- **A 股注意：** 原始系统常用于可双向交易的市场，A 股需要改成多头版本并重新验证。

### 时间序列动量

- **来源：** [AQR Time Series Momentum](https://www.aqr.com/insights/research/journal-article/time-series-momentum)
- **思想：** 根据资产自身过去一段时间的收益方向决定持有方向。
- **类别：** 趋势/动量
- **适合阶段：** 中级
- **A 股注意：** 股票现货主要实现为多头择时或 ETF 趋势，不能直接照搬期货多空版本。

## 3. 反转和均值回归类

### 短期反转

- **来源：** [De Bondt 与 Thaler 反转研究](https://www.aeaweb.org/articles?id=10.1257/jep.3.1.189)
- **思想：** 短期极端上涨或下跌可能包含过度反应，价格之后可能部分回归。
- **类别：** 反转/均值回归
- **适合阶段：** 中级
- **A 股注意：** 需要排除基本面恶化、退市、停牌和跌停无法卖出的股票。

### 配对交易

- **来源：** [Gatev、Goetzmann、Rouwenhorst 配对交易研究](https://www.nber.org/papers/w7032)
- **思想：** 选择历史关系稳定的两个资产，交易两者之间的相对价差。
- **类别：** 相对价值/统计套利
- **适合阶段：** 中级以后
- **A 股注意：** 做空和融券限制会破坏理论上的多空中性，先做价差研究，不要直接假设可以实盘对冲。

## 4. ETF 轮动和组合轮换

### A 股 ETF 动量轮动框架

- **来源：** [ETF 动量轮动回测框架](https://github.com/roverway/etf-momentum-rotation)
- **来源：** [ETF 数据同步、回测和模拟盘](https://github.com/zhuleimed/etf-daily-sync-and-backtest)
- **来源：** [多因子 ETF 轮动研究](https://github.com/cloudinbanana/etf-rotation-strategy)
- **思想：** 在宽基、行业、风格或商品 ETF 中按动量、波动率或趋势评分，定期持有相对强的标的。
- **类别：** ETF 轮动/组合管理
- **适合阶段：** 入门后
- **A 股注意：** 这些是社区项目，需独立核对数据源、交易时点、涨跌停、换手和回测区间；不要直接相信仓库中的收益排行。

## 5. 可转债策略

### 可转债筛选和套利

- **来源：** [A 股可转债套利仓库](https://github.com/mytac/convertible-bond-arbitrage)
- **来源：** [中国可转债定价研究](https://github.com/ericxuzhesheng/Convertible-Bond-Pricing-Research)
- **思想：** 根据转债价格、转股价值、回售/赎回条款、到期收益和正股风险筛选标的，或估计理论价值与市场价格的偏离。
- **类别：** 可转债/相对价值
- **适合阶段：** 中级以后
- **A 股注意：** 社区项目依赖外部数据和账户配置，条款、信用风险、强赎和流动性必须自己复核；“套利”不代表无风险。

## 6. ETF 申赎套利

### ETF 与净值偏离

- **来源：** [FCA ETF Mispricing 研究](https://www.fca.org.uk/publications/occasional-papers-fca-research/occasional-paper-68-etf-mispricing)
- **来源：** [Federal Reserve ETF arbitrage 研究](https://www.federalreserve.gov/econres/feds/files/2020097pap.pdf)
- **来源：** [BIS ETF 套利机制](https://www.bis.org/publ/qtrpdf/r_qt2103d.htm)
- **思想：** 比较 ETF 二级市场价格、净值和申购/赎回篮子，在价差足够覆盖成本时进行创建或赎回。
- **类别：** ETF 套利/市场结构
- **适合阶段：** 进阶
- **A 股注意：** 通常需要申赎权限、成分股资金、实时篮子和低延迟执行；上述来源主要是研究，不是个人可直接运行的 A 股代码。

## 7. Carry 和期限结构

### Carry 因子

- **来源：** [AQR Carry 研究](https://www.aqr.com/search?Topics=Carry)
- **来源：** [FuturesBacktest Carry 文档](https://www.futuresbacktest.com/docs/strategies/carry/)
- **思想：** 在市场价格不变的假设下，持有具有较高隐含收益、利差或期限收益的资产。
- **类别：** 风险溢价/期限结构
- **适合阶段：** 进阶
- **A 股注意：** 典型案例多来自外汇、债券和期货，不适合直接迁移到 A 股股票；需要先理解融资、展期和崩溃风险。

## 8. 新闻、情绪和另类数据

### FinBERT 情绪信号

- **来源：** [FinBERT 源代码](https://github.com/ProsusAI/finBERT)
- **思想：** 将金融文本转换为正面、负面或中性情绪分数，再作为选股或风险过滤信号。
- **类别：** 另类数据/NLP
- **适合阶段：** 中级以后
- **A 股注意：** FinBERT 本身只是情绪模型，不是完整交易策略；中文新闻、公告发布时间、文本去重和标签时间必须重新处理。

## 9. 强化学习和动态组合

### Qlib RL 示例

- **来源：** [Qlib 强化学习订单执行示例](https://github.com/microsoft/qlib/tree/main/examples/rl_order_execution)
- **思想：** 将仓位调整或订单执行建模为连续决策问题，让模型在环境中优化目标函数。
- **类别：** 强化学习/执行优化
- **适合阶段：** 进阶研究
- **A 股注意：** 训练环境、奖励函数、交易成本和样本外验证比模型名称更重要，不建议作为第一个策略。

## 10. 因子和机器学习类

### Alpha158 / Alpha360 因子工作流

- **来源：** [Qlib 模型基准](https://github.com/microsoft/qlib/tree/main/examples/benchmarks)
- **结果说明：** [Qlib 基准说明](https://github.com/microsoft/qlib/blob/main/examples/benchmarks/README.md)
- **思想：** 从价量和基本面数据构造因子，预测未来收益或进行股票排序，再做组合回测。
- **类别：** 因子/机器学习
- **适合阶段：** 中级以后
- **A 股注意：** 这是研究 workflow 和模型基准，不是现成的实盘策略；必须重新检查数据版本、样本外结果和交易成本。

Qlib 仓库还提供 LightGBM、MLP、LSTM、Transformer 等模型示例。模型名称不等于策略思想，必须继续追踪数据、标签、组合构建和执行部分。

### 多因子选股

- **来源：** [Qlib workflow_by_code 示例](https://github.com/microsoft/qlib/blob/main/examples/workflow_by_code.py)
- **思想：** 计算多个因子或模型分数，按分数排序后构建组合。
- **类别：** 因子/指数增强
- **适合阶段：** 中级
- **A 股注意：** 需要控制行业、规模、换手和单股集中度，避免把行业暴露误认为 Alpha。

## 11. 事件、组合和执行类

### 指数调仓和被动资金流

- **来源：** [指数权重调整与价格压力研究](https://doi.org/10.1108/03074350910973676)
- **思想：** 指数成分和权重变化会带来规则驱动的资金流，研究调仓前后的价格压力和回归。
- **类别：** 事件驱动
- **适合阶段：** 中级以后
- **A 股注意：** 必须使用当时已公布的成分和权重，不能把事后数据回填到历史。

### 组合优化和风险控制

- **来源：** [VectorBT 官方资源中的组合优化示例](https://github.com/polakowo/vectorbt/blob/master/docs/docs/getting-started/resources.md)
- **思想：** 在信号之外决定仓位、风险预算、再平衡和最大集中度。
- **类别：** 组合构建
- **适合阶段：** 中级
- **A 股注意：** 组合优化结果必须加交易成本和换手限制。

### VWAP/TWAP 和执行算法

- **来源：** [vn.py 策略应用和 Gateway 文档](https://www.vnpy.com/docs/cn/community/info/gateway.html)
- **思想：** 将大订单拆分，在时间或成交量约束下减少市场冲击。
- **类别：** 执行优化
- **适合阶段：** 实盘工程阶段
- **A 股注意：** 依赖券商接口、行情质量和成交回报，不能用普通日线回测证明执行效果。

## 12. 框架官方示例

### RQAlpha

- [源代码](https://github.com/ricequant/rqalpha)
- [策略示例](https://github.com/ricequant/rqalpha/blob/master/docs/source/intro/examples.rst)
- [回测教程](https://github.com/ricequant/rqalpha/blob/master/docs/source/intro/tutorial.rst)
- **最适合：**快速学习买入持有、黄金交叉、海龟和股票账户回测。
- **限制：**仓库说明有非商业使用限制，使用前检查许可证。

### VectorBT

- [源代码](https://github.com/polakowo/vectorbt)
- [示例资源](https://github.com/polakowo/vectorbt/blob/master/docs/docs/getting-started/resources.md)
- **最适合：**双均线、止损、参数网格、走步验证和组合实验。
- **限制：**开源版本和专业版本能力不同，商业使用前检查许可证。

### Backtrader

- [快速开始](https://github.com/backtrader/backtrader-docs/blob/master/docs/quickstart/quickstart.rst)
- [策略生命周期](https://github.com/backtrader/backtrader-docs/blob/master/docs/strategy.rst)
- **最适合：**理解事件驱动策略、指标、数据源和 Broker 生命周期。
- **限制：**需要自行补齐 A 股 T+1、涨跌停、停牌和费用模型。

### vn.py

- [CTA 策略模板](https://github.com/vnpy/vnpy/blob/master/docs/community/app/cta_strategy.md)
- [Gateway 文档](https://www.vnpy.com/docs/cn/community/info/gateway.html)
- **最适合：**学习策略文件组织、订单管理和实盘系统结构。
- **限制：**A 股能否实盘取决于券商提供的 Gateway 和账户权限。

## 13. 现成策略的正确使用流程

```text
找到源码
    -> 看许可证
    -> 原样运行
    -> 阅读数据和信号
    -> 加入 A 股交易规则
    -> 加入手续费/滑点
    -> 与买入并持有比较
    -> 样本外验证
    -> 才能考虑仿真
```

论坛帖子、收益截图和“自动选股”项目只能作为线索，不能直接当作策略有效性的证明。每个策略都要重新回答：

1. 它利用了什么市场假设？
2. 它的交易对手或收益支付机制是什么？
3. 扣除成本后是否仍有正期望？
4. 是否存在未来数据、幸存者偏差或参数过拟合？
5. A 股真实交易规则是否允许它执行？
