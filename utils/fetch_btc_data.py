import yfinance as yf
import pandas as pd

def fetch_eth_data():
    df = yf.download("ETH-USD", interval="4h", period="7d", auto_adjust=True, progress=False)
    df.dropna(inplace=True)

    close_price = df["Close"].iloc[-1]
    support = df["Low"][-20:].min()
    resistance = df["High"][-20:].max()
    atr = (df["High"] - df["Low"]).rolling(window=14).mean().iloc[-1]
    volume = df["Volume"].rolling(window=5).mean().iloc[-1]

    # 策略逻辑推导
    if close_price > support and close_price < resistance:
        if close_price > (support + resistance) / 2:
            strategy = "看涨偏多，可考虑轻仓做多。"
            long_tp = resistance + 1.5 * atr
            long_sl = support - 1.2 * atr
            result = {
                "signal": "轻仓做多",
                "price": round(close_price, 2),
                "support": round(support, 2),
                "resistance": round(resistance, 2),
                "atr": round(atr, 2),
                "volume": round(volume, 2),
                "strategy_note": strategy,
                "tp": round(long_tp, 2),
                "sl": round(long_sl, 2)
            }
        else:
            strategy = "震荡偏空，观察支撑是否跌破。"
            short_tp = support - 1.5 * atr
            short_sl = support + 1.2 * atr
            result = {
                "signal": "观望或轻仓做空",
                "price": round(close_price, 2),
                "support": round(support, 2),
                "resistance": round(resistance, 2),
                "atr": round(atr, 2),
                "volume": round(volume, 2),
                "strategy_note": strategy,
                "tp": round(short_tp, 2),
                "sl": round(short_sl, 2)
            }
    else:
        result = {
            "signal": "区间外波动",
            "price": round(close_price, 2),
            "support": round(support, 2),
            "resistance": round(resistance, 2),
            "atr": round(atr, 2),
            "volume": round(volume, 2),
            "strategy_note": "当前价格已突破震荡区间，建议等待确认后操作。",
            "tp": None,
            "sl": None
        }

    return result
