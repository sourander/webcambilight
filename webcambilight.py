# usage sudo python $(which python) -i webcambilight.py

# Import packages
import cv2
import imutils
from wambilight import Hdmi, Ledupdater, ConfigIO, calibrate


""" REPLACE THIS WITH WEBCAM IMAGE """
videores = 720
calibres = 540

image = cv2.imread("images/tv-test-3.png")
image = imutils.resize(image, height = videores)

stream = cv2.imread("images/tv-test-3-nemo.png")
stream = imutils.resize(stream, height = videores)
""" REPLACE THIS WITH WEBCAM IMAGE """

""" ::::::::: Instansiate objects ::::::::::

-Hdmi is PyGame surface for displaying images on HDMI output

-Config is for r/w cornerpoints to/from file

-Stripcontroller controls WS2801 RGB LED strip

-Ledupdater generates edgepixels and uses Stripcontroller to/from
 add those RGB values to led strip

"""
hdmi = Hdmi()
config = ConfigIO()
cornerpoints = calibrate(image, hdmi, calibres, timetohold=2, padding=0)
leds = Ledupdater(cornerpoints, 1, hdmi)


def ten_times():
    for i in range(0,10):
        leds.warp_and_draw(stream)



