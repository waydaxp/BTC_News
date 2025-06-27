# ✅ generate_data.py
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index
from datetime import datetime, timedelta

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_event_summary()
    fear_data = get_fear_and_greed_index()

    # 判断信号方向
    signal = btc.get("signal", "")
    if "做多" in signal:
        show_long = True
        show_short = False
    elif "做空" in signal:
        show_long = False
        show_short = True
    else:
        show_long = False
        show_short = False

    now_bj = datetime.utcnow() + timedelta(hours=8)
    updated_time = now_bj.strftime("%Y-%m-%d %H:%M（北京时间）")

    data = {
        # BTC 数据
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": signal,
        "btc_entry": btc.get("entry_price", "N/A"),
        "btc_stop": btc.get("stop_loss", "N/A"),
        "btc_target": btc.get("take_profit", "N/A"),
        "btc_risk": btc.get("max_loss", "N/A"),
        "btc_position": btc.get("per_trade_position", "N/A"),
        "btc_long_strategy": "✅ 做多：买入 → 涨\n止损：跌 1.5%\n止盈：涨 3%",
        "btc_short_strategy": "🔻 做空：卖出 → 跌\n止损：涨 1.5%\n止盈：跌 3%",

        # ETH 数据
        "eth_price": eth.get("price", "N/A"),
        "eth_ma20": eth.get("ma20", "N/A"),
        "eth_rsi": eth.get("rsi", "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        # 宏观
        "macro_events": macro,

        # 情绪
        "fear_index": fear_data.get("index", "N/A"),
        "fear_level": fear_data.get("level", "N/A"),
        "fear_date": fear_data.get("date", "N/A"),

        # 控制开关
        "show_long": show_long,
        "show_short": show_short,
        "updated_time": updated_time
    }

    return data
