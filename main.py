# main.py

import os
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary
from utils.plot_generator import generate_plot
from telegram_push import send_telegram_message

def main():
    # 获取 BTC 和 ETH 技术面分析
    btc_analysis = get_btc_analysis()
    eth_analysis = get_eth_analysis()

    # 获取宏观事件提醒
    macro_events = get_macro_events()

    # 获取恐惧与贪婪指数
    sentiment_msg = get_sentiment_summary()

    # 生成图表并返回路径
    plot_path = generate_plot()  # 默认生成 BTC/ETH 技术图

    # 汇总消息
    final_message = f"""📈【数字货币分析简报】
{btc_analysis}

{eth_analysis}

📅【宏观事件提醒】
{macro_events}

{sentiment_msg}

📌 操作建议
💰 初始资金：$1000 / 杠杆：20x
🎯 单笔最大风险建议：$20（即2%）
✅ 控制每日总开仓次数 ≤ 3，避免过度交易
🧠 建议：根据信号只做顺势交易，避免震荡期双向被止损
"""

    # 推送图文消息
    send_telegram_message(final_message, image_path=plot_path)


if __name__ == "__main__":
    main()
