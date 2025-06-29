from datetime import datetime
from utils.fetch_btc_data    import get_btc_analysis
from utils.fetch_eth_data    import get_eth_analysis
from utils.fetch_macro_events import get_macro_events
from utils.fetch_fear_greed  import get_fear_and_greed   # 假设已有

def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    # 恐惧贪婪
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()

    return {
        # BTC
        "btc_price":      btc["price"],
        "btc_ma20":       btc["ma20"],
        "btc_rsi":        btc["rsi"],
        "btc_atr":        btc["atr"],
        "btc_signal":     btc["signal"],
        "btc_sl":         btc["sl"],
        "btc_tp":         btc["tp"],
        "btc_qty":        btc["qty"],
        "btc_risk":       btc["risk_usd"],
        "btc_update_time":btc["update_time"],

        # ETH
        "eth_price":      eth["price"],
        "eth_ma20":       eth["ma20"],
        "eth_rsi":        eth["rsi"],
        "eth_atr":        eth["atr"],
        "eth_signal":     eth["signal"],
        "eth_sl":         eth["sl"],
        "eth_tp":         eth["tp"],
        "eth_qty":        eth["qty"],
        "eth_risk":       eth["risk_usd"],
        "eth_update_time":eth["update_time"],

        # 宏观 & 心理面
        "macro_events":   "<br>".join(get_macro_events(5)),
        "fg_idx":         fg_idx,
        "fg_txt":         fg_txt,
        "fg_emoji":       fg_emoji,
        "fg_ts":          fg_ts,

        # 页面更新时间
        "page_update":    datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
