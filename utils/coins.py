import pandas as pd
from utils.constants import OHLCVCtQN_clm


def get_coins_names(client, quote: list = ["USDT", "BUSD"]) -> list:
    info = client.get_all_tickers()
    ls_without_quote = []
    coins = []
    for q in quote:
        coins_quote = [coin["symbol"] for coin in info if coin["symbol"].endswith(q)]
        ls = [coin.replace(q, "") for coin in coins_quote if coin.replace(q, "") not in ls_without_quote]
        ls_without_quote.extend(ls)
        ls_with_quote = [coin + q for coin in ls]
        coins.extend(ls_with_quote)

    return coins


def get_coins_data(client, coin: str, interval: str = '1m', lookback: str = '60 day') -> pd.DataFrame:
    try:
        df = pd.DataFrame(
            client.get_historical_klines(coin, interval, lookback + " ago UTC")
        )
    except ValueError:
        df = pd.DataFrame(columns=OHLCVCtQN_clm)
    if df.empty:
        return df
    df = df.iloc[:, :9]
    df.columns = OHLCVCtQN_clm
    df.CloseTime = pd.to_datetime(df.CloseTime.values, unit="ms")
    df = df.astype({"Close": "float"})
    df = df.astype({"Volume": "float"})
    return df
