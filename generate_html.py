# -*- coding: utf-8 -*-
"""
渲染 index_template.html → index.html
"""
from pathlib import Path
from jinja2 import Template
from generate_data import get_all_analysis

TEMPLATE = Path("index_template.html").read_text(encoding="utf-8")

def main() -> None:
    ctx  = get_all_analysis()
    html = Template(TEMPLATE).render(**ctx)
    Path("index.html").write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()
