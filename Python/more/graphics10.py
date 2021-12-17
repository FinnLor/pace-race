# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

@author: emilo
"""

#import matplotlib.pyplot as plt
import numpy as np
import math as m
import time as t
import tkinter as tk
import random as rnd



class car:
    
    def __init__(self,canvas,x,y,psi,color):
        #print("___init__")
        
        self.canvas = canvas
        self.psi = psi # car_angle
        self.delta = 0 # car_front_wheel_angle
        self.color = color 
        self.dc = (0, 0) # velocity of car_center
        self.cl = 40 # car length
        self.cw = 20 # car width
        self.c1 = (x-self.cl/2, y+self.cw/2) # create upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # create bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # create bottom right corner of car
        self.c4 = (x+self.cl/2, y+self.cw/2) # create upper right corner of car
        self.car_center = canvas.create_bitmap(x, y) # create car_center position
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color)
        self.car_rotd(psi) # call method car_rotd

   
    def car_move(self,dx,dy,dpsi): # complete movement and rotation
        #print("car_move")
        
        self.dc = (dx, dy) # velocity of car
        self.dpsi = dpsi # angle velocity of car
        self.car_rotd(dpsi) # let the car rotate with the desired delta-psi
        self.canvas.move(self.car_center,self.dc[0],self.dc[1]) # move the car_center
        self.canvas.move(self.car_polygon,self.dc[0],self.dc[1]) # move the car_polygon



    def car_rotd(self,dpsi): # only rotation difference
        #print("car_rotd")
        
        rot = np.array([[np.cos(dpsi), np.sin(dpsi)], [-np.sin(dpsi), np.cos(dpsi)]]) # rotation matrix physically correct    
        c_p = self.canvas.coords(self.car_polygon) # extract car_polygon position data
        c_c = self.canvas.coords(self.car_center) # extract car_center position data
        
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

        self.canvas.delete(self.car_polygon) # delete old car
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # set new, rotated car
    
    
    
    def car_rot(self,psi): # only rotation
        #print("car_rot")
        
        # set car horizontally
        c_c = self.canvas.coords(self.car_center) # extract car_center position data
        self.c1 = (c_c[0]-self.cl/2,  c_c[1]+self.cw/2) # set upper left corner of car
        self.c2 = (c_c[0]-self.cl/2,  c_c[1]-self.cw/2) # set bottom left corner of car
        self.c3 = (c_c[0]+self.cl/2, c_c[1]-self.cw/2)  # set bottom right corner of car
        self.c4 = (c_c[0]+self.cl/2,  c_c[1]+self.cw/2) # set upper right corner of car
     
        # get vector of corner
        cc_c1 = np.array([self.c1[0] - c_c[0],self.c1[1] - c_c[1]]) # vector from car_center to c1
        cc_c2 = np.array([self.c2[0] - c_c[0],self.c2[1] - c_c[1]]) # vector from car_center to c2
        cc_c3 = np.array([self.c3[0] - c_c[0],self.c3[1] - c_c[1]]) # vector from car_center to c3
        cc_c4 = np.array([self.c4[0] - c_c[0],self.c4[1] - c_c[1]]) # vector from car_center to c4
        
        rot = np.array([[np.cos(psi), np.sin(psi)], [-np.sin(psi), np.cos(psi)]]) # rotation matrix physically correct  
        
        # rotate corner
        cc_c1n = np.dot(rot, cc_c1) # vector from car_center to rotated c1
        cc_c2n = np.dot(rot, cc_c2) # vector from car_center to rotated c2
        cc_c3n = np.dot(rot, cc_c3) # vector from car_center to rotated c3
        cc_c4n = np.dot(rot, cc_c4) # vector from car_center to rotated c4
        
        # set new corner 
        self.c1 = (cc_c1n[0] + c_c[0], cc_c1n[1] + c_c[1]) # new polygon vector from canvas_GUI to c1
        self.c2 = (cc_c2n[0] + c_c[0], cc_c2n[1] + c_c[1]) # new polygon vector from canvas_GUI to c2
        self.c3 = (cc_c3n[0] + c_c[0], cc_c3n[1] + c_c[1]) # new polygon vector from canvas_GUI to c3
        self.c4 = (cc_c4n[0] + c_c[0], cc_c4n[1] + c_c[1]) # new polygon vector from canvas_GUI to c4
        
        # update car polygon
        self.canvas.delete(self.car_polygon) # delete old car
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # set new, rotated car
        
    
    
    def set_car_pos(self,x,y,psi): # set new car postion and angles (with zero velocities)
        #print("set_car_pos")
        
        self.psi = psi # car_angle
        self.dc = (0, 0) # velocity of car
        self.dpsi = 0 # velocity of car_angle
        self.c1 = (x-self.cl/2, y+self.cw/2) # upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # bottom right corner of car
        self.c4 = (x+self.cl/2, y+self.cw/2) # upper right corner of car
        self.car_rot(psi) # call method car_rot
        self.canvas.delete(self.car_center) # delete old car_center
        self.car_center = canvas.create_bitmap(x, y)
        self.canvas.delete(self.car_polygon) # delete old car polygon
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # set new, rotated car


    
    def car_pos_reset(self): # reset car position
        #print("car_pos_reset")

        self.dc = (0, 0) # velocity of car
        self.dpsi = 0 # velocity of car_angle
        self.psi = 0 # car_angle
        self.c1 = (-self.cl/2,  self.cw/2) # upper left corner of car
        self.c2 = (-self.cl/2, -self.cw/2) # bottom left corner of car
        self.c3 = ( self.cl/2, -self.cw/2) # bottom right corner of car
        self.c4 = ( self.cl/2,  self.cw/2) # upper right corner of car
        self.canvas.delete(self.car_center) # delete old car_center
        self.car_center = canvas.create_bitmap(0, 0) # create new car_center with reset data
        self.canvas.delete(self.car_polygon) # delete old car polygon
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # create new car_polygon with reset data
    
    
    
win_track = tk.Tk()

WIDTH = 800
HEIGHT = 600
canvas = tk.Canvas(win_track, width=WIDTH, height=HEIGHT)
canvas.pack()
tk.Button(win_track, text='enough', command = lambda:win_track.destroy()).pack(expand=True) # close GUI

# construct track
track_coords = [20, 20, 50, 20, 700, 580, 500, 580, 20, 50, 20, 20]
track_polygon = canvas.create_polygon(track_coords, fill="grey", outline="green")

# construct car
# startposition x, startposition y, startangle 
car01 = car(canvas, 140, 100,  0.4, "green")
car02 = car(canvas, 100, 100,  0.6, "blue")
car03 = car(canvas, 110,  90,  0, "orange")
car04 = car(canvas, 120, 100,  1, "black")
car05 = car(canvas, 500, 500,  1.3, "white")
car06 = car(canvas, 500, 500,  1.3, "brown")
car07 = car(canvas, 140, 100,  0.4, "pink")
car08 = car(canvas, 100, 100,  0.6, "olive")
car09 = car(canvas, 110,  90,  0, "cyan")
car10 = car(canvas, 120, 100,  1, "red")
car11 = car(canvas, 500, 500,  1.3, "purple")
car12 = car(canvas, 500, 500,  1.3, "grey")

t0 = t.time()

for i in range(0,200):
#while True:

    car01.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car02.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car03.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car04.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car05.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car06.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car07.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car08.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car09.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car10.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car11.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car12.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi))
    # car01.car_move(1.5,1.8,0.03)
    car02.car_move(1.8,1.5,0.01)
    # car03.car_move(1.5,1.2,-0.01)
    # car04.car_move(1.0,1.5,-0.10)
    # car05.car_move(-0.7,-0.6,0.11)
    # car06.car_move(-0.8,-0.8,0.02)
    # car07.car_move(1.5,1.5,0.00)
    # car08.car_move(1.1,1.2,-0.02)
    # car09.car_move(1.2,1.5,-0.10)
    # car10.car_move(2.8,1.5,0.05)
    # car11.car_move(0.1,-1.2,-0.03)
    # car12.car_move(1.0,1.2,-0.10)
    
    car03.car_rotd(-0.1)
    win_track.update()
    t.sleep(0.01)

#car01.car_pos_reset()
#car02.car_pos_reset()
#car03.car_pos_reset()
#win_track.update()

t1 = t.time()-t0
print("elapsed time [s]: ", t1)  
#win_track.mainloop()


