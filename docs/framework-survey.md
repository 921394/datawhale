# 开源量化交易框架调查

更新时间：2026-08-23

## 结论

没有一个框架在研究、回测、实盘接入和低延迟方面都最好。研究层和执行层可以分开选择。

| 框架 | 适合场景 | 主要特点 | 定位 |
| --- | --- | --- | --- |
| [QuantConnect LEAN](https://github.com/QuantConnect/Lean) | 全球股票、期货、期权、外汇、加密货币 | C# 核心，支持 Python；事件驱动；本地回测和实盘 | 综合平台 |
| [NautilusTrader](https://nautilustrader.io/docs/) | 多市场、多交易所、对延迟和回测一致性有要求 | Rust 原生核心，Python 写策略；回测和实盘共用事件模型 | 生产级执行 |
| [vn.py / VeighNa](https://www.vnpy.com/) | 中国期货、股票、期权、CTP | Python；国内 Gateway 较丰富；包含 CTA、套利和算法交易应用 | 国内市场优先 |
| [Microsoft Qlib](https://github.com/microsoft/qlib) | 因子研究、机器学习、组合优化 | 覆盖数据处理、因子、模型训练、回测、风险和组合流程 | 研究层 |
| [VectorBT](https://vectorbt.dev/) | 参数扫描、因子研究、快速回测 | 基于 NumPy、pandas、Numba/Rust，适合批量实验 | 研究层 |
| [Freqtrade](https://github.com/freqtrade/freqtrade) | 加密货币趋势策略 | Python；回测、Dry-run、实盘、Web UI、参数优化 | 加密机器人 |
| [Hummingbot](https://github.com/hummingbot/hummingbot) | 加密货币做市、套利、CEX/DEX | 交易所连接器多，专注自动化做市和套利 | 加密执行 |
| [Backtrader](https://www.backtrader.com/docu/) | 学习、简单策略和传统回测 | Python；接口直观，指标和 Broker 支持丰富 | 传统回测 |
| [Zipline Reloaded](https://github.com/fstp/zipline-reloaded) | 股票研究和事件驱动回测 | Quantopian Zipline 的社区维护版本 | 研究层 |

## 国内市场怎么选

- **A 股研究和本地回测：**先用 Python、`pandas` 和 VectorBT；不要先接券商接口。
- **A 股实盘：**先找支持量化接口的券商，再根据券商提供的 XTP、TORA、QMT、PTrade 等接口选择 Gateway。
- **国内期货：**`vn.py + CTP` 的接入路径相对直接，但本项目当前不以期货为目标。
- **机器学习因子：**等基础回测正确后再考虑 Qlib，不要把模型复杂度当作策略质量。

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
