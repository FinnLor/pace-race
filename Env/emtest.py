# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 19:21:19 2022

@author: emilo
"""

# Import the required libraries
from tkinter import *
from shapely.geometry import LineString, Point
import numpy as np
from cls_Car import Car

# Create an instance of tkinter frame or window
win=Tk()

# Set the size of the tkinter window
win.geometry("700x350")

# Create a canvas widget
canvas=Canvas(win, width=500, height=300)
canvas.pack()

# Add a line in canvas widget

test2 = 5e5
print(test2)

line = ([[100,200],[200,10],[400, 50]])

ls = LineString(line)
x, y = LineString(ls).xy

min_x = min(x)
bias_x = min_x
max_x = max(x)
min_y = min(y)
bias_y = min_y
max_y = max(y)
delta_x = max_x - min_x
delta_y = max_y - min_y

x = 0.5 * np.add(x, -min_x)
                
line_data  = list((np.ravel(([x,y]),'F'))) # list is neccessary for a correct separation with comma
canvas.create_line(line_data, fill="green", width=1)





win.mainloop()