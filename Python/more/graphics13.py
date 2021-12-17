# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

@author: em, fl, fs
"""

import numpy as np
import math as m
import time as t
import tkinter as tk
import shapely as sh
import random as rnd
import matplotlib.pyplot as plt
from shapely.geometry import box, Polygon, LineString # Object 'box' could be more effective?
from shapely.validation import explain_validity



class car:
    
    def __init__(self,canvas,x,y,psi,factor,color):
        #print("___init__ of car")
        
        self.factor = factor # resizing factor, e.g. FAKTOR=10 => 10pixel==1m
        self.canvas = canvas
        self.psi = psi # car_angle
        self.delta = 0 # car_front_wheel_angle
        self.color = color 
        self.dc = (0, 0) # velocity of car_center
        self.cl = 4 * self.factor # car length
        self.cw = 2 * self.factor # car width
        self.c1 = (x-self.cl/2, y+self.cw/2) # create upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # create bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # create bottom right corner of car
        self.c4 = (x+self.cl/2, y+self.cw/2) # create upper right corner of car
        
        self.car_center = canvas.create_bitmap(x, y) # car_center position
        self.light_center = canvas.create_bitmap(x+self.cl/2, y) # light_center_position
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color)
        self.car_rot_d(psi) # call method car_rot_d


   
    def car_move_d(self,dx,dy,dpsi): # difference-movement and -rotation
        #print("car_move_d")
        
        self.dc = (dx, dy) # velocity of car
        self.dpsi = dpsi # angle velocity of car
        self.car_rot_d(dpsi) # let the car rotate with the desired delta-psi
        self.canvas.move(self.car_center,self.dc[0],self.dc[1]) # move the car_center
        self.canvas.move(self.car_polygon,self.dc[0],self.dc[1]) # move the car_polygon



    def car_rot_d(self,dpsi): # only rotation difference
        #print("car_rot_d")
        
        rot = np.array([[np.cos(dpsi), np.sin(dpsi)], [-np.sin(dpsi), np.cos(dpsi)]]) # rotation matrix physically correct  

        c_c = self.canvas.coords(self.car_center) # extract car_center position data
        l_c = self.canvas.coords(self.light_center) # extract light_center data
        c_p = self.canvas.coords(self.car_polygon) # extract car_polygon position data 
        
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

    

    def get_car_polygon(self):
        # print ("get_car_polygon")
        
        car_polygon = self.canvas.coords(self.car_polygon) # extract car_polygon position data 
        return car_polygon
    
    
    
    def get_car_center(self):
        # print ("get_car_center")
        
        car_center = self.canvas.coords(self.car_center) # extract car_center position data
        return car_center
        
        
        
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
    
    
    
    
    
    
class track:
    
    def __init__(self,canvas,FACTOR,WIDTH,HEIGHT,NPOINTS):
        #print("__init__ of track")

        self.factor = FACTOR # dimension, e.g. FAKTOR=10 => 10pixel==1m
        self.width = WIDTH
        self.height = HEIGHT
        self.npoints = NPOINTS
        self.canvas = canvas
        
        # generate track_data
        n = np.linspace(0.5, 2*m.pi, self.npoints)
        x = m.pow((-1),rnd.randrange(1,3,1)) * (n + 3*rnd.uniform(0,1)*np.tan(0.2*n))
        y = 1./n + rnd.uniform(0,1)*3.*np.cos(n)*np.power(np.sin(n),2)

        # align track
        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        w_scale = self.width - 40
        h_scale = self.height - 40
        x = w_scale/(x_max - x_min) * (x-x_min)
        y = h_scale/(y_max - y_min) * (y-y_min)
        h_diff = self.width - (max(x)-min(x))
        v_diff = self.height - (max(y)-min(y))
        x = x + h_diff/2
        y = y + v_diff/2
        
        # generate track
        line_data1 = (np.ravel(([x,y]),'F')) # test = np.vstack((xc,yc)).ravel('F')
        line_data  = list(line_data1) # neccessary for the correct separation with comma
        self.track_line = canvas.create_line(line_data)
        

    def get_track_polyline(self):
        # print ("get_track_polyline")
        
        
        self.track_line
        
        track_polyline = self.canvas.coords(self.track_line) # extract car_center position data
        return track_polyline
 
    
        #track_data = self.track_line
        #track_line = LineString(track_data)
        #car_line = car.canvas.coo
        #car_data = car.
        #dist = track.distance(car_line)




#################################
### ENVIRONMENT COMMUNICATION ###
#################################

### CONFIGURE GUI
win_env = tk.Tk() # window for canvas-rendering of the environment
WIDTH = 1800
HEIGHT = 900
NPOINTS = 1000
FACTOR = 3 # resizing factor, e.g. FAKTOR=10 => 10pixel==1m
canvas = tk.Canvas(win_env, width=WIDTH, height=HEIGHT)
canvas.pack()
tk.Button(win_env, text='enough', command = lambda:win_env.destroy()).pack(expand=True) # close GUI

### CONSTRUCT TRACK
c_track = track(canvas,FACTOR,WIDTH,HEIGHT,NPOINTS)

### CONSTRUCT CAR
# startposition x, startposition y, startangle 
car01 = car(canvas, 140, 100,  0.4, FACTOR, "green")
car02 = car(canvas, 100, 200,  0.6, FACTOR, "blue")
car03 = car(canvas, 110,  90,    0, FACTOR, "orange")
car04 = car(canvas, 120, 100,    1, FACTOR, "black")
car05 = car(canvas, 500, 400,  1.3, FACTOR, "white")
car06 = car(canvas, 300, 500,  1.3, FACTOR, "brown")
car07 = car(canvas, 140,  10,  0.4, FACTOR, "yellow")
car08 = car(canvas, 150,  50,  0.6, FACTOR, "olive")
car09 = car(canvas, 110,  90,    0, FACTOR, "cyan")
car10 = car(canvas, 120, 100,    1, FACTOR, "red")
car11 = car(canvas, 200, 300,  1.3, FACTOR, "purple")
car12 = car(canvas, 200, 500,  1.3, FACTOR, "pink")
     
### PREPARE TRACK FOR DISTANCE-MEASURE
track_polyline = c_track.get_track_polyline()
track_data = np.reshape(track_polyline, (NPOINTS,2))
t_data = LineString(track_data)

t0 = t.time()

### TESTS
# test with moving and rendering of tracks, cars and sensors
for i in range(0,100):
#while True:

    ### PREPARE CARS FOR DISTANCE-MEASURE
    car01_polygon  = car01.get_car_polygon()
    car01_data = np.reshape(car01_polygon, (4,2))
    c01_data = Polygon(car01_data) #
    dist_car01_track = t_data.distance(c01_data)
    
    car02_polygon  = car02.get_car_polygon()
    car02_data = np.reshape(car02_polygon, (4,2))
    c02_data = Polygon(car02_data) #
    dist_car02_track = t_data.distance(c02_data)
    # print("Distance blue car - track")
    # print(dist_car02_track)
    
    car03_polygon  = car03.get_car_polygon()
    car03_data = np.reshape(car03_polygon, (4,2))
    c03_data = Polygon(car03_data) #
    dist_car03_track = t_data.distance(c03_data)
    
    car04_polygon  = car04.get_car_polygon()
    car04_data = np.reshape(car04_polygon, (4,2))
    c04_data = Polygon(car04_data) #
    dist_car04_track = t_data.distance(c04_data)
    
    car05_polygon  = car05.get_car_polygon()
    car05_data = np.reshape(car05_polygon, (4,2))
    c05_data = Polygon(car05_data) #
    dist_car05_track = t_data.distance(c05_data)
    
    car06_polygon  = car06.get_car_polygon()
    car06_data = np.reshape(car06_polygon, (4,2))
    c06_data = Polygon(car06_data) #
    dist_car06_track = t_data.distance(c06_data)
    
    car07_polygon  = car07.get_car_polygon()
    car07_data = np.reshape(car07_polygon, (4,2))
    c07_data = Polygon(car07_data) #
    dist_car07_track = t_data.distance(c07_data)
    
    car08_polygon  = car08.get_car_polygon()
    car08_data = np.reshape(car08_polygon, (4,2))
    c08_data = Polygon(car08_data) #
    dist_car08_track = t_data.distance(c08_data)
    
    car09_polygon  = car09.get_car_polygon()
    car09_data = np.reshape(car09_polygon, (4,2))
    c09_data = Polygon(car09_data) #
    dist_car09_track = t_data.distance(c09_data)
    
    car10_polygon  = car10.get_car_polygon()
    car10_data = np.reshape(car10_polygon, (4,2))
    c10_data = Polygon(car10_data) #
    dist_car10_track = t_data.distance(c10_data)
    
    car11_polygon  = car11.get_car_polygon()
    car11_data = np.reshape(car11_polygon, (4,2))
    c11_data = Polygon(car11_data) #
    dist_car11_track = t_data.distance(c11_data)
    
    car12_polygon  = car12.get_car_polygon()
    car12_data = np.reshape(car12_polygon, (4,2))
    c12_data = Polygon(car12_data) #
    dist_car12_track = t_data.distance(c12_data)

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
    # car01.car_move_d(1.5,1.8,0.03)
    car02.car_move_d(1.8,1.5,0.01)
    car03.car_move_d(1.5,1.2,-0.01)
    car04.car_move_d(1.0,1.5,-0.10)
    car05.car_move_d(-0.7,-0.6,0.11)
    car06.car_move_d(-0.8,-0.8,0.02)
    car07.car_move_d(1.5,1.5,0.00)
    car08.car_move_d(1.1,1.2,-0.02)
    car09.car_move_d(1.2,1.5,-0.10)
    car10.car_move_d(2.8,1.5,0.05)
    car11.car_move_d(0.1,-1.2,-0.03)
    car12.car_move_d(1.0,1.2,-0.10)
    
    car03.car_rot_d(-0.1)
    win_env.update()
    t.sleep(0.001)
    #print(i)

#car01.car_pos_reset()
#car02.car_pos_reset()
#car03.car_pos_reset()
#win_env.update()

t1 = t.time()-t0
print("elapsed time [s]: ", t1)  
win_env.mainloop() # only nessecary for refreshing window


