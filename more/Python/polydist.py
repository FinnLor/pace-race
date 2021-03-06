# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 12:32:03 2021

@author: em, fl, fs
"""

import numpy as np
import random
import time
import matplotlib.pyplot as plt
from shapely.geometry import box, Polygon

t = time.time()

pol_small= np.array([[30, 10], [60, 10], [80, 15], [90,30], [70,45], [60,35], [35,25]])
pol_big = np.array([[x, y] for x,y in zip(range(34,-1100,-1), range(26,1160,+1))])

pol1 = np.append(pol_small, pol_big, axis=0)
pol2 = np.array([[50, 20], [60, 20], [60,25], [50,25]])
pol3 = np.array([[48, 30], [58, 30], [58,35], [48,35]])  #schneidet Polygon
pol4 = np.array([[40, 40], [50, 40], [50,45], [40,45]])

#plt.scatter(pol1[:,0],pol1[:,1])
#plt.scatter(pol1_big[:,0],pol1_big[:,1])

plt.plot(pol1[:,0],pol1[:,1])
plt.plot(pol2[:,0],pol2[:,1])
plt.plot(pol3[:,0],pol3[:,1])
plt.plot(pol4[:,0],pol4[:,1])

polygon_shape = Polygon(pol1)
car_shape2 = Polygon(pol2)
car_shape3 = Polygon(pol3)
car_shape4 = Polygon(pol4)

check_pol2 = polygon_shape.intersection(car_shape2).area == car_shape2.area
check_pol3 = polygon_shape.intersection(car_shape3).area == car_shape3.area
check_pol4 = polygon_shape.intersection(car_shape4).area == car_shape4.area

check_tmp = polygon_shape.intersection(car_shape3) is car_shape3

print(check_pol2)
print(check_pol3)
print(check_pol4)
print(check_tmp)

elapsed = time.time()-t
print(elapsed)