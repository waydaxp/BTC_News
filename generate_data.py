def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()
    macro = get_macro_event_summary()
    page_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        # BTC
        "btc_price":        btc["price"],
        "btc_ma20":         btc["ma20"],
        "btc_rsi":          btc["rsi"],
        "btc_atr":          btc["atr"],
        "btc_signal":       btc["signal"],
        "btc_sl":           btc["sl"],
        "btc_tp":           btc["tp"],
        "btc_qty":          btc["qty"],
        "btc_risk":         btc["risk_usd"],
        "btc_update_time":  btc["update_time"],
        "btc_entry_15m":    btc.get("entry_15m", "N/A"),
        "btc_sl_15m":       btc.get("sl_15m", "N/A"),
        "btc_tp_15m":       btc.get("tp_15m", "N/A"),
        "btc_entry_1h":     btc.get("entry_1h", "N/A"),
        "btc_sl_1h":        btc.get("sl_1h", "N/A"),
        "btc_tp_1h":        btc.get("tp_1h", "N/A"),
        "btc_entry_4h":     btc.get("entry_4h", "N/A"),
        "btc_sl_4h":        btc.get("sl_4h", "N/A"),
        "btc_tp_4h":        btc.get("tp_4h", "N/A"),

        # ETH
        "eth_price":        eth["price"],
        "eth_ma20":         eth["ma20"],
        "eth_rsi":          eth["rsi"],
        "eth_atr":          eth["atr"],
        "eth_signal":       eth["signal"],
        "eth_sl":           eth["sl"],
        "eth_tp":           eth["tp"],
        "eth_qty":          eth["qty"],
        "eth_risk":         eth["risk_usd"],
        "eth_update_time":  eth["update_time"],
        "eth_entry_15m":    eth.get("entry_15m", "N/A"),
        "eth_sl_15m":       eth.get("sl_15m", "N/A"),
        "eth_tp_15m":       eth.get("tp_15m", "N/A"),
        "eth_entry_1h":     eth.get("entry_1h", "N/A"),
        "eth_sl_1h":        eth.get("sl_1h", "N/A"),
        "eth_tp_1h":        eth.get("tp_1h", "N/A"),
        "eth_entry_4h":     eth.get("entry_4h", "N/A"),
        "eth_sl_4h":        eth.get("sl_4h", "N/A"),
        "eth_tp_4h":        eth.get("tp_4h", "N/A"),

        # 恐惧与贪婪
        "fg_idx":           fg_idx,
        "fg_txt":           fg_txt,
        "fg_emoji":         fg_emoji,
        "fg_ts":            fg_ts,

        # 宏观事件
        "macro_events":     macro,

        # 更新时间
        "page_update":      page_update,
    }
