import numpy as np
import cv2
from imutils.perspective import four_point_transform


class Edgegenerator:
    def __init__(self, verleds, horleds, blendframes, blend_inwards, blur):
        self.pts = None
        self.vertleds = verleds
        self.horleds = horleds
        self.led_count = self.vertleds + self.horleds*2
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
        resized = cv2.resize(warped, (self.vertleds, self.horleds+1), 
                             interpolation = cv2.INTER_CUBIC)
        resized = cv2.GaussianBlur(resized,(self.blur,self.blur),0)
        return resized
        
        
    def border_average(self, img, avg):
        # Right-1-REVERSED, Top-REVERSED, Left-1
        edgepixels = np.concatenate((img[:0:-1,-avg:],
                                     img[:avg,::-1].transpose(1,0,2),
                                     img[1:,:avg]))
                              
        average = np.mean((edgepixels),axis=1, keepdims=True, dtype='uint16')
        average = average.astype('uint8')
        return average


    def generate(self, image):
        # Warp the image. Rescale to M*N
        img = self.warpandresize(image)
        
        # Grab edge pixels into an array (leds * 1 * 3)
        edgepixels = self.border_average(img, self.blend_inwards)
        
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
        history = np.roll(history, 1, axis=1)
        history[:,:1] = new_entry
                
        # Setter
        self.history = history
                
        # Calculate mean of the last n entries in history.
        blend = np.mean((history),axis=1, keepdims=True, dtype='uint16')
        blend = blend.astype('uint8')
                
        return blend
        
    def lut_transform(self, image, lut_r, lut_g, lut_b):

        b, g, r = cv2.split(image)
        
        r = cv2.LUT(r, lut_r).astype(np.uint8)
        g = cv2.LUT(g, lut_g).astype(np.uint8)
        b = cv2.LUT(b, lut_b).astype(np.uint8)
                
        merged = cv2.merge((b, g, r))
        
        return merged


    def saturation(self, image, lut_s, hueshift=0):
        h, s, v = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
    
        s = cv2.LUT(s, lut_s).astype(np.uint8)
        
        # Adjust hue
        h = self.hue(h, hueshift)
    
        merged = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)
        
        return merged
        
    
    def hue(self, h, shift):
        # 180 to 360 range in 16-bit
        h = h.astype('uint16')
        h = h * 2

        # Nudge hue
        h = h + (shift * 2)

        # Find cells where value is larger than 180
        h[h > 360] = h[h > 360] - 360
        h[h < 0] = h[h < 0] + 360


        # 360 back to 180 in 8-bit
        h = (h / 2).astype('uint8')
        
        return h

        
