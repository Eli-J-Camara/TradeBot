import config, csv
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

# If we were to use the indicators the way they were originally intended than we would be using day long intervals.
# This function would have a parameter called "days". When each indicator called this function it would pervide the
# required days it needs in order to start producing data.

def history():
    # csvfile = open('data_test/OneDayAgo.csv', 'w', newline='')
    # csv_writer = csv.writer(csvfile, delimiter = ',')
    historical_closes = []
    candlesticks = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_1MINUTE, '1 day ago UTC')
    for candlestick in candlesticks:
        # candlestick[0] = candlestick[0] / 1000
        # csv_writer.writerow(candlestick)
        historical_closes.append(float(candlestick[4]))
    return historical_closes[-50:]
    # return historical_closes


