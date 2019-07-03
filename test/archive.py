# This is for omitted methods and other tests

    
def creategreenscreen(width=1920, height=1080):
    canvas = np.zeros((height, width, 3), dtype="uint8")
    cv2.rectangle(canvas, (10, 10), (1900, 1000), (0,255,0), -1)
    return canvas
    
def fbitoscreen(imPath):
    os.system("killall -9 fbi")
    os.system("fbi -T 2 images/greenscreen.png")

