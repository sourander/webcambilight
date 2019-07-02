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
cornerpoints = calibrate(image, hdmi, calibres)

# Instansiate Ledupdater
leds = Ledupdater(cornerpoints)

""" REPLACE THIS WITH WEBCAM VIDEO STREAM """
image = cv2.imread("images/tv-test-3-nemo.png")
image = imutils.resize(image, height = videores)
""" REPLACE THIS WITH WEBCAM VIDEO STREAM """

leds.warp_and_draw(image, hdmi)