import os
from generate_data import get_all_analysis

TEMPLATE = open("index_template.html", encoding="utf-8").read()

def main():
    ctx  = get_all_analysis()
    html = TEMPLATE.format(**ctx)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html 已更新")

if __name__ == "__main__":
    main()
