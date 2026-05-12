import requests as req
import pandas as pd


def fetch_historical_data(symbol='BTCUSDT', timeframe="1h"):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        'symbol': symbol,
        'interval': timeframe,
        'limit': 1000
    }

    try:
        response = req.get(url, params=params, timeout=10)

        # Check HTTP status
        if response.status_code != 200:
            print("HTTP Error:", response.status_code)
            return pd.DataFrame()

        data = response.json()

        # Check if Binance returned an error object
        if isinstance(data, dict):
            print("Binance Error:", data)
            return pd.DataFrame()

        # Check empty response
        if not data or len(data) < 2:
            print("Not enough market data")
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=[
            'OpenTime',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'CloseTime',
            'Quote Asset Volume',
            'Number of Trades',
            'Taker Buy Base Asset Volume',
            'Taker Buy Quote Asset Volume',
            'Ignore'
        ])

        columns_to_convert = [
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Quote Asset Volume',
            'Number of Trades',
            'Taker Buy Base Asset Volume',
            'Taker Buy Quote Asset Volume'
        ]

        df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric)

        df['OpenTime'] = pd.to_datetime(df['OpenTime'], unit='ms')
        df['CloseTime'] = pd.to_datetime(df['CloseTime'], unit='ms')

        df['OpenTime'] = (
            df['OpenTime']
            .dt.tz_localize('UTC')
            .dt.tz_convert('Asia/Kolkata')
            .dt.tz_localize(None)
        )

        df['CloseTime'] = (
            df['CloseTime']
            .dt.tz_localize('UTC')
            .dt.tz_convert('Asia/Kolkata')
            .dt.tz_localize(None)
        )

        df = df.sort_values('OpenTime', ascending=False).reset_index(drop=True)

        df['date'] = df['OpenTime']

        df = df.set_index('OpenTime')

        return df

    except Exception as e:
        print("Fetch Error:", e)
        return pd.DataFrame()