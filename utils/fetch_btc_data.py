import pandas as pd
import yfinance as yf
from datetime import datetime, timezone
from core.indicators import add_basic_indicators
from core.signal      import make_signal
from core.risk        import calc_position_size, ATR_MULT_SL, ATR_MULT_TP

PAIR = "BTC-USD"

# 不同级别 K 线下载配置
INTERVALS = {
    "1h":  {"interval": "60m", "period": "4d"},
    "4h":  {"interval": "240m", "period": "30d"},
    "15m": {"interval": "15m", "period": "2d"},
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """下载并附加指标"""
    df: pd.DataFrame = yf.download(
        PAIR, interval=interval, period=period, progress=False
    )
    # Yahoo 的列是大写首字母
    df.columns = [c.capitalize() for c in df.columns]
    df.index   = df.index.tz_localize("UTC").tz_convert("Asia/Shanghai")
    df         = add_basic_indicators(df)  # MA20 / ATR / RSI
    return df.dropna()

def get_btc_analysis() -> dict:
    """生成 BTC 多空信号 & 交易参数"""
    dfs      = {k: _download_tf(**cfg) for k, cfg in INTERVALS.items()}
    df_1h, df_4h, df_15m = dfs["1h"], dfs["4h"], dfs["15m"]

    # ➊ 最新行情
    last_1h = df_1h.iloc[-1]
    price   = float(last_1h["Close"])
    atr     = float(last_1h["ATR"])

    # ➋ 生成信号（注意参数顺序：1h → 15m → 4h）
    signal, trend_up = make_signal(df_1h, df_15m, df_4h)

    # ➌ 计算风控
    risk_usd, qty     = calc_position_size(price, atr)
    stop_loss         = round(price - ATR_MULT_SL * atr, 2) if trend_up else round(price + ATR_MULT_SL * atr, 2)
    take_profit       = round(price + ATR_MULT_TP * atr, 2) if trend_up else round(price - ATR_MULT_TP * atr, 2)

    return {
        "price":      price,
        "ma20":       float(last_1h["MA20"]),
        "rsi":        float(last_1h["RSI"]),
        "signal":     signal,
        "entry":      price,
        "stop":       stop_loss,
        "target":     take_profit,
        "risk_usd":   risk_usd,
        "position":   qty,
        "atr":        atr,
        "update":     datetime.now(timezone.utc).astimezone().strftime("%F %T"),
    }
