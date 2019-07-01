import time
import imutils
import cv2
from imutils.perspective import four_point_transform

def calibrate(image, hdmi):
    """ Find TV from image. """
    ratio = image.shape[0] / 540.0
    orig = image.copy()
    image = imutils.resize(image, height = 540)


    """ ISOLATE GREEN CHANNEL for better contrast """
    # Green = Green channel - Blue channel - Red channel 
    (b, g, r) = cv2.split(image)
    g = cv2.subtract(cv2.subtract(g, b), r)

    # Blur and find edges. Blur 3 or 5 gets best results.
    g = cv2.GaussianBlur(g,(3,3),cv2.BORDER_DEFAULT) 
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
        print("No TV found in the image. Adjust settings.\nReturning 'None' cornerpoints.")
        return None

    # apply the four point transform to obtain a top-down
    # view of the original image
    pts = pts.reshape(4, 2) * ratio
    
    # Show the 'warped' original image to verify that things went well
    warped = four_point_transform(orig, pts)
    hdmi.drawimg(warped)
    
    time.sleep(4)
    return pts