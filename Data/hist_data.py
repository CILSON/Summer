import requests as req # Install requests module first.
import pandas as pd
from datetime import datetime


def fetch_historical_data(symbol='BTCUSDT', timeframe="1h"):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        'symbol': symbol,
        'interval': timeframe,
        'limit': 1000
    }

    data = req.get(url, params=params).json()
    df = pd.DataFrame(data, columns=['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    
    columns_to_convert = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']
    df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric)

    df['OpenTime'] = pd.to_datetime(df['OpenTime'], unit='ms')
    df['CloseTime'] = pd.to_datetime(df['CloseTime'], unit='ms')
    
    df['OpenTime'] = df['OpenTime'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
    df['CloseTime'] = df['CloseTime'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
    
    df = df.sort_values('OpenTime', ascending=False).reset_index(drop=True)
    df['date'] = df['OpenTime']
    df = df.set_index('OpenTime')
    
    return df
   
df = fetch_historical_data()

df.to_csv('historical_data.csv', index=False)
