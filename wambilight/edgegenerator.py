import numpy as np
import cv2
from imutils.perspective import four_point_transform
from scipy.ndimage.interpolation import shift


class Edgegenerator:
    def __init__(self, verleds, horleds, cornerpoints, blendframes=1):
        self.pts = cornerpoints
        # NOTE! Do not count corner LED's twice
        self.vertleds = verleds
        self.horleds = horleds
        self.led_count = self.vertleds*2 + self.horleds*2
        self.blendamount = blendframes
        self. history =  np.zeros((self.led_count, 
                                   self.blendamount, 3), 
                                   dtype='uint8')

                                  
    def warpandresize(self, image):
        
        cornerpoints = self.pts
        
        warped = four_point_transform(image, cornerpoints)
               
        resized = cv2.resize(warped, (self.vertleds, self.horleds+2), 
                             interpolation = cv2.INTER_CUBIC) 
        return resized


    def generate(self, image):

        img = self.warpandresize(image)
        
        # Grab edge pixels into an array
        # Top, Right, Bottom, Left
        edgepixels = np.concatenate((img[:1,:].transpose(1,0,2), 
                                     img[1:-1,-1:], 
                                     np.flip(img[-1:,:].transpose(1,0,2)), 
                                     np.flip(img[1:-1,:1])))
      
        if (self.blendamount >= 2):
            edgepixels = self.blendhistory(edgepixels)
        
        return edgepixels



        
    def set_cornerpoints(self, cornerpoints):
        self.pts = cornerpoints

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
        

            
        


    

