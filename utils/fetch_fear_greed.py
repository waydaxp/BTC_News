import requests

def get_fear_and_greed_index():
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url)
        data = response.json()

        if "data" not in data or not data["data"]:
            return {
                "index": "N/A",
                "level": "未知",
                "date": "未知"
            }

        latest = data["data"][0]
        return {
            "index": latest["value"],
            "level": latest["value_classification"],
            "date": latest["timestamp"]
        }

    except Exception as e:
        return {
            "index": "错误",
            "level": str(e),
            "date": "N/A"
        }
