from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis

def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    # 统一 Key，前端模板里就用 btc_* / eth_* 取值
    ctx = {
        # ----- BTC -----
        "btc_price"       : btc["price"],
        "btc_signal"      : btc["signal"],
        "btc_ma20"        : btc["ma20"],
        "btc_rsi"         : btc["rsi"],
        "btc_atr"         : btc["atr"],
        "btc_sl"          : btc["sl"],
        "btc_tp"          : btc["tp"],
        "btc_qty"         : btc["qty"],
        "btc_risk"        : btc["risk_usd"],
        "btc_update_time" : btc["update_time"],
        # ----- ETH -----
        "eth_price"       : eth["price"],
        "eth_signal"      : eth["signal"],
        "eth_ma20"        : eth["ma20"],
        "eth_rsi"         : eth["rsi"],
        "eth_atr"         : eth["atr"],
        "eth_sl"          : eth["sl"],
        "eth_tp"          : eth["tp"],
        "eth_qty"         : eth["qty"],
        "eth_risk"        : eth["risk_usd"],
        "eth_update_time" : eth["update_time"],
    }
    return ctx
