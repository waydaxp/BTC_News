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
    emoji = {
        "Extreme Fear":"😨", "Fear":"😨",
        "Neutral":"😐",
        "Greed":"😊", "Extreme Greed":"😊"
    }.get(txt, "")
    ts = datetime.utcfromtimestamp(int(rec["timestamp"])).replace(
        tzinfo=pytz.utc
    ).astimezone(pytz.timezone("Asia/Shanghai"))
    ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    return idx, txt, emoji, ts_str
