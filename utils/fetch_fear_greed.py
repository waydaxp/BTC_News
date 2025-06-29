# utils/fetch_fear_greed.py

import requests
from datetime import datetime
import pytz

def get_fear_and_greed():
    url = "https://api.alternative.me/fng/?limit=1"
    data = requests.get(url, timeout=5).json().get("data", [])
    if not data:
        return 0, "Unknown", "", ""
    
    rec = data[0]
    idx = int(rec["value"])
    txt = rec["value_classification"]

    # 表情映射
    emoji = {
        "Extreme Fear": "😨",
        "Fear": "😨",
        "Neutral": "😐",
        "Greed": "😊",
        "Extreme Greed": "😊"
    }.get(txt, "")

    # 时间戳转换为北京时间
    utc_dt = datetime.utcfromtimestamp(int(rec["timestamp"]))  # UTC 时间
    beijing_tz = pytz.timezone("Asia/Shanghai")
    beijing_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(beijing_tz)
    ts_str = beijing_dt.strftime("%Y-%m-%d %H:%M:%S")  # 格式化北京时间

    return idx, txt, emoji, ts_str
