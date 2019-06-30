import pygame
import os
import imutils

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
        
    def drawimg(self, arrayimg):
        """OpenCV and NumPy use (h, w, c) ordering.
        This method will scale down image and swap 
        axis for PyGame surfarray"""
        
        # Fit the image to PyGame Surface bbox        
        (height, width) = arrayimg.shape[:2]
        if ( (width/height) >= (self.w/self.h)):
            resized = imutils.resize(arrayimg, width=self.w)
        else:
            resized = imutils.resize(arrayimg, width=self.h)
        
        # Degub check
        print(resized.shape)
        
        # Draw swapped axis
        pygame.surfarray.blit_array(self.lcd, arrayimg.swapaxes(0,1))
        pygame.display.flip()

        