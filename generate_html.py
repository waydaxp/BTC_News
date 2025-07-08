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
    base_dir      = os.path.dirname(os.path.abspath(__file__))
    template_name = 'index_template.html'  # 或者你的模板文件名
    output_path   = os.path.join(base_dir, 'index.html')

    # ── 获取原始数据 ─────────────────────────────────────────────────
    raw_btc = get_btc_analysis()        # e.g. { "15m": {...}, "1h": {...}, "4h": {...} }
    raw_eth = get_eth_analysis()
    fg      = get_fear_and_greed()      # 返回 tuple 或 dict

    # ── 扁平化数据字典 ────────────────────────────────────────────────
    data = {}

    # BTC 指标拆平：btc_<字段>_<周期>
    for tf, metrics in raw_btc.items():
        for key, val in metrics.items():
            field = 'strategy' if key == 'strategy_note' else key
            data[f'btc_{field}_{tf}'] = val

    # ETH 指标拆平：eth_<字段>_<周期>
    for tf, metrics in raw_eth.items():
        for key, val in metrics.items():
            field = 'strategy' if key == 'strategy_note' else key
            data[f'eth_{field}_{tf}'] = val

    # 恐惧与贪婪：兼容 tuple 和 dict
    if isinstance(fg, tuple) and len(fg) >= 3:
        fg_idx, fg_txt, fg_emoji = fg[0], fg[1], fg[2]
    else:
        fg_idx   = fg.get('value')
        fg_txt   = fg.get('text')
        fg_emoji = fg.get('emoji')

    data['fg_idx']   = fg_idx
    data['fg_txt']   = fg_txt
    data['fg_emoji'] = fg_emoji

    # 页面更新时间（北京时间）
    bj_tz           = pytz.timezone('Asia/Shanghai')
    now_str         = datetime.now(bj_tz).strftime('%Y-%m-%d %H:%M:%S')
    data['page_update'] = now_str

    # ── 渲染模板 ────────────────────────────────────────────────────
    env = Environment(
        loader=FileSystemLoader(base_dir),
        autoescape=False
    )
    template = env.get_template(template_name)
    rendered = template.render(data=data)

    # ── 输出到 index.html ────────────────────────────────────────────
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    print(f'✅ index.html 已更新：{now_str}')

if __name__ == '__main__':
    main()
