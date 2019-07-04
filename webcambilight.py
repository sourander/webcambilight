# usage sudo python $(which python) -i webcambilight.py

# Import packages
import cv2
import imutils
from wambilight import Hdmi, Ledupdater, ConfigIO, calibrate, WebcamVideoStream
import time
from imutils.video import FPS

# Configuration
videores = 480
calibres = 480

""" CODE BEGINS """

def snapshot(exposure=30, gain=400, focus=15):
    webcam = WebcamVideoStream(exposure, gain, focus, src=0).start()
    (w, h) = webcam.getres()
    time.sleep(2.0)
    frame = webcam.read()
    hdmi.drawimg(frame)
    webcam.stop()
    return frame

def test(exposure=30, gain=800, focus=15):
    webcam = WebcamVideoStream(exposure, gain, focus, src=0).start()
    time.sleep(2.0)
    for i in range (0,90):
        frame = webcam.read()
        leds.warp_and_draw(frame)
    webcam.stop()

hdmi = Hdmi()
config = ConfigIO()

# Generate image for calibration. Screen around 150cd/m
# image = snapshot(exposure=400, gain=30, focus=10)

# Read items
image = cv2.imread("images/test.png")


cornerpoints = calibrate(image, hdmi, image.shape[0], timetohold=2, padding=0,  blur=3, perimultiplier=0.01)

leds = Ledupdater(cornerpoints, hdmi, debugging=True)

# For testing, do...
# test()


# Nice test data
# eso = cv2.imread("images/eso.png")
# yle = cv2.imread("images/yle-tv.png")