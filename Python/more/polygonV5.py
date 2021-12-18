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
from shapely.geometry import box, Polygon, LineString
from shapely.validation import explain_validity

t0 = t.time()

track_data_small= np.array([[30, 20], [60, 10], [80, 15], [90,30], [70,45], [35,25], [35,45]])
# track_data_big = np.array([[x, y] for x,y in zip(range(34,-5100,-1), range(26,5160,+1))])
# track_data = np.append(track_data_small, track_data_big, axis=0)
track_data = track_data_small

track = LineString(track_data)

car1_data = np.array([[50, 20], [60, 20], [60,25], [50,25]])
car2_data = np.array([[48, 30], [58, 30], [58,35], [48,35]])  # intersects Polygon
car3_data = np.array([[40, 40], [50, 40], [50,45], [40,45]])

plt.plot(track_data[:,0],track_data[:,1])
plt.plot(car1_data[:,0],car1_data[:,1])
plt.plot(car2_data[:,0],car2_data[:,1])
plt.plot(car3_data[:,0],car3_data[:,1])

car1_ls = LineString(car1_data)
car2_ls = LineString(car2_data)
car3_ls = LineString(car3_data)

border_data_left = np.array(track.parallel_offset(2,"left",join_style=1))
border_data_right = np.array(track.parallel_offset(2,"right",join_style=1))

plt.plot(border_data_left[:,0], border_data_left[:,1])
plt.plot(border_data_right[:,0], border_data_right[:,1])



p_start = track_data[0,:]-track_data[1,:]
xv = np.array([10, 0])



angle = np.arccos(np.dot(p_start,xv)/(np.linalg.norm(p_start)*np.linalg.norm(xv)))
print(p_start)
print(xv)
print(angle)



#for i in range(0,100):
dist1 = track.distance(car1_ls)
dist2 = track.distance(car2_ls)
dist3 = track.distance(car3_ls)
# dist1 = car1.distance(track)
# dist2 = car2.distance(track)
# dist3 = car3.distance(track)

t1 = t.time()-t0
print("elapsed time [s]: ", t1)

# print(dist1)
# print(dist2)
# print(dist3)



