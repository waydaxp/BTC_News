def generate_strategy_text_dynamic(price: float, support: float, resistance: float, atr: float, volume_up: bool = False) -> str:
    """
    根据当前价格、支撑/阻力、ATR 和成交量判断，生成动态策略建议文字。
    """
    content = []

    content.append("当前 ETH/USDT 永续合约行情已显示。接下来我们深入分析未来 4 小时走势，并给出方向建议：")
    content.append("\n⸻\n")

    content.append("🧠 技术分析综述：")
    content.append(
        f"• 当前价格处于 ${support:.0f}（支撑）–${resistance:.0f}（阻力）宽幅震荡区间内。"
    )
    content.append("• RSI 若突破 50 并上扬，价格若守住 50EMA，短线或有望冲高。")
    content.append(
        f"• 若突破 ${resistance:.0f} 区间，短期目标可望扩张至 ${resistance + atr*2:.0f} ～ ${resistance + atr*2.5:.0f}。")
    content.append(
        f"• 若跌破 ${support:.0f} 区间，短线恐将下探至 ${support - atr:.0f} 或更低。")

    content.append("\n⸻\n")
    content.append("🔍 短时策略建议（未来 4 小时）：")

    if price >= support and volume_up:
        content.append(f"守住 ${support:.0f}–${support + 20:.0f} 且成交量回暖 => 看涨偏多，可倾向做多。")
        content.append(f"🎯 止盈目标设在 ${resistance:.0f}、{resistance + 50:.0f}。")
        content.append(f"🛑 止损建议设在支撑下方 ${support - 10:.0f}。")
    elif price < support:
        content.append(f"跌破 ${support:.0f} 区间伴随高成交量 => 看空趋势增强，可考虑做空。")
        content.append(f"🎯 目标可设至 ${support - 40:.0f} 下方，止盈点位于 ${support:.0f} 附近。")
        content.append(f"🛑 止损建议略上方于 ${support + 20:.0f}。")
    else:
        content.append("当前价格处于震荡整理期，建议观望等待方向突破确认。")

    content.append("\n⸻\n")
    content.append("✅ 结论推荐：")
    content.append(f"• 若偏向多头：等待确认守住 ${support:.0f} 区间并有放量，入场做多，目标 ${resistance:.0f} 上方。")
    content.append(f"• 若偏空：若放量跌破支撑 ${support:.0f}，可择机做空，目标 ${support - 40:.0f} 区间。")

    content.append("\n⸻\n")
    content.append("⚠️ 风险提示：")
    content.append("• 合约具高杠杆风险，请务必设置止损，严格控制仓位。")
    content.append("• 策略建议基于技术图形及成交量等指标，仅供参考。")
    content.append("• 建议同时关注 funding rate 和 BTC 同步趋势变化。")

    return "\n".join(content)
