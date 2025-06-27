import os
import datetime
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_info
from utils.plot_generator import generate_plots

import requests

# ======================= Telegram 推送封装 ======================
def send_telegram_message(text):
    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not bot_token or not chat_id:
        print("❌ 缺少 BOT_TOKEN 或 CHAT_ID 环境变量")
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, data=payload)
        print("✅ 已发送 Telegram 消息")
    except Exception as e:
        print("❌ Telegram 发送失败：", e)

# ======================= 主逻辑 ======================
if __name__ == "__main__":
    print("⏳ 开始生成 BTC & ETH 分析报告...")

    # 1. 获取分析内容
    btc_analysis = get_btc_analysis()
    eth_analysis = get_eth_analysis()
    macro_events = get_macro_events()
    sentiment_info = get_sentiment_info()

    # 2. 拼接信息
    full_report = f"""
📊【BTC 日内策略分析】
{btc_analysis}

🟣【ETH 对照分析建议】
{eth_analysis}

📅【宏观事件提醒】
{macro_events}

🧠【多空情绪与持仓比】
{sentiment_info}
"""

    print(full_report)
    send_telegram_message(full_report)

    # 3. 图表生成
    try:
        generate_plots()
    except Exception as e:
        print("⚠️ 图表生成失败：", e)
