import numpy as np
import cv2
from imutils.perspective import four_point_transform


class Edgegenerator:
    def __init__(self, verleds, horleds, blendframes, blend_inwards, blur):
        self.pts = None
        self.vertleds = verleds
        self.horleds = horleds
        self.led_count = self.vertleds*2 + self.horleds*2
        self.blendamount = blendframes
        self.blend_inwards = blend_inwards
        self.blur = blur
        self. history =  np.zeros((self.led_count, 
                                   self.blendamount, 3), 
                                   dtype='uint8')

                                  
    def warpandresize(self, image):
        # Warp image based on cornerpoint data
        cornerpoints = self.pts
        warped = four_point_transform(image, cornerpoints)
        resized = cv2.resize(warped, (self.vertleds, self.horleds+2), 
                             interpolation = cv2.INTER_CUBIC)
        resized = cv2.GaussianBlur(resized,(self.blur,self.blur),0)
        return resized
        
        
    def border_average(self, img, avg):
        edgepixels = np.concatenate((img[:avg,:].transpose(1,0,2), 
                                     img[1:-1,-avg:], 
                                     np.flip(img[-avg:,:].transpose(1,0,2)), 
                                     np.flip(img[1:-1,:avg])))
                              
        average = np.mean((edgepixels),axis=1, dtype='uint16')
        average = average.reshape(self.led_count,1,3).astype('uint8')
        return average


    def generate(self, image):

        img = self.warpandresize(image)
        
        # Grab edge pixels into an array (leds * 1 * 3)
        edgepixels = self.border_average(img, self.blend_inwards)
        
        if (self.blendamount >= 2):
            edgepixels = self.blendhistory(edgepixels)
        
        return edgepixels


    def set_cornerpoints(self, cornerpoints):
        self.pts = cornerpoints

    """ NOTE! Blending over time drops the FPS quite dramatically """
    def blendhistory(self, new_entry):
        # Blend current edgepixeldata with n-amount of previous
        # images. 

        # Getter
        lenght = self.led_count
        history = self.history

        # Nudge history 1 pixel down. Add new entry.
        history = np.roll(history, 1, axis=0)
        history[:,:1] = new_entry
                
        # Setter
        self.history = history
                
        # Calculate mean of the last n entries in history.
        blend = np.mean((history),axis=1, dtype='uint16')
        blend = blend.reshape(lenght,1,3).astype('uint8')
                
        return blend
        
    def lift(image, lift):
        # Lift black levels without touching whitepoint
        image16 = image.astype('int16') * (1-(lift/255)) + lift
        image16 = np.clip(image16, 0, 255)
        image = image16.astype('uint8')
        return image
        
    def whitepoint(image, lift):
        # Change whitepoint
        image16 = image.astype('int16') * (1+(lift/255))
        image16 = np.clip(image16, 0, 255)
        image = image16.astype('uint8')
        return image
        
    def whitebalance(image, greenred, blueyellow):
        """
        Usage: Give negative or positive value to
        
        -128      ...        127
        <- (-)  greenred  (+) ->
        <- (-) blueyellow (+) ->
        """
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab).astype('int16')
        lab[:,:,1] += greenred
        lab[:,:,2] += blueyellow
        lab = np.clip(lab, 0, 255).astype('uint8')
        image = cv2.cvtColor(lab, cv2.COLOR_Lab2BGR)
        return image


    

