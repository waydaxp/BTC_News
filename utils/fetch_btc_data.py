# -*- coding: utf-8 -*-
"""
拉取 Binance BTC/USDT K 线 & 生成分析 dict
----------------------------------------
依赖：python-binance, pandas, pandas_market_calendars
"""

import pandas as pd
from datetime import datetime, timezone
from binance.spot import Spot as Client

from core.signal import make_signal
from indicators import add_basic_indicators

BINANCE = Client()

PAIR = "BTCUSDT"
LIMIT = 500           # 500 根足够
INTERVALS = {
    "15m": "15m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d"
}


def _fetch(interval: str) -> pd.DataFrame:
    k = BINANCE.klines(PAIR, interval=interval, limit=LIMIT)
    df = pd.DataFrame(k, columns=[
        "open_time", "open", "high", "low", "close",
        "volume", "_c1", "_c2", "_c3", "_c4", "_c5", "_c6"
    ]).astype({"open": float, "high": float,
               "low": float, "close": float, "volume": float})
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.set_index("open_time", inplace=True)
    return df


def get_btc_analysis() -> dict:
    dfs = {k: _fetch(v) for k, v in INTERVALS.items()}

    sig = make_signal(dfs["1h"], dfs["4h"], dfs["1d"], dfs["15m"])

    price = dfs["1h"]["close"].iloc[-1]
    side_txt = {"long": "✅ 做多", "short": "🔻 做空", "neutral": "⏸ 观望"}[sig["direction"]]

    strategy_note = f"{side_txt}：{('买入→涨' if sig['direction']=='long' else '卖出→跌')}" \
                    f" 跌 {round(sig['atr'] / price * 100,2)}% 止损，涨 {round(sig['atr'] * 1.5 / price * 100,2)}% 止盈" \
                    if sig["direction"] in ("long", "short") else "等待方向明确"

    return {
        "symbol": "BTC/USDT",
        "price": price,
        "direction": sig["direction"],
        "strategy_text": strategy_note,
        "sl": sig["sl"],
        "tp": sig["tp"],
        "update_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    }
