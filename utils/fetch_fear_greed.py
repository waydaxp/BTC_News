# utils/fetch_fear_greed.py

import requests
from datetime import datetime
import pytz

def get_fear_and_greed():
    """
    从 Alternative.me 的 Fear & Greed Index API 获取最新数据，
    返回 (指数值:int, 文本分类:str, 表情符号:str, 更新时间:str) 四元组。
    """
    url = "https://api.alternative.me/fng/?limit=1"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    if not data:
        # 如果接口失效，返回占位
        now = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M")
        return 0, "N/A", "😐", now

    item = data[0]
    value = int(item.get("value", 0))
    text  = item.get("value_classification", "N/A")
    ts    = int(item.get("timestamp", 0))

    # 转 UTC→北京时间
    dt_utc = datetime.utcfromtimestamp(ts).replace(tzinfo=pytz.utc)
    dt_cn  = dt_utc.astimezone(pytz.timezone("Asia/Shanghai"))
    ts_str = dt_cn.strftime("%Y-%m-%d %H:%M")

    # 简易表情：小于50恐惧，否则贪婪
    emoji = "😨" if value < 50 else "😊"

    return value, text, emoji, ts_str
