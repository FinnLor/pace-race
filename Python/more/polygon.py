# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 12:32:03 2021

@author: em, fl, fs

Testfunktion in vereinfachter Umgebung

"""

import numpy as np
import math as m
import time as t
import tkinter as tk
import random as rnd
import shapely as sh
import matplotlib.pyplot as plt
from shapely.geometry import box, Polygon, LineString, Point
from shapely.validation import explain_validity
from shapely.ops import nearest_points

t0 = t.time()



# initialize road
BORDER = 5
road_data_small= np.array([[30, 10], [60, 5], [80, 15], [90,30], [70,45], [35,25], [35,45]])
# road_data_big = np.array([[x, y] for x,y in zip(range(34,-5100,-1), range(26,5160,+1))])
# road_data = np.append(road_data_small, road_data_big, axis=0)
road_data_center  = road_data_small
road_lsc  = LineString(road_data_center)
border_data_left  = np.array(road_lsc.parallel_offset(BORDER,"left",join_style=1))
road_lsl  = LineString(border_data_left)
border_data_right = np.array(road_lsc.parallel_offset(BORDER,"right",join_style=1))
road_lsr  = LineString(border_data_right)



# initialize cars
car_data = np.array([[42, 40.5], [47, 40.5], [47,43], [42,43]]) # out (due to distance)
car1_data = np.array([[80, 32.5], [85, 32.5], [85,35], [80,35]]) # out (due to collision)
car1_c = [30.5, 47.75] # car1 center
car2_data = np.array([[48, 32.5], [53, 32.5], [53,35], [48,35]]) # fine
car3_data = np.array([[42, 40.5], [47, 40.5], [47,43], [42,43]]) # out (due to distance)
car4_data = np.array([[30, 5], [35, 5], [35,7.5], [30,7.5]]) # out (due to distance)
car1_ls = LineString(car1_data)
car2_ls = LineString(car2_data)
car3_ls = LineString(car3_data)
car4_ls = LineString(car4_data)



### SENSOR 1
# initialize sensor
l1 = np.array([[97, 30],[25, 43]])
ref_p = Point(l1[0,:]) # Reference point, source of all Sensor_lines
l1_p = Point(l1[1,:]) # Outer sensor point
l1_ls = LineString(l1)
isp_l = np.array(l1_ls.intersection(road_lsl)) # absolute position of intersection point(s) of sensor with left BORDER
isp_r = np.array(l1_ls.intersection(road_lsr)) # absolute position of intersection point(s) of sensor with right BORDER

# collect all distances for sensor 1
distances1_l = []
distances1_r = []
if isp_l.ndim == 2:
    for i in range(0,isp_l.shape[0]): # if there are more than one intersections with left BORDER
       distances1_l.append(ref_p.distance(Point(isp_l[i,:])))
    dist1_l = min(distances1_l)
else:
    if len(isp_l)==0: # if there is no intersection with left BORDER
        dist1_l = ref_p.distance(l1_p)
    else:
        dist1_l = ref_p.distance(Point(isp_l)) # if there is one intersection with left BORDER
if isp_r.ndim == 2:
    for i in range(0,isp_r.shape[0]): # if there are more than one intersections with right BORDER
       distances1_r.append(ref_p.distance(Point(isp_r[i,:])))
    dist1_r = min(distances1_r)
else:
    if len(isp_r)==0: # if there is no intersection with right BORDER
        dist1_r = ref_p.distance(l1_p)
    else:
        dist1_r = ref_p.distance(Point(isp_r)) # if there is one intersection with left BORDER
distances = np.array([dist1_l, dist1_r]) # distance to left, right border



# return start position for the car
s_vec = road_data_center[1,:]-road_data_center[0,:]
x_vec = np.array([10, 0])
angle = np.arccos(np.dot(s_vec,x_vec)/(np.linalg.norm(s_vec)*np.linalg.norm(x_vec)))



# return the resumed (nearest middle of track) car position and angle (x, y, psi, (delta=0))
c_c = Point(car1_c)
#c_c_dm = c_c.distance(road_lsc)
c_c_dl = c_c.distance(road_lsl)
c_c_dr = c_c.distance(road_lsr)
pathlength = road_lsc.project(c_c,normalized = False) # return pathlength from polyline-start to shortest point-distance
point_on_line = np.array(road_lsc.interpolate(pathlength)) # get coordinates for pathlength
if c_c_dl >c_c_dr:
    rot = np.array([[np.cos(m.pi/2), -np.sin(m.pi/2)], [np.sin(m.pi/2), np.cos(m.pi/2)]]) # rotation matrix clockwise 
elif c_c_dl < c_c_dr:
    rot = np.array([[np.cos(m.pi/2), np.sin(m.pi/2)], [-np.sin(m.pi/2), np.cos(m.pi/2)]]) # rotation matrix counter-clockwise 
else:
    print("testNIE")



c_c_np = np.array(c_c)
v_forward = np.dot(rot,  (c_c_np - point_on_line)) # get forward-direction
v_x = np.array([10, 0])
psi_forward = np.arccos(np.dot(v_forward,v_x)/(np.linalg.norm(v_forward)*np.linalg.norm(v_x)))
delta = 0
#set_car_pos(point_on_line[0],point_on_line[1],psi_forward,delta) # oder so ähnliches muss aufgerufen werden



path_length = road_lsc.project(c_c,normalized = True)
print("c_c ", c_c)
print("Path length ", path_length)



# return True if the car did violate a BORDER (as an offest from central polyline!)
c_p1 = Point(car1_data[0,:])
c_p2 = Point(car1_data[1,:])
c_p3 = Point(car1_data[2,:])
c_p4 = Point(car1_data[3,:])
c_p1_d = c_p1.distance(road_lsc)
c_p2_d = c_p2.distance(road_lsc)
c_p3_d = c_p3.distance(road_lsc)
c_p4_d = c_p4.distance(road_lsc)
c_maxdist = max(c_p1_d, c_p2_d, c_p3_d, c_p4_d)
if c_maxdist > BORDER:
    what = True
else:
    what = False
    
    
    
# measure time needed
t1 = t.time()-t0
print("elapsed time [s]: ", t1)



# plot data
plt.plot(road_data_center[:,0],road_data_center[:,1])
plt.plot(car_data[:,0],car_data[:,1])
plt.plot(car1_data[:,0],car1_data[:,1])
plt.plot(car2_data[:,0],car2_data[:,1])
plt.plot(car3_data[:,0],car3_data[:,1])
plt.plot(car4_data[:,0],car4_data[:,1])
plt.plot(l1[:,0],l1[:,1])
plt.plot(border_data_left[:,0], border_data_left[:,1])
plt.plot(border_data_right[:,0], border_data_right[:,1])
plt.scatter(point_on_line[0],point_on_line[1])
plt.scatter(v_forward[0] + point_on_line[0], v_forward[1] + point_on_line[1])
plt.scatter(car1_c[0], car1_c[1])


