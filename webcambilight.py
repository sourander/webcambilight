# usage sudo python $(which python) -i webcambilight.py

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

def activate_loop():
    global do_the_loop
    do_the_loop = True

def on_press_action(notification):
    global do_the_loop
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
    webcam = WebcamVideoStream(30, 250, 160).start()
    time.sleep(2.0)

    # Keyboard hooks
    keyboard.on_press_key("enter", on_press_action)
    keyboard.on_press_key("backspace", quit_abmlight)
    
    while(running):
        #hdmi.fill(0,255,0)
        #image = snapshot(330, 5, 250)

        image = cv2.imread("images/tv-test-1.png") # PTS will succeed
        #image = cv2.imread("images/test.png") # PTS will fail

        pts = calibrate(image, hdmi, image.shape[0], timetohold=2, padding=0,  blur=3, perimultiplier=0.01)

        try:
            pts.any()
        except AttributeError:
            print("Calibration file has no data. Skipping the main loop.")
        else:
            print("Activating loop.")
            activate_loop()
        
        if(do_the_loop):
            print("Entering main loop")
            while(do_the_loop):
                frame = webcam.read()
                hdmi.drawimg(frame)
            print("Exiting the LED loop.")
              
    print("Exiting WebcAmbilight!")
    webcam.stop()
    hdmi.quit()
    
if __name__ == "__main__":
    run()

# leds = Ledupdater(total_leds)
# leds.to_color(edgepixels)
