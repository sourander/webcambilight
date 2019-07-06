from threading import Thread
import cv2


class WebcamVideoStream:
    def __init__(self, exposure, gain, sat=128, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        
        # Toggle off auto exposure
        self.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.stream.set(cv2.CAP_PROP_FOCUS, 15)
        
        self.stream.set(cv2.CAP_PROP_GAIN, gain)
        self.stream.set(cv2.CAP_PROP_EXPOSURE, exposure)
        self.stream.set(cv2.CAP_PROP_AUTO_WB, 0)
        self.stream.set(cv2.CAP_PROP_TEMPERATURE, 6000)
        self.stream.set(cv2.CAP_PROP_SATURATION, sat)
        
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stream.set(cv2.CAP_PROP_FPS , 30)
        

        (self.grabbed, self.frame) = self.stream.read()

        self.printspecs()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
 
    def set_exposure(self, exposure, gain, sat):
        self.stream.set(cv2.CAP_PROP_EXPOSURE, exposure)
        self.stream.set(cv2.CAP_PROP_GAIN, gain)
        self.stream.set(cv2.CAP_PROP_SATURATION, sat)
        
    def printspecs(self):
        # List of modes is in url
        # https://docs.opencv.org/4.1.0/d4/d15/group__videoio__flags__base.html
        width = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = self.stream.get(cv2.CAP_PROP_FPS)
        gain = self.stream.get(cv2.CAP_PROP_GAIN)
        exposure = self.stream.get(cv2.CAP_PROP_EXPOSURE )
        wb = self.stream.get(cv2.CAP_PROP_TEMPERATURE)
        
        focusmode = self.stream.get(cv2.CAP_PROP_AUTOFOCUS)
        focus = self.stream.get(cv2.CAP_PROP_FOCUS)
     
        
        print("W: {} H: {} @ {}", width, height, fps)
        print("Gain: ", gain)
        print("Exposure: ", exposure)
        print("White Balance: ", wb)
        
 

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True