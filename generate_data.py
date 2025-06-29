# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from datetime import datetime
import pytz

def get_all_analysis() -> dict:
    # 各币种技术分析
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    # 恐惧与贪婪指数
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()

    # 宏观事件
    macro = get_macro_event_summary()

    # 页面更新时间（北京时间）
    cn_time = datetime.now(pytz.timezone("Asia/Shanghai"))
    page_update = cn_time.strftime("%Y-%m-%d %H:%M:%S")

    return {
        # BTC 技术分析
        "btc_price": btc["price"],
        "btc_ma20": btc["ma20"],
        "btc_rsi": btc["rsi"],
        "btc_atr": btc["atr"],
        "btc_signal": btc["signal"],
        "btc_sl": btc["sl"],
        "btc_tp": btc["tp"],
        "btc_qty": btc["qty"],
        "btc_risk": btc["risk_usd"],
        "btc_update_time": btc["update_time"],

        # ETH 技术分析
        "eth_price": eth["price"],
        "eth_ma20": eth["ma20"],
        "eth_rsi": eth["rsi"],
        "eth_atr": eth["atr"],
        "eth_signal": eth["signal"],
        "eth_sl": eth["sl"],
        "eth_tp": eth["tp"],
        "eth_qty": eth["qty"],
        "eth_risk": eth["risk_usd"],
        "eth_update_time": eth["update_time"],

        # 恐惧与贪婪
        "fg_idx": fg_idx,
        "fg_txt": fg_txt,
        "fg_emoji": fg_emoji,
        "fg_ts": fg_ts,

        # 宏观事件
        "macro_events": macro,

        # 页面更新时间
        "page_update": page_update
    }


if __name__ == "__main__":
    import pprint, json
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
