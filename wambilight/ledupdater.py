import numpy as np
from imutils.perspective import four_point_transform
from timeit import default_timer as timer



class Ledupdater:
    def __init__(self, cornerpoints):
        self.pts = cornerpoints
       

    def warp_and_draw(self, image, hdmi):
        # TIMER
        start = timer()

        warped = four_point_transform(image, self.pts)

        # TIMER
        end = timer()
        print((end - start)*1000)
        
        hdmi.drawimg(warped)

"""
FIRST METHOD OF GETTING EDGE PIXELS

image = np.array([[ 0,  1,  2,  3,  4,  5],
                  [ 6,  7,  8,  9, 10, 11],
                  [12, 13, 14, 15, 16, 17],
                  [18, 19, 20, 21, 22, 23],
                  [24, 25, 26, 27, 28, 29],
                  [30, 31, 32, 33, 34, 35]])

left = np.flip(image[1:,0])
top = image[0,:]
right = image[1:,-1]
bottom = np.flip(image[-1,1:-1])

edgepixels = np.concatenate((top, right, bottom, left), axis=0)
"""