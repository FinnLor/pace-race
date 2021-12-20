# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021



methoden:
    - set_start_pos:    warum muss set_car_pos zweimal aufgerufen werden? s xxx
    
    - resume_race:      ca auf nächster Spurmitte setzen 
    
    - car_collision:    true zurückgeben wenn??? zB entferntester 
                        carpolygonpunkt weiter weg von Spurmitte
    
    - car_sensor_data:  entfernungen zu den jeweiligen intersection
    
- weitere Sensoren hinzufügen
- anfangsposition setzen können
- maßstabsdefinitionen für weg und zeit
- kollisionsdaten car auslesen
- sensordaten auslesen
- rendering optional einschalten
- Anwendbarkeit von # test_ls = track.simplify(1,True) #  ... abklären (könnte für komplexe polygonlines sehr nützlich sein)





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
    
    def __init__(self,canvas,x,y,psi,delta,FACTOR,SENSFACTOR,color):
        #print("__init__ of car")
        
        self.FACTOR = FACTOR # resizing FACTOR, e.g. FAKTOR=10 => 10pixel==1m
        self.SENSFACT = SENSFACTOR
        self.canvas = canvas
        self.psi = psi # car_angle
        self.delta = delta # front_wheel_angle
        self.color = color 
        self.dc = (0, 0) # velocity of car_center
        self.cl = 4 * self.FACTOR # car length
        self.cw = 2 * self.FACTOR # car WIDTH
        self.c1 = (x-self.cl/2, y+self.cw/2) # create upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # create bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # create bottom right corner of car
        self.c4 = (x+self.cl/1.5, y) # create sensor_center of car
        self.c5 = (x+self.cl/2, y+self.cw/2) # create upper right corner of car
       
        # self.s01 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s02 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s03 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s04 = (self.c4[0], self.c4[1]-self.cw*3/4)
        self.s05 = (self.c4[0]+self.SENSFACT*self.cl, self.c4[1]) # create sensor point no 05
        # self.s06 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s07 = (self.c4[0], self.c4[1]+self.cw*3/4)
        # self.s08 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s09 = (self.c4[0], self.c4[1]+self.cw*3/4)

        self.car_center = canvas.create_bitmap(x, y) # car_center position
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, self.c5, fill = self.color)
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color)
        self._car_rot_d(psi) # call method _car_rot_d
        self._sensor_rot(delta) # call method _sensor_rot


   
    def _car_move_d(self,dx,dy,dpsi): # difference-movement and -rotation
        #print("_car_move_d")
        
        self.dc = (dx, dy) # velocity of car
        self.dpsi = dpsi # angle velocity of car
        self._car_rot_d(dpsi) # let the car rotate with the desired delta-psi
        self.canvas.move(self.sensor05,self.dc[0],self.dc[1])
        self.canvas.move(self.car_center,self.dc[0],self.dc[1]) # move the car_center
        self.canvas.move(self.car_polygon,self.dc[0],self.dc[1]) # move the car_polygon



    def _car_rot_d(self,dpsi): # only _car_rotation difference
        #print("_car_rot_d")

        # RECIEVE CAR POSITION
        c_c      = self.canvas.coords(self.car_center) # extract car_center position data
        c_p      = self.canvas.coords(self.car_polygon) # extract car_polygon position data 
        c_s05    = self.canvas.coords(self.sensor05) # extract sensor05 data
        
        # GET RELATIVE CORNER VECTORS
        cc_c1    = np.array([c_p[0]   - c_c[0],c_p[1]   - c_c[1]]) # vector from car_center to c1
        cc_c2    = np.array([c_p[2]   - c_c[0],c_p[3]   - c_c[1]]) # vector from car_center to c2
        cc_c3    = np.array([c_p[4]   - c_c[0],c_p[5]   - c_c[1]]) # vector from car_center to c3
        cc_c4    = np.array([c_p[6]   - c_c[0],c_p[7]   - c_c[1]]) # vector from car_center to c4 (sensor_center)
        cc_c5    = np.array([c_p[8]   - c_c[0],c_p[9]   - c_c[1]]) # vector from car_center to c5
        cc_s05   = np.array([c_s05[2] - c_c[0],c_s05[3] - c_c[1]]) # vector from car_center to s05
        
        # ROTATE CORNER VECTORS
        rot = np.array([[np.cos(dpsi), np.sin(dpsi)], [-np.sin(dpsi), np.cos(dpsi)]]) # rotation matrix physically correct  
        cc_c1n   = np.dot(rot,  cc_c1) # vector from car_center to rotated c1
        cc_c2n   = np.dot(rot,  cc_c2) # vector from car_center to rotated c2
        cc_c3n   = np.dot(rot,  cc_c3) # vector from car_center to rotated c3
        cc_c4n   = np.dot(rot,  cc_c4) # vector from car_center to rotated c4 (sensor_center)
        cc_c5n   = np.dot(rot,  cc_c5) # vector from car_center to rotated c5
        cc_s05n  = np.dot(rot, cc_s05) # vector from car_center to rotated s05
        
        # SET ABSOLUTE CORNER VECTORS
        self.c1  = (cc_c1n[0]  + c_c[0], cc_c1n[1]  + c_c[1]) # update vector from canvas_GUI to c1
        self.c2  = (cc_c2n[0]  + c_c[0], cc_c2n[1]  + c_c[1]) # update vector from canvas_GUI to c2
        self.c3  = (cc_c3n[0]  + c_c[0], cc_c3n[1]  + c_c[1]) # update vector from canvas_GUI to c3
        self.c4  = (cc_c4n[0]  + c_c[0], cc_c4n[1]  + c_c[1]) # update vector from canvas_GUI to c4 (sensor_center)
        self.c5  = (cc_c5n[0]  + c_c[0], cc_c5n[1]  + c_c[1]) # update vector from canvas_GUI to c5
        self.s05 = (cc_s05n[0] + c_c[0], cc_s05n[1] + c_c[1]) # update vector from canvas_GUI to s05

        # UPDATE OBJECT
        self.canvas.delete(self.sensor05) # delete old sensor
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.car_polygon) # delete old car
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, self.c5, fill = self.color) # set new, rotated car
    
    
    
    def _car_rot(self,psi): # only rotation
        #print("_car_rot")
        
        # SET CAR HORIZONTALLY
        c_c = self.canvas.coords(self.car_center) # extract car_center position data
        self.c1  = (c_c[0]-self.cl/2,   c_c[1]+self.cw/2) # set upper left corner of car
        self.c2  = (c_c[0]-self.cl/2,   c_c[1]-self.cw/2) # set bottom left corner of car
        self.c3  = (c_c[0]+self.cl/2,   c_c[1]-self.cw/2) # set bottom right corner of car
        self.c4  = (c_c[0]+self.cl/1.5, c_c[1]) # set sensor center of car
        self.c5  = (c_c[0]+self.cl/2,   c_c[1]+self.cw/2) # set upper right corner of car
        self.s05 = (self.c4[0]+self.SENSFACT*self.cl, self.c4[1]) # set sensor point no 05
        
        # GET RELATIVE CORNER VECTORS
        cc_c1    = np.array([self.c1[0]  - c_c[0],self.c1[1]  - c_c[1]]) # vector from car_center to c1
        cc_c2    = np.array([self.c2[0]  - c_c[0],self.c2[1]  - c_c[1]]) # vector from car_center to c2
        cc_c3    = np.array([self.c3[0]  - c_c[0],self.c3[1]  - c_c[1]]) # vector from car_center to c3
        cc_c4    = np.array([self.c4[0]  - c_c[0],self.c4[1]  - c_c[1]]) # vector from car_center to c4 (sensor_center)
        cc_c5    = np.array([self.c5[0]  - c_c[0],self.c5[1]  - c_c[1]]) # vector from car_center to c5
        cc_s05   = np.array([self.s05[0] - c_c[0],self.s05[1] - c_c[1]]) # vector from car_center to s05
        
        # ROTATE RELATIVE CORNER VECTORS
        rot = np.array([[np.cos(psi), np.sin(psi)], [-np.sin(psi), np.cos(psi)]]) # rotation matrix physically correct  
        cc_c1n   = np.dot(rot,  cc_c1) # vector from car_center to rotated c1
        cc_c2n   = np.dot(rot,  cc_c2) # vector from car_center to rotated c2
        cc_c3n   = np.dot(rot,  cc_c3) # vector from car_center to rotated c3
        cc_c4n   = np.dot(rot,  cc_c4) # vector from car_center to rotated c4
        cc_c5n   = np.dot(rot,  cc_c5) # vector from car_center to rotated c4
        cc_s05n  = np.dot(rot, cc_s05) # vector from car_center to rotated s05
        
        # SET ABSOLUTE CORNER VECTORS
        self.c1  = (cc_c1n[0]  + c_c[0], cc_c1n[1]  + c_c[1]) # update vector from canvas_GUI to c1
        self.c2  = (cc_c2n[0]  + c_c[0], cc_c2n[1]  + c_c[1]) # update vector from canvas_GUI to c2
        self.c3  = (cc_c3n[0]  + c_c[0], cc_c3n[1]  + c_c[1]) # update vector from canvas_GUI to c3
        self.c4  = (cc_c4n[0]  + c_c[0], cc_c4n[1]  + c_c[1]) # update vector from canvas_GUI to c4
        self.c5  = (cc_c5n[0]  + c_c[0], cc_c5n[1]  + c_c[1]) # update vector from canvas_GUI to c4
        self.s05 = (cc_s05n[0] + c_c[0], cc_s05n[1] + c_c[1]) # update vector from canvas_GUI to s05
        
        # UPDATE OBJECT
        self.canvas.delete(self.sensor05) # delete old sensor
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.car_polygon) # delete old car
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # set new, rotated car



    def _sensor_rot(self,delta):
        # print("_sensor_rot")
        
        # generate relative horizontal sensor vectors
        s05_h_r = (self.SENSFACT*self.cl, 0) # sensor s05 horizontal and relative to sensor_center

        # rotate sensor vectors
        deltapsi = delta + self.psi
        rot = np.array([[np.cos(deltapsi), np.sin(deltapsi)], [-np.sin(deltapsi), np.cos(deltapsi)]]) # rotation matrix physically correct  
        cc_s05n = np.dot(rot, s05_h_r)

        # set absolute sensor vectors
        self.s05 = (cc_s05n[0] + self.c4[0], cc_s05n[1] + self.c4[1]) # update vector from canvas_GUI to s05
        
        # update object
        self.canvas.delete(self.sensor05) # delete old sensor
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor-line
    
    
    
    def set_car_pos(self,x,y,psi,delta): # set new car postion and angles (with zero velocities)
        #print("set_car_pos")
        
        self.psi = psi # car_angle
        self.delta = delta  # front_wheel_angle
        self.dc = (0, 0) # velocity of car
        self.dpsi = 0 # velocity of car_angle
        self.c1 = (x-self.cl/2, y+self.cw/2) # upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # bottom right corner of car
        self.c4 = (x+self.cl/1.5, y) # sensor_center of car
        self.c5 = (x+self.cl/2, y+self.cw/2) # upper right corner of car
        self.s05 = (self.c4[0]+self.SENSFACT*self.cl, self.c4[1]) # create sensor point no 05
        self._car_rot(psi) # call method _car_rot
        self._sensor_rot(delta) # call method _sensor_rot
        self.canvas.delete(self.car_center) # delete old car_center
        self.car_center = canvas.create_bitmap(x, y)
        #self.canvas.delete(self.sensor05) # delete old sensor
        #self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.car_polygon) # delete old car polygon
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, self.c5, fill = self.color) # set new, rotated car

    

    def get_car_polygon(self):
        
        car_polygon = self.canvas.coords(self.car_polygon) # extract car_polygon position data 
        return car_polygon
    
    
    
    def get_car_center(self):
        
        car_center = self.canvas.coords(self.car_center) # extract car_center position data
        return car_center
      
        
      
    def set_start_pos(self,road_data):
        self.delta = 0  # front_wheel_angle
        
        rd = np.array(road_data)
        size = np.shape(rd)[0]
        rs = np.reshape(road_data,(int(0.5*size),2))

        v_start = rs[1,:] - rs[0,:]
        x = road_data[0]
        y = road_data[1]
        v_x = np.array([10, 0])
        psi = np.arccos(np.dot(v_start,v_x)/(np.linalg.norm(v_start)*np.linalg.norm(v_x)))

        print("xxx hier weiter")
        print(x)
        print(y)
        self.set_car_pos(x,y,psi,0)
        self.set_car_pos(x,y,psi,0)
        
        
    def car_pos_reset(self): # reset car position

        self.dc = (0, 0) # velocity of car
        self.dpsi = 0 # velocity of car_angle
        self.psi = 0 # car_angle
        self.c1  = (-self.cl/2,   self.cw/2) # upper left corner of car
        self.c2  = (-self.cl/2,  -self.cw/2) # bottom left corner of car
        self.c3  = ( self.cl/2,  -self.cw/2) # bottom right corner of car
        self.c4  = ( self.cl/1.5,  0) # light_center of car
        self.c5  = ( self.cl/2,   self.cw/2) # upper right corner of car
        self.s05 = ( self.c4[0]+5*self.cl, self.c4[1]) # create sensor point no 05
        self.canvas.delete(self.car_center) # delete old car_center
        self.car_center = canvas.create_bitmap(0, 0) # create new car_center with reset data
        self.canvas.delete(self.sensor05) # delete old sensor
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.car_polygon) # delete old car polygon
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, self.c5, fill = self.color) # create new car_polygon with reset data
    
    
    
    
    
    
class road:
    
    def __init__(self,canvas,FACTOR,WIDTH,HEIGHT,NPOINTS, ROADWIDTH):
        #print("__init__ of road")

        self.FACTOR = FACTOR # dimension, e.g. FAKTOR=10 => 10pixel==1m
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.NPOINTS = NPOINTS
        self.rw = ROADWIDTH
        self.canvas = canvas
        
        # GENERATE ROAD DATA
        n = np.linspace(0.5, 2*m.pi, self.NPOINTS)
        x = m.pow((-1),rnd.randrange(1,3,1)) * (n + 3*rnd.uniform(0,1)*np.tan(0.2*n))
        y = 1./n + rnd.uniform(0,1)*3.*np.cos(n)*np.power(np.sin(n),2)

        # ALIGN ROAD
        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        w_scale = self.WIDTH - 40
        h_scale = self.HEIGHT - 40
        x = w_scale/(x_max - x_min) * (x-x_min)
        y = h_scale/(y_max - y_min) * (y-y_min)
        h_diff = self.WIDTH - (max(x)-min(x))
        v_diff = self.HEIGHT - (max(y)-min(y))
        x = x + h_diff/2
        y = y + v_diff/2
                
        # GENERATE ROAD AND BORDER    
        line_data  = list((np.ravel(([x,y]),'F'))) # list is neccessary for a correct separation with comma
        road_center_ls = LineString(np.reshape(line_data,(self.NPOINTS,2)))
        road_right_line1 = np.array(road_center_ls.parallel_offset(self.FACTOR*self.rw/2,"right",join_style=1))
        road_right_line = list((np.ravel(([road_right_line1[:,0],road_right_line1[:,1]]),'F')))
        road_left_line1 = np.array(road_center_ls.parallel_offset(self.FACTOR*self.rw/2,"left",join_style=1))
        road_left_line = list((np.ravel(([road_left_line1[:,0],road_left_line1[:,1]]),'F')))
        
        # ASSIGN ROADS TO OBJECT
        self.road_center_line = canvas.create_line(line_data, dash = (4), fill = "grey")
        self.road_right_line   = canvas.create_line(road_right_line, fill = "brown")
        self.road_left_line   = canvas.create_line(road_left_line, fill = "brown")
        


    def get_road_line(self):
        # print ("get_road_line")
        
        road_centerline = self.canvas.coords(self.road_center_line) # extract car_center position data
        return road_centerline
 


#################################
### ENVIRONMENT COMMUNICATION ###
#################################

### CONFIGURE GUI
win_env = tk.Tk() # window for canvas-rendering of the environment
WIDTH = 1800
HEIGHT = 900
NPOINTS = 1000
ROADWIDTH = 8
FACTOR = 5 # resizing FACTOR, e.g. FAKTOR=10 => 10pixel==1m
SENSFACTOR = 7
canvas = tk.Canvas(win_env, width=WIDTH, height=HEIGHT)
canvas.pack()
tk.Button(win_env, text='enough', command = lambda:win_env.destroy()).pack(expand=True) # close GUI

### CONSTRUCT ROAD
c_road = road(canvas,FACTOR,WIDTH,HEIGHT,NPOINTS, ROADWIDTH)

### CONSTRUCT CAR
# startposition x, startposition y, startangle 
car01 = car(canvas, 140, 100,  0.4, 0.4, FACTOR, SENSFACTOR, "purple")
car02 = car(canvas, 100, 200,  0.6, -0.6, FACTOR, SENSFACTOR, "green")
car03 = car(canvas, 110,  90,    0,   0, FACTOR, SENSFACTOR, "orange")
car04 = car(canvas, 120, 100,    1,   1, FACTOR, SENSFACTOR, "black")
car05 = car(canvas, 500, 400,  1.3, 1.3, FACTOR, SENSFACTOR, "white")
car06 = car(canvas, 300, 500,  1.3, -1.3, FACTOR, SENSFACTOR, "brown")
car07 = car(canvas, 140,  10,  0.4, -0.4, FACTOR, SENSFACTOR, "yellow")
car08 = car(canvas, 150,  50,  0.6, 0.6, FACTOR, SENSFACTOR, "olive")
car09 = car(canvas, 110,  90,    0,   0, FACTOR, SENSFACTOR, "cyan")
car10 = car(canvas, 120, 100,    1,   1, FACTOR, SENSFACTOR, "red")
car11 = car(canvas, 200, 300,  1.3, -1.3, FACTOR, SENSFACTOR, "pink")
car12 = car(canvas, 200, 500,  1.3, 1.3, FACTOR, SENSFACTOR, "blue")
     
### PREPARE ROAD FOR DISTANCE-MEASURE
print("xxx hier weiter")
road_centerline = c_road.get_road_line()
road_data = np.reshape(road_centerline, (NPOINTS,2))
t_data = LineString(road_data)

t0 = t.time()

### TESTS
# test with moving and rendering of roads, cars and sensors
for i in range(0,100):
#while True:

    ### PREPARE CARS FOR DISTANCE-MEASURE
    car01_polygon  = car01.get_car_polygon()
    car01_data = np.reshape(car01_polygon, (5,2))
    c01_data = Polygon(car01_data) #
    dist_car01_road = t_data.distance(c01_data)
    
    car02_polygon  = car02.get_car_polygon()
    car02_data = np.reshape(car02_polygon, (5,2))
    c02_data = Polygon(car02_data) #
    dist_car02_road = t_data.distance(c02_data)
    # print("Distance blue car - road")
    # print(dist_car02_road)
    
    car03_polygon  = car03.get_car_polygon()
    car03_data = np.reshape(car03_polygon, (5,2))
    c03_data = Polygon(car03_data) #
    dist_car03_road = t_data.distance(c03_data)
    
    car04_polygon  = car04.get_car_polygon()
    car04_data = np.reshape(car04_polygon, (5,2))
    c04_data = Polygon(car04_data) #
    dist_car04_road = t_data.distance(c04_data)
    
    car05_polygon  = car05.get_car_polygon()
    car05_data = np.reshape(car05_polygon, (5,2))
    c05_data = Polygon(car05_data) #
    dist_car05_road = t_data.distance(c05_data)
    
    car06_polygon  = car06.get_car_polygon()
    car06_data = np.reshape(car06_polygon, (5,2))
    c06_data = Polygon(car06_data) #
    dist_car06_road = t_data.distance(c06_data)
    
    car07_polygon  = car07.get_car_polygon()
    car07_data = np.reshape(car07_polygon, (5,2))
    c07_data = Polygon(car07_data) #
    dist_car07_road = t_data.distance(c07_data)
    
    car08_polygon  = car08.get_car_polygon()
    car08_data = np.reshape(car08_polygon, (5,2))
    c08_data = Polygon(car08_data) #
    dist_car08_road = t_data.distance(c08_data)
    
    car09_polygon  = car09.get_car_polygon()
    car09_data = np.reshape(car09_polygon, (5,2))
    c09_data = Polygon(car09_data) #
    dist_car09_road = t_data.distance(c09_data)
    
    car10_polygon  = car10.get_car_polygon()
    car10_data = np.reshape(car10_polygon, (5,2))
    c10_data = Polygon(car10_data) #
    dist_car10_road = t_data.distance(c10_data)
    
    car11_polygon  = car11.get_car_polygon()
    car11_data = np.reshape(car11_polygon, (5,2))
    c11_data = Polygon(car11_data) #
    dist_car11_road = t_data.distance(c11_data)
    
    car12_polygon  = car12.get_car_polygon()
    car12_data = np.reshape(car12_polygon, (5,2))
    c12_data = Polygon(car12_data) #
    dist_car12_road = t_data.distance(c12_data)

    car01.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car02.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car03.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car04.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car05.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car06.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car07.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car08.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car09.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car10.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car11.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car12.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))
    # car01._car_move_d(1.5,1.8,0.03)
    #car02._car_move_d(1.8,1.5,0.01)
    car03._car_move_d(1.5,1.2,-0.01)
    car04._car_move_d(1.0,1.5,-0.10)
    car05._car_move_d(-0.7,-0.6,0.11)
    car06._car_move_d(-0.8,-0.8,0.02)
    car07._car_move_d(1.5,1.5,0.00)
    car08._car_move_d(1.1,1.2,-0.02)
    car09._car_move_d(1.2,1.5,-0.10)
    car10._car_move_d(2.8,1.5,0.05)
    car11._car_move_d(0.1,-1.2,-0.03)
    car12._car_move_d(1.0,1.2,-0.10)
    
    car02._sensor_rot(-0.7+i/100)
    
    car03._car_rot_d(-0.1)
    
    win_env.update()
    t.sleep(0.005)

car01.set_start_pos(c_road.get_road_line())
car02.set_start_pos(c_road.get_road_line())
car03.set_start_pos(c_road.get_road_line())
car04.set_start_pos(c_road.get_road_line())
car05.set_start_pos(c_road.get_road_line())
car06.set_start_pos(c_road.get_road_line())
car07.set_start_pos(c_road.get_road_line())
car08.set_start_pos(c_road.get_road_line())
car09.set_start_pos(c_road.get_road_line())
car10.set_start_pos(c_road.get_road_line())
car11.set_start_pos(c_road.get_road_line())
car12.set_start_pos(c_road.get_road_line())

car01.car_pos_reset()
#car02.car_pos_reset()
#car03.car_pos_reset()
win_env.update()

t1 = t.time()-t0
print("elapsed time [s]: ", t1)  
win_env.mainloop() # only nessecary for refreshing window


