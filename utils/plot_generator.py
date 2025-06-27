# utils/plot_generator.py
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

def generate_chart(symbol="BTC-USD", filename="btc_chart.png"):
    data = yf.download(symbol, period="1mo", interval="1d")
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data["Close"], label="Close")
    plt.title(f"{symbol} 日线图")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    return filename

