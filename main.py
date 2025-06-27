from telegram_push import send_telegram_message
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary
from utils.plot_generator import generate_plot

def main():
    print("📊 正在生成加密货币分析报告...")

    # 获取分析内容
    btc_msg = get_btc_analysis()
    eth_msg = get_eth_analysis()
    macro_msg = get_macro_events()
    sentiment_msg = get_sentiment_summary()
    
    # 组合消息
    final_message = (
        f"📈 <b>BTC & ETH 每日策略简报</b>\n\n"
        f"{btc_msg}\n"
        f"{eth_msg}\n"
        f"{macro_msg}\n"
        f"{sentiment_msg}"
    )

    # 发送文字报告
    send_telegram_message(final_message)

    # 生成图像（图像推送功能可扩展支持 sendPhoto）
    img_path = generate_plot()
    if img_path:
        print(f"📷 图表已保存至: {img_path}")

if __name__ == "__main__":
    main()
