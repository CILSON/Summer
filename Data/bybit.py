from pybit.unified_trading import HTTP

import pandas as pd

from datetime import datetime


def fetch_historical_data1(symbol='BTCUSDT', timeframe="1M"):
    try:
        url = "https://api.bybit.com/v5/market/kline"

        params = {
            "category": "spot",
            "symbol": "BTCUSDT",
            "interval": "60",
            "limit": 10
        }

        response = requests.get(url, params=params)

        data = response.json()

        print(data)

        data = data['result']['list']

        if not data or len(data) < 2:
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=[
            'OpenTime',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Quote Asset Volume'
        ])

        columns_to_convert = [
            'OpenTime',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Quote Asset Volume'
        ]

        df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric)

        df['OpenTime'] = pd.to_datetime(df['OpenTime'], unit='ms')

        df['OpenTime'] = (
            df['OpenTime']
            .dt.tz_localize('UTC')
            .dt.tz_convert('Asia/Kolkata')
            .dt.tz_localize(None)
        )

        df = df.sort_values('OpenTime', ascending=False).reset_index(drop=True)

        return df

    except Exception as e:
        print("Bybit Error:", e)
        return pd.DataFrame()
