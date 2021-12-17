# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

@author: em, fl, fs
"""

# funktioniert nicht. beim move geht psi nicht als zus parameter?



#import matplotlib.pyplot as plt
#import numpy as np
import math as m
import time
import tkinter as tk


class car:
    
    def __init__(self,track,x,y,psi,color):
        self.track = track
        self.psi = psi
        # corner_ul_x = -20 * m.cos(psi) - 10 * m.sin(psi)
        # corner_ul_y = -20 * m.sin(psi) + 10 * m.cos(psi)
        # corner_dl_x = -20 * m.cos(psi) - 10 * m.sin(psi)
        # corner_dl_y = -20 * m.sin(psi) + 10 * m.cos(psi)
        # corner_ur_x = -20 * m.cos(psi) - 10 * m.sin(psi)
        # corner_ur_y = -20 * m.sin(psi) + 10 * m.cos(psi)
        # corner_dr_x = -20 * m.cos(psi) - 10 * m.sin(psi)
        # corner_dr_y = -20 * m.sin(psi) + 10 * m.cos(psi)
        # self.ul = (x+corner_ul_x, y+corner_ul_y)
        # self.dl = (x+corner_dl_x, y-corner_dl_y)
        # self.dr = (x+corner_ur_x, y-corner_ur_y)
        # self.ur = (x+corner_dr_x, y+corner_dr_y)
        self.ul = (x-20, y+20)
        self.dl = (x-20, y-10)
        self.dr = (x+20, y-10)
        self.ur = (x+20, y+10)
        
        self.image1 = track.create_polygon(self.ul, self.dl, self.dr, self.ur, fill=color)
        #self.image1 = canvas.create_rectangle(x,y,x+30,y+18,fill=color)
        #self.image2 = canvas.create_oval(x,y,25,18,fill=color)
      
    def move(self,xV,yV):
        self.xV = xV
        self.yV = yV
        self.psi = 0
        
        
        self.ul = [23,23]
        self.image1 = track.create_polygon(self.ul, self.dl, self.dr, self.ur, fill="green")
        
        
        
        coordinates = self.track.coords(self.image1)
        print(coordinates)
        self.track.move(self.image1,self.xV,self.yV)


  
    def pos(self):
        return self.track.coords(self.image1)


wdw01 = tk.Tk()

WIDTH = 800
HEIGHT = 600
track = tk.Canvas(wdw01, width=WIDTH, height=HEIGHT)
track.pack()
tk.Button(wdw01, text='enough', command = lambda:wdw01.destroy()).pack(expand=True)

# background fix
pace_coords = [2, 2, 50, 2, 630, 598, 550, 598, 2, 50, 2, 2]
track.create_polygon(pace_coords, fill="grey", outline="green")

# cars moving
car01 = car(track,100,100,0,"blue")

for i in range(0,20):
#while True:

    car01.move(1,1)
    wdw01.update()
    time.sleep(0.02)

wdw01.mainloop()




