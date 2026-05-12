from pybit.unified_trading import HTTP

import pandas as pd

from datetime import datetime


def fetch_historical_data1(symbol='BTCUSDT', timeframe="1M"):
    try:
        session = HTTP(testnet=False)
        data = session.get_kline(
            category="spot",
            symbol="BTCUSDT",
            interval="60"
        )

        data = data['result']['list']

        df = pd.DataFrame(data, columns=['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume'])

        columns_to_convert = ['OpenTime','Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume']
        df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric)

        df['OpenTime'] = pd.to_datetime(df['OpenTime'], unit='ms')
        df['OpenTime'] = df['OpenTime'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
        
        df = df.sort_values('OpenTime', ascending=False).reset_index(drop=True)

        return df

    except Exception as e:
        print(e)
        return pd.DataFrame()
