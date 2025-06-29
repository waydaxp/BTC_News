import yfinance as yf
import pandas as pd                    # ← 新增
from datetime import datetime
from core.indicators import add_basic_indicators

PAIR = "ETH-USD"

CFG = {
    "15m": dict(interval="15m", period="3d"),
    "1h" : dict(interval="60m", period="14d"),
    "4h" : dict(interval="4h",  period="60d"),
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:   # ← 修改
    df = yf.download(
        PAIR,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=False,
    ).dropna()

    df = add_basic_indicators(df)
    df.index = df.index.tz_localize("UTC")
    return df

def get_eth_analysis() -> dict:
    dfs      = {k: _download_tf(**v) for k, v in CFG.items()}
    df_1h    = dfs["1h"]
    df_4h    = dfs["4h"]
    df_15m   = dfs["15m"]

    last_1h  = df_1h.iloc[-1]
    last_4h  = df_4h.iloc[-1]
    price    = float(last_1h["Close"])
    ma20     = float(last_1h["MA20"])
    rsi      = float(last_1h["RSI"])
    atr      = float(last_1h["ATR"])

    trend_up = (last_4h["Close"] > last_4h["MA20"]) and \
               (df_15m["Close"].tail(12) > df_15m["MA20"].tail(12)).all()
    trend_dn = (last_4h["Close"] < last_4h["MA20"]) and \
               (df_15m["Close"].tail(12) < df_15m["MA20"].tail(12)).all()

    if trend_up and price > ma20 and 30 < rsi < 70:
        direction = "long"
        signal    = "✅ 做多信号：多级别均线上方 & RSI 健康"
    elif trend_dn and price < ma20 and 30 < rsi < 70:
        direction = "short"
        signal    = "🔻 做空信号：多级别均线下方 & RSI 健康"
    else:
        direction = "neutral"
        signal    = "⏸ 中性信号：观望为主"

    entry = round(price, 2)
    if direction == "long":
        stop   = round(price - atr, 2)
        target = round(price + 1.5 * atr, 2)
    elif direction == "short":
        stop   = round(price + atr, 2)
        target = round(price - 1.5 * atr, 2)
    else:
        stop = target = None

    account_usd       = 1000
    risk_per_trade    = 0.02
    max_loss          = round(account_usd * risk_per_trade, 2)
    leverage          = 20
    position_usd      = round(max_loss * leverage, 2)

    return {
        "price"        : price,
        "ma20"         : ma20,
        "rsi"          : rsi,
        "atr"          : atr,
        "signal"       : signal,
        "direction"    : direction,
        "entry_price"  : entry,
        "stop_loss"    : stop,
        "take_profit"  : target,
        "max_loss"     : max_loss,
        "position_usd" : position_usd,
        "update_time"  : datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    }
