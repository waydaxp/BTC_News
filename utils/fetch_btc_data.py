import yfinance as yf
import pandas as pd

def fetch_btc_data():
    # 下载过去7天的4小时K线
    df = yf.download("BTC-USD", interval="4h", period="7d", auto_adjust=True, progress=False)
    df.dropna(inplace=True)

    # 关键参数计算
    close_price = df["Close"].iloc[-1]
    support = df["Low"][-20:].min()
    resistance = df["High"][-20:].max()
    atr = (df["High"] - df["Low"]).rolling(window=14).mean().iloc[-1]
    ma20 = df["Close"].rolling(window=20).mean().iloc[-1]
    rsi = compute_rsi(df["Close"], 14)
    volume = df["Volume"].rolling(window=5).mean().iloc[-1]

    # 策略逻辑判断
    if support < close_price < resistance:
        if close_price > (support + resistance) / 2:
            signal = "轻仓做多"
            strategy_note = (
                "当前价格在区间中上部运行，走势偏多。\n"
                f"📈 若突破 ${round(resistance)} 可上看 {round(resistance + 2 * atr)}～{round(resistance + 2.5 * atr)}。\n"
                f"📊 仓位建议：30%以内，止盈止损结合 ATR 设置。"
            )
            sl = round(support - 1.2 * atr, 2)
            tp = round(resistance + 2 * atr, 2)
        else:
            signal = "观望或轻仓做空"
            strategy_note = (
                "当前价格偏向区间下沿，若跌破支撑需警惕下行。\n"
                f"📉 若跌破 ${round(support)}，目标可设至 {round(support - 2 * atr)}，止损设在 {round(support + 1.2 * atr)}。\n"
                f"📊 仓位建议：20%以内，严格风控。"
            )
            sl = round(support + 1.2 * atr, 2)
            tp = round(support - 2 * atr, 2)
    else:
        signal = "区间外震荡"
        strategy_note = "当前价格已脱离支撑/阻力区间，建议等待回踩或放量确认后再操作。"
        sl = None
        tp = None

    return {
        "price": round(close_price, 2),
        "ma20": round(ma20, 2),
        "rsi": round(rsi, 2),
        "atr": round(atr, 2),
        "volume": round(volume, 2),
        "support": round(support, 2),
        "resistance": round(resistance, 2),
        "signal": signal,
        "strategy_note": strategy_note,
        "tp": tp,
        "sl": sl,
        "update_time": pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    }

def compute_rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]
