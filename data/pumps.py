from utils.log_utils import *
from technical_analysis.indicators import *
import datetime


class PumpsData:
    def __init__(self, client, coins: list, interval: str, lookback: str,
                 num_candle_back: int = 5, num_candle_forw: int = None, data_interval: int = 3):
        self.client = client
        self.coins = coins
        self.interval = interval
        self.lookback = lookback
        self.num_candle_back = num_candle_back
        self.num_candle_forw = num_candle_forw
        self.data_interval = data_interval

    def get_pumps(self, coin: str):
        df = get_coins_data(self.client, coin, self.interval, self.lookback)
        if df.empty:
            return
        try:
            df['ID_Coin'] = coin
            df = df.astype({"Close": "float"})
            df = df.astype({"High": "float"})
            df = df.astype({"Volume": "float"})

            df['Pt-1'] = df['Close'].shift(1).ffill()
            df['Pt+1buyHigh'] = df['High'].shift(-1).ffill()
            df['Pt+5c'] = df['Close'].shift(-5).ffill()
            df['Pt+10c'] = df['Close'].shift(-10).ffill()
            df['Vt-1'] = df['Volume'].shift(1).ffill()
            df['sma_price'] = df['Pt-1'].rolling(60).mean()
            df['std_price'] = df['Pt-1'].rolling(60).std()
            df['sma_volume'] = df['Vt-1'].rolling(60).mean()
            df['std_volume'] = df['Vt-1'].rolling(60).std()
            df['is_PumP'] = ((df['Close'] - df['Pt-1']) / df['Pt-1'] > 0.01) & \
                            ((df['Pt+5c'] - df['Pt+1buyHigh']) / df['Pt+1buyHigh'] > 0.02) & \
                            ((df['Pt+10c'] - df['Pt+1buyHigh']) / df['Pt+1buyHigh'] > 0.05) & \
                            (df['Volume'] > 10000)
        except:
            print('New Coin')

        if df[df['is_PumP'] == True].empty:
            return
        else:
            df_final = df[df['is_PumP'] == True]
            df_final = df_final.drop('is_PumP', axis=1)
            return df_final

    def get_data_at_timestamp(self, coin: str, timestamp: int):
        ''' timestamp in ms '''
        interval_dict = {1: self.client.KLINE_INTERVAL_1MINUTE,
                         3: self.client.KLINE_INTERVAL_3MINUTE,
                         5: self.client.KLINE_INTERVAL_5MINUTE,
                         15: self.client.KLINE_INTERVAL_15MINUTE,
                         30: self.client.KLINE_INTERVAL_30MINUTE}

        if self.data_interval not in interval_dict.keys():
            print('Enter a valid value of interval : 1, 3, 5, 15 or 30')
            return

        timestamp_start = timestamp - 60000 * ((self.num_candle_back + 15) * self.data_interval)
        if self.num_candle_forw is None:
            timestamp_end = timestamp
        else:
            timestamp_end = timestamp + 60000 * self.num_candle_forw * self.data_interval
        df = pd.DataFrame(self.client.get_historical_klines(coin, interval_dict[self.data_interval],
                                                            timestamp_start,
                                                            timestamp_end))

        df = df.iloc[:, :9]
        df.columns = OHLCVCtQN_clm
        df = df.astype({'Close': float, 'High': float, 'Low': float, 'Volume': float})
        df = rsi_df(df)
        df = mfi_df(df)
        df = vwap_df(df)

        df.CloseTime = pd.to_datetime(df.CloseTime.values, unit="ms")
        df = df.astype({'Close': float, 'High': float, 'Low': float, 'Volume': float})

        return df

    def complete_pumps_data(self, df_pump):
        features = {'Pt': 'Close', 'Vt': 'Volume',
                    'QAVol': 'QuoteAssetVolume', 'Trades': 'NumberOfTrades',
                    'rsi': 'rsi', 'mfi': 'mfi', 'vwap': 'vwap'}
        if df_pump is None:
            return
        # Add backward columns
        for i in range(1, self.num_candle_back + 1):
            for feature in features.keys():
                feature_name = feature + str(self.data_interval) + ' -' + str(i * self.data_interval)
                df_pump[feature_name] = ''

        # Add forward columns (binance api starts from the current candle)
        if self.num_candle_forw is not None:
            for cl in range(0, self.num_candle_forw):
                for feature in features.keys():
                    feature_name = feature + str(self.data_interval) + ' +' + str(cl * self.data_interval)
                    df_pump[feature_name] = ''

        # Get complete data for every pump
        for raw in range(0, df_pump.shape[0]):

            try:
                df_data_pump = self.get_data_at_timestamp(coin=str(df_pump.loc[raw, 'ID_Coin']),
                                                          timestamp=int(df_pump.loc[raw, 'Time']))

                # Add data to backward and forward columns
                for cl in range(1, self.num_candle_back + 1):
                    for key, value in features.items():
                        feature_name = key + str(self.data_interval) + ' -' + str(cl * self.data_interval)
                        df_pump.loc[raw, feature_name] = df_data_pump[value].T.iloc[
                            - self.num_candle_forw - cl]

                for cl in range(0, self.num_candle_forw):
                    for key, value in features.items():
                        feature_name = key + str(self.data_interval) + ' +' + str(cl * self.data_interval)
                        df_pump.loc[raw, feature_name] = df_data_pump[value].T.iloc[
                            cl - self.num_candle_forw]
            except:
                print('New coin in binance')

        return df_pump

    def pumps(self, version=''):
        flag = 0
        df = pd.DataFrame()
        for coin in self.coins:
            log_coins_pump(self.coins, coin)
            df_pumps = self.get_pumps(coin)
            if df_pumps is not None:
                # delete sequence times < 10 min
                df_pumps['timediff'] = pd.to_numeric(df_pumps['Time']).diff().fillna(400000)
                df_pumps = df_pumps[df_pumps['timediff'] > 300000]
                df_pumps = df_pumps.drop(['timediff', 'CloseTime'], axis=1)
                flag = 1
                log_pump_found(df_pumps, coin)
                df = pd.concat([df, df_pumps], ignore_index=True).reset_index(drop=True)

        if flag:
            df['Time_human'] = pd.to_datetime(df['Time'], unit='ms')
            file_time = datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
            df.to_csv("data\\datasets\\DB_lite_{}_{}.csv".format(version, file_time), mode='w', header=True)
            log_add_data_pumps(df)
            df_final = self.complete_pumps_data(df)

            # Reorder columns
            df_ordred = df_final.drop(['Time', 'Time_human', 'Open', 'High', 'Low', 'Close', 'ID_Coin'], axis=1)
            df_ordred = df_ordred.reindex(sorted(df_ordred.columns), axis=1)
            df_out = df_final[['Time', 'ID_Coin', 'Time_human', 'Open', 'High', 'Low', 'Close']]
            df_out = pd.concat([df_out, df_ordred], axis=1)

            df_out.to_csv("data\\datasets\\DB_pumps_{}_{}.csv".format(version, file_time), mode='w', header=True)
            print("End... Check the file created.")

            return df_out
        else:
            print('End. No pump founded')
            return
