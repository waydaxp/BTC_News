# -*- coding: utf-8 -*-
"""
聚合 BTC / ETH 数据供 HTML 模板渲染
"""
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis

def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    return {
        # BTC
        "btc_price":  btc["price"],
        "btc_ma20":   btc["ma20"],
        "btc_rsi":    btc["rsi"],
        "btc_signal": btc["strategy_text"],
        "btc_risk":   btc["risk_usd"],
        "btc_qty":    btc["qty"],
        "btc_entry":  btc["entry"],
        "btc_sl":     btc["sl"],
        "btc_tp":     btc["tp"],
        # ETH
        "eth_price":  eth["price"],
        "eth_ma20":   eth["ma20"],
        "eth_rsi":    eth["rsi"],
        "eth_signal": eth["strategy_text"],
        "eth_risk":   eth["risk_usd"],
        "eth_qty":    eth["qty"],
        "eth_entry":  eth["entry"],
        "eth_sl":     eth["sl"],
        "eth_tp":     eth["tp"],
    }
