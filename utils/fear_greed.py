# utils/fear_greed.py
"""
Coingecko Fear & Greed Index
--------------------------------
API:  https://api.alternative.me/fng/?limit=1

返回值：
    idx   -> int      (数值 0-100)
    grade -> str      ("Extreme Fear", …)
    ts_bj -> str      北京时间，格式 "YYYY-MM-DD HH:MM"
"""
from datetime import datetime, timezone, timedelta
import requests

_URL = "https://api.alternative.me/fng/?limit=1"

_CN_TZ = timezone(timedelta(hours=8))          # Beijing UTC+8

def get_fear_and_greed():
    try:
        j = requests.get(_URL, timeout=8).json()["data"][0]
        idx   = int(j["value"])
        grade = j["value_classification"]

        # 原时间戳是秒级 UTC
        utc_ts = datetime.fromtimestamp(int(j["timestamp"]), tz=timezone.utc)
        bj_ts  = utc_ts.astimezone(_CN_TZ).strftime("%Y-%m-%d %H:%M")

        # 用 emoji 简单映射情绪
        emo = "😨" if idx < 50 else "😊"

        return idx, grade, emo, bj_ts
    except Exception as e:                      # 网络 / 解析失败
        print("⚠️ Fear&Greed fetch failed:", e)
        return None, "N/A", "❔", ""
