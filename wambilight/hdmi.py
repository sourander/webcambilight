import pygame
import os
import imutils
import numpy as np

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
        print(pygame.display.Info())
        self.w = pygame.display.Info().current_w 
        self.h = pygame.display.Info().current_h 
        self.lcd = pygame.display.set_mode((self.w,self.h), pygame.FULLSCREEN, 24)
    
    
    def fill(self, r,g,b):
        self.lcd.fill((r,g,b))
        pygame.display.flip()
    
    
    def update(self):
        pygame.display.flip()
        
    
    def crop_or_pad(self, image, lcd_dim, direction):
        """ Add padding or remove rows/cols from image to 
        make sure that image is exactly fitting to 
        PyGame Surface (self.lcd) """
        
        diff = lcd_dim - image.shape[direction]
        
        # Let's remove some cols or rows
        if(diff > 0):
            if(direction==0):
                print("Debug code 1")
                new_col = np.zeros((diff, self.w, 3), dtype="uint8")
                image = np.concatenate((image.copy(), new_col), direction)
            else:
                print("Debug code 2")
                new_col = np.zeros((self.h, diff, 3), dtype="uint8")
                image = np.concatenate((image.copy(), new_col), direction)
        
        # ...or maybe we want to remove cols or rows
        elif(diff < 0):
            print("Debug code 3")
            diff = abs(diff)
            image = np.delete(image, (range(0, diff)), axis=direction)
        
        print("New size")
        print(image.shape)
        
        return image    
          
          
    def drawimg(self, arrayimg):
        """OpenCV and NumPy use (h, w, c) ordering.
        This method will scale down image and swap 
        axis for PyGame surfarray"""
    
        (height, width) = arrayimg.shape[:2]
        
        if( (width/height) >= (self.w/self.h)):
            resized = imutils.resize(arrayimg, width=self.w) 
            if(resized.shape[0] != self.h):
                resized = self.crop_or_pad(resized, self.h, direction=0)
        else:
            resized = imutils.resize(arrayimg, height=self.h)
            if(resized.shape[1] != self.w):
                resized = self.crop_or_pad(resized, self.w, direction=1)

        pygame.surfarray.blit_array(self.lcd, resized.swapaxes(0,1))
        pygame.display.flip()

        