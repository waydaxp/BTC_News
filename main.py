import yfinance as yf
import pandas as pd
import datetime
import requests
import os

# ===== Telegram 配置 =====
ENABLE_TELEGRAM = True
BOT_TOKEN = "8149475252:AAEkYJRGJSQje6w1i57gjPOFhXRiZ2Ghf-0"
CHAT_ID = "5264947511"

def send_telegram_message(message):
    if not ENABLE_TELEGRAM:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("❌ Telegram 发送失败：", e)

# ===== 技术分析（BTC）=====
def analyze_btc():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")

    data["MA20"] = data["Close"].rolling(window=20).mean()
    delta = data["Close"].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = -delta.clip(upper=0).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))
    data["ATR"] = data["High"].rolling(window=14).max() - data["Low"].rolling(window=14).min()

    latest = data.iloc[-1]
    close = latest["Close"]
    ma20 = latest["MA20"]
    rsi = latest["RSI"]
    atr = latest["ATR"]

    # 交易信号判断
    if close > ma20 and rsi < 70:
        signal = "✅ 做多信号（价格高于 MA20，RSI 正常）"
    elif close < ma20 and rsi > 30:
        signal = "❌ 做空信号（价格低于 MA20，RSI 正常）"
    else:
        signal = "⏸ 观望（无明确方向）"

    stop_loss = close - atr
    take_profit = close + 2 * atr

    msg = f"""【BTC 技术分析】
📈 当前价格: ${close:.2f}
📊 MA20: ${ma20:.2f}
🧮 RSI: {rsi:.2f}
📉 ATR（日内波动参考）: ${atr:.2f}
📌 信号建议: {signal}

💡 日内操作建议：
✅ 入场位：${close:.2f}
📍止损位：${stop_loss:.2f}
🎯止盈位：${take_profit:.2f}
"""
    return msg

# ===== 宏观事件提醒 =====
def get_macro_events():
    today = datetime.date.today()
    events = [
        {"event": "美国CPI公布", "time": "2025-06-28", "impact": "若超预期，BTC或承压"},
        {"event": "FOMC利率会议", "time": "2025-07-03", "impact": "加息可能引发波动"},
        {"event": "SEC审查比特币ETF", "time": "2025-07-10", "impact": "若通过，或引发大涨"},
    ]
    msg = "\n📅【宏观事件提醒】\n"
    for e in events:
        d = datetime.datetime.strptime(e["time"], "%Y-%m-%d").date()
        days = (d - today).days
        msg += f"- {e['event']}（{e['time']}，{days}天后）：{e['impact']}\n"
    return msg

# ===== 执行入口 =====
if __name__ == "__main__":
    analysis = analyze_btc()
    macro = get_macro_events()
    full_message = analysis + macro
    print(full_message)
    send_telegram_message(full_message)
