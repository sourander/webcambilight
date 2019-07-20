# usage sudo python $(which python) webcambilight.py

# Import packages
import cv2
import imutils
from wambilight import Hdmi, Ledupdater, ConfigIO, calibrate
from wambilight import Edgegenerator, WebcamVideoStream
from wambilight.camsetting import set_exposure, init_settings                       
import time
import os
# from imutils.video import FPS
import RPi.GPIO as GPIO  

# Global variables
v_leds = 39 # DO NOT COUNT
h_leds = 22 # leds in the corner twice!
total_leds = 83 # Change to actual value

# Set up GPIO pins
GPIO.setmode(GPIO.BCM) 
blue_btn = 5
red_btn = 6

# Image Blending options
blendframes = 6
blend_inwards = 4
blur = 15 # odd number!

# Do not change these
do_the_loop = False
running = True
pts = None
GPIO.setup(blue_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(red_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 



def activate_loop():
    global do_the_loop
    do_the_loop = True

def deactivate_loop(notification):
    global do_the_loop
    global pts
    pts = None
    do_the_loop = False

def quit_abmlight(notification):
    global running
    global do_the_loop
    running = False
    do_the_loop = False

def run():
    # Initialize objects
    hdmi = Hdmi()
    config = ConfigIO()
    edge = Edgegenerator(v_leds, h_leds, blendframes, blend_inwards, blur)
    leds = Ledupdater(total_leds)
    
    # Video Capture (linear capture)
    # webcam = cv2.VideoCapture(0)
    # init_settings(webcam)

    # Threading version
    webcam = WebcamVideoStream(30, 255, 160).start()

    # Let the camera warm up
    time.sleep(2.0)

    # Get last run's config from wambilight/config/cornerpoint.npy
    global pts
    pts = config.get()
    lut_r, lut_g, lut_b = config.get_luts()


    while(running):
        """ If 'pts' has no calibration data, run calibration.
        Else, run main loop until user presses:
            
        'Blue button' : to run calibration again 
        'Red button'  : to exit software completely """               
        try:
            pts.any()
        except AttributeError:
            print("Calibration file has no data. Running the calibration again.")
            
            
            webcam.set_exposure(300, 5, 250)
            #set_exposure(webcam, 300, 5, 250)
            
            leds.clear()
            (grabbed, image) = webcam.read()
            pts = calibrate(image, hdmi, image.shape[0], timetohold=4, padding=0,  blur=3, perimultiplier=0.01)
        else:
            print("Activating loop.")
            activate_loop()



        if(do_the_loop):
            # Do once before endless loop
            print("Changing exposure, gain and sat. Starting 'The Loop'.")
            webcam.set_exposure(30, 255, 160)
            # set_exposure(webcam, 30, 255, 160)
            edge.set_cornerpoints(pts)
            
            
            # The loop
            while(do_the_loop):
                # Grab a frame from the webcam
                frame = webcam.read()
                #(grabbed, frame) = webcam.read()
                
                # Calculate edge pixels
                edgepixels = edge.generate(frame)
                
                # Apply LUT magic
                edgepixels = edge.lut_transform(edgepixels, lut_r, lut_g, lut_b)
                
                # UPDATE LEDS with edgepixels data
                leds.to_color(edgepixels)
                
                if GPIO.input(red_btn):
                    quit_abmlight("RED button")
                
                if GPIO.input(blue_btn):
                    deactivate_loop("BLUE button")
            
            
            # Perform after exiting 'The Loop'
            print("Exiting the LED loop.")
            
    
    # Perform right before exiting the software
    config.to_file(pts)
    print("Exiting WebcAmbilight!")
    webcam.stop()
    # webcam.release()
    leds.clear()
    hdmi.quit()
    
if __name__ == "__main__":
    run()