from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from utils.strategy_helper import get_strategy_explanation
from datetime import datetime, timedelta, timezone

def get_all_analysis() -> dict:
    # 获取分析数据
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()
    macro = get_macro_event_summary()

    # 设置北京时间
    beijing_tz = timezone(timedelta(hours=8))
    page_update = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")

    return {
        # === BTC 数据 ===
        "btc_price":        btc.get("price"),
        "btc_ma20":         btc.get("ma20"),
        "btc_rsi":          btc.get("rsi"),
        "btc_atr":          btc.get("atr"),
        "btc_signal":       btc.get("signal"),
        "btc_signal_15m":   btc.get("signal_15m"),
        "btc_signal_1h":    btc.get("signal_1h"),
        "btc_signal_4h":    btc.get("signal_4h"),
        "btc_sl":           btc.get("sl_1h"),
        "btc_tp":           btc.get("tp_1h"),
        "btc_qty":          btc.get("qty_1h"),
        "btc_risk":         btc.get("risk_usd"),
        "btc_update_time":  btc.get("update_time"),
        "btc_entry_15m":    btc.get("entry_15m"),
        "btc_sl_15m":       btc.get("sl_15m"),
        "btc_tp_15m":       btc.get("tp_15m"),
        "btc_entry_1h":     btc.get("entry_1h"),
        "btc_sl_1h":        btc.get("sl_1h"),
        "btc_tp_1h":        btc.get("tp_1h"),
        "btc_entry_4h":     btc.get("entry_4h"),
        "btc_sl_4h":        btc.get("sl_4h"),
        "btc_tp_4h":        btc.get("tp_4h"),
        "btc_win_rate":     btc.get("win_rate", 0),
        "btc_reason_15m":   btc.get("reason_15m"),
        "btc_reason_1h":    btc.get("reason_1h"),
        "btc_reason_4h":    btc.get("reason_4h"),
        "btc_strategy_15m": get_strategy_explanation(btc.get("signal_15m", "")),
        "btc_strategy_1h":  get_strategy_explanation(btc.get("signal_1h", "")),
        "btc_strategy_4h":  get_strategy_explanation(btc.get("signal_4h", "")),

        # === ETH 数据 ===
        "eth_price":        eth.get("price"),
        "eth_ma20":         eth.get("ma20"),
        "eth_rsi":          eth.get("rsi"),
        "eth_atr":          eth.get("atr"),
        "eth_signal":       eth.get("signal"),
        "eth_signal_15m":   eth.get("signal_15m"),
        "eth_signal_1h":    eth.get("signal_1h"),
        "eth_signal_4h":    eth.get("signal_4h"),
        "eth_sl":           eth.get("sl_1h"),
        "eth_tp":           eth.get("tp_1h"),
        "eth_qty":          eth.get("qty_1h"),
        "eth_risk":         eth.get("risk_usd"),
        "eth_update_time":  eth.get("update_time"),
        "eth_entry_15m":    eth.get("entry_15m"),
        "eth_sl_15m":       eth.get("sl_15m"),
        "eth_tp_15m":       eth.get("tp_15m"),
        "eth_entry_1h":     eth.get("entry_1h"),
        "eth_sl_1h":        eth.get("sl_1h"),
        "eth_tp_1h":        eth.get("tp_1h"),
        "eth_entry_4h":     eth.get("entry_4h"),
        "eth_sl_4h":        eth.get("sl_4h"),
        "eth_tp_4h":        eth.get("tp_4h"),
        "eth_win_rate":     eth.get("win_rate", 0),
        "eth_reason_15m":   eth.get("reason_15m"),
        "eth_reason_1h":    eth.get("reason_1h"),
        "eth_reason_4h":    eth.get("reason_4h"),
        "eth_strategy_15m": get_strategy_explanation(eth.get("signal_15m", "")),
        "eth_strategy_1h":  get_strategy_explanation(eth.get("signal_1h", "")),
        "eth_strategy_4h":  get_strategy_explanation(eth.get("signal_4h", "")),

        # === 市场情绪 & 宏观事件 ===
        "fg_idx":           fg_idx,
        "fg_txt":           fg_txt,
        "fg_emoji":         fg_emoji,
        "fg_ts":            fg_ts,
        "macro_events":     macro,
        "page_update":      page_update,
    }
