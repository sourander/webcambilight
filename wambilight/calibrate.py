import time
import imutils
import cv2
from imutils.perspective import four_point_transform
from scipy.spatial import distance as dists

def nudge_towards_centroid(points, padding):
    """
    Make the cornerpoint area n %-units smaller 
    
    Useful for hiding problems in the image edged
    e.g. captions/letterbox 
    """
    
    # Centroid of bounding box
    centroid = points.mean(axis=0)
    
    # Calculate Euclidean distances centroid <-> corners
    distances = []
    for i in range(4):
        distances.append(dists.euclidean(points[i], centroid))
    
    # Keep the smallest distance. Create n %-units nudge.
    nudge = min(distances) * (padding / 100)
    
    # Perform nudge for each corner
    for p in points:
        for i in range(2):
            if p[i] > centroid[i]:
                p[i] -= nudge
            else:
                p[i]+= nudge
                
    return points

def calibrate(image, hdmi, calibres, timetohold = 4, padding=0, blur=3, perimultiplier=0.01):
    # Find TV from image. 
    # image should be in videores (e.g. 720p)
    # calibres : resolution used in this method (e.g. 540p) 
    
    ratio = image.shape[0] / float(calibres)
    image = imutils.resize(image, height = calibres)
    
    # Subtract B&R from G for higher contrast
    (b, g, r) = cv2.split(image)
    g = cv2.subtract(cv2.subtract(g, b), r)
    
    
    # Blur and find edges.
    g = cv2.GaussianBlur(g,(blur,blur),cv2.BORDER_DEFAULT) 
    edged = imutils.auto_canny(g)

    # Find and sort the contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    # Find a contour with 4 corners
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, perimultiplier * peri, True)
        print("Amount of corners {}".format(len(approx)))
        if len(approx) == 4:
            pts = approx
            break

    if 'pts' in locals():
        cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
        (x, y, w, h) = cv2.boundingRect(approx)
        cv2.putText(image, "TV here?", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 255), 2)
    else:
        print("No TV found in the image. Adjust settings.\nReturning 'None' cornerpoints.")
        return None

    # Display the image for evaluation
    print("Displaying the calibration image for {} seconds".format(timetohold))
    hdmi.drawimg(image)
    time.sleep(timetohold)

    # Ratio is used to scale cornerpoint data
    # from calibres -> videores
    # e.g. 540p -> 720p
    pts = pts.reshape(4, 2) * ratio
    
    if (padding > 0):
        pts = nudge_towards_centroid(pts, padding)
    
    return pts


