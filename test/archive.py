# This is for omitted methods and other tests

def writeimage(image, filename, dirname="images"):
    try:
        # Create target Directory
        os.mkdir(dirname)
        print("Directory " , dirname ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirname ,  " already exists")
    
    status = cv2.imwrite('images/greenscreen.png',image) 
    print("Image written to file-system : ",status) 
    
def creategreenscreen(width=1920, height=1080):
    canvas = np.zeros((height, width, 3), dtype="uint8")
    cv2.rectangle(canvas, (10, 10), (1900, 1000), (0,255,0), -1)
    return canvas
    
def fbitoscreen(imPath):
    os.system("killall -9 fbi")
    os.system("fbi -T 2 images/greenscreen.png")
