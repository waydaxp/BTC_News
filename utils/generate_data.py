import yfinance as yf
import pandas as pd
from strategy_helper import generate_strategy_note

def compute_rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def fetch_crypto_data(symbol="ETH-USD", interval="4h", period="7d"):
    df = yf.download(symbol, interval=interval, period=period, auto_adjust=True, progress=False)
    df.dropna(inplace=True)

    close_price = df["Close"].iloc[-1]
    support = df["Low"][-20:].min()
    resistance = df["High"][-20:].max()
    atr = (df["High"] - df["Low"]).rolling(window=14).mean().iloc[-1]
    ma20 = df["Close"].rolling(window=20).mean().iloc[-1]
    rsi = compute_rsi(df["Close"], 14)
    volume = df["Volume"].rolling(window=5).mean().iloc[-1]

    result = {
        "price": round(close_price, 2),
        "ma20": round(ma20, 2),
        "rsi": round(rsi, 2),
        "atr": round(atr, 2),
        "volume": round(volume, 2),
        "support": round(support, 2),
        "resistance": round(resistance, 2),
        "update_time": pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    }

    signal, strategy_note, sl, tp, pos = generate_strategy_note(close_price, support, resistance, atr, rsi, symbol)
    result.update({
        "signal": signal,
        "strategy_note": strategy_note,
        "tp": tp,
        "sl": sl,
        "position": pos,
        "winrate": "64.5%"  # 可替换为真实回测模块
    })
    return result

def get_all_analysis():
    eth_data = fetch_crypto_data("ETH-USD", "4h", "7d")
    btc_data = fetch_crypto_data("BTC-USD", "4h", "7d")

    return {
        "eth_price": eth_data["price"],
        "eth_ma20": eth_data["ma20"],
        "eth_rsi": eth_data["rsi"],
        "eth_atr": eth_data["atr"],
        "eth_volume": eth_data["volume"],
        "eth_signal_4h": eth_data["signal"],
        "eth_reason_4h": eth_data["strategy_note"],
        "eth_entry_4h": eth_data["price"],
        "eth_sl_4h": eth_data["sl"],
        "eth_tp_4h": eth_data["tp"],
        "eth_strategy_4h": eth_data["strategy_note"],
        "btc_price": btc_data["price"],
        "btc_ma20": btc_data["ma20"],
        "btc_rsi": btc_data["rsi"],
        "btc_atr": btc_data["atr"],
        "btc_volume": btc_data["volume"],
        "btc_signal_4h": btc_data["signal"],
        "btc_reason_4h": btc_data["strategy_note"],
        "btc_entry_4h": btc_data["price"],
        "btc_sl_4h": btc_data["sl"],
        "btc_tp_4h": btc_data["tp"],
        "btc_strategy_4h": btc_data["strategy_note"],
        "fg_idx": "52",  # 示例恐惧贪婪指数
        "fg_txt": "中性",
        "fg_emoji": "😐",
        "page_update": pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    }
