# Import packages
import cv2
import numpy as np
from wambilight import Hdmi
import imutils
from imutils.perspective import four_point_transform
import time


# Instansiate a PyGame Surface
hdmi = Hdmi()

"""
Generate various size images for testing
gfx = np.full([800, 300, 3], (25, 255, 255), dtype=np.uint8)
"""

""" REPLACE THIS WITH WEBCAM IMAGE """
image = cv2.imread("images/tv-test-3.png")
""" REPLACE THIS WITH WEBCAM IMAGE """


""" Find TV from image. """
ratio = image.shape[0] / 540.0
orig = image.copy()
image = imutils.resize(image, height = 540)


""" ISOLATE GREEN CHANNEL for better contrast """
# Green = Green channel - Blue channel - Red channel 
(b, g, r) = cv2.split(image)
g = cv2.subtract(cv2.subtract(g, b), r)

# Blur and find edges. Blur 3 or 5 gets best results.
g = cv2.GaussianBlur(g,(5,5),cv2.BORDER_DEFAULT) 
edged = imutils.auto_canny(g)

# Find the contours in the edged image. Keep 5 largest.
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# Loop over the contours. Approx and find 4 corners.
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)
    print("Amount of corners {}".format(len(approx)))
    if len(approx) == 4:
        pts = approx
        break

if 'pts' in locals():
    cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
    (x, y, w, h) = cv2.boundingRect(approx)
    cv2.putText(image, "TV here?", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 255), 2)
    hdmi.drawimg(image)
    time.sleep(4)
else:
    print("No TV found in the image. Adjust settings.")

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, pts.reshape(4, 2) * ratio)
hdmi.drawimg(warped)
time.sleep(4)
