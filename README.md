# 开源量化交易平台调查

更新时间：2026-08-23

## 结论先行

没有一个框架在研究、回测、实盘接入和低延迟方面都最好。建议把研究层和执行层分开选：

- 国内期货/股票：`vn.py + VectorBT/Qlib`
- 全球多资产：`LEAN`
- 多交易所、强调回测与实盘一致性：`NautilusTrader`
- 加密货币趋势策略：`Freqtrade`
- 加密货币做市/套利：`Hummingbot`
- 机器学习因子研究：`Qlib`

## 框架对比

| 框架 | 适合场景 | 主要特点 | 适合作为完整平台 |
| --- | --- | --- | --- |
| [QuantConnect LEAN](https://github.com/QuantConnect/Lean) | 全球股票、期货、期权、外汇、加密货币 | C# 核心，支持 Python；事件驱动；本地回测和实盘；多资产 | 是 |
| [NautilusTrader](https://nautilustrader.io/docs/) | 多市场、多交易所、对延迟和回测一致性有要求 | Rust 原生核心，Python 写策略；回测和实盘共用事件模型 | 是 |
| [vn.py / VeighNa](https://www.vnpy.com/) | 中国期货、股票、期权、CTP | Python；国内 Gateway 较丰富；包含 CTA、套利和算法交易应用 | 是，国内市场优先 |
| [Microsoft Qlib](https://github.com/microsoft/qlib) | 因子研究、机器学习、组合优化 | 覆盖数据处理、因子、模型训练、回测、风险和组合流程 | 研究层为主 |
| [VectorBT](https://vectorbt.dev/) | 参数扫描、因子研究、快速回测 | 基于 NumPy、pandas、Numba/Rust，适合批量实验 | 否，研究层为主 |
| [Freqtrade](https://github.com/freqtrade/freqtrade) | 加密货币趋势策略 | Python；回测、Dry-run、实盘、Web UI、Telegram、参数优化 | 是，偏个人机器人 |
| [Hummingbot](https://github.com/hummingbot/hummingbot) | 加密货币做市、套利、CEX/DEX | 交易所连接器多，专注自动化做市和套利 | 是，偏加密执行 |
| [Backtrader](https://www.backtrader.com/docu/) | 学习、简单策略和传统回测 | Python；接口直观，指标和 Broker 支持丰富 | 不建议作为新平台核心 |
| [Zipline Reloaded](https://github.com/fstp/zipline-reloaded) | 股票研究和事件驱动回测 | Quantopian Zipline 的社区维护版本 | 研究层为主 |

## 推荐架构

```text
数据层：行情、复权、合约信息、交易日历
研究层：因子、特征、回测、组合优化
执行层：订单路由、成交回报、撤单、重连、持仓同步
风控层：限仓、限频、最大亏损、熔断、人工接管
```

推荐先完成一个最小闭环：

```text
历史回测 -> 仿真盘/Dry-run -> 小资金实盘
```

## 选型说明

### 国内市场

优先看 `vn.py`。它对 CTP、期货、期权和国内交易场景的接入更直接。研究部分可以用 `VectorBT` 做快速实验，或用 `Qlib` 做因子和机器学习流程。

### 全球多资产

优先看 `LEAN`。它的事件驱动模型、资产类别覆盖和本地运行能力适合搭建通用平台。需要更强的性能、确定性模拟和研究到实盘一致性时，考虑 `NautilusTrader`。

### 加密货币

- 趋势、网格、量化择时：`Freqtrade`
- 做市、跨所套利、CEX/DEX：`Hummingbot`
- 需要更通用的多交易所生产引擎：`NautilusTrader`

## 需要提前确认的风险

1. 开源框架不代表行情数据免费。数据质量、复权、合约生命周期和交易日历往往是主要工作量。
2. 回测通过不代表实盘可靠。订单状态同步、断线恢复、重复下单保护和人工接管必须单独验证。
3. 商业化前检查许可证。不同项目的许可证不同，例如 Freqtrade 使用 GPL-3.0，不能默认按任意方式闭源分发。
4. 不要一开始同时部署多个框架。先选一个市场和一个策略，完成回测、仿真和小资金实盘闭环。

## 参考链接

- [LEAN Engine 文档](https://www.quantconnect.com/docs/v2/lean-engine)
- [NautilusTrader 文档](https://nautilustrader.io/docs/)
- [VeighNa 官网](https://www.vnpy.com/)
- [Qlib GitHub](https://github.com/microsoft/qlib)
- [VectorBT 文档](https://vectorbt.dev/)
- [Freqtrade GitHub](https://github.com/freqtrade/freqtrade)
- [Hummingbot GitHub](https://github.com/hummingbot/hummingbot)
- [Backtrader 文档](https://www.backtrader.com/docu/)
- [Zipline Reloaded GitHub](https://github.com/fstp/zipline-reloaded)
