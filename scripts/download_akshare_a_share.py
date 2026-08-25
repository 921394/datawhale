#!/usr/bin/env python3
"""Download resumable A-share daily bars from AKShare."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
from datetime import date
from pathlib import Path

import akshare as ak
import requests


_REQUEST = requests.sessions.Session.request


def _request_with_timeout(self, method, url, **kwargs):
    kwargs.setdefault("timeout", 20)
    return _REQUEST(self, method, url, **kwargs)


# AKShare's Sina adapter does not set a timeout for every request.
requests.sessions.Session.request = _request_with_timeout


COLUMN_MAP = {
    "日期": "date",
    "开盘": "open",
    "最高": "high",
    "最低": "low",
    "收盘": "close",
    "成交量": "volume",
    "成交额": "amount",
    "振幅": "amplitude",
    "涨跌幅": "change_pct",
    "涨跌额": "change",
    "换手率": "turnover_pct",
    "outstanding_share": "float_shares",
    "turnover": "turnover_ratio",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", default="20210101", help="YYYYMMDD")
    parser.add_argument("--end-date", default=date.today().strftime("%Y%m%d"), help="YYYYMMDD")
    parser.add_argument("--adjust", choices=("", "qfq", "hfq"), default="qfq")
    parser.add_argument(
        "--provider",
        choices=("auto", "sina", "eastmoney"),
        default="auto",
        help="AKShare history endpoint; auto tries Sina before Eastmoney",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("../market_data/akshare/a_share_daily"))
    parser.add_argument("--limit", type=int, default=0, help="only download the first N symbols")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--sleep", type=float, default=0.3, help="seconds between requests")
    parser.add_argument("--workers", type=int, default=1, help="parallel download workers")
    return parser.parse_args()


def load_symbols(retries: int) -> list[str]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            frame = ak.stock_info_a_code_name()
            code_column = next(
                column for column in ("code", "证券代码", "A股代码") if column in frame.columns
            )
            codes = frame[code_column].astype(str).str.extract(r"(\d{6})")[0].dropna().unique().tolist()
            return sorted(code for code in codes if code.startswith(("0", "3", "4", "6", "8", "9")))
        except Exception as error:  # network providers can fail transiently
            last_error = error
            if attempt < retries:
                time.sleep(attempt * 2)
    raise RuntimeError(f"failed to load A-share symbol list: {last_error}") from last_error


def download_symbol(code: str, args: argparse.Namespace) -> tuple[int, str]:
    output_path = args.output_dir / f"{code}.csv"
    if output_path.exists() and output_path.stat().st_size > 100:
        return 0, "skipped"

    last_error: Exception | None = None
    for attempt in range(1, args.retries + 1):
        try:
            providers = ("sina", "eastmoney") if args.provider == "auto" else (args.provider,)
            frame = None
            provider_used = ""
            provider_error: Exception | None = None
            for provider in providers:
                try:
                    if provider == "sina":
                        prefix = "sh" if code.startswith("6") else "sz" if code.startswith(("0", "3")) else "bj"
                        frame = ak.stock_zh_a_daily(
                            symbol=f"{prefix}{code}",
                            start_date=args.start_date,
                            end_date=args.end_date,
                            adjust=args.adjust,
                        )
                    else:
                        frame = ak.stock_zh_a_hist(
                            symbol=code,
                            period="daily",
                            start_date=args.start_date,
                            end_date=args.end_date,
                            adjust=args.adjust,
                        )
                    provider_used = provider
                    break
                except Exception as error:
                    provider_error = error
            if frame is None:
                raise RuntimeError(f"all providers failed: {provider_error}")
            if frame.empty:
                return 0, "empty"
            frame = frame.rename(columns=COLUMN_MAP)
            missing = {"date", "open", "high", "low", "close"} - set(frame.columns)
            if missing:
                raise ValueError(f"{code}: missing columns {sorted(missing)}")
            if "turnover_ratio" in frame:
                frame["turnover_pct"] = frame["turnover_ratio"] * 100
                frame = frame.drop(columns=["turnover_ratio"])
            frame.insert(0, "code", code)
            frame.insert(1, "provider", provider_used)
            temporary_path = output_path.with_suffix(".csv.tmp")
            frame.to_csv(temporary_path, index=False)
            temporary_path.replace(output_path)
            return len(frame), f"downloaded:{provider_used}"
        except Exception as error:  # keep one failed symbol from stopping the batch
            last_error = error
            if attempt < args.retries:
                time.sleep(attempt * 2)
    return -1, f"failed: {last_error}"


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbols_path = args.output_dir / "symbols.json"
    if symbols_path.exists():
        symbols = json.loads(symbols_path.read_text(encoding="utf-8"))
    else:
        symbols = load_symbols(args.retries)
        symbols_path.write_text(json.dumps(symbols, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.limit > 0:
        symbols = symbols[: args.limit]

    manifest_path = args.output_dir / "manifest.json"
    manifest = {
        "source": "AKShare.stock_zh_a_daily or AKShare.stock_zh_a_hist",
        "adjust": args.adjust or "raw",
        "start_date": args.start_date,
        "end_date": args.end_date,
        "symbols_requested": len(symbols),
        "completed": {},
    }
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["completed"].update(previous.get("completed", {}))

    def record(index: int, code: str, result: tuple[int, str]) -> None:
        rows, status = result
        manifest["completed"][code] = {"rows": rows, "status": status}
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{index}/{len(symbols)}] {code}: {status} ({rows})", flush=True)

    if args.workers <= 1:
        for index, code in enumerate(symbols, start=1):
            record(index, code, download_symbol(code, args))
            time.sleep(args.sleep)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            jobs = {executor.submit(download_symbol, code, args): (index, code) for index, code in enumerate(symbols, 1)}
            for future in concurrent.futures.as_completed(jobs):
                index, code = jobs[future]
                try:
                    result = future.result()
                except Exception as error:
                    result = (-1, f"failed: {error}")
                record(index, code, result)

    downloaded = sum(item["status"].startswith("downloaded") for item in manifest["completed"].values())
    failed = sum(item["status"].startswith("failed") for item in manifest["completed"].values())
    print(f"finished: downloaded={downloaded}, failed={failed}, output={args.output_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
