import pygame
import os
import imutils
import numpy as np
import cv2

class Hdmi:
    """This creates a PyGame Surface for displaying
    images on HDMI output of RasPi"""
    
    def __init__(self):
        # Initialize Surface   
        os.putenv('SDL_FBDEV', '/dev/fb0')
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        pygame.display.init()
        pygame.mouse.set_visible(False)
        
        # Get and set width and height
        # print(pygame.display.Info())
        self.w = pygame.display.Info().current_w 
        self.h = pygame.display.Info().current_h 
        self.lcd = pygame.display.set_mode((self.w,self.h), pygame.FULLSCREEN, 24)
    
    
    def fill(self, r,g,b):
        self.lcd.fill((r,g,b))
        pygame.display.flip()
           
    
    def pad(self, image, lcd_dim, direction):
        """ Add some letterboxing to the image
        direction 0 adds rows, direction 1 adds columns """
 
        diff = lcd_dim - image.shape[direction]

        if(direction==0):
            new_item = np.zeros((diff, self.w, 3), dtype="uint8")
        else:
            new_item = np.zeros((self.h, diff, 3), dtype="uint8")
        
        # Add the array to the image and center image
        image = np.concatenate((image.copy(), new_item), direction)
        image = np.roll(image, int(diff / 2), axis=direction)
        
        return image    
          
          
    def drawimg(self, arrayimg, par=1.0):
        """OpenCV and NumPy use (h, w, c) ordering.
        This method will scale down image and swap 
        axis for PyGame surfarray. """
        

        # Convert grayscale image to colour
        if(arrayimg.ndim < 3):
            arrayimg = cv2.cvtColor(arrayimg,cv2.COLOR_GRAY2RGB)
            
        arrayimg = cv2.cvtColor(arrayimg, cv2.COLOR_BGR2RGB)
    
        if (par != 1.0):
            (height, width) = arrayimg.shape[:2]
            arrayimg = cv2.resize(arrayimg, (round(width * par), height))
            
        (height, width) = arrayimg.shape[:2]
        
        # Compare aspect ratio to lcd aspect ratio.
        if( (width/height) >= (self.w/self.h)):
            resized = imutils.resize(arrayimg, width=self.w) 
            if(resized.shape[0] != self.h):
                resized = self.pad(resized, self.h, direction=0)
        else:
            resized = imutils.resize(arrayimg, height=self.h)
            if(resized.shape[1] != self.w):
                resized = self.pad(resized, self.w, direction=1)


        pygame.surfarray.blit_array(self.lcd, resized.swapaxes(0,1))
        pygame.display.flip()
        
    def quit(self):
        pygame.display.quit()

        