import os
from telegram_push import send_telegram_message
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary
from utils.plot_generator import generate_plot

def main():
    # 基础分析
    btc_msg = get_btc_analysis()
    eth_msg = get_eth_analysis()
    macro_msg = get_macro_events()
    sentiment_msg = get_sentiment_summary()

    # 资金与仓位控制建议
    capital = 1000  # 美元
    leverage = 20
    risk_per_trade = 0.01
    max_loss = capital * risk_per_trade
    advice = f"💰 建议单笔风险金额: ${max_loss:.2f}（总资金 ${capital}，杠杆 x{leverage}）\n📌 仓位控制建议: 每次不超过总仓位的 5~10%\n🧠 心态提示: 控制情绪、严守止损、勿频繁加仓\n"

    # 图表生成
    plot_path = generate_plot()

    # 汇总消息
    final_message = f"""📈【BTC/ETH 技术分析】
{btc_msg}
{eth_msg}
📊【多空情绪】
{sentiment_msg}
📅【宏观事件提醒】
{macro_msg}
📋【交易建议】
{advice}
"""

    print(final_message)

    # Telegram 推送（文字 + 图片）
    send_telegram_message(final_message.strip(), image_path=plot_path)

if __name__ == "__main__":
    main()
