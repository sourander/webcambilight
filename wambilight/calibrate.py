import time
import imutils
import cv2
from imutils.perspective import four_point_transform

def calibrate(image, hdmi, webcamres=540):
    # Find TV from image. 
    # image : a high quality still (e.g. 1920x1080)
    # webcamres : stream quality (e.g. 720p, 540p) 
    
    ratio = image.shape[0] / float(webcamres)
    orig = image.copy()
    image = imutils.resize(image, height = webcamres)
    timetohold = 4 # For displaying the image to user
    
    # Subtract B&R from G for higher contrast
    (b, g, r) = cv2.split(image)
    g = cv2.subtract(cv2.subtract(g, b), r)

    # Blur and find edges.
    g = cv2.GaussianBlur(g,(3,3),cv2.BORDER_DEFAULT) 
    edged = imutils.auto_canny(g)

    # Find and sort the contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    # Find a contour with 4 corners.
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
        # Display the image for user for n seconds.

    else:
        print("No TV found in the image. Adjust settings.\nReturning 'None' cornerpoints.")
        return None

    # Display the image for evaluation
    print("Displaying the calibration image for {} seconds".format(timetohold))
    hdmi.drawimg(image)
    time.sleep(timetohold)

    # Scale the cornerpoints to match webcamres
    pts = pts.reshape(4, 2) * ratio
        
    return pts


