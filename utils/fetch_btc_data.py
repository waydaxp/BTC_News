# utils/fetch_btc_data.py

import yfinance as yf
import pandas as pd


def get_btc_analysis():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")

    # ✅ 初步数据检查
    if data.empty or len(data) < 30:
        return _fallback_data("⚠️ 数据不足")

    # ✅ MA20 + RSI 计算
    data["MA20"] = data["Close"].rolling(window=20).mean()
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    latest = data.iloc[-1]
    try:
        close_price = float(latest["Close"])
        ma20 = float(latest["MA20"])
        rsi = float(latest["RSI"])

        # ✅ 容错处理：防止 NaN
        if pd.isna(ma20) or pd.isna(rsi):
            return _fallback_data("⚠️ MA20 / RSI 数据未就绪")

        # ✅ 操作建议
        entry = round(close_price, 2)
        stop = round(entry * 0.985, 2)
        target = round(entry * 1.03, 2)

        signal = (
            "✅ 做多信号：突破 MA20 且 RSI 健康" if close_price > ma20 and rsi < 70
            else "🔻 做空信号：跌破 MA20 且 RSI 弱势" if close_price < ma20 and rsi > 30
            else "⏸ 中性信号：观望为主"
        )

        # ✅ 仓位管理
        account_usd = 1000
        leverage = 20
        risk_per_trade = 0.02
        risk = round(account_usd * risk_per_trade, 2)
        position = round(risk * leverage, 2)

        return {
            "price": close_price,
            "ma20": ma20,
            "rsi": rsi,
            "signal": signal,
            "entry_price": entry,
            "stop_loss": stop,
            "take_profit": target,
            "max_loss": risk,
            "per_trade_position": position
        }

    except Exception as e:
        print(f"[ERROR] BTC analysis error: {e}")
        return _fallback_data("⚠️ 分析失败")


def _fallback_data(signal_note: str = "⚠️ 数据异常"):
    """统一返回 fallback 格式，避免 template 报错"""
    return {
        "price": "N/A",
        "ma20": "N/A",
        "rsi": "N/A",
        "signal": signal_note,
        "entry_price": "N/A",
        "stop_loss": "N/A",
        "take_profit": "N/A",
        "max_loss": "N/A",
        "per_trade_position": "N/A",
    }
