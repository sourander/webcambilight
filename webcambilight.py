# usage sudo python $(which python) -i webcambilight.py

# Import packages
import cv2
import imutils
from wambilight import Hdmi, Ledupdater, ConfigIO, calibrate


# Instansiate Hdmi object (a PyGame Surface)
hdmi = Hdmi()
config = ConfigIO()
videores = 720
calibres = 540

""" REPLACE THIS WITH WEBCAM IMAGE """
image = cv2.imread("images/tv-test-3.png")
image = imutils.resize(image, height = videores)
""" REPLACE THIS WITH WEBCAM IMAGE """

# Find TV's cornerpoints from image using an image
# downscaled to calibres
cornerpoints = calibrate(image, hdmi, calibres, timetohold=2, padding=0)

# Instansiate Ledupdater
leds = Ledupdater(cornerpoints, blendvalue=1)

""" REPLACE THIS WITH WEBCAM VIDEO STREAM """
stream = cv2.imread("images/tv-test-3-nemo.png")
stream = imutils.resize(stream, height = videores)
""" REPLACE THIS WITH WEBCAM VIDEO STREAM """

def ten_times():
    for i in range(0,10):
        leds.warp_and_draw(stream, hdmi)


leds.warp_and_draw(stream, hdmi)