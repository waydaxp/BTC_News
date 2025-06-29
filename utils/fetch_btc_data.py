# utils/fetch_btc_data.py
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators

PAIR = "BTC-USD"

# 每个周期下载参数
CFG = {
    "15m": dict(interval="15m", period="3d",  limit=800),   # 3 天覆盖 ~288 根
    "1h" : dict(interval="60m", period="14d", limit=800),
    "4h" : dict(interval="4h",  period="60d", limit=800),
}

def _download_tf(interval: str, period: str, **_) -> yf.pd.DataFrame:
    """
    下载并补充指标；返回索引为 timezone-aware DatetimeIndex 的 DataFrame
    """
    df = yf.download(
        PAIR,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=False,  # 显式关闭自动复权，避免 FutureWarning
    )
    df = df.dropna()
    df = add_basic_indicators(df)
    df.index = df.index.tz_localize("UTC")  # 统一成 UTC，便于后续合并
    return df

def get_btc_analysis() -> dict:
    """
    汇总三周期数据 → 生成交易建议
    """
    dfs = {k: _download_tf(**v) for k, v in CFG.items()}
    df_1h  = dfs["1h"]
    df_4h  = dfs["4h"]
    df_15m = dfs["15m"]

    last_1h  = df_1h.iloc[-1]
    last_4h  = df_4h.iloc[-1]
    price    = float(last_1h["Close"])
    ma20     = float(last_1h["MA20"])
    rsi      = float(last_1h["RSI"])
    atr      = float(last_1h["ATR"])

    # ---- 信号逻辑 ----------------------------------------------------------
    # 大趋势：4h MA20； 短趋势：15m MA20 最近 12 根连续方向验证
    trend_up_4h  = last_4h["Close"] > last_4h["MA20"]
    trend_up_15m = (df_15m["Close"].tail(12) > df_15m["MA20"].tail(12)).all()
    trend_dn_4h  = last_4h["Close"] < last_4h["MA20"]
    trend_dn_15m = (df_15m["Close"].tail(12) < df_15m["MA20"].tail(12)).all()

    if trend_up_4h and trend_up_15m and price > ma20 and 30 < rsi < 70:
        direction = "long"
        signal    = "✅ 做多信号：多级别均线上方 & RSI 健康"
    elif trend_dn_4h and trend_dn_15m and price < ma20 and 30 < rsi < 70:
        direction = "short"
        signal    = "🔻 做空信号：多级别均线下方 & RSI 健康"
    else:
        direction = "neutral"
        signal    = "⏸ 中性信号：观望为主"

    # ---- 风控/仓位 --------------------------------------------------------
    entry = round(price, 2)
    if direction == "long":
        stop   = round(price - atr, 2)          # ATR 止损
        target = round(price + 1.5 * atr, 2)    # 1:R=1.5 动态止盈
    elif direction == "short":
        stop   = round(price + atr, 2)
        target = round(price - 1.5 * atr, 2)
    else:
        stop = target = None

    # 资金管理（示例）
    account_usd      = 1000
    risk_per_trade   = 0.02          # 2 %
    max_loss         = round(account_usd * risk_per_trade, 2)
    leverage         = 20
    position_size_usd= round(max_loss * leverage, 2)

    return {
        "price"      : price,
        "ma20"       : ma20,
        "rsi"        : rsi,
        "atr"        : atr,
        "signal"     : signal,
        "direction"  : direction,
        "entry_price": entry,
        "stop_loss"  : stop,
        "take_profit": target,
        "max_loss"   : max_loss,
        "position_usd": position_size_usd,
        "update_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    }
