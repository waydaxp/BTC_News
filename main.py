import yfinance as yf
import pandas as pd
import datetime
import requests
import os

# ========= ✅ 配置 Telegram =========
ENABLE_TELEGRAM = True  # 是否启用推送

# 建议使用环境变量：适用于本地运行或 GitHub Actions
BOT_TOKEN = os.environ.get("8149475252:AAEkYJRGJSQje6w1i57gjPOFhXRiZ2Ghf-0")
CHAT_ID = os.environ.get("BTCYing_bot") 

def send_telegram_message(message):
    if not ENABLE_TELEGRAM:
        print("🔕 Telegram 推送未启用")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        print("✅ Telegram 发送成功")
        print("响应：", response.text)
    except Exception as e:
        print("❌ Telegram 发送失败：", e)

# ========= ✅ 获取 BTC 分析 =========
def analyze_btc():
    print("📈 获取 BTC 数据中...")
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")

    if data.empty:
        return "❌ 无法获取 BTC 数据"

    # MA20 和 RSI
    data["MA20"] = data["Close"].rolling(window=20).mean()
    delta = data["Close"].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = (-delta.clip(upper=0)).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    latest = data.iloc[-1]
    close = latest["Close"]
    ma20 = latest["MA20"]
    rsi = latest["RSI"]

    # 生成信号
    if close > ma20 and rsi < 70:
        signal = "✅ 做多信号（价格 > MA20 且 RSI 健康）"
    elif close < ma20 and rsi > 30:
        signal = "❌ 做空信号（价格 < MA20 且 RSI 健康）"
    else:
        signal = "⏸ 观望（无明显趋势）"

    return f"""【BTC 技术分析】
现价: ${close:.2f}
MA20: ${ma20:.2f}
RSI: {rsi:.2f}
信号: {signal}
"""

# ========= ✅ 宏观事件提醒 =========
def get_macro_events():
    today = datetime.date.today()
    events = [
        {"event": "美国CPI公布", "time": "2025-06-28", "impact": "若超预期，BTC或承压"},
        {"event": "FOMC利率会议", "time": "2025-07-03", "impact": "加息可能引发波动"},
        {"event": "SEC审查比特币ETF", "time": "2025-07-10", "impact": "若通过，或引发大涨"},
    ]
    message = "📅【宏观事件提醒】\n"
    for e in events:
        date_obj = datetime.datetime.strptime(e["time"], "%Y-%m-%d").date()
        days_left = (date_obj - today).days
        message += f"- {e['event']}（{e['time']}，{days_left}天后）：{e['impact']}\n"
    return message

# ========= ✅ 主执行 =========
if __name__ == "__main__":
    try:
        btc_msg = analyze_btc()
        macro_msg = get_macro_events()
        final_msg = btc_msg + "\n" + macro_msg
        print(final_msg)
        send_telegram_message(final_msg)
    except Exception as err:
        print("❌ 脚本执行出错：", err)
        send_telegram_message(f"❌ BTC Bot 执行失败：{err}")
