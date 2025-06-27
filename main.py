from telegram_push import send_telegram_message
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary
from utils.plot_generator import generate_plot

def main():
    print("🚀 正在执行每日分析任务...")

    # 获取各项分析数据
    btc_msg = get_btc_analysis()
    eth_msg = get_eth_analysis()
    macro_msg = get_macro_events()
    sentiment_msg = get_sentiment_summary()

    # 组合完整消息
    final_message = (
        f"📈 <b>BTC & ETH 每日策略简报</b>\n\n"
        f"{btc_msg}\n"
        f"{eth_msg}\n"
        f"{macro_msg}\n"
        f"{sentiment_msg}"
    )

    # 发送 Telegram 推送
    send_telegram_message("✅ GitHub 每5分钟任务触发成功")  # 每次运行成功提示
    send_telegram_message(final_message)

    # 生成并保存图表（如需后续拓展自动推图功能）
    img_path = generate_plot()
    if img_path:
        print(f"📷 图表已保存：{img_path}")

if __name__ == "__main__":
    main()
