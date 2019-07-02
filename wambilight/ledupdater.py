import numpy as np
import cv2
from imutils.perspective import four_point_transform
from timeit import default_timer as timer



class Ledupdater:
    def __init__(self, cornerpoints):
        self.pts = cornerpoints
        self.vertleds = 60
        self.horleds = 30
       

    def warp_and_draw(self, image, hdmi):
        # TIMER
        start = timer()

        warped = four_point_transform(image, self.pts)

        resized = cv2.resize(warped, (self.vertleds, self.horleds), 
                             interpolation = cv2.INTER_CUBIC) 
        
        # Grab edge pixels into an array
        top = resized[0,:]
        right = resized[1:,-1]
        bottom = np.flip(resized[-1,1:-1])
        left = np.flip(resized[1:,0])
        edgepixels = np.concatenate((top, right, bottom, left), axis=0)
        
        # TIMER
        end = timer()
        print(round((end - start)*1000, 2), "milliseconds")
        
        hdmi.drawimg(resized)
        


"""
FIRST METHOD OF GETTING EDGE PIXELS

image = np.array([[ 0,  1,  2,  3,  4,  5],
                  [ 6,  7,  8,  9, 10, 11],
                  [12, 13, 14, 15, 16, 17],
                  [18, 19, 20, 21, 22, 23],
                  [24, 25, 26, 27, 28, 29],
                  [30, 31, 32, 33, 34, 35]])



"""