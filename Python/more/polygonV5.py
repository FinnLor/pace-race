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

t0 = t.time()

road_data_small= np.array([[30, 10], [60, 5], [80, 15], [90,30], [70,45], [35,25], [35,45]])
# road_data_big = np.array([[x, y] for x,y in zip(range(34,-5100,-1), range(26,5160,+1))])
# road_data = np.append(road_data_small, road_data_big, axis=0)
road_data = road_data_small

road_ls = LineString(road_data)

car1_data = np.array([[80, 22.5], [85, 22.5], [85,25], [80,25]]) # out (due to collision)
car2_data = np.array([[48, 32.5], [53, 32.5], [53,35], [48,35]]) # fine
car3_data = np.array([[42, 42.5], [47, 42.5], [47,45], [42,45]]) # out (due to distance)
car1_ls = LineString(car1_data)
car2_ls = LineString(car2_data)
car3_ls = LineString(car3_data)

BORDER = 5
border_data_left = np.array(road_ls.parallel_offset(BORDER,"left",join_style=1))
border_data_right = np.array(road_ls.parallel_offset(BORDER,"right",join_style=1))

s_vec = road_data[1,:]-road_data[0,:]
x_vec = np.array([10, 0])
angle = np.arccos(np.dot(s_vec,x_vec)/(np.linalg.norm(s_vec)*np.linalg.norm(x_vec)))
# print(p_start)
# print(xv)
# print(angle)

#for i in range(0,100):
# dist1 = car1_ls.distance(road_ls) # 
# print(dist1)

c1_p1 = Point(car1_data[0,:])
c1_p2 = Point(car1_data[1,:])
c1_p3 = Point(car1_data[2,:])
c1_p4 = Point(car1_data[3,:])
c1_p1_d = c1_p1.distance(road_ls)
c1_p2_d = c1_p2.distance(road_ls)
c1_p3_d = c1_p3.distance(road_ls)
c1_p4_d = c1_p4.distance(road_ls)
c1_maxdist = max(c1_p1_d, c1_p2_d, c1_p3_d, c1_p4_d)
if c1_maxdist > BORDER:
    print("car.is.OUT!")
else:
    print("no worries, go go go")



t1 = t.time()-t0
print("elapsed time [s]: ", t1)

# plot data
plt.plot(road_data[:,0],road_data[:,1])
plt.plot(car1_data[:,0],car1_data[:,1])
plt.plot(car2_data[:,0],car2_data[:,1])
plt.plot(car3_data[:,0],car3_data[:,1])
plt.plot(border_data_left[:,0], border_data_left[:,1])
plt.plot(border_data_right[:,0], border_data_right[:,1])


