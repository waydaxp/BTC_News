from utils.fetch_btc_data import analyze_btc
from utils.fetch_eth_data import analyze_eth
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_data
from utils.plot_generator import generate_charts
from telegram import send_telegram_message

def run():
    msg_btc = analyze_btc()
    msg_eth = analyze_eth()
    msg_macro = get_macro_events()
    msg_sentiment = get_sentiment_data()
    charts = generate_charts()

    final_msg = msg_btc + msg_eth + msg_sentiment + msg_macro
    send_telegram_message(final_msg, charts)

if __name__ == "__main__":
    run()
