# 本次流水线运行记录

本文记录 2026-08-25 在 `/home/opc/trader` 实际完成的操作，并区分已完成、部分完成和下一步。数据研究采用“先筛选、后研究”，不会把全部股票无条件转换成 Qlib 数据。

## 目标流水线

```text
AKShare 全市场日线
    -> 本地条件筛选
    -> 候选股票/候选日期子集
    -> Qlib 历史特征和标签统计
    -> vn.py 图形化调参和回测
    -> gupiao 每日扫描
    -> 模拟交易
```

全市场数据用于做股票池和日期筛选；Qlib 只处理筛选后的研究样本；vn.py 只承载已经明确的策略逻辑和参数回测。

## 已执行操作

### 1. 仓库检查

```bash
cd /home/opc/trader/datawhale
git branch --show-current
git remote -v
git status --short --branch
```

结果：当前分支为 `main`，远程为 `https://github.com/921394/datawhale.git`，工作区干净。

### 2. 写入方案和下载脚本

已提交：

- `docs/multi-tool-short-term-pipeline.md)：工具分工和研究约束；
- `scripts/download_akshare_a_share.py`：AKShare 下载、重试、并发、断点续传和 manifest；
- `.gitignore`：忽略 Python 缓存。

相关提交：

```text
9a5c3dc docs: add multi-tool short-term data workflow
928e315 feat: make AKShare download resumable
6ce41ef fix: bound AKShare request time
efd0ecd fix: preserve row counts on resume
```

### 3. 环境和烟雾测试

使用已有环境确认 AKShare：

```bash
/home/opc/trader/gupiao/.venv/bin/python -m pip show akshare
```

版本为 `1.18.94`。先下载 3 只股票测试：

```bash
/home/opc/trader/gupiao/.venv/bin/python scripts/download_akshare_a_share.py \
  --start-date 20250101 \
  --end-date 20260825 \
  --adjust qfq \
  --limit 3 \
  --output-dir /home/opc/trader/market_data/akshare/a_share_daily
```

结果：`000001`、`000002`、`000006` 成功，每只约 398 条记录。由于东方财富接口出现远端断开，脚本改为优先使用 AKShare 新浪日线接口，失败时再尝试东方财富。

### 4. 全市场下载

通过 AKShare 的沪深京股票列表接口建立并缓存 5,550 只股票代码，然后执行：

```bash
setsid nohup /home/opc/trader/gupiao/.venv/bin/python -u \
  /home/opc/trader/datawhale/scripts/download_akshare_a_share.py \
  --start-date 20210101 \
  --end-date 20260825 \
  --adjust qfq \
  --provider auto \
  --workers 8 \
  --retries 2 \
  --sleep 0.1 \
  --output-dir /home/opc/trader/market_data/akshare/a_share_daily_20210101_20260825 \
  > /home/opc/trader/market_data/akshare/full_download.log 2>&1 < /dev/null &
```

输出目录：

```text
/home/opc/trader/market_data/akshare/a_share_daily_20210101_20260825
```

每只股票一个 CSV，并配套 `symbols.json` 和 `manifest.json`。重复执行会跳过已有非空文件，适合断点续传。

### 5. 下载修复和校验

部分 AKShare 请求没有默认超时，脚本增加 20 秒统一 HTTP 超时后续传。最终校验结果：

| 项目 | 结果 |
| --- | --- |
| 股票清单 | 5,550 |
| 已生成 CSV | 5,548 |
| 总行数 | 6,821,615 |
| 日期范围 | 2021-01-04 至 2026-08-24 |
| 目录大小 | 约 651 MB |
| 空文件 | 0 |
| 字段格式不一致 | 0 |

实际字段：

```text
code,provider,date,open,high,low,close,volume,amount,float_shares,turnover_pct
```

失败项为 `688835` 和 `689009`，两套接口均返回远端断开或空响应，已保留在 `manifest.json`，没有用其他股票或当前值填补。

## 正确的分区方式

不建议把 5,548 只股票全部转成 Qlib 数据后再开始研究。建议分三层：

```text
全市场 CSV
    -> 日期 T 的粗筛：市值、价格、成交量、换手率、停牌状态
    -> 候选股票池：例如 20-200 只
    -> 候选池的历史特征/标签统计
    -> Qlib 研究和参数验证
```

历史研究按日期分区，不能先用今天的条件筛出股票再回看过去；每个历史日期都必须只使用当时可见的数据。流通股本可以参与计算，但历史流通市值需要按当日有效股本和价格计算，不能用当前市值回填。

## 可视化条件筛选页面结论

现成的高 star 开源项目里，暂时没有同时满足“A 股、网页条件组合筛选、历史日期回放、参数回测和模拟交易”的成熟一体化页面。

- **vn.py**：有桌面 GUI 回测和参数优化，但不是全市场拖拽式条件筛选器。
- **Qlib**：适合研究和回测，主要是 Python、配置和 Notebook，不提供成熟的条件筛选页面。
- **RQAlpha**：支持回测和结果图表，但条件筛选主要通过代码或命令行完成。
- **聚宽、米筐**：网页条件筛选体验更接近目标，但属于云平台，不是完整开源项目。
- **gupiao**：当前 Web 页面适合展示和执行既有扫描逻辑，暂时不是通用条件编辑器。

因此当前最小实现应是：用全市场 CSV 做一个“条件筛选表”，先支持日期、价格、均线、成交量、换手率和市值区间；筛选结果再导出给 Qlib/vn.py。这样页面只处理结果集，不需要加载全部历史数据到浏览器。

## 当前状态

```text
[已完成] AKShare 环境和接口测试
[已完成] 5,550 只股票代码清单
[已完成] 5,548 只股票多年日线 CSV
[已完成] 字段、日期、空文件和目录校验
[部分完成] 688835、689009 数据重试
[未开始] 全市场日期 T 的条件筛选表
[未开始] 候选股票/日期子集的 Qlib 统计
[未开始] vn.py 策略类和图形化回测
[未开始] gupiao 每日扫描复用同一套条件
[未开始] 模拟交易和成交/滑点验证
```

## 恢复下载

```bash
/home/opc/trader/gupiao/.venv/bin/python -u \
  /home/opc/trader/datawhale/scripts/download_akshare_a_share.py \
  --start-date 20210101 \
  --end-date 20260825 \
  --adjust qfq \
  --provider auto \
  --workers 2 \
  --retries 5 \
  --output-dir /home/opc/trader/market_data/akshare/a_share_daily_20210101_20260825
```

CSV 数据没有上传 GitHub，仓库只保存文档、脚本和可恢复命令。
