#!/usr/bin/env python3
# utils/generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from utils.strategy_helper import generate_strategy_text_dynamic
from datetime import datetime, timedelta, timezone

# 我们支持的时间周期清单
TIMEFRAMES = ["15m", "1h", "4h"]

def wrap_asset(asset: dict, symbol: str) -> dict:
    """
    将某个资产（btc 或 eth）的原始三周期数据扁平化：
    例如 asset["15m"]["price"] 变成 {"btc_price_15m": ...}
    同时，我们把原来存放在 strategy_note 的文字
    也搬到对应的 {symbol}_strategy_{tf}。
    """
    out = {}
    for tf in TIMEFRAMES:
        data = asset.get(tf, {}) or {}
        prefix = f"{symbol}_"
        # 简单字段
        out[f"{prefix}price_{tf}"]        = data.get("price", "-")
        out[f"{prefix}ma20_{tf}"]         = data.get("ma20", "-")
        out[f"{prefix}rsi_{tf}"]          = data.get("rsi", "-")
        out[f"{prefix}atr_{tf}"]          = data.get("atr", "-")
        out[f"{prefix}volume_{tf}"]       = data.get("volume", "-")
        out[f"{prefix}support_{tf}"]      = data.get("support", "-")
        out[f"{prefix}resistance_{tf}"]   = data.get("resistance", "-")
        # 策略相关
        out[f"{prefix}signal_{tf}"]       = data.get("signal", "-")
        out[f"{prefix}tp_{tf}"]           = data.get("tp", "-")
        out[f"{prefix}sl_{tf}"]           = data.get("sl", "-")
        out[f"{prefix}win_rate_{tf}"]     = data.get("win_rate", "-")
        # 原先叫 strategy_note，改成 strategy_{tf}
        out[f"{prefix}strategy_{tf}"]     = data.get("strategy_note", "-")
    return out

def get_all_analysis() -> dict:
    """
    获取所有分析，并扁平化输出一个字典，
    直接可用于 Jinja2 render(**ctx)。
    """
    # 1. 拉取原始数据
    btc_raw = {}
    eth_raw = {}
    try:
        btc_raw = get_btc_analysis()
    except Exception:
        pass
    try:
        eth_raw = get_eth_analysis()
    except Exception:
        pass

    fg_idx, fg_txt, fg_emoji, fg_ts = (0, "未知", "❓", "N/A")
    try:
        fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()
    except Exception:
        pass

    macro = ""
    try:
        macro = get_macro_event_summary()
    except Exception:
        pass

    # 2. 北京时间页面更新时间
    beijing = timezone(timedelta(hours=8))
    page_update = datetime.now(beijing).strftime("%Y-%m-%d %H:%M:%S")

    # 3. 扁平化所有字段
    ctx = {}
    ctx.update(wrap_asset(btc_raw, "btc"))
    ctx.update(wrap_asset(eth_raw, "eth"))

    # 4. 恐惧贪婪指数等全局字段
    ctx["fg_idx"]        = fg_idx
    ctx["fg_txt"]        = fg_txt
    ctx["fg_emoji"]      = fg_emoji
    ctx["fg_ts"]         = fg_ts
    ctx["macro_events"]  = macro
    ctx["page_update"]   = page_update

    return ctx
