import cv2
import numpy as np
import pygame
import os

def initializepygame():
    # Initialize PyGame
    os.putenv('SDL_FBDEV', '/dev/fb0')
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    pygame.display.init()
    
    # Get width and height
    print(pygame.display.Info())
    w = pygame.display.Info().current_w 
    h = pygame.display.Info().current_h 
    lcd = pygame.display.set_mode((w,h), pygame.FULLSCREEN)
    lcd.fill((255,0,0))
    pygame.display.update()
    pygame.mouse.set_visible(False)


initializepygame()