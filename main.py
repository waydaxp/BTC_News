import yfinance as yf
import datetime
import requests

# === 手动写入配置 ===
ENABLE_TELEGRAM = True
BOT_TOKEN = "8149475252:AAEkYJRGJSQje6w1i57gjPOFhXRiZ2Ghf-0"
CHAT_ID = "5264947511"

def send_telegram_message(message):
    if not ENABLE_TELEGRAM:
        print("Telegram 推送未启用")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        print("✅ Telegram 返回：", response.status_code, response.text)
    except Exception as e:
        print("❌ Telegram 发送失败：", e)

def analyze_btc():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")
    data["MA20"] = data["Close"].rolling(window=20).mean()
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    latest = data.iloc[-1]
    close_price = latest["Close"]
    ma20 = latest["MA20"]
    rsi = latest["RSI"]

    if close_price > ma20 and rsi < 70:
        signal = "✅ 做多信号：价格高于 MA20，RSI 正常"
    elif close_price < ma20 and rsi > 30:
        signal = "❌ 做空信号：价格低于 MA20，RSI 正常"
    else:
        signal = "⏸ 观望信号：价格在震荡区间，无明确信号"

    output = f"""【BTC 技术分析】
当前价格: ${close_price:.2f}
MA20: ${ma20:.2f}
RSI: {rsi:.2f}
信号建议: {signal}
"""
    return output

def get_macro_events():
    today = datetime.date.today()
    events = [
        {"event": "美国CPI公布", "time": "2025-06-28", "impact": "若超预期，BTC或承压"},
        {"event": "FOMC利率会议", "time": "2025-07-03", "impact": "加息可能引发波动"},
        {"event": "SEC审查比特币ETF", "time": "2025-07-10", "impact": "若通过，或引发大涨"},
    ]
    msg = "\n【宏观事件提醒】\n"
    for e in events:
        d = datetime.datetime.strptime(e["time"], "%Y-%m-%d").date()
        days = (d - today).days
        msg += f"- {e['event']}（{e['time']}，{days}天后）：{e['impact']}\n"
    return msg

if __name__ == "__main__":
    btc_msg = analyze_btc()
    macro_msg = get_macro_events()
    final_msg = btc_msg + macro_msg
    print(final_msg)
    send_telegram_message(final_msg)
