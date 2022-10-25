import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_csv('DB_pumps_V2.csv', index_col=[0])

df = df.dropna(how='any')

# Reorder columns and apply Percentages

columns = ['NumberOfTrades', 'Pt+10c', 'Pt+1buyHigh',
           'Pt+5c', 'Pt-1', 'Pt1 +0', 'Pt1 +1', 'Pt1 +2', 'Pt1 +3', 'Pt1 +4', 'Pt1 +5', 'Pt1 +6', 'Pt1 +7', 'Pt1 +8',
           'Pt1 +9', 'Pt1 -1', 'Pt1 -10', 'Pt1 -2', 'Pt1 -3', 'Pt1 -4', 'Pt1 -5', 'Pt1 -6', 'Pt1 -7', 'Pt1 -8',
           'Pt1 -9',
           'QAVol1 +0', 'QAVol1 +1', 'QAVol1 +2', 'QAVol1 +3', 'QAVol1 +4', 'QAVol1 +5', 'QAVol1 +6', 'QAVol1 +7',
           'QAVol1 +8', 'QAVol1 +9', 'QAVol1 -1', 'QAVol1 -10', 'QAVol1 -2', 'QAVol1 -3', 'QAVol1 -4', 'QAVol1 -5',
           'QAVol1 -6', 'QAVol1 -7', 'QAVol1 -8', 'QAVol1 -9', 'QuoteAssetVolume', 'Trades1 +0', 'Trades1 +1',
           'Trades1 +2', 'Trades1 +3', 'Trades1 +4', 'Trades1 +5', 'Trades1 +6', 'Trades1 +7', 'Trades1 +8',
           'Trades1 +9', 'Trades1 -1', 'Trades1 -10', 'Trades1 -2', 'Trades1 -3', 'Trades1 -4', 'Trades1 -5',
           'Trades1 -6',
           'Trades1 -7', 'Trades1 -8', 'Trades1 -9', 'Volume', 'Vt1 +0', 'Vt1 +1', 'Vt1 +2', 'Vt1 +3', 'Vt1 +4',
           'Vt1 +5',
           'Vt1 +6', 'Vt1 +7', 'Vt1 +8', 'Vt1 +9', 'Vt1 -1', 'Vt1 -10', 'Vt1 -2', 'Vt1 -3', 'Vt1 -4', 'Vt1 -5',
           'Vt1 -6',
           'Vt1 -7', 'Vt1 -8', 'Vt1 -9', 'mfi1 +0', 'mfi1 +1', 'mfi1 +2', 'mfi1 +3', 'mfi1 +4', 'mfi1 +5', 'mfi1 +6',
           'mfi1 +7', 'mfi1 +8', 'mfi1 +9', 'mfi1 -1', 'mfi1 -10', 'mfi1 -2', 'mfi1 -3', 'mfi1 -4', 'mfi1 -5',
           'mfi1 -6',
           'mfi1 -7', 'mfi1 -8', 'mfi1 -9', 'rsi1 +0', 'rsi1 +1', 'rsi1 +2', 'rsi1 +3', 'rsi1 +4', 'rsi1 +5', 'rsi1 +6',
           'rsi1 +7', 'rsi1 +8', 'rsi1 +9', 'rsi1 -1', 'rsi1 -10', 'rsi1 -2', 'rsi1 -3', 'rsi1 -4', 'rsi1 -5',
           'rsi1 -6',
           'rsi1 -7', 'rsi1 -8', 'rsi1 -9', 'vwap1 +0', 'vwap1 +1', 'vwap1 +2', 'vwap1 +3', 'vwap1 +4', 'vwap1 +5',
           'vwap1 +6',
           'vwap1 +7', 'vwap1 +8', 'vwap1 +9', 'vwap1 -1', 'vwap1 -10', 'vwap1 -2', 'vwap1 -3', 'vwap1 -4', 'vwap1 -5',
           'vwap1 -6', 'vwap1 -7', 'vwap1 -8', 'vwap1 -9']


init = ['Time', 'ID_Coin', 'Time_human', 'pt-sma/sma', 'pt-sma/std', 'sma+2std/pt-1', 'vt-sma/sma', 'vt-sma/std', 'sma+2std/vt-1']
price = ['Pt1 -9', 'Pt1 -7', 'Pt1 -5', 'Pt1 -4', 'Pt1 -3', 'Pt1 -2', 'Pt1 -1', 'Close',
         'Pt+1buyHigh', 'Pt1 +0', 'Pt1 +3', 'Pt1 +5', 'Pt1 +9']
volume = ['Vt1 -9', 'Vt1 -7', 'Vt1 -5', 'Vt1 -4', 'Vt1 -3', 'Vt1 -2', 'Vt1 -1', 'Volume', 'Vt1 +0',
          'Vt1 +1', 'Vt1 +3', 'Vt1 +5', 'Vt1 +9']
QuoteAsset = ['QAVol1 -9', 'QAVol1 -7', 'QAVol1 -5', 'QAVol1 -4', 'QAVol1 -3', 'QAVol1 -2', 'QAVol1 -1',
              'QuoteAssetVolume', 'QAVol1 +0', 'QAVol1 +1', 'QAVol1 +3', 'QAVol1 +5', 'QAVol1 +9']
NumberOfTrades = ['Trades1 -9', 'Trades1 -7', 'Trades1 -5', 'Trades1 -4', 'Trades1 -3', 'Trades1 -2', 'Trades1 -1',
                  'NumberOfTrades', 'Trades1 +0', 'Trades1 +1', 'Trades1 +3', 'Trades1 +5', 'Trades1 +9']
rsi = ['rsi1 -9', 'rsi1 -7', 'rsi1 -5', 'rsi1 -4', 'rsi1 -3', 'rsi1 -2', 'rsi1 -1', 'rsi1 +0', 'rsi1 +1', 'rsi1 +3',
       'rsi1 +5', 'rsi1 +9']
mfi = ['mfi1 -9', 'mfi1 -7', 'mfi1 -5', 'mfi1 -4', 'mfi1 -3', 'mfi1 -2', 'mfi1 -1', 'mfi1 +0', 'mfi1 +1', 'mfi1 +3',
       'mfi1 +5', 'mfi1 +9']
vwap = ['vwap1 -9', 'vwap1 -7', 'vwap1 -5', 'vwap1 -4', 'vwap1 -3', 'vwap1 -2', 'vwap1 -1', 'vwap1 +0', 'vwap1 +1',
        'vwap1 +3', 'vwap1 +5', 'vwap1 +9']

ispump = ['pump']
ispump_df = df[ispump]
init_df = df[init]

price_df = df[price]
for column in price_df.columns.tolist():
    if column != 'Pt1 -1':
        price_df[column] = (price_df[column] - price_df['Pt1 -1'])/price_df['Pt1 -1']
print('price ok')
volume_df = df[volume]
for column in volume_df.columns.tolist():
    if column != 'Vt1 -1':
        volume_df[column] = (volume_df[column] - volume_df['Vt1 -1'])/volume_df['Vt1 -1']
print('volume ok')
QuoteAsset_df = df[QuoteAsset]
for column in QuoteAsset_df.columns.tolist():
    if column != 'QAVol1 -1':
        QuoteAsset_df[column] = (QuoteAsset_df[column] - QuoteAsset_df['QAVol1 -1'])/QuoteAsset_df['QAVol1 -1']
print('asset ok')
NumberOfTrades_df = df[NumberOfTrades]
for column in NumberOfTrades_df.columns.tolist():
    if column != 'Trades1 -1':
        NumberOfTrades_df[column] = (NumberOfTrades_df[column] - NumberOfTrades_df['Trades1 -1'])/NumberOfTrades_df['Trades1 -1']
print('num ok')
rsi_df = df[rsi]
for column in rsi_df.columns.tolist():
    if column != 'rsi1 -1':
        rsi_df[column] = (rsi_df[column] - rsi_df['rsi1 -1'])/rsi_df['rsi1 -1']
print('rsi ok')
mfi_df = df[mfi]
for column in mfi_df.columns.tolist():
    if column != 'mfi1 -1':
        mfi_df[column] = (mfi_df[column] - mfi_df['mfi1 -1'])/mfi_df['mfi1 -1']
print('mfi ok')
vwap_df = df[vwap]
for column in vwap_df.columns.tolist():
    if column != 'vwap1 -1':
        vwap_df[column] = (vwap_df[column] - vwap_df['vwap1 -1'])/vwap_df['vwap1 -1']
print('vwap ok')

df_final = pd.concat([init_df, price_df, volume_df, QuoteAsset_df, NumberOfTrades_df, rsi_df, mfi_df, vwap_df, ispump_df], axis=1)


df_final.to_csv("DB_V2_pourcentage.csv", mode='w', header=True)