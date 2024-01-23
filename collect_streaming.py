###################### MongoDB data Loading function ###########################

from pymongo import MongoClient
from datetime import datetime
import websocket
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def insert_into_mongodb(data):
    data['timestamp'] = datetime.now()
    client = MongoClient(
        host="127.0.0.1",
        port=27017,
        username=os.getenv('login'),
        password=os.getenv('password')
    )
    db = client.OPA_MongoDB
    collection = db.CandlessticksCollection
    collection.insert_one(data)

########################################################################
######################  WEBSOCKET STREAMING  ###########################

cc = 'btceur'
interval = '1s'

socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'
print("WebSocket used:", socket)

dates, closes, highs, lows = [], [], [], []

def on_message(ws, message):
    try:
        json_message = json.loads(message)
        candle = json_message['k']
        is_candle_closed = candle['x']
        close = candle['c']
        high = candle['h']
        low = candle['l']

        if is_candle_closed:
            current_time = datetime.now()
            dates.append(current_time)
            closes.append(float(close))
            highs.append(float(high))
            lows.append(float(low))

            print('Date:', current_time)
            print('Closes:', closes)
            print('Highs:', highs)
            print('Lows:', lows)

            # MongoDB
            insert_into_mongodb({'date': current_time, 'close': float(close), 'high': float(high), 'low': float(low)})

    except Exception as e:
        print(f"Error processing message: {e}")

def on_close(ws, close_status_code, close_msg):
    print(f"Closed connection with status code: {close_status_code}, message: {close_msg}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_open(ws):
    print("WebSocket opened")

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)

try:
    ws.run_forever()
except KeyboardInterrupt:
    print("WebSocket connection closed by user.")
finally:
    ws.close()
