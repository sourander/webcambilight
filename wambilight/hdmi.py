import pygame
import os

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
        self.lcd = pygame.display.set_mode((self.w,self.h), pygame.FULLSCREEN)
    
    def fill(self, r,g,b):
        self.lcd.fill((r,g,b))
        pygame.display.update()
    
    def update(self):
        pygame.display.update()