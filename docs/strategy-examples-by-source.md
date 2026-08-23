# 网站与源码中的现成策略清单

这一页专门记录从公开网站、官方文档和开源仓库找到的具体策略示例。它们适合学习和复现，不代表已经证明能在 A 股实盘赚钱。

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

## 4. 因子和机器学习类

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

## 5. 事件、组合和执行类

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

## 6. 框架官方示例

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

## 7. 现成策略的正确使用流程

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
