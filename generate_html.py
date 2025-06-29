# generate_html.py
from generate_data import get_all_analysis

def main():
    tpl = open("index_template.html", encoding="utf-8").read()
    ctx = get_all_analysis()
    html = tpl.format(**ctx)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
