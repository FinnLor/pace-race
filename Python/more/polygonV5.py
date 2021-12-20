# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 12:32:03 2021

@author: em, fl, fs
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
car1_c = [82.5, 33.75] # car1 center
car2_data = np.array([[48, 32.5], [53, 32.5], [53,35], [48,35]]) # fine
car3_data = np.array([[42, 40.5], [47, 40.5], [47,43], [42,43]]) # out (due to distance)
car4_data = np.array([[30, 5], [35, 5], [35,7.5], [30,7.5]]) # out (due to distance)
car1_ls = LineString(car1_data)
car2_ls = LineString(car2_data)
car3_ls = LineString(car3_data)
car4_ls = LineString(car4_data)



# return start position for the car
s_vec = road_data_center[1,:]-road_data_center[0,:]
x_vec = np.array([10, 0])
angle = np.arccos(np.dot(s_vec,x_vec)/(np.linalg.norm(s_vec)*np.linalg.norm(x_vec)))



# return the resumed (nearest middle of track) car position and angle (x, y, psi, (delta=0))
c_c = Point(car1_c)
#c_c_dm = c_c.distance(road_lsc)
c_c_dl = c_c.distance(road_lsl)
c_c_dr = c_c.distance(road_lsr)
print("Abstände")
#print(c_c_dm)
print(c_c_dl)
print(c_c_dr)
pathlength = road_lsc.project(c_c,normalized = False) # return pathlength from polyline-start to shortest point-distance
point_on_line = np.array(road_lsc.interpolate(pathlength).coords) # get coordinates for pathlength

# xxx todo pseudocode:
# if distance_car left_border < distance_car right_border
#   turn vector (c_c - point_on_line) pi/2-wise negative
# elseif distance_car left_border > distance_car right_border
#   turn vector (c_c - Point_on_line) pi/2-wise positive
# else
#   print("Car position is not valid or street is too small.")



# return True if the car did violate a BORDER (as an offest from central polyline!)
c_p1 = Point(car_data[0,:])
c_p2 = Point(car_data[1,:])
c_p3 = Point(car_data[2,:])
c_p4 = Point(car_data[3,:])
c_p1_d = c_p1.distance(road_lsc)
c_p2_d = c_p2.distance(road_lsc)
c_p3_d = c_p3.distance(road_lsc)
c_p4_d = c_p4.distance(road_lsc)
c_maxdist = max(c_p1_d, c_p2_d, c_p3_d, c_p4_d)
if c_maxdist > BORDER:
    print("car.is.OUT!")
else:
    print("go go go")



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
plt.plot(border_data_left[:,0], border_data_left[:,1])
plt.plot(border_data_right[:,0], border_data_right[:,1])
plt.scatter(point_on_line[0,0],point_on_line[0,1])
plt.scatter(car1_c[0], car1_c[1])


