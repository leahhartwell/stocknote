from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import get_data
import random
import time
from gpiozero import LED, Buzzer, Button
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import threading

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
font = ImageFont.load_default()


class last_ten:
    def __init__(self):
        self.data = []
    def add(self,val):
        if len(self.data)==10:
            self.data=self.data[1:]+[val]
        else:
            self.data+=[val]

def current_price(ticker, ticker_last_ten, price_diff_prev, price_diff_now):
    blue.off()
    green.off()
    red.off()
    draw.text((x, top),       "Ticker: " + str(ticker),  font=font, fill=255)
    print(ticker)
    price = round(si.get_live_price(ticker),2)
    #price = round(price_data,2)
    #price = round(random.random()*100,2)
    draw.text((x, top+8),     "Price: $" + str(price), font=font, fill=255)
    print(price)
    ticker_last_ten.add(price)
    print(ticker_last_ten.data)

    if (len(ticker_last_ten.data) >= 10):
        price_diff_now = ticker_last_ten.data[9] - ticker_last_ten.data[8]
        print(price_diff_now)
        price_diff_prev = ticker_last_ten.data[8] - ticker_last_ten.data[7]
        print(price_diff_prev)
        price_last_ten = ticker_last_ten.data[9] - ticker_last_ten.data[0]
        print(price_last_ten)

        if price_last_ten > 10 or price_last_ten < -10:
            print("price change increased/decreased")
            draw.text((x, top+16),    "Large Price Change",  font=font, fill=255)
            blue.on()
            buzzer.beep()
        else:
            print("minor price change")
            draw.text((x, top+16),    "Minor Price Change",  font=font, fill=255)
            blue.off()
            buzzer.off()
            

        if (abs(price_diff_now) > abs(price_diff_prev)) and (price_diff_now > 0):
            print("price change accelerating and increasing")
            draw.text((x, top+25),    "Price Accel + Gain",  font=font, fill=255)
            green.blink(0.1,0.1)
            yellow.off()
            red.off()
        elif (abs(price_diff_now) > abs(price_diff_prev)) and (price_diff_now < 0):
            print("price change accelerating and decreasing")
            draw.text((x, top+25),    "Price Accel + Loss",  font=font, fill=255)
            red.blink(0.1,0.1)
            yellow.off()
            green.off()
        elif (abs(price_diff_now) < abs(price_diff_prev)) and (price_diff_now > 0):
            print("price change decelerating and increasing")
            draw.text((x, top+25),    "Price Decel + Gain",  font=font, fill=255)
            green.blink(0.5,0.5)
            yellow.off()
            red.off()
        elif (abs(price_diff_now) < abs(price_diff_prev)) and (price_diff_now < 0):
            print("price change decelerating and decreasing")
            draw.text((x, top+25),    "Price Decel + Loss",  font=font, fill=255)
            red.blink(0.5,0.5)
            yellow.off()
            green.off()
        else:
            print("no change")
            draw.text((x, top+25),    "No Price Change",  font=font, fill=255)
            yellow.on()
        
    disp.image(image)
    disp.display()
    time.sleep(.1)        
            
# stocks
stock = ["aapl", "logi", "nflx"]

#storage
last = [last_ten(), last_ten(), last_ten()]
price_diff_prev = [0, 0, 0]
price_diff_now = [0, 0, 0]
prev = [0, 0, 0]
now = [0, 0, 0]
last_ten = [0, 0, 0]

#components
blue = LED(14)
green = LED(11)
yellow = LED(26)
red = LED(12)
buzzer = Buzzer(1)
button = Button(18)

#while True:
#    for i in range(len(stock)):
#        current_price(stock[i], last[i], prev[i], now[i])
#        time.sleep(10)

def main():
    
#    aapl_data = get_data("aapl", "01/01/2020", "11/20/2020", False, "1d")
#    aapl_price = aapl_data["open"].tolist()
#    logi_data = get_data("logi", "01/01/2020", "11/20/2020", False, "1d")
#    logi_price = logi_data["open"].tolist()
#    nflx_data = get_data("nflx", "01/01/2020", "11/20/2020", False, "1d")
#    nflx_price = nflx_data["open"].tolist()
    
    blue.off()
    green.off()
    red.off()
    button_toggle = 0
    
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        
        if (button.is_pressed) and (button_toggle < len(stock) - 1):
            button_toggle = button_toggle + 1
            print(button_toggle)
            current_price(stock[button_toggle], last[button_toggle], prev[button_toggle], now[button_toggle])
        elif (button.is_pressed) and (button_toggle >= len(stock) - 1):
            button_toggle = 0
            current_price(stock[button_toggle], last[button_toggle], prev[button_toggle], now[button_toggle])
        else:
            current_price(stock[button_toggle], last[button_toggle], prev[button_toggle], now[button_toggle])
        #time.sleep(1)
        
if __name__ == "__main__":
    main()
    
    





