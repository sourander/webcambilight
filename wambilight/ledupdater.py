import numpy as np
from multiprocessing.dummy import Pool as ThreadPool

# import WS2801 stuff

class Ledupdater:
    def __init__(self, led_count):
        self.led_count = led_count
        # self.ws2801 = cv2.VideoCapture(src)

    """ DRAFT """
    def to_color(self, edgepixels):
        pixel_count = self.led_count
        
        """ HyperThreading test 
        pool = ThreadPool(4)
        pool.map(self.process_pixels, edgepixels)
        pool.close()
        pool.join()
        """
        
        # The linear processing version
        self.process_pixels(edgepixels)
    
    def process_pixels(self, pixelrow):
        for led in range(self.led_count):
            (b,g,r) = pixelrow[0].reshape(3,1)
            self.ws2801.set_pixel_rgb(led, r, g, b)