import websocket, json, pprint, talib, numpy
import config
import price_hist
from binance.client import Client
from binance.enums import *

SOCKET = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.00415

closes = price_hist.history()
in_position = False
client = Client(config.API_KEY, config.API_SECRET, tld='us')

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
        print(f'closes: {closes}')
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            # print('All RSI\'s calculated so far')
            # print(rsi)
            last_rsi = rsi[-1]
            print(f'The current rsi is {last_rsi}')
            # print(f'rsi overbought: {RSI_OVERBOUGHT}')
            # print(f'rsi oversold: {RSI_OVERSOLD}')

            if last_rsi > RSI_OVERBOUGHT:
                print('RSI > 70')
                print(in_position)
                if in_position:
                    print("Sell now.")
                    # put binance sell logic here
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print('Nothing to sell.')
            else:
                print('RSI is not overbought.')

            if last_rsi < RSI_OVERSOLD:
                print('rsi < 30')
                print(in_position)
                if in_position:
                    print('It is oversold, but you already own it, nothing to do.')
                else:
                    print('BUY NOW!!!')
                    # put binance buy order logic here
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True
            else:
                print('RSI is not oversold.')



ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()

