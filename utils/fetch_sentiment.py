# utils/fetch_sentiment.py
import requests

def get_sentiment():
    try:
        response = requests.get("https://api.alternative.me/fng/?limit=1")
        data = response.json()
        value = data['data'][0]['value']
        value_text = data['data'][0]['value_classification']
        return f"🧠【情绪指数】今日恐惧&贪婪指数为 {value}（{value_text}）"
    except Exception as e:
        return "⚠️ 获取情绪指数失败"
