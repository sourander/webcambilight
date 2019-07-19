import cv2

def init_settings(webcam):
    webcam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    webcam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    webcam.set(cv2.CAP_PROP_FOCUS, 15)
    
    webcam.set(cv2.CAP_PROP_GAIN, 255)
    webcam.set(cv2.CAP_PROP_EXPOSURE, 30)
    webcam.set(cv2.CAP_PROP_AUTO_WB, 0)
    webcam.set(cv2.CAP_PROP_TEMPERATURE, 6000)
    webcam.set(cv2.CAP_PROP_SATURATION, 160)
    
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    webcam.set(cv2.CAP_PROP_FPS , 30)

def set_exposure(webcam, exposure, gain, sat):
    webcam.set(cv2.CAP_PROP_EXPOSURE, exposure)
    webcam.set(cv2.CAP_PROP_GAIN, gain)
    webcam.set(cv2.CAP_PROP_SATURATION, sat)