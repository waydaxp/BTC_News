# utils/plot_generator.py
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

def generate_charts():
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    tickers = ["BTC-USD", "ETH-USD"]
    paths = []
    for t in tickers:
        data = yf.Ticker(t).history(period="7d", interval="1h")
        data["MA20"] = data["Close"].rolling(20).mean()
        plt.figure()
        plt.title(f"{t} 日线走势 - {now}")
        plt.plot(data["Close"], label="Close")
        plt.plot(data["MA20"], label="MA20")
        plt.legend()
        path = f"chart_{t.split('-')[0]}.png"
        plt.savefig(path)
        paths.append(path)
    return paths
