import yfinance as yf
import pandas as pd
import datetime
import requests
import os

# ========= 配置 Telegram 推送（可选） =========
ENABLE_TELEGRAM = False  # 设置为 True 启用推送
BOT_TOKEN = os.environ.get("8149475252:AAEkYJRGJSQje6w1i57gjPOFhXRiZ2Ghf-0")
CHAT_ID = os.environ.get("BTCYing_bot")


def send_telegram_message(message):
    if not ENABLE_TELEGRAM:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("❌ Telegram 发送失败：", e)


# ========= 获取 BTC 数据并分析 =========
def analyze_btc():
    print("获取 BTC 数据中...")
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")

    # 计算 MA20 和 RSI
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

    # 生成信号
    if close_price > ma20 and rsi < 70:
        signal = "✅ 做多信号：价格高于 MA20，RSI 正常"
    elif close_price < ma20 and rsi > 30:
        signal = "❌ 做空信号：价格低于 MA20，RSI 正常"
    else:
        signal = "⏸ 观望信号：价格在震荡区间，无明确信号"

    # 格式化输出
    output = f"""【BTC 技术分析】
当前价格: ${close_price:.2f}
MA20: ${ma20:.2f}
RSI: {rsi:.2f}
信号建议: {signal}
"""
    return output


# ========= 宏观事件提醒 =========
def get_macro_events():
    today = datetime.date.today()
    events = [
        {"event": "美国CPI公布", "time": "2025-06-28", "impact": "若超预期，BTC或承压"},
        {"event": "FOMC利率会议", "time": "2025-07-03", "impact": "加息可能引发波动"},
        {
            "event": "SEC审查比特币ETF",
            "time": "2025-07-10",
            "impact": "若通过，或引发大涨",
        },
    ]
    message = "\n【宏观事件提醒】\n"
    for e in events:
        d = datetime.datetime.strptime(e["time"], "%Y-%m-%d").date()
        days = (d - today).days
        message += f"- {e['event']}（{e['time']}，{days}天后）：{e['impact']}\n"
    return message


# ========= 主执行 =========
if __name__ == "__main__":
    btc_msg = analyze_btc()
    event_msg = get_macro_events()
    final_msg = btc_msg + event_msg
    print(final_msg)

    # 可选：发送 Telegram 消息
    send_telegram_message(final_msg)
