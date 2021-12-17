# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 12:32:03 2021

@author: em, fl, fs
"""

import numpy as np
import shapely as sh
import shapely.geometry as shgeo
import random
import time
import matplotlib.pyplot as plt

# polygon_data = np.array [(-157, 898), (159, 892), (-165, 892), (-162, 898)]
# point_data = np.array(-162, 895)

# line = geometry.LineString(polygon_data)
# polygon = geometry.Polygon(line)
# point = geometry.Point(p_x, p_y)

t0 = time.time()

track_small= np.array([[30, 10], [60, 10], [80, 15], [90,30], [70,45], [60,35], [35,25]])
track_big = np.array([[x, y] for x,y in zip(range(34,-1100,-1), range(26,1160,+1))])
track = np.append(track_small, track_big, axis=0)
# track = track_small
p_track = shgeo.Polygon(track)


if sh.validation.explain_validity(p_track) == "Valid Geometry": # check: Does polyline not intersect itself
    car1 = np.array([[50, 20], [60, 20], [60,25], [50,25]])
    car2 = np.array([[48, 30], [58, 30], [58,35], [48,35]])  # intersects Polygon
    car3 = np.array([[40, 40], [50, 40], [50,45], [40,45]])

    # plt.plot(track[:,0],track[:,1])
    # plt.plot(car1[:,0],car1[:,1])
    # plt.plot(car2[:,0],car2[:,1])
    # plt.scatter(car2[:,0],car2[:,1])
    # plt.plot(car3[:,0],car3[:,1])
    
    print("contains check")
    line = sh.geometry.LineString(track)
    polyline = sh.geometry.Polygon(line)
    c1_p1 = sh.geometry.Point(car1[0,:])
    c1_p2 = sh.geometry.Point(car1[1,:])
    c1_p3 = sh.geometry.Point(car1[2,:])
    c1_p4 = sh.geometry.Point(car1[3,:])
    c2_p1 = sh.geometry.Point(car2[0,:])
    c2_p2 = sh.geometry.Point(car2[1,:])
    c2_p3 = sh.geometry.Point(car2[2,:])
    c2_p4 = sh.geometry.Point(car2[3,:])
    c3_p1 = sh.geometry.Point(car3[0,:])
    c3_p2 = sh.geometry.Point(car3[1,:])
    c3_p3 = sh.geometry.Point(car3[2,:])
    c3_p4 = sh.geometry.Point(car3[3,:])
    print(polyline.contains(c1_p1))
    print(polyline.contains(c1_p2))
    print(polyline.contains(c1_p3))
    print(polyline.contains(c1_p4))
    print(polyline.contains(c2_p1))
    print(polyline.contains(c2_p2))
    print(polyline.contains(c2_p3))
    print(polyline.contains(c2_p4))
    print(polyline.contains(c3_p1))
    print(polyline.contains(c3_p2))
    print(polyline.contains(c3_p3))
    print(polyline.contains(c3_p4))
    
    print("intersection check")
    car_shape1 = shgeo.Polygon(car1)
    car_shape2 = shgeo.Polygon(car2)
    car_shape3 = shgeo.Polygon(car3)
    check_car1 = p_track.intersection(car_shape1).area == car_shape1.area
    check_car2 = p_track.intersection(car_shape2).area == car_shape2.area
    check_car3 = p_track.intersection(car_shape3).area == car_shape3.area
    print(check_car1)
    print(check_car2)
    print(check_car3)
else:
    print("Generated track is not a valid polygon")

t1 = time.time()-t0
print(t1)