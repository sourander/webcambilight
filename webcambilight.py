# usage sudo python $(which python) -i webcambilight.py

# Import packages
import cv2
import imutils
from wambilight import Hdmi, Ledupdater, ConfigIO, calibrate


# Instansiate Hdmi object (a PyGame Surface)
hdmi = Hdmi()
config = ConfigIO()
webcamres = 540

""" REPLACE THIS WITH WEBCAM IMAGE """
image = cv2.imread("images/tv-test-3.png")
""" REPLACE THIS WITH WEBCAM IMAGE """


# Find TV's cornerpoints from image.
cornerpoints = calibrate(image, hdmi, webcamres)

# Instansiate Ledupdater
leds = Ledupdater(cornerpoints)

image = cv2.imread("images/tv-test-3-nemo.png")
image = imutils.resize(image, height = webcamres)

# usage leds.warp_and_draw(image, hdmi)