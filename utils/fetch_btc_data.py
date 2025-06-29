# utils/fetch_btc_data.py
import yfinance as yf
from datetime import datetime, timezone, timedelta

from core.indicators import add_basic_indicators

PAIR = "BTC-USD"      # Coinbase 现货
PERIOD = "7d"
INTERVAL = "60m"


def get_btc_analysis() -> dict:
    df = yf.download(PAIR, period=PERIOD, interval=INTERVAL, progress=False)
    df = df.rename(columns=str.title)        # 高低收列转大写首字母
    df = add_basic_indicators(df)

    last = df.iloc[-1]

    price = float(last["Close"])
    ma20 = float(last["MA20"])
    rsi = float(last["RSI"])
    atr = float(last["ATR"])

    # === 信号判定 ===
    if price > ma20 and 30 < rsi < 70:
        direction = "long"
        signal = "✅ 做多信号：站上 MA20 且 RSI 健康"
    elif price < ma20 and 30 < rsi < 70:
        direction = "short"
        signal = "🔻 做空信号：跌破 MA20 且 RSI 弱势"
    else:
        direction = "flat"
        signal = "⏸ 中性信号：观望为主"

    # === 风控（ATR 动态止损 / 止盈 1:1.5） ===
    risk_usd = 20            # 单笔可承受亏损
    leverage = 20
    position = risk_usd * leverage

    if direction == "long":
        stop_loss = round(price - atr, 2)
        take_profit = round(price + 1.5 * atr, 2)
    elif direction == "short":
        stop_loss = round(price + atr, 2)
        take_profit = round(price - 1.5 * atr, 2)
    else:
        stop_loss = take_profit = None

    bj_time = datetime.now(timezone(timedelta(hours=8))).strftime("%F %T")

    return {
        "price": price,
        "ma20": ma20,
        "rsi": rsi,
        "atr": atr,
        "signal": signal,
        "direction": direction,
        "entry_price": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_usd": risk_usd,
        "position": position,
        "updated_time": bj_time,
    }
