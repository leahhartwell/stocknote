from yahoo_fin import stock_info as si
import random
import time
from gpiozero import LED, Buzzer

prev = [0, 0, 0]
now = [0, 0, 0]
last_ten = [0, 0, 0]

class last_ten:
    def __init__(self):
        self.data = []
    def add(self,val):
        if len(self.data)==10:
            self.data=self.data[1:]+[val]
        else:
            self.data+=[val]

def current_price(ticker, ticker_last_ten, price_diff_prev, price_diff_now):
    #price = round(si.get_live_price(ticker),2)
    price = round(random.random()*100,2)
    print(price)
    ticker_last_ten.add(price)
    print(ticker_last_ten.data)

    if (len(ticker_last_ten.data) >= 10):
        price_diff_now = ticker_last_ten.data[9] - ticker_last_ten.data[8]
        print(price_diff_now)
        price_diff_prev = ticker_last_ten.data[8] - ticker_last_ten.data[7]
        print(price_diff_prev)
        price_last_ten = ticker_last_ten.data[9] - ticker_last_ten.data[1]
        print(price_last_ten)

        if price_last_ten > 3:
            print("price change increased over $3 in 5 mins")
        elif price_last_ten < -3:
            print("price change decreased over $3 in 5 mins")
        else:
            print("minor price change in last 5 mins")

        if (price_diff_now > price_diff_prev) and (price_diff_now > 0):
            print("price change accelerating and increasing")
        elif (price_diff_now > price_diff_prev) and (price_diff_now < 0):
            print("price change accelerating and decreasing")
        elif (price_diff_now < price_diff_prev) and (price_diff_now > 0):
            print("price change decelerating and increasing")
        elif (price_diff_now < price_diff_prev) and (price_diff_now < 0):
            print("price change decelerating and decreasing")  
        else:
            print("no change")


# stocks
stock = ["aapl", "logi", "nflx"]
last = [last_ten(), last_ten(), last_ten()]
price_diff_prev = [0, 0, 0]
price_diff_now = [0, 0, 0]

while True:
    for i in range(len(stock)):
        current_price(stock[i], last[i], prev[i], now[i])
        
    #time.sleep(30)
    





