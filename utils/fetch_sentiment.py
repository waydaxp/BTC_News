# utils/fetch_sentiment.py
import requests

def get_sentiment_data():
    try:
        response = requests.get("https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=5m&limit=1")
        data = response.json()[0]
        long_ratio = float(data['longAccount']) * 100
        short_ratio = float(data['shortAccount']) * 100
        msg = f"\n📊【市场情绪】\n多头占比: {long_ratio:.2f}%\n空头占比: {short_ratio:.2f}%"
        if long_ratio > 60:
            msg += "\n⚠️ 多头过热，谨防回调"
        elif short_ratio > 60:
            msg += "\n✅ 空头集中，或有反弹机会"
        else:
            msg += "\n⏸ 市场情绪均衡"
        return msg
    except Exception as e:
        return f"\n⚠️ 无法获取情绪数据: {e}"
