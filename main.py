import os
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary
from utils.plot_generator import generate_price_plot
from utils.telegram_sender import send_telegram_message


def main():
    # 获取 BTC 分析
    btc_message = get_btc_analysis()

    # 获取 ETH 分析
    eth_message = get_eth_analysis()

    # 获取宏观事件提醒
    macro_message = get_macro_events()

    # 获取市场情绪摘要（可选）
    sentiment = get_sentiment_summary()

    # 生成图表
    chart_path = generate_price_plot()

    # 合并消息内容
    final_message = f"""
    
