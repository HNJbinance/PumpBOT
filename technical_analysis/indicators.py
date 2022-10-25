import pandas as pd
import numpy as np
import re
from utils.coins import get_coins_data
from utils.constants import *


def bollinger_upper(client, coin: str, interval: str, lookback: str, calc_period: float, bandwidth: float) -> list:
    coin_data = get_coins_data(client, coin, interval, lookback)
    # calculate n moving average
    coin_data[str(calc_period) + 'sma'] = coin_data['Close'].rolling(calc_period).mean()
    # Get standard deviation
    coin_data['std'] = coin_data['Close'].rolling(calc_period).std()
    # Calculate upper and lower Bollinger band
    coin_data['upper'] = coin_data[str(calc_period) + 'sma'] + (bandwidth * coin_data['std'])
    list_upper = coin_data['upper'].values.tolist()

    return list_upper[-2]


def bollinger_lower(client, coin: str, interval: str, lookback: str, calc_period: float, bandwidth: float) -> list:
    coin_data = get_coins_data(client, coin, interval, lookback)
    # calculate n moving average
    coin_data[str(calc_period) + 'sma'] = coin_data['Close'].rolling(calc_period).mean()
    # Get standard deviation
    coin_data['std'] = coin_data['Close'].rolling(calc_period).std()
    # Calculate upper and lower Bollinger band
    coin_data['lower'] = coin_data[str(calc_period) + 'sma'] - (bandwidth * coin_data['std'])
    list_lower = coin_data['lower'].values.tolist()

    return list_lower[-2]


def rsi_df(df):
    df2 = df.copy()
    df2['change'] = df2['Close'].diff(1)  # Calculate change
    # calculate gain / loss from every change
    df2['gain'] = np.select([df2['change'] > 0, df2['change'].isna()],
                           [df2['change'], np.nan],
                           default=0)
    df2['loss'] = np.select([df2['change'] < 0, df2['change'].isna()],
                           [-df2['change'], np.nan],
                           default=0)

    # create avg_gain /  avg_loss columns with all nan
    df2['avg_gain'] = np.nan
    df2['avg_loss'] = np.nan

    n = 14  # what is the window

    # keep first occurrence of rolling mean
    df2['avg_gain'][n] = df2['gain'].rolling(window=n).mean().dropna().iloc[0]
    df2['avg_loss'][n] = df2['loss'].rolling(window=n).mean().dropna().iloc[0]
    # Alternatively
    df2['avg_gain'][n] = df2.loc[:n, 'gain'].mean()
    df2['avg_loss'][n] = df2.loc[:n, 'loss'].mean()

    # This is not a pandas way, looping through the pandas series, but it does what you need
    for i in range(n + 1, df2.shape[0]):
        df2['avg_gain'].iloc[i] = (df2['avg_gain'].iloc[i - 1] * (n - 1) + df2['gain'].iloc[i]) / n
        df2['avg_loss'].iloc[i] = (df2['avg_loss'].iloc[i - 1] * (n - 1) + df2['loss'].iloc[i]) / n

    # calculate rs and rsi
    df2['rs'] = df2['avg_gain'] / df2['avg_loss']
    df2['rsi'] = 100 - (100 / (1 + df2['rs']))

    return df.join(df2['rsi'])


def mfi_df(df):
    df2 = df.copy()
    df2['Typical_Price'] = (df2['Close'] + df2['High'] + df2['Low']) / 3
    df2['Money_Flow'] = df2['Typical_Price'] * df2['Volume']
    df2['change'] = df2['Money_Flow'].diff(1)
    # calculate gain / loss from every change
    df2['gain'] = np.select([df2['change'] > 0, df2['change'].isna()],
                           [df2['change'], np.nan],
                           default=0)
    df2['loss'] = np.select([df2['change'] < 0, df2['change'].isna()],
                           [-df2['change'], np.nan],
                           default=0)

    # create avg_gain /  avg_loss columns with all nan
    df2['avg_gain'] = np.nan
    df2['avg_loss'] = np.nan

    n = 14  # what is the window

    # keep first occurrence of rolling mean
    df2['avg_gain'][n] = df2['gain'].rolling(window=n).mean().dropna().iloc[0]
    df2['avg_loss'][n] = df2['loss'].rolling(window=n).mean().dropna().iloc[0]
    # Alternatively
    df2['avg_gain'][n] = df2.loc[:n, 'gain'].mean()
    df2['avg_loss'][n] = df2.loc[:n, 'loss'].mean()

    # This is not a pandas way, looping through the pandas series, but it does what you need
    for i in range(n + 1, df2.shape[0]):
        df2['avg_gain'].iloc[i] = (df2['avg_gain'].iloc[i - 1] * (n - 1) + df2['gain'].iloc[i]) / n
        df2['avg_loss'].iloc[i] = (df2['avg_loss'].iloc[i - 1] * (n - 1) + df2['loss'].iloc[i]) / n

    # calculate rs and rsi
    df2['mf'] = df2['avg_gain'] / df2['avg_loss']
    df2['mfi'] = 100 - (100 / (1 + df2['mf']))

    return df.join(df2['mfi'])

def vwap_df(df, n=2):
    df2 = df.copy()
    df2['Typical_Price'] = (df2['Close'] + df2['High'] + df2['Low']) / 3
    df2['Typical_Price * Volume'] = df2['Typical_Price'] * df2['Volume']
    df2['Moving_Typical_Price * Volume'] = df2['Typical_Price * Volume'].rolling(n).sum()
    df2['Moving_Sum_Volume'] = df2['Volume'].rolling(n).sum()
    new_df = df.assign(vwap=(df2['Moving_Typical_Price * Volume']) / df2['Moving_Sum_Volume'])
    return df.join(new_df['vwap'])


def rsi_mfi_vwap(client, coin: str, interval: str, periode: int = 14, timestamp: int = None, num_bars: int = 5):

    lookback = str(periode + 20 * int(re.findall(r'\d+', interval)[0])) + ' ' + re.findall(r'\D+', interval)[0].strip()
    kline_minute = int(re.findall(r'\d+', interval)[0])

    if timestamp is None:
        df = get_coins_data(client, coin, interval, lookback)

    else:
        df = pd.DataFrame(client.get_historical_klines(coin, client.KLINE_INTERVAL_1MINUTE,
                                                       timestamp - 60000 * (periode + num_bars + 20), timestamp))
    df = df.iloc[:, :9]
    df.columns =OHLCVCtQN_clm
    df = df.astype({'Close': float, 'High': float, 'Low': float, 'Volume': float})

    df_rsi = rsi_df(df)
    df_mfi = mfi_df(df)
    df_vwap = vwap_df(df)

    return (df_rsi.join(df_mfi['mfi'])).join(df_vwap['vwap'])