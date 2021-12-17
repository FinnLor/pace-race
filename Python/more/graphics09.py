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
        #print("___init__")
        
        self.track = track
        self.psi = psi # car_angle
        self.color = color 
        self.dc = (0, 0) # velocity of car_center
        self.cl = 40 # car length
        self.cw = 20 # car width
        self.c1 = (x-self.cl/2, y+self.cw/2) # upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # bottom right corner of car
        self.c4 = (x+self.cl/2, y+self.cw/2) # upper right corner of car
        self.car_center = track.create_bitmap(x, y) # car_center position
        self.car_polygon = track.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color)
        self.car_rotate(psi) # call method car_rotate

   
    def car_move(self,dx,dy,dpsi): # complete movement and rotation
        #print("car_move")
        
        self.dc = (dx, dy) # velocity of car
        self.dpsi = dpsi # angle velocity of car
        self.car_rotate(dpsi) # let the car rotate with the desired delta-psi
        self.track.move(self.car_center,self.dc[0],self.dc[1]) # move the car_center
        self.track.move(self.car_polygon,self.dc[0],self.dc[1]) # move the car_polygon



    def car_rotate(self,dpsi): # only rotation
        #print("car_rotate")
        
        #rot = np.array([[np.cos(dpsi), -np.sin(dpsi)], [np.sin(dpsi), np.cos(dpsi)]]) # rotation matrix clockwise
        rot = np.array([[np.cos(dpsi), np.sin(dpsi)], [-np.sin(dpsi), np.cos(dpsi)]]) # rotation matrix physically correct    
        c_p = self.track.coords(self.car_polygon) # extract car_polygon position data
        c_c = self.track.coords(self.car_center) # extract car_center position data
        
        cc_c1 = np.array([c_p[0] - c_c[0],c_p[1] - c_c[1]]) # vector from car_center to c1
        cc_c2 = np.array([c_p[2] - c_c[0],c_p[3] - c_c[1]]) # vector from car_center to c2
        cc_c3 = np.array([c_p[4] - c_c[0],c_p[5] - c_c[1]]) # vector from car_center to c3
        cc_c4 = np.array([c_p[6] - c_c[0],c_p[7] - c_c[1]]) # vector from car_center to c4
        cc_c1n = np.dot(rot, cc_c1) # vector from car_center to rotated c1
        cc_c2n = np.dot(rot, cc_c2) # vector from car_center to rotated c2
        cc_c3n = np.dot(rot, cc_c3) # vector from car_center to rotated c3
        cc_c4n = np.dot(rot, cc_c4) # vector from car_center to rotated c4
        
        self.c1 = (cc_c1n[0] + c_c[0], cc_c1n[1] + c_c[1]) # polygon vector from canvas_GUI to c1
        self.c2 = (cc_c2n[0] + c_c[0], cc_c2n[1] + c_c[1]) # polygon vector from canvas_GUI to c2
        self.c3 = (cc_c3n[0] + c_c[0], cc_c3n[1] + c_c[1]) # polygon vector from canvas_GUI to c3
        self.c4 = (cc_c4n[0] + c_c[0], cc_c4n[1] + c_c[1]) # polygon vector from canvas_GUI to c4

        self.track.delete(self.car_polygon) # delete old car
        self.car_polygon = track.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # set new, rotated car
    
    
    
    def set_car_pos(self,x,y,psi): # set new car postion with zero velocities
        #print("set_car_pos")
        
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
        #print("car_pos_reset")

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
# startposition x, startposition y, startangle psi
car01 = car(track, 140, 100,  0.4, "green")
car02 = car(track, 100, 100,  0.6, "blue")
car03 = car(track, 110,  90,  0, "orange")
car04 = car(track, 120, 100,  1, "black")
car05 = car(track, 500, 500,  1.3, "white")
car06 = car(track, 500, 500,  1.3, "brown")
car07 = car(track, 140, 100,  0.4, "green")
car08 = car(track, 100, 100,  0.6, "blue")
car09 = car(track, 110,  90,  0, "orange")
car10 = car(track, 120, 100,  1, "red")
car11 = car(track, 500, 500,  1.3, "purple")
car12 = car(track, 500, 500,  1.3, "grey")

t0 = time.time()
for i in range(0,500):
#while True:
    # dx, dy, dpsi

    car01.car_move(1.5,1.8,0.03)
    car02.car_move(1.8,1.5,0.00)
    car03.car_move(1.5,1.2,-0.01)
    car04.car_move(1.0,1.5,-0.10)
    car05.car_move(-0.7,-0.6,0.11)
    car06.car_move(-0.8,-0.8,0.02)
    car07.car_move(1.5,1.5,0.00)
    car08.car_move(1.1,1.2,-0.02)
    car09.car_move(1.2,1.5,-0.10)
    car10.car_move(2.8,1.5,0.05)
    car11.car_move(0.1,-1.2,-0.03)
    car12.car_move(1.0,1.2,-0.10)
    
    #wdw01.update()
    #time.sleep(0.01)
    
t1 = time.time()-t0
print(t1)  
wdw01.mainloop()


