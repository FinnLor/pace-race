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
        print("___init__")
        
        self.track = track
        self.c = (x, y) # car_center position
        self.psi = psi # car_angle
        self.color = color
        
        self.dc = (0, 0) # velocity of car_center
        self.cl = 20 # car length
        self.cw = 10 # car width
        #self.cd = m.sqrt(m.pow(0.5*self.cl,2) + m.pow(0.5*self.cw,2)) # corner distance
        self.c1 = (x-self.cl/2, y+self.cw/2) # upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # bottom right corner of car
        self.c4 = (x+self.cl/2, y+self.cw/2) # upper right corner of car
        
        self.car_center = track.create_bitmap(x, y)
        self.car_polygon = track.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color)
   
        print("test")
        print(self.c)
        print(self.car_center[0])

   
    def car_move(self,dx,dy,dpsi): # complete movement and rotation
        print("car_move")
        
        self.dc = (dx, dy) # velocity of car
        self.dpsi = dpsi
       
        self.car_rotate(dpsi) # let the car rotate with the desired delta-psi
        self.track.move(self.car_center,self.dc[0],self.dc[1])
        self.c = self.track.coords(self.car_center) # vector from canvas_reference to car_center
        self.track.move(self.car_polygon,self.dc[0],self.dc[1])



    def car_rotate(self,dpsi): # only rotation
        print("car_rotate")
        
        #rot = np.array([[np.cos(dpsi), -np.sin(dpsi)], [np.sin(dpsi), np.cos(dpsi)]]) # rotation matrix clockwise
        rot = np.array([[np.cos(dpsi), np.sin(dpsi)], [-np.sin(dpsi), np.cos(dpsi)]]) # rotation matrix physically correct
        
        cpoly = self.track.coords(self.car_polygon) # extract car_polygon data
        c1c = np.array([cpoly[0]-self.c[0],cpoly[1]-self.c[1]]) # vector from car_center to c1
        c2c = np.array([cpoly[2]-self.c[0],cpoly[3]-self.c[1]]) # vector from car_center to c2
        c3c = np.array([cpoly[4]-self.c[0],cpoly[5]-self.c[1]]) # vector from car_center to c3
        c4c = np.array([cpoly[6]-self.c[0],cpoly[7]-self.c[1]]) # vector from car_center to c4
    
        c1cn = np.dot(rot, c1c) # rotated vector from car_center to c1
        c2cn = np.dot(rot, c2c) # rotated vector from car_center to c2
        c3cn = np.dot(rot, c3c) # rotated vector from car_center to c3
        c4cn = np.dot(rot, c4c) # rotated vector from car_center to c4
        
        self.c1 = (c1cn[0] + self.c[0], c1cn[1]+self.c[1]) # polygon vector from canvas_GUI to c1
        self.c2 = (c2cn[0] + self.c[0], c2cn[1]+self.c[1]) # polygon vector from canvas_GUI to c2
        self.c3 = (c3cn[0] + self.c[0], c3cn[1]+self.c[1]) # polygon vector from canvas_GUI to c3
        self.c4 = (c4cn[0] + self.c[0], c4cn[1]+self.c[1]) # polygon vector from canvas_GUI to c4

        self.track.delete(self.car_polygon) # delete old car
        self.car_polygon = track.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # set new, rotated car
    
    
    
    def set_car_pos(self,x,y,psi): # set new car postion with zero velocities
        print("set_car_pos")
        
        self.c = (x, y) # car_center position
        self.psi = psi # car_angle
        self.dc = (0, 0) # velocity of car
        self.dpsi = 0 # velocity of car_angle
        self.c1 = (x-self.cl/2, y+self.cw/2) # upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # bottom right corner of car
        self.c4 = (x+self.cl/2, y+self.cw/2) # upper right corner of car

        self.car_rotate(psi) # call method car_rotate
        
        self.track.delete(self.car_center) # delete old car_center
        self.car_center = track.create_bitmap(x, y)
        self.track.delete(self.car_polygon) # delete old car polygon
        self.car_polygon = track.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # set new, rotated car


    
    def car_pos_reset(self): # rest car position
        print("car_pos_reset")

        self.c = (0, 0) # car_center position
        self.psi = 0 # car_angle
        self.dc = (0, 0) # velocity of car
        self.dpsi = 0 # velocity of car_angle
        self.c1 = (-self.cl/2,  self.cw/2) # upper left corner of car
        self.c2 = (-self.cl/2, -self.cw/2) # bottom left corner of car
        self.c3 = ( self.cl/2, -self.cw/2) # bottom right corner of car
        self.c4 = ( self.cl/2,  self.cw/2) # upper right corner of car
        
        self.track.delete(self.car_center) # delete old car_center
        self.car_center = track.create_bitmap(0, 0) # create new car_center with reset data
        self.track.delete(self.car_polygon) # delete old car polygon
        self.car_polygon = track.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # create new car_polygon with reset data
    
    
    
wdw01 = tk.Tk()

WIDTH = 800
HEIGHT = 600
track = tk.Canvas(wdw01, width=WIDTH, height=HEIGHT)
track.pack()
tk.Button(wdw01, text='enough', command = lambda:wdw01.destroy()).pack(expand=True)

# background fix
track_coords = [2, 2, 50, 2, 630, 598, 550, 598, 2, 50, 2, 2]
track.create_polygon(track_coords, fill="grey", outline="green")

# construct car
x = 100 # startposition x
y = 100 # startposition y
psi = 0 # startangle
color = "blue"
car01 = car(track, x, y,  psi, color)


for i in range(0,300):
#while True:
    car01.car_move(1.5,1.5,0.03) # dx, dy, dpsi
    wdw01.update()
    time.sleep(0.001)

wdw01.mainloop()

