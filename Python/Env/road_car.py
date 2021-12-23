# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

- sensordaten:  in Prozent zwischern [0, 1] auslesen
Todo:    
- maßstäbe für Weg, Zeit, Geschwindigkeit definieren.
- "track.simplify(1,True)" aus dem pkg "shapely" könnte für komplexe polygone nützlich sein

@author: em, fl, fs
"""



from shapely.geometry import box, Polygon, LineString, Point
from shapely.validation import explain_validity
import math as m
import matplotlib.pyplot as plt
import numpy as np
import shapely as sh
import time as t
import tkinter as tk
import random as rnd



class Car:
    '''
    Die Klasse 'Car' beschreibt im Wesentlichen das geometrische Objekt 'Car' 
    und bietet dem Anwender die Option, die Position zu bestimmen und 
    positions- kollisions- und Sensordaten abzufragen
    Die Geometrie von 'Car' besteht aus: 
        - einem geschlossenen Polygon mit fünf Punkten, 
        - einem Drehpunktzentrum des Fahrzeugs und
        - mindestens einem Sensor, bestehend aus einer Linie mit zwei Punkten: 
                --- dem Sensorreferenzpunkt, der gleichzeitig Sensordrehpunkt 
                    ist und für alle Sensoren der selbe ist.
                --- dem Sensorendpunkt.
    Der car-Polygonzug dreht sich in Abhängigkeit zum Winkel 'psi'
    Der Sensor / die Sensoren drehen sich in Abhängigkeit zum eingeschlagenen 
    Lenkwinkel 'delta'.
    Die Klasse 'Car' benötigt die Klasse 'canvas' zur Datenformatierung, 
    Datenverwaltung und zum optionalen Rendern.
    Folgende Methoden stehen zur Verfügung
    (BEISPIELE zur Instanzierung und zur Nutzung der implementierten Methoden 
     befinden sich in der aufrufenden Umgebung):
        - set_car_pos: 
            HAUPTFUNKTION zum Setzen des 'Car'. Der Anwender gibt die
            Koordinaten x[m], y[m], psi[rad] und delta[rad] vor.
        - get_car_polygon: 
            Bislang nur zur visuellen Kontrolle benötigt.
        - get_car_center:  
            Bislang nur zur visuellen Kontrolle benötigt. 
        - set_start_pos: 
            Setzt 'Car' auf Startposition der Strecke und richtet
            'Car' auch korrekt aus.
            Der Lenkeinschlag 'delta' wird dabei auf '0[rad]' gesetzt
            Die Methode benötigt die Mittellinie der Strecke als Übergabe.
        - set_resume_pos:
            Setzt 'Car' (u.a. nach einer Kollision) wieder korrekt ausgerichtet
            im kürzesten Abstand auf die Mittellinie der Strecke zurück. 
            Der Lenkeinschlag wird hierbei auf 'delta = 0 [rad]' zurückgesetzt.
            Die Methode benötigt Mittel- und Randlinien der Strecke.
    '''
    
    
    def __init__(self,canvas,x,y,psi,delta,FACTOR,SENSFACTOR,color):
        
        # initialize
        self.FACTOR = FACTOR # resizing FACTOR, e.g. FAKTOR=10 => 10pixel==1m
        self.SENSFACT = SENSFACTOR # scaling factor for sensors as a multiplier of car length
        self.canvas = canvas
        self.Y = canvas.winfo_reqheight() # Flipping y-axis (minus 4?)
        self.psi = psi # car_angle
        self.delta = delta # front_wheel_angle
        self.color = color 
        self.dc = (0, 0) # velocity of car_center
        self.cl = 4 * self.FACTOR # car BOX length
        self.cw = 2 * self.FACTOR # car width
        self.c1 = (x-self.cl/2, self.Y-y+self.cw/2) # create corner of the car
        self.c2 = (x-self.cl/2, self.Y-y-self.cw/2)
        self.c3 = (x+self.cl/2, self.Y-y-self.cw/2)
        self.c4 = (x+self.cl/1.5, self.Y-y) # create sensor_center of car
        self.c5 = (x+self.cl/2, self.Y-y+self.cw/2)
       
        # initialize sensors
        self.s01 = (self.c4[0], self.c4[1]-self.cw) # create sensor point no 01 (left side)
        # self.s02 = (self.c4[0], self.c4[1]-self.cw)
        self.s03 = (self.c4[0]+self.SENSFACT*self.cl*5*3/4, self.c4[1]-self.cw)
        # self.s04 = (self.c4[0], self.c4[1]-self.cw)
        self.s05 = (self.c4[0]+self.SENSFACT*self.cl*5, self.c4[1]) # create sensor point no 05
        # self.s06 = (self.c4[0], self.c4[1]+self.cw)
        self.s07 = (self.c4[0]+self.SENSFACT*self.cl*5*3/4, self.c4[1]+self.cw)
        # self.s08 = (self.c4[0], self.c4[1]+self.cw)
        self.s09 = (self.c4[0], self.c4[1]+self.cw) # create sensor point no 09 (right side)

        # further initializations
        self.car_center = canvas.create_bitmap(float(x), float(self.Y-y)) # car_center position
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, self.c5, fill = self.color)
        self.sensor01 = canvas.create_line((self.c4,self.s01) , fill = self.color)
        self.sensor03 = canvas.create_line((self.c4,self.s03) , fill = self.color)
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color)
        self.sensor07 = canvas.create_line((self.c4,self.s07) , fill = self.color)
        self.sensor09 = canvas.create_line((self.c4,self.s09) , fill = self.color)
        self._car_rot_d(psi) # call method _car_rot_d
        self._sensor_rot(delta) # call method _sensor_rot


   
    def _car_move_d(self,dx,dy,dpsi): # difference-movement and -rotation
        
        self.dc = (dx, -dy) # velocity of car
        self.dpsi = dpsi # angle velocity of car
        self._car_rot_d(dpsi) # let the car rotate with the desired delta-psi
        self.canvas.move(self.sensor01,self.dc[0],self.dc[1])
        self.canvas.move(self.sensor03,self.dc[0],self.dc[1])
        self.canvas.move(self.sensor05,self.dc[0],self.dc[1])
        self.canvas.move(self.sensor07,self.dc[0],self.dc[1])
        self.canvas.move(self.sensor09,self.dc[0],self.dc[1])
        self.canvas.move(self.car_center,self.dc[0],self.dc[1]) # move the car_center
        self.canvas.move(self.car_polygon,self.dc[0],self.dc[1]) # move the car_polygon



    def _car_rot_d(self,dpsi): # only _car_rotation difference

        # RECIEVE CAR POSITION
        c_c      = self.canvas.coords(self.car_center) # extract car_center position data
        c_p      = self.canvas.coords(self.car_polygon) # extract car_polygon position data 
        c_s01    = self.canvas.coords(self.sensor01) # extract sensor01 data
        c_s03    = self.canvas.coords(self.sensor03) # extract sensor03 data
        c_s05    = self.canvas.coords(self.sensor05) # extract sensor05 data
        c_s07    = self.canvas.coords(self.sensor07) # extract sensor07 data
        c_s09    = self.canvas.coords(self.sensor09) # extract sensor09 data
        
        # GET RELATIVE CORNER VECTORS
        cc_c1    = np.array([c_p[0]   - c_c[0],c_p[1]   - c_c[1]]) # vector from car_center to c1
        cc_c2    = np.array([c_p[2]   - c_c[0],c_p[3]   - c_c[1]]) # vector from car_center to c2
        cc_c3    = np.array([c_p[4]   - c_c[0],c_p[5]   - c_c[1]]) # vector from car_center to c3
        cc_c4    = np.array([c_p[6]   - c_c[0],c_p[7]   - c_c[1]]) # vector from car_center to c4 (sensor_center)
        cc_c5    = np.array([c_p[8]   - c_c[0],c_p[9]   - c_c[1]]) # vector from car_center to c5
        cc_s01   = np.array([c_s01[2] - c_c[0],c_s01[3] - c_c[1]]) # vector from car_center to s01
        cc_s03   = np.array([c_s03[2] - c_c[0],c_s03[3] - c_c[1]]) # vector from car_center to s03
        cc_s05   = np.array([c_s05[2] - c_c[0],c_s05[3] - c_c[1]]) # vector from car_center to s05
        cc_s07   = np.array([c_s07[2] - c_c[0],c_s07[3] - c_c[1]]) # vector from car_center to s07
        cc_s09   = np.array([c_s09[2] - c_c[0],c_s09[3] - c_c[1]]) # vector from car_center to s09
        
        # ROTATE CORNER VECTORS
        rot = np.array([[np.cos(dpsi), np.sin(dpsi)], [-np.sin(dpsi), np.cos(dpsi)]]) # rotation matrix physically correct  
        
        cc_c1n   = np.dot(rot,  cc_c1) # vector from car_center to rotated c1
        cc_c2n   = np.dot(rot,  cc_c2) # vector from car_center to rotated c2
        cc_c3n   = np.dot(rot,  cc_c3) # vector from car_center to rotated c3
        cc_c4n   = np.dot(rot,  cc_c4) # vector from car_center to rotated c4 (sensor_center)
        cc_c5n   = np.dot(rot,  cc_c5) # vector from car_center to rotated c5
        cc_s01n  = np.dot(rot, cc_s01) # vector from car_center to rotated s01
        cc_s03n  = np.dot(rot, cc_s03) # vector from car_center to rotated s03
        cc_s05n  = np.dot(rot, cc_s05) # vector from car_center to rotated s05
        cc_s07n  = np.dot(rot, cc_s07) # vector from car_center to rotated s07
        cc_s09n  = np.dot(rot, cc_s09) # vector from car_center to rotated s09
        
        # SET ABSOLUTE CORNER VECTORS
        self.c1  = (cc_c1n[0]  + c_c[0], cc_c1n[1]  + c_c[1]) # update vector from canvas_GUI to c1
        self.c2  = (cc_c2n[0]  + c_c[0], cc_c2n[1]  + c_c[1]) # update vector from canvas_GUI to c2
        self.c3  = (cc_c3n[0]  + c_c[0], cc_c3n[1]  + c_c[1]) # update vector from canvas_GUI to c3
        self.c4  = (cc_c4n[0]  + c_c[0], cc_c4n[1]  + c_c[1]) # update vector from canvas_GUI to c4 (sensor_center)
        self.c5  = (cc_c5n[0]  + c_c[0], cc_c5n[1]  + c_c[1]) # update vector from canvas_GUI to c5
        self.s01 = (cc_s01n[0] + c_c[0], cc_s01n[1] + c_c[1]) # update vector from canvas_GUI to s01
        self.s03 = (cc_s03n[0] + c_c[0], cc_s03n[1] + c_c[1]) # update vector from canvas_GUI to s03
        self.s05 = (cc_s05n[0] + c_c[0], cc_s05n[1] + c_c[1]) # update vector from canvas_GUI to s05
        self.s07 = (cc_s07n[0] + c_c[0], cc_s07n[1] + c_c[1]) # update vector from canvas_GUI to s07
        self.s09 = (cc_s09n[0] + c_c[0], cc_s09n[1] + c_c[1]) # update vector from canvas_GUI to s09

        # UPDATE OBJECT
        self.canvas.delete(self.sensor01) # delete old sensor
        self.sensor01 = canvas.create_line((self.c4,self.s01) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.sensor03) # delete old sensor
        self.sensor03 = canvas.create_line((self.c4,self.s03) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.sensor05) # delete old sensor
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.sensor07) # delete old sensor
        self.sensor07 = canvas.create_line((self.c4,self.s07) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.sensor09) # delete old sensor
        self.sensor09 = canvas.create_line((self.c4,self.s09) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.car_polygon) # delete old car
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, self.c5, fill = self.color) # set new, rotated car
    
    
    
    def _car_rot(self,psi): # only rotation
        
        # SET CAR HORIZONTALLY
        c_c = self.canvas.coords(self.car_center) # extract car_center position data
        self.c1  = (c_c[0]-self.cl/2,   c_c[1]+self.cw/2) # set corner of car
        self.c2  = (c_c[0]-self.cl/2,   c_c[1]-self.cw/2)
        self.c3  = (c_c[0]+self.cl/2,   c_c[1]-self.cw/2)
        self.c4  = (c_c[0]+self.cl/1.5, c_c[1]) # set sensor center of car
        self.c5  = (c_c[0]+self.cl/2,   c_c[1]+self.cw/2)
        self.s01 = (self.c4[0], self.c4[1]-self.cw) # set sensor point no 01
        self.s03 = (self.c4[0]+self.SENSFACT*self.cl*5*3/4, self.c4[1]-self.cw)
        self.s05 = (self.c4[0]+self.SENSFACT*self.cl*5, self.c4[1]) # create sensor point no 05
        self.s07 = (self.c4[0]+self.SENSFACT*self.cl*5*3/4, self.c4[1]+self.cw)
        self.s09 = (self.c4[0], self.c4[1]+self.cw) # set sensor point no 09
        
        # GET RELATIVE CORNER VECTORS
        cc_c1    = np.array([self.c1[0]  - c_c[0],self.c1[1]  - c_c[1]]) # vector from car_center to c1
        cc_c2    = np.array([self.c2[0]  - c_c[0],self.c2[1]  - c_c[1]]) # vector from car_center to c2
        cc_c3    = np.array([self.c3[0]  - c_c[0],self.c3[1]  - c_c[1]]) # vector from car_center to c3
        cc_c4    = np.array([self.c4[0]  - c_c[0],self.c4[1]  - c_c[1]]) # vector from car_center to c4 (sensor_center)
        cc_c5    = np.array([self.c5[0]  - c_c[0],self.c5[1]  - c_c[1]]) # vector from car_center to c5
        cc_s01   = np.array([self.s01[0] - c_c[0],self.s01[1] - c_c[1]]) # vector from car_center to s01
        cc_s03   = np.array([self.s03[0] - c_c[0],self.s03[1] - c_c[1]]) # vector from car_center to s05
        cc_s05   = np.array([self.s05[0] - c_c[0],self.s05[1] - c_c[1]]) # vector from car_center to s05
        cc_s07   = np.array([self.s07[0] - c_c[0],self.s07[1] - c_c[1]]) # vector from car_center to s05
        cc_s09   = np.array([self.s09[0] - c_c[0],self.s09[1] - c_c[1]]) # vector from car_center to s09
        
        # ROTATE RELATIVE CORNER VECTORS
        rot = np.array([[np.cos(psi), np.sin(psi)], [-np.sin(psi), np.cos(psi)]]) # rotation matrix physically correct  
        cc_c1n   = np.dot(rot,  cc_c1) # vector from car_center to rotated c1
        cc_c2n   = np.dot(rot,  cc_c2) # vector from car_center to rotated c2
        cc_c3n   = np.dot(rot,  cc_c3) # vector from car_center to rotated c3
        cc_c4n   = np.dot(rot,  cc_c4) # vector from car_center to rotated c4
        cc_c5n   = np.dot(rot,  cc_c5) # vector from car_center to rotated c4
        cc_s01n  = np.dot(rot, cc_s01) # vector from car_center to rotated s01
        cc_s03n  = np.dot(rot, cc_s03) # vector from car_center to rotated s05
        cc_s05n  = np.dot(rot, cc_s05) # vector from car_center to rotated s05
        cc_s07n  = np.dot(rot, cc_s07) # vector from car_center to rotated s05
        cc_s09n  = np.dot(rot, cc_s09) # vector from car_center to rotated s09
        
        # SET ABSOLUTE CORNER VECTORS
        self.c1  = (cc_c1n[0]  + c_c[0], cc_c1n[1]  + c_c[1]) # update vector from canvas_GUI to c1
        self.c2  = (cc_c2n[0]  + c_c[0], cc_c2n[1]  + c_c[1]) # update vector from canvas_GUI to c2
        self.c3  = (cc_c3n[0]  + c_c[0], cc_c3n[1]  + c_c[1]) # update vector from canvas_GUI to c3
        self.c4  = (cc_c4n[0]  + c_c[0], cc_c4n[1]  + c_c[1]) # update vector from canvas_GUI to c4
        self.c5  = (cc_c5n[0]  + c_c[0], cc_c5n[1]  + c_c[1]) # update vector from canvas_GUI to c4
        self.s01 = (cc_s01n[0] + c_c[0], cc_s01n[1] + c_c[1]) # update vector from canvas_GUI to s01
        self.s03 = (cc_s03n[0] + c_c[0], cc_s03n[1] + c_c[1]) # update vector from canvas_GUI to s03
        self.s05 = (cc_s05n[0] + c_c[0], cc_s05n[1] + c_c[1]) # update vector from canvas_GUI to s05
        self.s07 = (cc_s07n[0] + c_c[0], cc_s07n[1] + c_c[1]) # update vector from canvas_GUI to s07
        self.s09 = (cc_s09n[0] + c_c[0], cc_s09n[1] + c_c[1]) # update vector from canvas_GUI to s09
        
        # UPDATE OBJECT
        self.canvas.delete(self.sensor01) # delete old sensor
        self.sensor01 = canvas.create_line((self.c4,self.s01) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.sensor03) # delete old sensor
        self.sensor03 = canvas.create_line((self.c4,self.s03) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.sensor05) # delete old sensor
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.sensor07) # delete old sensor
        self.sensor07 = canvas.create_line((self.c4,self.s07) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.sensor09) # delete old sensor
        self.sensor09 = canvas.create_line((self.c4,self.s09) , fill = self.color) # set new, rotated sensor-line
        self.canvas.delete(self.car_polygon) # delete old car
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, fill = self.color) # set new, rotated car



    def _sensor_rot(self,delta):
        
        # generate relative sensor vectors
        s01_h_r = (0, -self.cw) # create sensor point no 01 (right side)
        s03_h_r = (self.SENSFACT*self.cl*5*3/4, -self.cw)
        s05_h_r = (self.SENSFACT*self.cl*5, 0) # sensor s05 horizontal and relative to sensor_center
        s07_h_r = (self.SENSFACT*self.cl*5*3/4, +self.cw)
        s09_h_r = (0, +self.cw) # create sensor point no 09 (right side)

        # rotate sensor vectors
        deltapsi = delta + self.psi
        rot = np.array([[np.cos(deltapsi), np.sin(deltapsi)], [-np.sin(deltapsi), np.cos(deltapsi)]]) # rotation matrix physically correct  
        cc_s01n = np.dot(rot, s01_h_r) # new relative sensor point position
        cc_s03n = np.dot(rot, s03_h_r) # new relative sensor point position
        cc_s05n = np.dot(rot, s05_h_r) # new relative sensor point position
        cc_s07n = np.dot(rot, s07_h_r) # new relative sensor point position
        cc_s09n = np.dot(rot, s09_h_r) # new relative sensor point position

        # set absolute sensor vectors
        self.s01 = (cc_s01n[0] + self.c4[0], cc_s01n[1] + self.c4[1]) # update vector from canvas_GUI to s01
        self.s03 = (cc_s03n[0] + self.c4[0], cc_s03n[1] + self.c4[1]) # update vector from canvas_GUI to s03
        self.s05 = (cc_s05n[0] + self.c4[0], cc_s05n[1] + self.c4[1]) # update vector from canvas_GUI to s05
        self.s07 = (cc_s07n[0] + self.c4[0], cc_s07n[1] + self.c4[1]) # update vector from canvas_GUI to s07
        self.s09 = (cc_s09n[0] + self.c4[0], cc_s09n[1] + self.c4[1]) # update vector from canvas_GUI to s09
        
        # update sensor data
        self.canvas.delete(self.sensor01) # delete old sensor
        self.sensor01 = canvas.create_line((self.c4,self.s01) , fill = self.color) # set new, rotated sensor data
        self.canvas.delete(self.sensor03) # delete old sensor
        self.sensor03 = canvas.create_line((self.c4,self.s03) , fill = self.color) # set new, rotated sensor data
        self.canvas.delete(self.sensor05) # delete old sensor
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor data
        self.canvas.delete(self.sensor07) # delete old sensor
        self.sensor07 = canvas.create_line((self.c4,self.s07) , fill = self.color) # set new, rotated sensor data
        self.canvas.delete(self.sensor09) # delete old sensor
        self.sensor09 = canvas.create_line((self.c4,self.s09) , fill = self.color) # set new, rotated sensor data
    
 
    
    ### SET ARBITRARY CAR POSITION
    def set_car_pos(self,x,y,psi,delta): # set new car postion and angles (with zero velocities)
        
        self.psi = psi # car_angle
        self.delta = delta  # front_wheel_angle
        self.dc = (0, 0) # velocity of car
        self.dpsi = 0 # velocity of car_angle
        self.c1 = (x-self.cl/2, self.Y-y+self.cw/2) # corner of car
        self.c2 = (x-self.cl/2, self.Y-y-self.cw/2)
        self.c3 = (x+self.cl/2, self.Y-y-self.cw/2) 
        self.c4 = (x+self.cl/1.5, self.Y-y) # sensor_center of car
        self.c5 = (x+self.cl/2, self.Y-y+self.cw/2)
        self.s01 = (self.c4[0], self.c4[1]-self.cw) # create sensor point no 01 (right side)
        self.s03 = (self.c4[0]+self.SENSFACT*self.cl*5*3/4, self.c4[1]-self.cw)
        self.s05 = (self.c4[0]+self.SENSFACT*self.cl*5, self.c4[1]) # create sensor point no 05   
        self.s07 = (self.c4[0]+self.SENSFACT*self.cl*5*3/4, self.c4[1]+self.cw)
        self.s09 = (self.c4[0], self.c4[1]+self.cw) # create sensor point no 09 (left side)
        
        # set new car_center
        self.canvas.delete(self.car_center) # delete old car_center
        self.car_center = canvas.create_bitmap(float(x), float(self.Y-y))
        self._car_rot(psi) # call method _car_rot
        self._sensor_rot(delta) # call method _sensor_rot
        self.canvas.delete(self.car_polygon) # delete old car polygon
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, self.c5, fill = self.color) # set new, rotated car


    
    ### GET CAR POLYGON
    def get_car_polygon(self):
        
        car_polygon = self.canvas.coords(self.car_polygon) # extract car_polygon position data 
        return car_polygon
    
    
    
    ### GET CAR CENTER COORDS
    def get_car_center(self):
        
        car_center = self.canvas.coords(self.car_center) # extract car_center position data
        return car_center
      
      
        
    ### SET CAR ON ROAD START POSITION
    def set_start_pos(self,center_line):
        
        self.delta = 0  # front_wheel_angle
        
        rd = np.array(center_line)
        size = np.shape(rd)[0]
        rs = np.reshape(center_line,(int(0.5*size),2))
        v_start = rs[1,:] - rs[0,:]
        x = center_line[0]
        y = self.Y-center_line[1]
        v_x = np.array([10, 0])
        if v_start[1] > 0:
            psi = -np.arccos(np.dot(v_start,v_x)/(np.linalg.norm(v_start)*np.linalg.norm(v_x)))
        else:
            psi = np.arccos(np.dot(v_start,v_x)/(np.linalg.norm(v_start)*np.linalg.norm(v_x)))
        self.set_car_pos(x,y,psi,0)



    ### SET CAR ON NEXT MIDLINE POSITION
    def set_resume_pos(self,center_line, right_line, left_line):
        
        # extract car_center position data
        car_center = self.canvas.coords(self.car_center) 
        c_c = Point(car_center)
        
        # transform road_data into correct format
        rd_cl = np.array(center_line)
        size_cl = np.shape(rd_cl)[0]
        rs_cl = np.reshape(center_line,(int(0.5*size_cl),2))
        rd_rl = np.array(right_line)
        size_rl = np.shape(rd_rl)[0]
        rs_rl = np.reshape(right_line,(int(0.5*size_rl),2))
        rd_ll = np.array(left_line)
        size_ll = np.shape(rd_ll)[0]
        rs_ll = np.reshape(left_line,(int(0.5*size_ll),2))
        road_lsc = LineString(rs_cl)
        road_lsr = LineString(rs_rl)
        road_lsl = LineString(rs_ll)

        # detect x-y-position for resumed car_center
        pathlength = road_lsc.project(c_c,normalized = False) # return pathlength from polyline-start to shortest point-distance
        point_on_line = np.array(road_lsc.interpolate(pathlength)) # get coordinates for pathlength
        x = point_on_line[0]
        y = self.Y-point_on_line[1]
  
        # detect psi for resumed car_direction
        c_c_dr = c_c.distance(road_lsr) # distance from car_center to right Road line
        c_c_dl = c_c.distance(road_lsl) # distance from car_center to left Road line
        c_c_np = np.array(c_c) 
        v_x = np.array([10, 0])
        
        if c_c_dl != c_c_dr:
            if c_c_dl > c_c_dr:
                rot = np.array([[np.cos(m.pi/2), np.sin(m.pi/2)], [-np.sin(m.pi/2), np.cos(m.pi/2)]]) # rotation matrix clockwise 
            elif c_c_dl < c_c_dr:
                rot = np.array([[np.cos(m.pi/2), -np.sin(m.pi/2)], [np.sin(m.pi/2), np.cos(m.pi/2)]]) # rotation matrix counter-clockwise 
            v_forward = np.dot(rot,(c_c_np - [x, self.Y-y])) # get forward-direction  
            if v_forward[1] > 0:
                psi_forward = -np.arccos(np.dot(v_forward,v_x)/(np.linalg.norm(v_forward)*np.linalg.norm(v_x))) 
            else:
                psi_forward = np.arccos(np.dot(v_forward,v_x)/(np.linalg.norm(v_forward)*np.linalg.norm(v_x))) 
            self.set_car_pos(x,y,psi_forward,0)
        
        else:
            print("Check whether car is already set to start or resume position.")


   
   
   
   
class Road:
    '''
    Die Klasse 'Road' erzeugt beim Instanzieren eine einfache, zufällig
    parametrisierte Strecke und beinhaltet eine Mittellinie und einen daraus
    abgeleiteten aber explizit vorhandene linken und rechten Rand.
    Die Klasse 'Road' benötigt die Klasse 'canvas' zur Datenformatierung, 
    Datenverwaltung und zum optionalen Rendern.
    Die Straßenbreite kann bei der Instanzierung vorgegeben werden, 
    ist aber über die gesamte Strecke konstant.
    Folgende Methoden stehen zur Verfügung
    (BEISPIELE zur Instanzierung und zur Nutzung der implementierten Methoden 
    befinden sich in der aufrufenden Umgebung):
    - get_center_line:
        Rückgabe der Mittellinie.
    - get_right_line:
        Rückgabe des rechten Randes.
    - get_left_line:
        Rückgabe des linken Randes.
    - path_length:
        Straßenposition des entsprechenden 'car', Wertebereich [0, 1] 
        (0: ganz zu Beginn; 1: am Ende der Straße)
        Bei Abfrage unmittelbar nach 'Kollision' entspricht dem Anteil der erreichten Strecke
    - collision_check:
        Rückgabe [bool], False: keine Kollision detektiert, True: Kollision detektiert.
        Benötigt das Objekt 'Car'.
        Hinweis zum Algorithmus: Es wird der minimale Abstand jedes einzelnen 
        Polygonpuntkes von 'Car' zur Mittellinie ermittelt. Wenn davon der 
        größte Wert die halbe Straßenbreite überschreitet, wird 'collision=True'
        gesetzt. Das Package 'shapely' gewährleistet, dass der geringste
        Abstand (Normalenabstand) über den ganzen Polygonzug ermittelt wird 
        und nicht nur zu den Polygonpunkten.
    - get_sensordata(car.c4, car_sensor):        
        Gibt den Abstand des Sensors zu BEIDEN Rändern zurück.
        Falls die 'Sensorreichweite' nicht bis zum 'Rand' kommt, gibt die 
        Methode die maximale Sensorreichweite an.
        Falls innerhalb der 'Sensorreichweite' mehrere 'intersection' mit 
        einem Rand vorhanden sind, wird der kürzeste Abstnand angegeben.
        Benötigt die Properties:
            - car.c4 (Ausgangspunkt für alle Sensoren)
            - car.sxx (jeweiliger Sensorendpunkt, zB car.s05)
        TODO:
        Derzeit wird nur EIN sensor ausgewertet (der einige Meter vor 'Car', 
        jedoch in 'delta-richtung')
        Die noch anstehende Implementierung sieht die Implementierung 
        weiterer Sensoren vor. Die Rückgabe wird dann ein nx2-Array sein
        (n: Anzahl Sensoren, 2: je ein Abstandswert f d linken u rechten Rand)
        
    HINWEIS: das Potenzial der Klasse könnte mit 
    "test_ls = track.simplify(1,True)" aus shapely höchstwahrscheinlich 
    effizienter gestaltet werden
    '''
    
    
    def __init__(self,canvas,FACTOR,WIDTH,HEIGHT,NPOINTS, ROADWIDTH):
        
        # initialize important Road data
        self.canvas = canvas
        self.FACTOR = FACTOR # dimension, e.g. FAKTOR=10 => 10pixel==1m
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.NPOINTS = NPOINTS
        self.ROADWIDTH = ROADWIDTH
        self.Y = canvas.winfo_reqheight() # Flipping y-axis (minus 4?)
        
        # generate center line of Road random-supported
        n = np.linspace(0.5, 2*m.pi, self.NPOINTS)
        x = m.pow((-1),rnd.randrange(1,3,1)) * (n + 3*rnd.uniform(0,1)*np.tan(0.2*n))
        y = self.Y - (1./n + rnd.uniform(0,1)*3.*np.cos(n)*np.power(np.sin(n),2))
        
        # align Road into canvas
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
                
        # generate Road- and border data 
        line_data  = list((np.ravel(([x,y]),'F'))) # list is neccessary for a correct separation with comma
        road_center_ls = LineString(np.reshape(line_data,(self.NPOINTS,2)))
        road_right_line1 = np.array(road_center_ls.parallel_offset(self.FACTOR*self.ROADWIDTH/2,"left",join_style=1)) # left for right side because of the -y canvas-coordinates
        road_right_line = list((np.ravel(([road_right_line1[:,0],road_right_line1[:,1]]),'F')))
        road_left_line1 = np.array(road_center_ls.parallel_offset(self.FACTOR*self.ROADWIDTH/2,"right",join_style=1))  # right for left side because of the -y canvas-coordinates
        road_left_line = list((np.ravel(([road_left_line1[:,0],road_left_line1[:,1]]),'F')))
        
        # assign main Road data
        self.road_center_line = canvas.create_line(line_data, dash = (4), fill = "grey")
        self.road_right_line   = canvas.create_line(road_right_line, fill = "brown")
        self.road_left_line   = canvas.create_line(road_left_line, fill = "brown")



    ### GET CENTER LINE OF THE ROAD
    def get_center_line(self):
        
        road_centerline = self.canvas.coords(self.road_center_line) 
        return road_centerline
 
    
 
    ### GET RIGHT LINE OF THE ROAD
    def get_right_line(self):
        
        road_rightline = self.canvas.coords(self.road_right_line) 
        return road_rightline
 
    
 
    ### GET LEFT LINE OF THE ROAD
    def get_left_line(self):

        road_leftline = self.canvas.coords(self.road_left_line)
        return road_leftline
    
    
    
    ### GET LENGTH OF THE ROAD FROM BEGINNING TO COLLISION
    def get_path_length(self,car):

        # get center line of Road
        road_lsc = LineString(np.reshape(self.canvas.coords(self.road_center_line), (self.NPOINTS,2)))
        
        # extract car_center position data
        car_center = car.canvas.coords(car.car_center) # extract car_center position data
        ccenter = Point(car_center)

        # get the current position of collision as center line path length
        path_length = road_lsc.project(ccenter,normalized = True)
        return path_length
    
    
    
    ### CHECK WHETHER CAR COLLIDES WITH BORDER OR IS OUTSIDE OF BORDER
    def collision_check(self,car):
        
        # get car border points
        c_p1 = Point(car.c1)
        c_p2 = Point(car.c2)
        c_p3 = Point(car.c3)
        c_p4 = Point(car.c4)
        c_p5 = Point(car.c5)
        
        # get center line of Road
        road_lsc = LineString(np.reshape(self.canvas.coords(self.road_center_line), (self.NPOINTS,2)))
 
        # calculate distances from car points to the center line
        c_p1_d = c_p1.distance(road_lsc)
        c_p2_d = c_p2.distance(road_lsc)
        c_p3_d = c_p3.distance(road_lsc)
        c_p4_d = c_p4.distance(road_lsc)
        c_p5_d = c_p5.distance(road_lsc)
        
        # select the point with max distance from center line
        c_maxdist = max(c_p1_d, c_p2_d, c_p3_d, c_p4_d, c_p5_d)/self.FACTOR

        # check if car exceeds border
        if c_maxdist > self.ROADWIDTH/2:
            collision = True
        else:
            collision = False
        return collision
        
        
        
    ### CHECK AND RETURN THE DISTANCES BETWEEN SENSOR-REFERENCE POINT AND BORDERS OF THE ROAD
    # Der Versuch, hier einen internen Funktionsaufruf als Schleife zu nutzen endet in der Fehlermeldung
    # "cannot unpack non-iterable NoneType object"
    def get_sensordata(self,car_c4,car_sensor):

        # transform sensor data
        sensorline = np.array([car_c4,car_sensor])
        ref_p = Point(sensorline[0,:]) # Reference point, source of all Sensor_lines
        l_p = Point(sensorline[1,:]) # Outer sensor point
        l_ls = LineString(sensorline)
        length_sensorline = ref_p.distance(l_p)
        
        # get and transform right and left border data
        left_line = self.canvas.coords(self.road_left_line) 
        rd_ll = np.array(left_line)
        size_ll = np.shape(rd_ll)[0]
        rs_ll = np.reshape(left_line,(int(0.5*size_ll),2))
        road_lsl = LineString(rs_ll)
        isp_l = np.array(l_ls.intersection(road_lsl)) # absolute position of intersection point(s) of sensor with left BORDER
        right_line = self.canvas.coords(self.road_right_line) 
        rd_rl = np.array(right_line)
        size_rl = np.shape(rd_rl)[0]
        rs_rl = np.reshape(right_line,(int(0.5*size_rl),2))
        road_lsr = LineString(rs_rl)
        isp_r = np.array(l_ls.intersection(road_lsr)) # absolute position of intersection point(s) of sensor with right BORDER

        
        # collect all possible distances for the sensor
        distances_l = []
        distances_r = []
        if isp_l.ndim == 2:
            for i in range(0,isp_l.shape[0]): # if there are more than one intersections with left BORDER
               distances_l.append(ref_p.distance(Point(isp_l[i,:])))
            dist_l = min(distances_l)
        else:
            if len(isp_l)==0: # if there is no intersection with left BORDER
                dist_l = ref_p.distance(l_p)
            else:
                dist_l = ref_p.distance(Point(isp_l)) # if there is one intersection with left BORDER
        
        if isp_r.ndim == 2:
            for i in range(0,isp_r.shape[0]): # if there are more than one intersections with right BORDER
               distances_r.append(ref_p.distance(Point(isp_r[i,:])))
            dist_r = min(distances_r)
        else:
            if len(isp_r)==0: # if there is no intersection with right BORDER
                dist_r = ref_p.distance(l_p)
            else:
                dist_r = ref_p.distance(Point(isp_r)) # if there is one intersection with left BORDER
        
        # resize sensor distances due to the max length of the sensorline and return values
        dist_r_r = dist_r/length_sensorline
        dist_r_l = dist_l/length_sensorline
        return dist_r_r, dist_r_l # returns left and right distances
        
        
        
        
        
        
######################################
### TEST ENVIRONMENT COMMUNICATION ###
######################################
'''
Umgebung mit
- Initialisierung der Umgebungsdaten
- Instanzierung der Klassen 'Car' und 'Road'
- Tests der entsprechenden Methoden
- Aufruf der Renderfunktionalität 'win_env.update()'
Beinhaltet:
- win_env: GUI-parent class, including: canvas: method for generating, saving 
and rendering. positive-x goes right, positive-y goes down.

TODO:
- "ShapelyDeprecationWarning: The array interface is deprecated and will no 
longer work in Shapely 2.0. Convert the '.coords' to a numpy array instead.
'''

### CONFIGURE ENVIRONMENT BASICS
win_env = tk.Tk() # parent window for the canvas
WIDTH = 1800
HEIGHT = 1000
VISUALIZE = True
NPOINTS = 1000 # no of points of the central Road line
ROADWIDTH = 8
FACTOR = 10 # resizing FACTOR, e.g. FAKTOR=10 => 10pixel==1m
SENSFACTOR = 1 # resizing factor for sensors 1 = standard
canvas = tk.Canvas(win_env, width=WIDTH, height=HEIGHT) # rendering area in GUI for cars, theirs sensors and a Road
if VISUALIZE == True:
    canvas.pack() # required to visualize the canvas
button = tk.Button(win_env, text='enough', command = lambda:win_env.destroy()).pack(expand=True) # EXPERIMENTAL added button for closing GUI

### CONSTRUCT ROAD
road = Road(canvas,FACTOR,WIDTH,HEIGHT,NPOINTS, ROADWIDTH)
road_lsc = LineString(np.reshape(road.get_center_line(), (NPOINTS,2))) # get center line of the road

### CONSTRUCT CARS
car01 = Car(canvas, 140, 20,  0, 0, FACTOR, SENSFACTOR, "yellow")
car02 = Car(canvas, 100, 200,  0.6, -0.6, FACTOR, SENSFACTOR, "green")
car03 = Car(canvas, 110,  90,    0,   0, FACTOR, SENSFACTOR, "blue")
car04 = Car(canvas, 180, 100,    1,   1, FACTOR, SENSFACTOR, "black")
car05 = Car(canvas, 900, 200,  1.3, 1.3, FACTOR, SENSFACTOR, "pink")
car06 = Car(canvas, 300, 500,  1.3, -1.3, FACTOR, SENSFACTOR, "brown")
car07 = Car(canvas, 140,  10,  0.4, -0.4, FACTOR, SENSFACTOR, "red")
car08 = Car(canvas, 750, 300,  0.6, 0.6, FACTOR, SENSFACTOR, "olive")
car09 = Car(canvas, 110,  90,    0,   0, FACTOR, SENSFACTOR, "cyan")
car10 = Car(canvas, 120, 100,    1,   1, FACTOR, SENSFACTOR, "purple")
car11 = Car(canvas, 700, 300,  1.3, -1.3, FACTOR, SENSFACTOR, "gray")
car12 = Car(canvas, 200, 600,  1.3, 1.3, FACTOR, SENSFACTOR, "orange")
  
### TESTS
# time measuring
t0 = t.time()
for i in range(0,100):
    
    # collision test
    collision_car01 = road.collision_check(car01)
    print("collision or outside yellow ", collision_car01)
    
    # distence test
    collision_car02 = road.collision_check(car02)
    print("distance green ", collision_car02)
    
    # positionstest
    path_length_car03 = road.get_path_length(car03)
    print("position blue ", path_length_car03)

    # set car test
    car04.set_car_pos(1000,500,1.5,0)

    # car sensor rotation test
    car05._sensor_rot(-0.7+i/5)

    # car moving test
    car06._car_move_d(1.0,1.0,-0.01)
    
    # car rotation test
    car07._car_rot_d(-0.1)
    
    # optional rendering
    if VISUALIZE == True:
        win_env.update()
        t.sleep(0.01)

# car set start pos test
car08.set_start_pos(road.get_center_line())

# car resume position test
car09.set_resume_pos(road.get_center_line(), road.get_right_line(), road.get_left_line())
car10.set_resume_pos(road.get_center_line(), road.get_right_line(), road.get_left_line())
car11.set_resume_pos(road.get_center_line(), road.get_right_line(), road.get_left_line())

# get sensordata
s1_rightborder, s1_leftborder = road.get_sensordata(car04.c4, car04.s01)
s3_rightborder, s3_leftborder = road.get_sensordata(car04.c4, car04.s03)
s5_rightborder, s5_leftborder = road.get_sensordata(car04.c4, car04.s05)
s7_rightborder, s7_leftborder = road.get_sensordata(car04.c4, car04.s07)
s9_rightborder, s9_leftborder = road.get_sensordata(car04.c4, car04.s09)
print("sensors black ")
print("sensor 1, distance to RIGHT border: ", s1_rightborder)
print("sensor 1, distance to LEFT border: ", s1_leftborder)
print("sensor 3, distance to RIGHT border: ", s3_rightborder)
print("sensor 3, distance to LEFT border: ", s3_leftborder)
print("sensor 5, distance to RIGHT border: ", s5_rightborder)
print("sensor 5, distance to LEFT border: ", s5_leftborder)
print("sensor 7, distance to RIGHT border: ", s7_rightborder)
print("sensor 7, distance to LEFT border: ", s7_leftborder)
print("sensor 9, distance to RIGHT border: ", s9_rightborder)
print("sensor 9, distance to LEFT border: ", s9_leftborder)

# get sensordata
s1_rightborder, s1_leftborder = road.get_sensordata(car12.c4, car12.s01)
s3_rightborder, s3_leftborder = road.get_sensordata(car12.c4, car12.s03)
s5_rightborder, s5_leftborder = road.get_sensordata(car12.c4, car12.s05)
s7_rightborder, s7_leftborder = road.get_sensordata(car12.c4, car12.s07)
s9_rightborder, s9_leftborder = road.get_sensordata(car12.c4, car12.s09)
print("sensors orange ")
print("sensor 1, distance to RIGHT border: ", s1_rightborder)
print("sensor 1, distance to LEFT border: ", s1_leftborder)
print("sensor 3, distance to RIGHT border: ", s3_rightborder)
print("sensor 3, distance to LEFT border: ", s3_leftborder)
print("sensor 5, distance to RIGHT border: ", s5_rightborder)
print("sensor 5, distance to LEFT border: ", s5_leftborder)
print("sensor 7, distance to RIGHT border: ", s7_rightborder)
print("sensor 7, distance to LEFT border: ", s7_leftborder)
print("sensor 9, distance to RIGHT border: ", s9_rightborder)
print("sensor 9, distance to LEFT border: ", s9_leftborder)

# collision test
collision_car08 = road.collision_check(car08)
print("collision or outside olive ", collision_car08)

# time measuring
t1 = t.time()-t0
print("elapsed time [s]: ", t1)  

# optional rendering
if VISUALIZE == True:
    win_env.update()
    win_env.mainloop()


