from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from utils.strategy_helper import get_strategy_explanation
from datetime import datetime, timedelta, timezone

def judge_style(signal: str, rsi: float, atr: float) -> str:
    if "强烈" in signal or (rsi > 65 and atr > 50):
        return "激进"
    elif "做多" in signal or "做空" in signal:
        return "平衡"
    else:
        return "保守"

def judge_trend_consistency(s15: str, s1h: str, s4h: str) -> str:
    if all("多" in s for s in [s15, s1h, s4h]):
        return "📈 多头趋势一致"
    elif all("空" in s for s in [s15, s1h, s4h]):
        return "📉 空头趋势一致"
    else:
        return "⏸ 趋势分歧（注意回撤）"

def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()
    macro = get_macro_event_summary()

    beijing_tz = timezone(timedelta(hours=8))
    page_update = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")

    btc_trend_note = judge_trend_consistency(btc["signal_15m"], btc["signal_1h"], btc["signal_4h"])
    eth_trend_note = judge_trend_consistency(eth["signal_15m"], eth["signal_1h"], eth["signal_4h"])

    result = {
        "fg_idx": fg_idx,
        "fg_txt": fg_txt,
        "fg_emoji": fg_emoji,
        "fg_ts": fg_ts,
        "macro_events": macro,
        "page_update": page_update,
    }

    for asset, data in zip(["btc", "eth"], [btc, eth]):
        trend_note = btc_trend_note if asset == "btc" else eth_trend_note
        result.update({
            f"{asset}_price": data.get("price"),
            f"{asset}_ma20": data.get("ma20"),
            f"{asset}_rsi": data.get("rsi"),
            f"{asset}_atr": data.get("atr"),
            f"{asset}_signal": data.get("signal"),
            f"{asset}_signal_15m": data.get("signal_15m"),
            f"{asset}_signal_1h": data.get("signal_1h"),
            f"{asset}_signal_4h": data.get("signal_4h"),
            f"{asset}_sl": data.get("sl_1h"),
            f"{asset}_tp": data.get("tp_1h"),
            f"{asset}_qty": data.get("qty_1h"),
            f"{asset}_risk": data.get("risk_usd"),
            f"{asset}_update_time": data.get("update_time"),
            f"{asset}_entry_15m": data.get("entry_15m"),
            f"{asset}_sl_15m": data.get("sl_15m"),
            f"{asset}_tp_15m": data.get("tp_15m"),
            f"{asset}_entry_1h": data.get("entry_1h"),
            f"{asset}_sl_1h": data.get("sl_1h"),
            f"{asset}_tp_1h": data.get("tp_1h"),
            f"{asset}_entry_4h": data.get("entry_4h"),
            f"{asset}_sl_4h": data.get("sl_4h"),
            f"{asset}_tp_4h": data.get("tp_4h"),
            f"{asset}_win_rate": data.get("win_rate", 0),
            f"{asset}_reason_15m": data.get("reason_15m"),
            f"{asset}_reason_1h": data.get("reason_1h"),
            f"{asset}_reason_4h": data.get("reason_4h"),
            f"{asset}_strategy_15m": get_strategy_explanation(data.get("signal_15m", "")),
            f"{asset}_strategy_1h": get_strategy_explanation(data.get("signal_1h", "")),
            f"{asset}_strategy_4h": get_strategy_explanation(data.get("signal_4h", "")),
            f"{asset}_style_1h": judge_style(data.get("signal_1h", ""), data.get("rsi", 50), data.get("atr", 20)),
            f"{asset}_trend_note": trend_note,
        })

    return result
