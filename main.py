import os
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary
from utils.telegram_bot import send_telegram_message

# 获取所有模块数据
btc_message = get_btc_analysis()
eth_message = get_eth_analysis()
macro_message = get_macro_events()
sentiment_summary = get_sentiment_summary()

# 组合最终推送内容
final_message = f"""
📊 BTC/ETH 每日策略简报（带图推送）

{btc_message}

{eth_message}

🧠 市场情绪与仓位建议：
{sentiment_summary}

📅 宏观事件提醒：
{macro_message}
"""

# 输出到控制台
print(final_message)

# 推送到 Telegram
send_telegram_message(final_message)
