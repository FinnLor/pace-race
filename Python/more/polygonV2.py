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

track_small= np.array([[30, 10], [60, 10], [80, 15], [90,30], [70,45], [60,35], [35,25]])
# track_big = np.array([[x, y] for x,y in zip(range(34,-1100,-1), range(26,1160,+1))])
# track_data = np.append(track_small, track_big, axis=0)
track_data = track_small


track = LineString(track_data)


if explain_validity(track) == "Valid Geometry": # check: Does polyline not intersect itself
    car1_data = np.array([[50, 20], [60, 20], [60,25], [50,25]])
    car2_data = np.array([[48, 30], [58, 30], [58,35], [48,35]])  # intersects Polygon
    car3_data = np.array([[40, 40], [50, 40], [50,45], [40,45]])

    plt.plot(track_data[:,0],track_data[:,1])
    plt.plot(car1_data[:,0],car1_data[:,1])
    plt.plot(car2_data[:,0],car2_data[:,1])
    plt.plot(car3_data[:,0],car3_data[:,1])
    
    car1 = LineString(car1_data)
    car2 = LineString(car2_data)
    car3 = LineString(car3_data)

    dist1 = track.distance(car1)
    dist2 = track.distance(car2)
    dist3 = track.distance(car3)

    print(dist1)
    print(dist2)
    print(dist3)
else:
    print("Generated polygon is not valid")



# track_data = [(2, 2), (50, 2), (630, 598), (550, 598), (2, 50)]
# car_data = [(10, 10), (20, 10), (20, 15), (10,15)]
# track = LineString(track_data)
# car = LineString(car_data)
# print(track.distance(car))

t0 = t.time()
t1 = t.time()-t0
print("elapsed time [s]: ", t1)