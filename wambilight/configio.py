import numpy as np
import os

class ConfigIO():
    def __init__(self):

        self.dirname = "config"
        self.filename = "cornerpoint.npy"
        
        # /home/pi/webcambilight/
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        
        # /home/pi/webcambilight/wambilight/config/
        self.configdir = os.path.join(self.basedir, self.dirname, "")
        
        # /home/pi/webcambilight/wambilight/config/cornerpoint.py
        self.filepath = os.path.join(self.configdir, self.filename)

        
    def to_file(self,pts):
        try:
            # Create target Directory
            os.mkdir(self.configdir)
            print("Directory '{}' created ".format(self.dirname)) 
        except FileExistsError:
            print("Config file will be placed in directory: '{}'".format(self.configdir)) 

        print("Writing a file {}".format(self.filepath))
        np.save(self.filepath, pts)
    
    def get(self):
        try:
            pts = np.load(self.filepath)
        except:
            return None
        return pts

    def delete(self):
        if os.path.isfile(self.filepath):
            os.remove(self.filepath)
        else:
            print("ConfigIO delete:{} file not found".format(self.filepath))
            
    def get_luts(self):
        lut_r = np.load(os.path.join(self.configdir, "lut_r.npy"))
        lut_g = np.load(os.path.join(self.configdir, "lut_g.npy"))
        lut_b = np.load(os.path.join(self.configdir, "lut_b.npy"))
        return lut_r, lut_g, lut_b