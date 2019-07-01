# usage sudo python $(which python) -i webcambilight.py

# Import packages
import cv2
from wambilight import Hdmi
from wambilight import calibrate




# Instansiate Hdmi object (a PyGame Surface)
hdmi = Hdmi()

""" REPLACE THIS WITH WEBCAM IMAGE """
image = cv2.imread("images/tv-test-3.png")
""" REPLACE THIS WITH WEBCAM IMAGE """


# Find TV's cornerpoints from image.
cornerpoints = calibrate(image, hdmi)
