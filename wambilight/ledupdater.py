import numpy as np
import cv2
from imutils.perspective import four_point_transform
from timeit import default_timer as timer
from scipy.ndimage.interpolation import shift

""" 
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
"""

class Ledupdater:
    def __init__(self, cornerpoints, blendvalue, hdmi):
        self.pts = cornerpoints
        # NOTE! Do not count corner LED's twice
        self.vertleds = 60
        self.horleds = 38
        self.led_count = self.vertleds*2 + self.horleds*2
        self.blendamount = blendvalue
        self.history = None
        self.generatehistory(mode=1)
        self.hdmi = hdmi
                                  

    def warp_and_draw(self, image):
        # TIMER
        start = timer()

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
      
        """ NOTE! Setting blend value gives nice smoothing of pixels
            based on previous pixels values.
            
            ...with the cost of lag. Blending 5 images adds around
            20 milliseconds of delay to the code. """
        if (self.blendamount >= 2):
            edgepixels = self.blendhistory(edgepixels)
            
        
        # TIMER
        end = timer()
        print(round((end - start)*1000, 2), "milliseconds")
        
        resized[1:-1,1:-1] = 0
        self.hdmi.drawimg(resized)

    """ DRAFT """
    def show_on_ws2801(self, pixelrow):
        pixel_count = self.led_count
        

        for i in range(pixel_count):
            (b,g,r) = pixelrow[0].reshape(3,1)
            pixels.set_pixel_rgb(i, r, g, b)
    """ DRAFT """

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
        
    """ 
    BELOW THIS LINE ARE FUNCTIONS THAT ARE SUPPORTING __INIT__
    OR FOR DEBUGGING/PRINTING STUFF TO CONSOLE
    """    
        
        
    def generatehistory(self, mode):
        # Getter
        lenght = self.led_count
        height = self.blendamount
        
        if (height < 2):
            pass
        
        if (mode == 1):
            history =  np.zeros((lenght, height, 3), dtype='uint8')
        elif (mode == 2):
            history = np.arange((lenght * height * 3), dtype='uint8').reshape(lenght, 5, 3)

        self.history = history

    def printhistory(self):
        # This is for debugging
        
        # Getter
        history = self.history
        
        for i in range(1, history.shape[1]):
            print("1x4 element of history {}".format(history[:,0:1][4]))
            print("2x4 element of history {}".format(history[:,1:2][4]))
            print("3x4 element of history {}".format(history[:,2:3][4]))
            print("4x4 element of history {}".format(history[:,3:4][4]))
            print("5x4 element of history {}".format(history[:,4:5][4]))
            print(" ")
        
        self.printmean()
        
    def printmean(self):
        # Getter
        history = self.history
        lenght = self.led_count
        temp = np.mean((history),axis=1, dtype='uint16').reshape(lenght,1,3)
        temp = temp.astype('uint8')
        print("Blend of nx4: {}".format(temp[:,0:1][4]))
        
            
        


    

