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
    
    def __init__(self,track,x,y,psi,color):
        self.track = track
        self.x = x # x-center of car 
        self.y = y # y-center of car
        self.color = car_color
        self.image1 = canvas.create_rectangle(self.x,self.y,self.x+30,self.y+18,fill=self.color)
        self.image2 = canvas.create_oval(self.x,self.y,25,18,fill=self.color)
      
    def move(self,xV,yV):
        self.xV = xV
        self.yV = yV
        #coordinates = self.canvas.coords(self.image1)
        #print(coordinates)
        self.canvas.move(self.image1,self.xV+0.23,self.yV-0.21)
        self.canvas.move(self.image2,self.xV,self.yV)
  
    def pos(self):
        return self.canvas.coords(self.image1)


wdw01 = tk.Tk()

WIDTH = 800
HEIGHT = 600
my_canvas = tk.Canvas(wdw01, width=WIDTH, height=HEIGHT)
my_canvas.pack()
tk.Button(wdw01, text='enough', command = lambda:wdw01.destroy()).pack(expand=True)

# background fix
pace_coords = [2, 2, 50, 2, 630, 598, 550, 598, 2, 50, 2, 2]
my_canvas.create_polygon(pace_coords, fill="grey", outline="green")

# construct some cars
car_init_pos = [0, 0]
car_color = "blue"
car01 = car(my_canvas,car_init_pos,car_color)
car_init_pos = [0, 0]
car_color = "green"
car02 = car(my_canvas,car_init_pos,car_color)

while True:
    car01.move(1,1)

    car02_x = car02.pos()[0]
    car02_y = car02.pos()[1]
    car02_Vx = 1 + m.ceil(m.sin(0.02*car02_x))
    car02_Vy = 1
    #print(car02_x, m.sqrt(car02_x))
    car02.move(car02_Vx,car02_Vy)
    
    wdw01.update()
    time.sleep(0.02)

wdw01.mainloop()

