import numpy as np
import cv2
from imutils.perspective import four_point_transform
from scipy.ndimage.interpolation import shift

""" 
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
"""

class Ledupdater:
    def __init__(self, cornerpoints, hdmi, blendframes=1, debugging=False):
        self.pts = cornerpoints
        # NOTE! Do not count corner LED's twice
        self.vertleds = 60
        self.horleds = 38
        self.led_count = self.vertleds*2 + self.horleds*2
        self.blendamount = blendframes
        self.debugging = debugging
        self. history =  np.zeros((self.led_count, 
                                   self.blendamount, 3), 
                                   dtype='uint8')
        self.hdmi = hdmi
                                  

    def warp_and_draw(self, image):

        warped = four_point_transform(image, self.pts)

        resized = cv2.resize(warped, (self.vertleds, self.horleds+2), 
                             interpolation = cv2.INTER_CUBIC) 
        
        # Grab edge pixels into an array
        # len(edgepixels) equals self.led_count
        top = resized[:1,:].transpose(1,0,2)
        bottom = np.flip(resized[-1:,:].transpose(1,0,2))
        right = resized[1:-1,-1:]
        left = np.flip(resized[1:-1,:1])
        edgepixels = np.concatenate((top, right, bottom, left))
      
        if (self.blendamount >= 2):
            edgepixels = self.blendhistory(edgepixels)
            
        if self.debugging:
            #resized[1:-1,1:-1] = 0
            self.hdmi.drawimg(resized)

    """ DRAFT """
    def show_on_ws2801(self, pixelrow):
        pixel_count = self.led_count
        

        for i in range(pixel_count):
            (b,g,r) = pixelrow[0].reshape(3,1)
            self.pixels.set_pixel_rgb(i, r, g, b)
    

    def blendhistory(self, new_entry):
        # Blend current edgepixeldata with n-amount of previous
        # images. 

        # Getter
        lenght = self.led_count
        history = self.history

        # Nudge history 1 pixel down. Add new entry.
        history = shift(history, (0,1,0), cval=0)
        history[:,:1] = new_entry
                
        # Setter
        self.history = history
                
        # Calculate mean of the last n entries in history.
        blend = np.mean((history),axis=1, dtype='uint16').reshape(lenght,1,3)
        blend = blend.astype('uint8')
                
        return blend
        

            
        


    

