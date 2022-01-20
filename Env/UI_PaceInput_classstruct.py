
# https://codereview.stackexchange.com/questions/229503/how-to-structure-tkinter-with-classes

# import required libraries
from shapely.geometry import LineString, Point
import numpy as np
# import matplotlib.pyplot as plt
# import random as rn
import tkinter as tk



class UIPace:
    """
    
    Class to grap the pacedata with an UI
    
    ...
    
    Attributes
    ----------
    work in progress
    
    Methods
    -------
    work in progress
        
    """
    def __init__(self, ROADWIDTH=8, NPOINTS: int = 1000): 
        pass
    
    def main():
        ui_pace = tk.Tk()
        ui_pace.minsize(840, 400)
        uiobject01 = UIPace(ui_pace)
        ui_pace.mainloop()

if __name__ == '__main__':
    UIPace.main()






