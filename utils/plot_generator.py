def generate_strategy_note(price, support, resistance):
    """
    简化策略说明文本，真实项目中应基于更多参数生成更复杂的建议
    """
    note = "当前价格靠近支撑区域，若跌破需警惕转空。\n"

    if price < support:
        note += f"📉 若跌破 ${support:.0f}，目标设至 {price - (resistance - support):.0f}，止损设在 {support + (resistance - support) * 0.5:.0f}。\n"
        note += "📊 仓位建议：20%以内，需防反抽。"
    else:
        note += "⚠️ 目前持币观望，等待有效信号。"

    return note
