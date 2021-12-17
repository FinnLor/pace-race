# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

@author: emilo
"""

#import matplotlib.pyplot as plt
import numpy as np
import math as m
import time
import tkinter as tk


class car:
    
    def __init__(self,track,x,y,psi,color):
        self.track = track
        self.x = x # x-center of car 
        self.y = y # y-center of car
        self.psi = psi
        self.color = color      
        self.cl = 20 # car length
        self.cw = 10 # car width
        self.x1 = (-self.cl/2) # upper left x-corner of car
        self.y1 =  (self.cw/2) # upper left y-corner of car
        self.x2 = (-self.cl/2) # bottom left x-corner of car
        self.y2 = (-self.cw/2) # bottom left y-corner of car
        self.x3 =  (self.cl/2) # bottom right x-corner of car
        self.y3 = (-self.cw/2) # ottom right y-corner of car
        self.x4 =  (self.cl/2) # upper right x-corner of car
        self.y4 =  (self.cw/2) # upper right y-corner of car
        self.image0 = track.create_bitmap(x, y)
        
        self.image1 = track.create_polygon([x-self.x1,y+self.y1], [x-self.x2,y-self.y2], [x+self.x3,y-self.y3], [x+self.x4,y+self.y4], fill = self.color)
        
    def move(self,dx,dy,dpsi):
        
        # print("Punkt 1 alt")
        # dpsi = 0.1
        # print(self.x, self.y, self.x1, self.y1)
        # self.x1 = self.x1*m.cos(dpsi) - self.y1*m.sin(dpsi)
        # self.y1 = self.x1*m.sin(dpsi) + self.y1*m.cos(dpsi)
        # print("Punkt 1 neu")
        # print(self.x, self.y, self.x1, self.y1)
        
        # self.x2 = self.x2*m.cos(dpsi) - self.y2*m.sin(dpsi)
        # self.y2 = self.x2*m.sin(dpsi) + self.y2*m.cos(dpsi)
        # self.x3 = self.x3*m.cos(dpsi) - self.y3*m.sin(dpsi)
        # self.y3 = self.x3*m.sin(dpsi) + self.y3*m.cos(dpsi)
        # self.x4 = self.x4*m.cos(dpsi) - self.y4*m.sin(dpsi)
        # self.y4 = self.x4*m.sin(dpsi) + self.y4*m.cos(dpsi)

        #self.image1 = track.create_polygon([self.x-self.x1,self.y+self.y1], [self.x-self.x2,self.y-self.y2], [self.x+self.x3,self.y-self.y3], [self.x+self.x4,self.y+self.y4], fill = self.color)
        #self.image1 = track.create_polygon([90,180], [130, 170], [140,185], [100,200], fill = self.color)
        
        print([self.x-self.x1,self.y+self.y1])
        print(dx,dy)
        self.track.move(self.image1,dx,dy)
        self.track.move(self.image0,dx,dy)
        self.x = self.track.coords(self.image0)[0]
        self.y = self.track.coords(self.image0)[1]
        
    def set_pos(self,x,y,psi):
        dx   = x-self.x
        dy   = y-self.y
        dpsi = psi-self.psi
        self.move(dx, dy, dpsi)


wdw01 = tk.Tk() # Generate a GUI-window

WIDTH = 800
HEIGHT = 600
track = tk.Canvas(wdw01, width=WIDTH, height=HEIGHT)
track.pack()
#enough_button = tk.Button(wdw01, text='enough', command = lambda:wdw01.destroy()).pack(expand=True) # Original
enough_button = tk.Button(wdw01, text='enough', command = lambda:wdw01.destroy())
enough_button.place(x=700, y=200)
newpos_button = tk.Button(wdw01, text='newpos')
newpos_button.place(x=700, y=400)
#enough_button.pack(expand=True)


# background fix
track_coords = [2, 2, 50, 2, 630, 598, 550, 598, 2, 50, 2, 2]
track.create_polygon(track_coords, fill="grey", outline="green")

# construct some cars into the track
car_init_x = 0
car_init_y = 0
car_init_psi = 0
car_color = "blue"
car01 = car(track,car_init_x,car_init_y,car_init_psi,car_color)

# car01.set_pos(200,200,0)


while True:
    dx = 1 # x-velocity [m/???]
    dy = 1 # y-velocity [m/???]
    dpsi = 1 # angle physically positive [rad]
    car01.move(dx,dy,dpsi)
    wdw01.update()
    time.sleep(0.01)

wdw01.mainloop()

