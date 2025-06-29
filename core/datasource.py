import yfinance as yf
import pandas as pd

def pull_ohlc(ticker: str, period="30d", interval="1h") -> pd.DataFrame:
    """
    统一数据源：yfinance，可后续替换为 Binance API
    """
    df = yf.Ticker(ticker).history(period=period, interval=interval)
    df.rename(columns=str.capitalize, inplace=True)  # 统一 High/Low/Close
    return df
