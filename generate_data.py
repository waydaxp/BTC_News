# 文件：generate_data.py
import json
from datetime import datetime
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_events
from utils.fetch_sentiment import get_fear_greed_index

# 获取所有分析结果
data = {
    "btc": get_btc_analysis(),
    "eth": get_eth_analysis(),
    "events": get_macro_events(),
    "sentiment": get_fear_greed_index(),
    "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
}

# 写入 JSON 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 数据已更新并保存到 data.json")
