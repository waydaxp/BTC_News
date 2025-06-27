# utils/fetch_sentiment.py

import requests
import datetime

def get_sentiment_summary():
    try:
        url = "https://api.alternative.me/fng/?limit=1"
        response = requests.get(url)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            index_data = data["data"][0]
            value = index_data["value"]
            value_classification = index_data["value_classification"]
            timestamp = int(index_data["timestamp"])
            date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

            summary = f"📊 恐惧与贪婪指数（{date}）\n当前值: {value}（{value_classification}）"
            return summary
        else:
            return "⚠️ 无法获取恐惧与贪婪指数数据"

    except Exception as e:
        return f"❌ 获取情绪指数失败：{str(e)}"
