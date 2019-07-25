import numpy as np
from threading import Thread

import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import time

# import WS2801 stuff

class Ledupdater:
    def __init__(self, led_count):
        self.led_count = led_count
        
        # Software SPI
        # self.pixels = Adafruit_WS2801.WS2801Pixels(self.led_count, clk=18, do=23)
        
        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.led_count, spi=SPI.SpiDev(0, 0))
        

    def to_color(self, edgepixels):
       
        self.process_pixels(edgepixels)
        

    def process_pixels(self, pixelrow):
                
        for led in range(self.led_count):
            r = int(pixelrow[led,0,:][2])
            g = int(pixelrow[led,0,:][1])
            b = int(pixelrow[led,0,:][0])


            self.pixels.set_pixel_rgb(led, r, g, b)
        # Update LEDs
        self.pixels.show()
        
    def clear(self):
        self.pixels.clear()
        time.sleep(0.01)
        self.pixels.show()