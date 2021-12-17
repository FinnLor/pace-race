# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

@author: emilo
"""

#import matplotlib.pyplot as plt
#import numpy as np
import math as m
import time
import tkinter as tk


class car:
    
    def __init__(self,canvas,car_init_pos,car_init_vel,car_color):
        self.canvas = canvas
        self.x = car_init_pos[0]
        self.y = car_init_pos[1]
        self.xp = car_init_vel[0]
        self.yp = car_init_vel[1]
        self.color = car_color
        self.image = canvas.create_rectangle(self.x,self.y,self.x+30,self.y+18,fill=self.color)
      
    def move(self):
        #self.xV = xV
        #self.yV = yV
        #coordinates = self.canvas.coords(self.image1)
        #print(coordinates)
        self.canvas.move(self.image,self.xp,self.yp)

  
    # def pos(self):
    #     return self.canvas.coords(self.image)


wdw01 = tk.Tk()

WIDTH = 800
HEIGHT = 600
track = tk.Canvas(wdw01, width=WIDTH, height=HEIGHT)
track.pack()
tk.Button(wdw01, text='enough', command = lambda:wdw01.destroy()).pack(expand=True)

# background fix
pace_coords = [2, 2, 50, 2, 630, 598, 550, 598, 2, 50, 2, 2]
track.create_polygon(pace_coords, fill="grey", outline="green")

# construct some cars
car_init_pos = [0, 0]
car_init_vel = [0, 0]
car_color = "blue"
car01 = car(track,car_init_pos,car_init_vel,car_color)


while True:
    #car01.move(1,1)

    car01.move()
    wdw01.update()
    time.sleep(0.02)

wdw01.mainloop()

