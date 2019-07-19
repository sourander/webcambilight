# usage sudo python $(which python) webcambilight.py

# Import packages
import cv2
import imutils
from wambilight import Hdmi, Ledupdater, ConfigIO, calibrate
from wambilight import Edgegenerator
from wambilight.camsetting import set_exposure, init_settings                       
import time
from imutils.video import FPS
import keyboard


# Global variables
v_leds = 35 # DO NOT COUNT
h_leds = 22 # leds in the corner twice!
total_leds = 22 # Change to actual value

blendframes = 1
blend_inwards = 3
blur = 11 # odd number!

do_the_loop = False # Do not change
running = True # Do not change
pts = None

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
    
    # Video Capture
    webcam = cv2.VideoCapture(0)
    init_settings(webcam)
   
    # Let the camera warm up
    time.sleep(2.0)

    # Keyboard hooks
    keyboard.on_press_key("enter", deactivate_loop)
    keyboard.on_press_key("backspace", quit_abmlight)
    
    # Get last run's config from wambilight/config/cornerpoint.npy
    global pts
    pts = config.get()
    


    while(running):
        """ If 'pts' has no calibration data, run calibration.
            Else, run main loop until user presses:
            
            'enter'     : to run calibration again 
            'backspace' : to exit software completely"""
        
        try:
            pts.any()
        except AttributeError:
            print("Calibration file has no data. Running the calibration again.")
            set_exposure(webcam, 300, 5, 250)
            leds.clear()
            (grabbed, image) = webcam.read()
            pts = calibrate(image, hdmi, image.shape[0], timetohold=4, padding=0,  blur=3, perimultiplier=0.01)
        else:
            print("Activating loop.")
            activate_loop()
        
        if(do_the_loop):
            # Do once before 'The Loop'
            print("Changing exposure, gain and sat. Starting 'The Loop'.")
            set_exposure(webcam, 30, 255, 160)
            edge.set_cornerpoints(pts)
            
            # For debugging. Start FPS counter.
            fps = FPS().start()
            
            while(do_the_loop):
                # Grab a frame from the webcam
                (grabbed, frame) = webcam.read()
                
                # Calculate edge pixels
                edgepixels = edge.generate(frame)
                
                # UPDATE LEDS with edgepixels data
                leds.to_color(edgepixels)
                
                # For debugging. Update FPS.
                fps.update()
            
            # Perform after exiting 'The Loop'
            print("Exiting the LED loop.")
            
            # For debugging. Show FPS.
            fps.stop()
            print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))  
    
    # Perform right before exiting the software
    config.to_file(pts)
    print("Exiting WebcAmbilight!")
    webcam.release()
    leds.clear()
    hdmi.quit()
    
if __name__ == "__main__":
    run()