# utils/plot_generator.py

import matplotlib.pyplot as plt
import yfinance as yf
import datetime

def generate_plot():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=14)

    btc = yf.download("BTC-USD", start=start, interval="1h")
    eth = yf.download("ETH-USD", start=start, interval="1h")

    # 计算 MA20
    btc["MA20"] = btc["Close"].rolling(window=20).mean()
    eth["MA20"] = eth["Close"].rolling(window=20).mean()

    # 创建图表
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axs[0].plot(btc.index, btc["Close"], label="BTC Close")
    axs[0].plot(btc.index, btc["MA20"], label="BTC MA20", linestyle="--")
    axs[0].set_title("BTC-USD")
    axs[0].legend()

    axs[1].plot(eth.index, eth["Close"], label="ETH Close", color="purple")
    axs[1].plot(eth.index, eth["MA20"], label="ETH MA20", color="orange", linestyle="--")
    axs[1].set_title("ETH-USD")
    axs[1].legend()

    plt.tight_layout()
    image_path = "output_plot.png"
    plt.savefig(image_path)
    plt.close()

    return image_path
