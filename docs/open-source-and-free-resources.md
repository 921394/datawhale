# 开源代码与免费资源

本文只列有公开代码或公开官方文档的项目。所谓“免费”不等于数据可以任意商用，也不等于策略可以直接赚钱；使用前要检查许可证、数据服务条款和维护状态。

## 推荐组合

做 A 股本地回测，先用这一条最短路径：

```text
AKShare 或 BaoStock
    -> pandas 清洗
    -> VectorBT / RQAlpha 回测
    -> Qlib 做因子研究
    -> 券商仿真接口
```

不要同时安装所有框架。先选一个数据源和一个回测框架，把一个策略跑通。

## 1. A 股数据源

| 项目 | 来源 | 适合做什么 | 限制 |
| --- | --- | --- | --- |
| AKShare | [GitHub](https://github.com/akfamily/akshare) / [文档](https://akshare.akfamily.xyz/) | Python 获取股票、指数、财务和宏观数据 | 官方声明主要用于学术研究；数据接口可能调整，需自行检查质量 |
| BaoStock | [官网](https://www.baostock.com/) / [知识库](https://www.baostock.com/mainContent?file=pythonAPI.md) | A 股历史 K 线、交易日、股票基本信息和部分财务数据 | 依赖远程服务；数据服务条款和频率限制要自行确认 |
| Tushare | [官网](https://tushare.pro/) / [API 文档](https://tushare.pro/document/2) | 结构化 A 股、财务和指数数据 | 通常需要注册 Token 和积分；免费额度、接口权限以官网为准 |
| Qlib CN 数据 | [Qlib](https://github.com/microsoft/qlib) | 直接运行中国 A 股和 CSI300 研究示例 | 数据版本和下载状态可能变化；先看仓库当前说明 |

数据源选择建议：

- 想快速试代码：先试 AKShare 或 BaoStock；
- 想做大量因子和财务字段：比较 Tushare、AKShare 和 Qlib 数据；
- 想做严肃研究：保存原始数据、下载日期、字段说明和数据版本，不要只保存最终 CSV。

## 2. 可直接运行的回测框架

### VectorBT

- [官方网站](https://vectorbt.dev/)
- [源代码](https://github.com/polakowo/vectorbt)
- [官方示例资源](https://github.com/polakowo/vectorbt/blob/master/docs/docs/getting-started/resources.md)

适合初学者快速测试均线、止损、参数组合和走步验证。官方资源包含双均线、止损、组合优化和样本外验证示例。

注意：开源版本与专业版本功能不同，许可证是 Apache 2.0 with Commons Clause，商业使用前要认真检查条款。

### RQAlpha

- [源代码](https://github.com/ricequant/rqalpha)
- [策略示例](https://github.com/ricequant/rqalpha/blob/master/docs/source/intro/examples.rst)
- [回测教程](https://github.com/ricequant/rqalpha/blob/master/docs/source/intro/tutorial.rst)

它对 A 股入门很直观，官方示例包含买入并持有、黄金交叉和海龟交易系统；教程展示了股票账户、基准和结果保存。

限制：仓库 README 明确标注仅限非商业使用；不要把它当作无条件的商业基础设施。

### Backtrader

- [官方网站](https://www.backtrader.com/docu/)
- [快速开始](https://github.com/backtrader/backtrader-docs/blob/master/docs/quickstart/quickstart.rst)
- [策略生命周期](https://github.com/backtrader/backtrader-docs/blob/master/docs/strategy.rst)

适合学习事件驱动策略、数据源、指标和 Broker。官方示例包含 SMA 交叉策略和分析器。

限制：默认不会自动替你正确模拟 A 股的 T+1、涨跌停、复权和券商费用，需要自行扩展。

### QuantConnect LEAN

- [源代码](https://github.com/QuantConnect/Lean)
- [Python 算法说明](https://www.quantconnect.com/docs/v2/writing-algorithms)

适合学习多资产事件驱动框架和研究到实盘的工程结构。它不是 A 股券商的直接接入方案，国内市场仍需自行确认数据和 Broker 适配。

## 3. 研究和机器学习框架

### Microsoft Qlib

- [源代码](https://github.com/microsoft/qlib)
- [模型基准](https://github.com/microsoft/qlib/tree/main/examples/benchmarks)
- [基准结果](https://github.com/microsoft/qlib/blob/main/examples/benchmarks/README.md)
- [官方文档](https://qlib.readthedocs.io/)

Qlib 的官方仓库提供 Alpha158、Alpha360、CSI300 和多个模型的 workflow 配置，可以用 `qrun` 运行完整的建模、回测和评估流程。

适合中级以后学习，不建议作为第一个项目：依赖较多，模型示例不等于策略有效，数据版本也会影响结果。

## 4. 实盘框架和策略模板

### vn.py

- [源代码组织](https://github.com/vnpy)
- [CTA 策略模板](https://github.com/vnpy/vnpy/blob/master/docs/community/app/cta_strategy.md)
- [Gateway 文档](https://www.vnpy.com/docs/cn/community/info/gateway.html)

CTA 模板展示了策略生命周期、K 线生成、订单管理和策略文件组织方式。它更适合作为“实盘工程结构”参考；A 股实际交易仍取决于券商提供的接口和权限。

### Freqtrade / Hummingbot

- [Freqtrade](https://github.com/freqtrade/freqtrade)：加密货币趋势机器人，不适用于 A 股；GPL-3.0。
- [Hummingbot](https://github.com/hummingbot/hummingbot)：加密货币做市和套利，不适用于 A 股。

这两个项目可以学习机器人工程和订单管理，但不要因为它们有 Web UI 就拿来做 A 股。

## 5. 可参考的社区成品

社区项目适合阅读目录结构和数据流水线，不应直接连接真实账户：

- [stock-quant](https://github.com/zhaoxusun/stock-quant)：包含 A 股数据、分析、策略和回测示例；先检查依赖、数据源和许可证。
- [baostock_experiments](https://github.com/Donaldshen27/baostock_experiments)：基于 BaoStock 的 A 股分析、回测和 Streamlit 示例；适合观察一个小型项目如何拆分模块。
- [BaoStock 数据下载器](https://github.com/zxygithub/baostock)：展示如何把 BaoStock 数据下载到 SQLite 并做完整性检查；这是数据工程参考，不是交易策略。

社区代码的检查顺序：

1. 看许可证和最近提交；
2. 找数据下载入口和数据字段；
3. 看策略是否使用未来数据；
4. 看是否模拟手续费、滑点、停牌和涨跌停；
5. 用小样本运行，确认结果可复现；
6. 删除所有真实账户、密钥和自动下单配置。

## 6. 现成策略的使用方式

先选一个最简单的策略，不要直接复制收益曲线：

```text
原样运行
    -> 阅读数据和信号
    -> 改成 A 股交易假设
    -> 加入手续费/滑点
    -> 与买入并持有比较
    -> 样本外验证
    -> 再修改策略规则
```

推荐入门顺序：

1. VectorBT 的双均线示例；
2. RQAlpha 的买入并持有和黄金交叉；
3. Backtrader 的 SMA 策略生命周期；
4. Qlib 的 LightGBM/Alpha158 workflow；
5. vn.py 的策略模板和订单管理。

不要把 Qlib 的模型基准、社区项目的收益截图或任何“自动选股”仓库当作实盘证明。

## 7. 免费不等于无条件可用

- 数据接口可能有频率、字段、历史范围和稳定性限制；
- 免费数据不一定允许商业分发；
- 回测框架的许可证可能限制商业使用；
- 开源代码不包含券商权限、交易柜台和合规资格；
- 任何收益示例都必须重新下载数据并独立验证。
