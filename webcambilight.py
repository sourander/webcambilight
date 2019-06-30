# Import packages
import cv2
import numpy as np
from wambilight import Hdmi
import imutils
from imutils import perspective


# Instansiate a PyGame Surface
hdmi = Hdmi()

"""
Generate various size images for testing
image = np.full([800, 300, 3], (25, 255, 255), dtype=np.uint8)
"""

""" REPLACE THIS WITH WEBCAM IMAGE """
image = cv2.imread("images/tv-test-1.png")
""" REPLACE THIS WITH WEBCAM IMAGE """


""" Find TV from image. """
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)


""" ISOLATE GREEN CHANNEL for better contrast """
(b, g, r) = cv2.split(image)
b_color = cv2.cvtColor(b,cv2.COLOR_GRAY2RGB)
g_color = cv2.cvtColor(g,cv2.COLOR_GRAY2RGB)
r_color = cv2.cvtColor(r,cv2.COLOR_GRAY2RGB)

g_blurred = cv2.GaussianBlur(g, (5, 5), 0)
g_edged = cv2.Canny(g_blurred, 75, 200)
g_canny = cv2.cvtColor(g_edged,cv2.COLOR_GRAY2RGB)

# convert the image to grayscale, blur it, and find edges
# in the image

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
