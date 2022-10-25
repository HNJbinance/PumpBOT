# IMPORT
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

from binance.client import Client
from utils.coins import *
from data.pumps import *
from utils.constants import *

# VARIABLE
client_binance = Client(api_key=api_key, api_secret=api_secret)
interval = '1m'
lookback = '90 day'
num_candle_back = 10
num_candle_forw = 10
data_interval = 1
stable_coins = ['USDT', 'BUSD']

# COINS LIST
coins = get_coins_names(client_binance, stable_coins)
# coins = ['USTCBUSD', 'UFTBUSD']


# GET PUMPS
log_bot_version(version="Alpha 1.0.0")
log_entry_detect_pumps(stable_coins)
coins_pumps = PumpsData(client_binance, coins, interval, lookback, num_candle_back, num_candle_forw, data_interval)
# coins_pumps.pumps(version='V2_1min')

