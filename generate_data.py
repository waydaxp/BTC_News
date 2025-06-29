# generate_data.py
"""
集中汇总 BTC 与 ETH 的行情解析，供 generate_html.py 调用。
"""

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis


def get_all_analysis() -> dict:
    """返回一个扁平化 dict，键名直接对接 index_template.html 内的占位符。"""
    btc = get_btc_analysis()   # 字段见 utils/fetch_btc_data.py
    eth = get_eth_analysis()   # 字段见 utils/fetch_eth_data.py

    return {
        # ===== BTC =====
        "btc_price"      : btc["price"],
        "btc_signal"     : btc["signal"],      # ✅ 已统一命名
        "btc_ma20"       : btc["ma20"],
        "btc_rsi"        : btc["rsi"],
        "btc_atr"        : btc["atr"],
        "btc_sl"         : btc["sl"],
        "btc_tp"         : btc["tp"],
        "btc_qty"        : btc["qty"],
        "btc_risk"       : btc["risk_usd"],
        "btc_update_time": btc["update_time"],

        # ===== ETH =====
        "eth_price"      : eth["price"],
        "eth_signal"     : eth["signal"],
        "eth_ma20"       : eth["ma20"],
        "eth_rsi"        : eth["rsi"],
        "eth_atr"        : eth["atr"],
        "eth_sl"         : eth["sl"],
        "eth_tp"         : eth["tp"],
        "eth_qty"        : eth["qty"],
        "eth_risk"       : eth["risk_usd"],
        "eth_update_time": eth["update_time"],
    }


if __name__ == "__main__":
    # 快速自测：打印汇总字典
    import pprint, json
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
