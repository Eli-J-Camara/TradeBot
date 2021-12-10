import websocket, json, pprint, talib, numpy, price_hist_test, config
from binance.client import Client
from binance.enums import *

SOCKET = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'

BBANDS_PERIOD = 4
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.00415

closes = price_hist_test.history()
in_position = False
print(in_position)
# client = Client(config.API_KEY, config.API_SECRET, tld='us')

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print('sending order')
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity)
        print(order)
    except Exception as e:
        return False
    return True


def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('connection closed')

# def data_stream_hist(closes, MACD, time):
#     with open('MACDtest1.txt', 'w') as test_file:
#         test_file.writelines(['this is', 'a', 'test', 'of', 'my', 'skills'])

def on_message(ws, message):
    global closes
    global in_position

    print('recieved message')
    format_message = json.loads(message)
    candle = format_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print(f"Candle is closed at {close}")
        closes.append(float(close))
        # print(f'closes: {closes}')
        if len(closes) > BBANDS_PERIOD:
            np_closes = numpy.array(closes)
            # rsi = talib.RSI(np_closes, RSI_PERIOD)
            # macd, macdsignal, macdhist = talib.MACD(np_closes, fastperiod=12, slowperiod=26, signalperiod=9)
            # print("create bbands")
            upperband, middleband, lowerband = talib.BBANDS(np_closes, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
            # print('All Bollinger Bands calculated so far')
            # print(f'Upper Bands: {upperband}')
            # print(f'Lower Bands: {lowerband}')
            last_upper = upperband[-1]
            last_lower = lowerband[-1]
            print(f'Current Upper Band: {last_upper}')
            print(f'Current Lower Band: {last_lower}')

            close = float(close)
            last_upper = float(last_upper)

            if close > last_upper:
                if in_position:
                    print("SELL NOW")
                    # put binance sell logic here
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        print("SELL ORDER SUCCEEDED")
                else:
                    print(f'Ethereum price is < {last_upper}.')
            elif close < last_lower:
                if in_position:
                    print('BUY NOW!!!')
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        print('BUY ORDER SUCCEEDED')
                else:
                    print(f'Ethereum price is > {last_upper}')
            else:
                print('Ethereum price is between Bollinger Bands')


                    
        
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()