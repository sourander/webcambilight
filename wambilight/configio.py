import numpy as np
import os

class ConfigIO():
    def __init__(self):
        self.dirName = "config/"
        self.fileName = "cornerpoint.npy"
        
    def to_file(self,pts):
        # Write numpy data to config/filename.npy
        print("Writing cornerpoint data to config file.")

        try:
            # Create target Directory
            os.mkdir(self.dirName)
            print("Directory '{}' created ".format(self.dirName)) 
        except FileExistsError:
            print("Config file will be placed in directory: '{}'".format(self.dirName)) 

        np.save(self.dirName + "/" + self.fileName, pts)
    
    def get(self):
        try:
            pts = np.load(self.dirName + self.fileName)
        except:
            return None
        return pts

