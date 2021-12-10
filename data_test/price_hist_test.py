import config, csv
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

def history():
    historical_closes = []
    candlesticks = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_1MINUTE, '1 day ago UTC')
    for candlestick in candlesticks:
        historical_closes.append(float(candlestick[4]))
    return historical_closes[-50:]

