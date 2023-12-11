import pandas as pd
import binance
import datetime
import pymysql
import mysql.connector
from sqlalchemy import create_engine

client =binance.Client()


def Recup_data(symbol,id_symbol,id_granularity,decalage):
    date='2021-11-01'
    start_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    #delta = 1000*60*60
   
    timestamp=int(datetime.datetime.timestamp(pd.to_datetime(start_date))*1000) # Conversion en timestamp
    
    if id_granularity == 1:   
        klines = client.get_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR,timestamp)
        
    else:
        klines = client.get_historical_klines(symbol, client.KLINE_INTERVAL_1DAY,timestamp,limit=1000 )
        
    data = pd.DataFrame(data = [row[1:7] for row in klines], columns = ['open', 'high', 'low', 'close', 'volume','close_time'])
    
    data['close_time'] = pd.to_datetime(data['close_time'] + decalage, unit='ms')
    data.loc[:, data.columns != 'close_time'] = data.loc[:, data.columns != 'close_time'].astype(float)
    
    data['symbol_id'] = id_symbol
    data['granularity_id'] = id_granularity
    df=data.reindex(columns=['close_time','symbol_id','granularity_id','open', 'high', 'low', 'close', 'volume'])
    
    return df

    
df_1h_BTCEUR=Recup_data("BTCEUR",1,1,1000*60*60)
df_1h_ETHEUR=Recup_data("ETHEUR",2,1,1000*60*60)
df_1d_BTCEUR=Recup_data("BTCEUR",1,2,0)
df_1d_ETHEUR=Recup_data("ETHEUR",2,2,0)

train_df_list = [df_1h_BTCEUR,df_1h_ETHEUR, df_1d_BTCEUR,df_1d_ETHEUR]

train_df = pd.concat(train_df_list, ignore_index=True)


my_conn =create_engine("mysql+pymysql://opa_user:opa_pwd@localhost/opa_db")


train_df.to_sql('history_Data', my_conn, if_exists = 'append', index=False)
