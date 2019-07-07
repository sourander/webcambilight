# usage sudo python $(which python) webcambilight.py

# Import packages
import cv2
import imutils
from wambilight import Hdmi, Ledupdater, ConfigIO, calibrate, WebcamVideoStream
from wambilight import Edgegenerator                        
import time
from imutils.video import FPS
import keyboard

# Global variables
v_leds = 60 # DO NOT COUNT
h_leds = 38 # leds in the corner twice!
total_leds = v_leds + h_leds + 2

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
    edge = Edgegenerator(v_leds, h_leds, blendframes=1)
    webcam = WebcamVideoStream(30, 250, 160).start()
    
    # Let the camera warm up
    time.sleep(2.0)

    # Keyboard hooks
    keyboard.on_press_key("enter", deactivate_loop)
    keyboard.on_press_key("backspace", quit_abmlight)
    
    while(running):
        """ If 'pts' has no calibration data, run calibration.
            Else, run main loop until user presses:
            
            'enter'     : to run calibration again 
            'backspace' : to exit software completely"""
        
        try:
            global pts
            pts.any()
        except AttributeError:
            print("Calibration file has no data. Running the calibration again.")
            webcam.set_exposure(300, 5, 250)
            image = webcam.read()
            pts = calibrate(image, hdmi, image.shape[0], timetohold=4, padding=0,  blur=3, perimultiplier=0.01)
        else:
            print("Activating loop.")
            activate_loop()
            print(pts.shape)
            print(pts)
        
        if(do_the_loop):
            # Do once before 'The Loop'
            print("Changing exposure, gain and sat. Starting 'The Loop'.")
            hdmi.drawimg(cv2.imread("images/status-calibration-done.png"))
            webcam.set_exposure(30, 255, 160)
            edge.set_cornerpoints(pts)
            fps = FPS().start()
            
            while(do_the_loop):
                frame = webcam.read()
                edgepixels = edge.generate(frame)
                # UPDATE LEDS with edgepixels data
                hdmi.drawimg(frame)
                fps.update()
            
            # Perform after exiting 'The Loop'
            print("Exiting the LED loop.")
            fps.stop()
            print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))  
    
    # Perform right before exiting the software
    print("Exiting WebcAmbilight!")
    webcam.stop()
    hdmi.quit()
    
if __name__ == "__main__":
    run()

# leds = Ledupdater(total_leds)
# leds.to_color(edgepixels)
