# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from datetime import datetime

def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()
    macro = get_macro_event_summary()
    page_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        # BTC 分析结果
        "btc_price":        btc["price"],
        "btc_ma20":         btc["ma20"],
        "btc_rsi":          btc["rsi"],
        "btc_atr":          btc["atr"],
        "btc_signal":       btc["signal"],
        "btc_sl":           btc["sl_1h"],
        "btc_tp":           btc["tp_1h"],
        "btc_qty":          btc["qty_1h"],
        "btc_risk":         btc["risk_usd"],
        "btc_update_time":  btc["update_time"],
        "btc_entry_15m":    btc["entry_15m"],
        "btc_sl_15m":       btc["sl_15m"],
        "btc_tp_15m":       btc["tp_15m"],
        "btc_entry_1h":     btc["entry_1h"],
        "btc_sl_1h":        btc["sl_1h"],
        "btc_tp_1h":        btc["tp_1h"],
        "btc_entry_4h":     btc["entry_4h"],
        "btc_sl_4h":        btc["sl_4h"],
        "btc_tp_4h":        btc["tp_4h"],

        # ETH 分析结果
        "eth_price":        eth["price"],
        "eth_ma20":         eth["ma20"],
        "eth_rsi":          eth["rsi"],
        "eth_atr":          eth["atr"],
        "eth_signal":       eth["signal"],
        "eth_sl":           eth["sl_1h"],
        "eth_tp":           eth["tp_1h"],
        "eth_qty":          eth["qty_1h"],
        "eth_risk":         eth["risk_usd"],
        "eth_update_time":  eth["update_time"],
        "eth_entry_15m":    eth["entry_15m"],
        "eth_sl_15m":       eth["sl_15m"],
        "eth_tp_15m":       eth["tp_15m"],
        "eth_entry_1h":     eth["entry_1h"],
        "eth_sl_1h":        eth["sl_1h"],
        "eth_tp_1h":        eth["tp_1h"],
        "eth_entry_4h":     eth["entry_4h"],
        "eth_sl_4h":        eth["sl_4h"],
        "eth_tp_4h":        eth["tp_4h"],

        # 恐惧与贪婪指数
        "fg_idx":           fg_idx,
        "fg_txt":           fg_txt,
        "fg_emoji":         fg_emoji,
        "fg_ts":            fg_ts,

        # 宏观事件
        "macro_events":     macro,

        # 页面更新时间
        "page_update":      page_update,
    }
