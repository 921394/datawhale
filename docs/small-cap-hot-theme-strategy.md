# 小盘股热点与补涨策略调查

> 这是一份研究记录，不是投资建议。当前项目只做本地回测和仿真，不连接真实账户。

## 结论先行

目前没有找到“拿来即能稳定盈利”的公开成品。比较有学习价值的是把两个方向拆开：

- **小市值基线**：用流动性和交易规则过滤后，定期买入小市值股票，收益假设是规模因子和轮动，而不是新闻预测。
- **热点补涨信号**：从涨幅榜、概念板块联动和新闻催化剂中找强势板块的滞涨股，属于候选生成器，需要独立回测证明有效性。

## 可直接研究的开源例子

### 1. CTBZStock：小市值回测基线

[CTBZStock](https://github.com/thisiszhou/CTBZStock) 的 `strategy/backtrade/small_cap_demo.py` 适合先跑通流程。核心逻辑包括：

- 股票池限定主板代码（`00`、`60`），排除 ST、停牌、退市风险和上市不足 30 天的股票；
- 排除开盘价缺失、涨跌停等无法按假设成交的情况；
- 按总市值升序选取每日前 `TOP_NUM=10`，全仓等权并按日轮换；
- 单笔交易金额低于 `MIN_TRADE_VALUE=5000` 时不交易。

它的潜在收益来源是**小盘股规模溢价 + 高频换仓**，没有新闻、情绪或热点判断。因此它更适合作为 A 组基线，而不是“上涨预告策略”。项目需要 MyQuant/Gm 数据和 Python 环境，README 没有给出经过独立验证的稳定实盘收益。

### 2. news-stock-selector：热点补涨候选生成器

[news-stock-selector](https://github.com/AXBIAO/news-stock-selector) 是 Claude Code Skill，不是独立的历史回测框架。它的 `catchup_engine.py` 体现了较清晰的研究假设：

- 从成交额达到约 `5e7` 的涨幅榜中取样；
- 按通达信概念板块聚类，要求至少 2 只领涨股和 1 只滞涨股；
- 领涨股涨幅至少约 5%，滞涨股涨幅低于约 2%；
- 用领涨平均涨幅、领涨数量和滞涨程度计算板块热度，再取前 5 个板块；
- 新闻分层评分由情绪、催化剂、置信度、策略匹配和“三高”构成，并对政策/并购、业绩、技术等催化剂加权；
- 对已涨停、接近涨停、消息已充分定价、市场或板块过热等情况做折扣或风险标记。

它适合提炼“板块先动、个股滞涨、新闻催化”的选股逻辑，但仓库内仍有硬编码示例数据，`feedback.jsonl` 只是简单的次日反馈记录，不等于无未来数据泄漏的样本外回测。小市值缺失时用“股价低于 20 元”做代理也不严谨，不能直接当作市值筛选。运行还依赖通达信和 Tushare 等本地数据配置。

## 可直接运行的相近项目

### 3. gupiao：全市场短线扫描

[gupiao](https://github.com/WCSY-YG/gupiao) 与当前目标最接近。它提供 `short_term` 1～3 个交易日模式、竞价开盘突破、温和缺口修复、放量突破和低波动突破等策略，并支持全市场扫描、买卖计划和回测。早盘模式只使用前一交易日及以前的日 K，加上当天 09:25 前的竞价数据；回测包含 T+1、涨停不可买、跌停不可卖和停牌不可成交等约束。

典型入口：

```bash
conda run -n agent env PYTHONPATH=src python -m gupiao.cli screen list
conda run -n agent env PYTHONPATH=src python -m gupiao.cli screen morning --db data/cache/market_scan.sqlite --trade-date 2026-05-29 --horizon short_term --top 20 --limit 500 --auction-provider local_jingjia
conda run -n agent env PYTHONPATH=src python -m gupiao.cli backtest morning --db data/cache/market_scan.sqlite --start 2026-01-01 --end 2026-05-29 --horizon short_term --auction-provider local_jingjia
```

它适合直接改造成“当前全市场候选扫描器”，但项目本身没有证明这些策略在未来仍能稳定盈利；竞价增强也应先与纯 K 线基线做对照。

### 4. a-share-quant-sim：小市值、动量和短持有期

[a-share-quant-sim](https://github.com/fkchaos/a-share-quant-sim) 是更适合研究参数的框架，包含动量、市值、流动性、换手率和情绪因子，支持横截面打分、回测、滚动 walk-forward 和模拟交易。项目提供无 API 密钥的快速运行路径：

```bash
git clone https://github.com/fkchaos/a-share-quant-sim.git
cd a-share-quant-sim
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python3 scripts/tools/init_project.py
python3 scripts/backtest/wf_runner.py --strategy v68
```

它的实验记录提到，部分有效版本与“硬动量过滤 + 小市值暴露 + 短持有期”有关，和本调查目标相近。不过仓库也明确提示成本模型、生存者偏差、容量和涨跌停成交仍有局限，应先做纸面交易。

### 5. limit-up-sniper：首板题材短线

[limit-up-sniper](https://github.com/guoyaohua/limit-up-sniper) 主要研究首板涨停、低流通市值、题材延续和 Tick 行情，提供离线回归测试、Tick 回测和模拟交易。它比“启动 3～5 天后持有 1～3 天”更激进，适合作为题材短线的对照策略，不适合直接当作本项目默认策略；QMT/XTQuant 实盘接口也应保持关闭。

综合适配度排序：`gupiao` 适合先做全市场短线扫描，`a-share-quant-sim` 适合研究小市值和动量参数，`CTBZStock` 适合参考完整的小市值回测/模拟交易链路，`news-stock-selector` 适合提取热点补涨规则，`limit-up-sniper` 适合作为高风险题材策略对照。

## 建议的验证实验

不要直接把热点规则接到实盘，先做同一数据集上的三组对照：

| 组别 | 选股逻辑 | 目的 |
| --- | --- | --- |
| A | 小市值基线 | 测量规模因子和轮动本身的收益 |
| B | A + 板块领涨/滞涨补涨 | 测量板块联动是否增加超额收益 |
| C | B + 带时间戳的新闻催化剂 | 测量新闻信息是否在成本后仍有增量 |

最低数据字段：交易日、股票代码、复权 OHLCV、成交额、流通市值、停牌/涨跌停状态、概念板块映射、新闻发布时间和新闻分类。标签至少包含信号后的 `T+1`、`T+3` 收益，以及相对中证全指或行业基准的超额收益。

验证时使用滚动或 walk-forward 时间切分，严格按新闻发布时间截断可见信息；把手续费、印花税、滑点、涨跌停无法成交、停牌和换手率纳入回测。除总收益外，重点看 `precision@k`、超额收益、最大回撤、换手率、收益稳定性和不同市场阶段的表现。

## 当前使用边界

这些仓库可以作为学习素材、回测基线和候选生成器，但都不能证明“根据热点提前买入就能稳定盈利”。本项目下一步应先复现 A 组，再逐项加入 B、C 的特征，并保留可解释的交易日志；在没有样本外、成本后结果前，不做自动下单。

## 如何拆解 gupiao，避免把它当黑盒

不要只看 Web 页面里的股票名单。应同时检查源码、单次输出、历史回测和输入数据。

### 1. 先看策略注册表

```bash
conda run -n agent env PYTHONPATH=src python -m gupiao.cli screen list
```

先记录每个策略的 ID、适用周期、决策时点、入场时点，以及是否依赖集合竞价。源码可以从 [`src/gupiao/strategies`](https://github.com/WCSY-YG/gupiao/tree/main/src/gupiao/strategies) 和 [`screening.py`](https://github.com/WCSY-YG/gupiao/blob/main/src/gupiao/strategies/screening.py) 开始阅读，再沿着 `factors`、`auction`、`backtest`、`signals` 和 `trade_plan.py` 追踪数据流。

### 2. 只复现一只股票和一个历史日期

```bash
conda run -n agent env PYTHONPATH=src python -m gupiao.cli screen run \
  --strategy momentum_pullback \
  --bars data/000001_daily.jsonl \
  --symbol 000001 \
  --as-of 2026-05-29
```

`--as-of` 表示只使用该日期及以前的数据，是检查未来数据泄漏的关键。先确认输入数据、信号日期和输出字段，再扩展到全市场。

### 3. 查看买卖计划，而不是只看“入选”

```bash
conda run -n agent env PYTHONPATH=src python -m gupiao.cli plan trade \
  --db data/cache/market_scan.sqlite \
  --symbol 000001 \
  --trade-date 2026-05-29 \
  --horizon short_term \
  --auction-provider local_jingjia
```

重点核对：入选原因、参考买入价、买入时点、止损、止盈、最长持有期、信号失效条件和不买条件。

### 4. 用回测报告验证交易假设

```bash
conda run -n agent env PYTHONPATH=src python -m gupiao.cli backtest morning \
  --db data/cache/market_scan.sqlite \
  --symbol 000001 \
  --start 2026-01-01 \
  --end 2026-05-29 \
  --horizon short_term \
  --auction-provider local_jingjia

conda run -n agent env PYTHONPATH=src python -m gupiao.cli report breakout \
  --bars data/000001_daily.jsonl \
  --symbol 000001 \
  --output reports/generated/000001_breakout.md
```

报告中应检查交易明细、成交价、手续费、滑点、最大回撤、持有期和无法成交的情况。网页 Dashboard 适合浏览，Markdown/JSON 产物更适合审计。

### 5. 最后才做批量扫描

```bash
conda run -n agent env PYTHONPATH=src python -m gupiao.cli screen candidates \
  --strategy low_volatility_breakout \
  --db data/cache/market_scan.sqlite \
  --as-of 2026-05-29 \
  --lookback 180 \
  --top 30 \
  --limit 500
```

`balanced`、`win_rate` 和 `return` 是候选排序目标，不等于校准过的上涨概率。尤其 `win_rate` 组不能解释为“每只股票有对应百分比的上涨概率”，仍必须回到逐笔交易和样本外结果验证。
