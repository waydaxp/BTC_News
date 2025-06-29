# -*- coding: utf-8 -*-
"""
generate_html.py
================
• 读取 Jinja 样式的简单占位符模板（index_template.html）
• 调用 generate_data.get_all_analysis() 取上下文
• 渲染成 index.html
"""

from pathlib import Path
from generate_data import get_all_analysis

TEMPLATE_FILE = Path("index_template.html")
OUTPUT_FILE   = Path("index.html")

def main() -> None:
    ctx = get_all_analysis()                  # 返回字典

    # 读取模板
    html_tpl = TEMPLATE_FILE.read_text(encoding="utf-8")

    # 简单 .format(**ctx) 渲染（若想用 Jinja2，可自行替换）
    rendered = html_tpl.format(**ctx)

    # 写出 HTML
    OUTPUT_FILE.write_text(rendered, encoding="utf-8")
    print(f"✅ 已更新 {OUTPUT_FILE} —— {ctx['update_time']}")

if __name__ == "__main__":
    main()
