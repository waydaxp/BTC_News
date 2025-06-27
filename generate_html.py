from utils.generate_data import get_all_analysis
from datetime import datetime


def generate_html(data):
    btc = data['btc']
    eth = data['eth']
    macro = data['macro']
    fear_greed = data['fear_greed']

    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>BTC & ETH 每日策略简报</title>
    </head>
    <body>
        <h2>
