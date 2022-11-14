import time
import pybithumb

def get_target_price():
    df = pybithumb.get_ohlcv("BTC")
    volatility = (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.6
    target_price = df.iloc[-1]['open'] + volatility
    return target_price

def sell_crypto_currency(bithumb):
    unit = bithumb.get_balance("BTC")[0]
    return bithumb.sell




target_price = get_target_price()

hold_flag = False

while True:

    price = pybithumb.get_current_price("BTC")
    print(price)

    time.sleep(1)