#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import pytz
from jinja2 import Environment, FileSystemLoader

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed

def main():
    # ── 路径设置 ────────────────────────────────────────────────────
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_name = 'index_template-2.html'  # 模板文件名（可根据实际改为 index_template.html）
    template_path = os.path.join(base_dir, template_name)
    output_path   = os.path.join(base_dir, 'index.html')

    # ── 获取原始数据 ─────────────────────────────────────────────────
    raw_btc = get_btc_analysis()        # 返回 { "15m": {...}, "1h": {...}, "4h": {...} } 等结构
    raw_eth = get_eth_analysis()
    fg      = get_fear_and_greed()      # 返回 { "value":..., "text":..., "emoji":... }

    # ── 扁平化数据字典 ────────────────────────────────────────────────
    data = {}

    # BTC 指标拆平：btc_<字段名>_<周期>
    for tf, metrics in raw_btc.items():
        for key, val in metrics.items():
            # strategy_note 字段在模板中对应 btc_strategy_<tf>
            field = 'strategy_note' if key == 'strategy_note' else key
            data[f'btc_{field}_{tf}'] = val

    # ETH 指标拆平：eth_<字段名>_<周期>
    for tf, metrics in raw_eth.items():
        for key, val in metrics.items():
            field = 'strategy_note' if key == 'strategy_note' else key
            data[f'eth_{field}_{tf}'] = val

    # 恐惧与贪婪
    data['fg_idx']   = fg.get('value')
    data['fg_txt']   = fg.get('text')
    data['fg_emoji'] = fg.get('emoji')

    # 页面更新时间（北京时间）
    bj_tz = pytz.timezone('Asia/Shanghai')
    now_str = datetime.now(bj_tz).strftime('%Y-%m-%d %H:%M:%S')
    data['page_update'] = now_str

    # ── 渲染模板 ────────────────────────────────────────────────────
    env = Environment(
        loader=FileSystemLoader(base_dir),
        autoescape=False
    )
    template = env.get_template(template_name)  # 模板中使用了 data["btc_price_" ~ tf] 等扁平化键  [oai_citation:0‡index_template-2.html](file-service://file-Ay8cKGD8vxaP3Q4iSvMKUF)
    rendered = template.render(data=data)

    # ── 输出到 index.html ────────────────────────────────────────────
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    print(f'✅ index.html 已更新：{now_str}')

if __name__ == '__main__':
    main()
