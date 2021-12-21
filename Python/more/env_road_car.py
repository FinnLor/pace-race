# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

- done:                     set_resume_pos: 
                            setzt Position zurück auf Mittellinie

- done:                     collision_check:
                            true zurückgeben wenn zB entferntester 
                            carpolygonpunkt weiter weg von Spurmitte
    
- minimalistic done:        get_sensor:  
                            1. entfernung zu den jew sensor-intersections
                            2. weitere sensoren zufügen (noch nicht)
    
- maßstäbe:                 für Weg, Zeit, Geschwindigkeit definieren.

- option:                   "test_ls = track.simplify(1,True)" aus shapely könnte für komplexe polygonlines nützlich sein



ACHTUNG: 
Dieses File beinhaltet derzeit die Klasse 'car', die Klasse 'road' und die aufrufende Umgebung.
Die Beschreibungen dieser drei Komponenten finden sich jeweils zu Beginn des entsprechenden Codes.

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



class car:
    
    '''
    Die Klasse 'car' beschreibt im Wesentlichen das geometrische Objekt 'car' 
    und bietet dem Anwender die Option, die Position zu bestimmen und 
    positions- kollisions- und Sensordaten abzufragen
    Die Geometrie von 'car' besteht aus: 
        - einem geschlossenen Polygon mit fünf Punkten, 
        - einem Drehpunktzentrum des Fahrzeugs und
        - mindestens einem Sensor, bestehend aus einer Linie mit zwei Punkten: 
                --- dem Sensorreferenzpunkt, der gleichzeitig Sensordrehpunkt 
                    ist und für alle Sensoren der selbe ist.
                --- dem Sensorendpunkt.
    Der car-Polygonzug dreht sich in Abhängigkeit zum Winkel 'psi'
    Der Sensor / die Sensoren drehen sich in Abhängigkeit zum eingeschlagenen 
    Lenkwinkel 'delta'.
    Die Klasse 'car' benötigt die Klasse 'canvas' zur Datenformatierung, 
    Datenverwaltung und zum optionalen Rendern.
    Folgende Methoden stehen zur Verfügung
    (BEISPIELE zur Instanzierung und zur Nutzung der implementierten Methoden 
     befinden sich in der aufrufenden Umgebung):
        - set_car_pos: 
            HAUPTFUNKTION zum Setzen des 'car'. Der Anwender gibt die
            Koordinaten x[m], y[m], psi[rad] und delta[rad] vor.
        - get_car_polygon: 
            Bislang nur zur visuellen Kontrolle benötigt.
        - get_car_center:  
            Bislang nur zur visuellen Kontrolle benötigt. 
        - set_start_pos: 
            Setzt 'car' auf Startposition der Strecke und richtet
            'car' auch korrekt aus.
            Der Lenkeinschlag 'delta' wird dabei auf '0[rad]' gesetzt
            Die Methode benötigt die Mittellinie der Strecke als Übergabe.
        - set_resume_pos:
            Setzt 'car' (u.a. nach einer Kollision) wieder korrekt ausgerichtet
            im kürzesten Abstand auf die Mittellinie der Strecke zurück. 
            Der Lenkeinschlag wird hierbei auf 'delta = 0 [rad]' zurückgesetzt.
            Die Methode benötigt Mittel- und Randlinien der Strecke.
        - set_reset_pos:
            Bislang nur zur visuellen Kontrolle benötigt.
     
    '''
    
    
    def __init__(self,canvas,x,y,psi,delta,FACTOR,SENSFACTOR,color):
        
        # initialize
        self.FACTOR = FACTOR # resizing FACTOR, e.g. FAKTOR=10 => 10pixel==1m
        self.SENSFACT = SENSFACTOR # scaling factor for sensors as a multiplier of car length
        self.canvas = canvas
        self.psi = psi # car_angle
        self.delta = delta # front_wheel_angle
        self.color = color 
        self.dc = (0, 0) # velocity of car_center
        self.cl = 4 * self.FACTOR # car length
        self.cw = 2 * self.FACTOR # car width
        self.c1 = (x-self.cl/2, y+self.cw/2) # create upper left corner of car
        self.c2 = (x-self.cl/2, y-self.cw/2) # create bottom left corner of car
        self.c3 = (x+self.cl/2, y-self.cw/2) # create bottom right corner of car
        self.c4 = (x+self.cl/1.5, y) # create sensor_center of car
        self.c5 = (x+self.cl/2, y+self.cw/2) # create upper right corner of car
       
        # initialize sensors
        # self.s01 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s02 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s03 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s04 = (self.c4[0], self.c4[1]-self.cw*3/4)
        self.s05 = (self.c4[0]+self.SENSFACT*self.cl, self.c4[1]) # create sensor point no 05
        # self.s06 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s07 = (self.c4[0], self.c4[1]+self.cw*3/4)
        # self.s08 = (self.c4[0], self.c4[1]-self.cw*3/4)
        # self.s09 = (self.c4[0], self.c4[1]+self.cw*3/4)

        # further initializations
        self.car_center = canvas.create_bitmap(x, y) # car_center position
        self.car_polygon = canvas.create_polygon(self.c1, self.c2, self.c3, self.c4, self.c5, fill = self.color)
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color)
        self._car_rot_d(psi) # call method _car_rot_d
        self._sensor_rot(delta) # call method _sensor_rot


   
    def _car_move_d(self,dx,dy,dpsi): # difference-movement and -rotation
        
        self.dc = (dx, dy) # velocity of car
        self.dpsi = dpsi # angle velocity of car
        self._car_rot_d(dpsi) # let the car rotate with the desired delta-psi
        self.canvas.move(self.sensor05,self.dc[0],self.dc[1])
        self.canvas.move(self.car_center,self.dc[0],self.dc[1]) # move the car_center
        self.canvas.move(self.car_polygon,self.dc[0],self.dc[1]) # move the car_polygon



    def _car_rot_d(self,dpsi): # only _car_rotation difference

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
        
        # generate relative horizontal sensor vectors
        s05_h_r = (self.SENSFACT*self.cl, 0) # sensor s05 horizontal and relative to sensor_center

        # rotate sensor vectors
        deltapsi = delta + self.psi
        rot = np.array([[np.cos(deltapsi), np.sin(deltapsi)], [-np.sin(deltapsi), np.cos(deltapsi)]]) # rotation matrix physically correct  
        cc_s05n = np.dot(rot, s05_h_r) # new relative sensor point position

        # set absolute sensor vectors
        self.s05 = (cc_s05n[0] + self.c4[0], cc_s05n[1] + self.c4[1]) # update vector from canvas_GUI to s05
        
        # update sensor data
        self.canvas.delete(self.sensor05) # delete old sensor
        self.sensor05 = canvas.create_line((self.c4,self.s05) , fill = self.color) # set new, rotated sensor data
    
 
    ### SET ARBITRARY CAR POSITION
    def set_car_pos(self,x,y,psi,delta): # set new car postion and angles (with zero velocities)
        
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
        
        # set new car_center
        self.canvas.delete(self.car_center) # delete old car_center
        self.car_center = canvas.create_bitmap(x, y)
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
        y = center_line[1]
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
        
        # detect psi for resumed car_direction
        c_c_dr = c_c.distance(road_lsr) # distance from car_center to right road line
        c_c_dl = c_c.distance(road_lsl) # distance from car_center to left road line
        c_c_np = np.array(c_c)
        v_x = np.array([10, 0])
        
        if c_c_dl != c_c_dr:
            if c_c_dl > c_c_dr:
                rot = np.array([[np.cos(m.pi/2), -np.sin(m.pi/2)], [np.sin(m.pi/2), np.cos(m.pi/2)]]) # rotation matrix clockwise 
            elif c_c_dl < c_c_dr:
                rot = np.array([[np.cos(m.pi/2), np.sin(m.pi/2)], [-np.sin(m.pi/2), np.cos(m.pi/2)]]) # rotation matrix counter-clockwise 
            v_forward = np.dot(rot,(c_c_np - point_on_line)) # get forward-direction  
            if v_forward[1] > 0:
                psi_forward = -np.arccos(np.dot(v_forward,v_x)/(np.linalg.norm(v_forward)*np.linalg.norm(v_x))) 
            else:
                psi_forward = np.arccos(np.dot(v_forward,v_x)/(np.linalg.norm(v_forward)*np.linalg.norm(v_x))) 
            self.set_car_pos(point_on_line[0],point_on_line[1],psi_forward,0)
        
        else:
            print("Check whether car is already set to start or resume position.")

        
    ### RESET CAR POSITION INTO x=0, y=0 (top left)   
    def set_reset_pos(self):

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
    '''
    Die Klasse 'road' erzeugt beim Instanzieren eine einfache, zufällig
    parametrisierte Strecke und beinhaltet eine Mittellinie und einen daraus
    abgeleiteten aber explizit vorhandene linken und rechten Rand.
    Die Klasse 'road' benötigt die Klasse 'canvas' zur Datenformatierung, 
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
    - collision_check:
        Bool-Rückgabe, ob eine Kollision detektiert wurde.
        Benötigt das Objekt 'car'.
        Hinweis zum Algorithmus: Es wird der minimale Abstand jedes einzelnen 
        Polygonpuntkes von 'car' zur Mittellinie ermittelt. Wenn davon der 
        größte Wert die halbe Straßenbreite überschreitet, wird 'collision=True'
        gesetzt. Das Package 'shapely' gewährleistet, dass der geringste
        Abstand (Normalenabstand) über den ganzen Polygonzug ermittelt wird 
        und nicht nur zu den Polygonpunkten.
    - get_sensordata:        
        Gibt den Abstand des Sensors zu BEIDEN Rändern zurück.
        Falls die 'Sensorreichweite' nicht bis zum 'Rand' kommt, gibt die 
        Methode die maximale Sensorreichweite an.
        Falls innerhalb der 'Sensorreichweite' mehrere 'intersection' mit 
        einem Rand vorhanden sind, wird der kürzeste Abstnand angegeben.
        Benötigt das Objekt 'car'.
        
        TODO:
        Derzeit wird nur EIN sensor ausgewertet (der einige Meter vor 'car', 
        jedoch in 'delta-richtung')
        Die noch anstehende Implementierung sieht die Implementierung 
        weiterer Sensoren vor. Die Rückgabe wird dann ein nx2-Array sein
        (n: Anzahl Sensoren, 2: je ein Abstandswert f d linken u rechten Rand)
        
    HINWEIS: das Potenzial der Klasse könnte mit 
    "test_ls = track.simplify(1,True)" aus shapely höchstwahrscheinlich 
    effizienter gestaltet werden
    '''
    
    
    def __init__(self,canvas,FACTOR,WIDTH,HEIGHT,NPOINTS, ROADWIDTH):
        
        # initialize important road data
        self.canvas = canvas
        self.FACTOR = FACTOR # dimension, e.g. FAKTOR=10 => 10pixel==1m
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.NPOINTS = NPOINTS
        self.ROADWIDTH = ROADWIDTH
        
        # generate center line of road random-supported
        n = np.linspace(0.5, 2*m.pi, self.NPOINTS)
        x = m.pow((-1),rnd.randrange(1,3,1)) * (n + 3*rnd.uniform(0,1)*np.tan(0.2*n))
        y = 1./n + rnd.uniform(0,1)*3.*np.cos(n)*np.power(np.sin(n),2)

        # align road into canvas
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
                
        # generate road- and border data 
        line_data  = list((np.ravel(([x,y]),'F'))) # list is neccessary for a correct separation with comma
        road_center_ls = LineString(np.reshape(line_data,(self.NPOINTS,2)))
        road_right_line1 = np.array(road_center_ls.parallel_offset(self.FACTOR*self.ROADWIDTH/2,"right",join_style=1))
        road_right_line = list((np.ravel(([road_right_line1[:,0],road_right_line1[:,1]]),'F')))
        road_left_line1 = np.array(road_center_ls.parallel_offset(self.FACTOR*self.ROADWIDTH/2,"left",join_style=1))
        road_left_line = list((np.ravel(([road_left_line1[:,0],road_left_line1[:,1]]),'F')))
        
        # assign main road data
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
    
   
    
    ### CHECK WHETHER CAR COLLIDES WITH BORDER OR IS OUTSIDE OF BORDER =>
    def collision_check(self,car):
        
        # get car border points
        c_p1 = Point(car.c1)
        c_p2 = Point(car.c2)
        c_p3 = Point(car.c3)
        c_p4 = Point(car.c4)
        c_p5 = Point(car.c5)
        
        # get center line of road
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
    def get_sensordata(self,car):
        
        # transform sensor data
        l1 = np.array([car.c4,car.s05])
        ref_p = Point(l1[0,:]) # Reference point, source of all Sensor_lines
        l1_p = Point(l1[1,:]) # Outer sensor point
        l1_ls = LineString(l1)
        
        # get and transform right and left border data
        right_line = self.canvas.coords(self.road_right_line) 
        rd_rl = np.array(right_line)
        size_rl = np.shape(rd_rl)[0]
        rs_rl = np.reshape(right_line,(int(0.5*size_rl),2))
        road_lsr = LineString(rs_rl)
        isp_r = np.array(l1_ls.intersection(road_lsr)) # absolute position of intersection point(s) of sensor with right BORDER
        left_line = self.canvas.coords(self.road_left_line) 
        rd_ll = np.array(left_line)
        size_ll = np.shape(rd_ll)[0]
        rs_ll = np.reshape(left_line,(int(0.5*size_ll),2))
        road_lsl = LineString(rs_ll)
        isp_l = np.array(l1_ls.intersection(road_lsl)) # absolute position of intersection point(s) of sensor with left BORDER
        
        # collect all distances for the sensor
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
        
        return dist1_l, dist1_r # returns left and right distances
    
    
    
    


#################################
### ENVIRONMENT COMMUNICATION ###
#################################

'''
Umgebung mit
- Initialisierung der Umgebungsdaten
- Instanzierung der Klassen 'car' und 'road'
- Tests der entsprechenden Methoden
- Aufruf der Renderfunktionalität 'win_env.update()'
Beinhaltet:
- win_env: GUI-parent class, including: canvas: method for generating, saving 
and rendering. positive-x goes right, positive-y goes down.

TODO:
- Teile davon (Initialisierungs- und Renderaufrufe)
 müssen wohl in die eigentliche aufrufende Funktion überführt werden
 
- hab' folgende Warnmeldung noch nicht wegbekommen: 
"ShapelyDeprecationWarning: The array interface is deprecated and will no 
longer work in Shapely 2.0. Convert the '.coords' to a numpy array instead.
'''

### CONFIGURE ENVIRONMENT BASICS
win_env = tk.Tk() # parent window for the canvas
WIDTH = 1800
HEIGHT = 900
VISUALIZE = True
NPOINTS = 1000 # no of points of the central road line
ROADWIDTH = 8
FACTOR = 10 # resizing FACTOR, e.g. FAKTOR=10 => 10pixel==1m
SENSFACTOR = 7 # resizing factor for sensors, e.g. SENSFACTOR = 5 => longest sensor distance is 5 times car-length
canvas = tk.Canvas(win_env, width=WIDTH, height=HEIGHT) # rendering area in GUI for cars, theirs sensors and a road
canvas.pack() # ist required to visualize the canvas
button = tk.Button(win_env, text='enough', command = lambda:win_env.destroy()).pack(expand=True) # EXPERIMENTAL added button for closing GUI

### CONSTRUCT ROAD
c_road = road(canvas,FACTOR,WIDTH,HEIGHT,NPOINTS, ROADWIDTH)

### CONSTRUCT CARS
car01 = car(canvas, 140, 20,  0, 0, FACTOR, SENSFACTOR, "yellow")
car02 = car(canvas, 100, 200,  0.6, -0.6, FACTOR, SENSFACTOR, "green")
car03 = car(canvas, 110,  90,    0,   0, FACTOR, SENSFACTOR, "blue")
car04 = car(canvas, 180, 100,    1,   1, FACTOR, SENSFACTOR, "black")
car05 = car(canvas, 900, 400,  1.3, 1.3, FACTOR, SENSFACTOR, "pink")
car06 = car(canvas, 300, 500,  1.3, -1.3, FACTOR, SENSFACTOR, "brown")
car07 = car(canvas, 140,  10,  0.4, -0.4, FACTOR, SENSFACTOR, "red")
car08 = car(canvas, 750, 300,  0.6, 0.6, FACTOR, SENSFACTOR, "olive")
car09 = car(canvas, 110,  90,    0,   0, FACTOR, SENSFACTOR, "cyan")
car10 = car(canvas, 120, 100,    1,   1, FACTOR, SENSFACTOR, "purple")
car11 = car(canvas, 700, 300,  1.3, -1.3, FACTOR, SENSFACTOR, "gray")
car12 = car(canvas, 200, 600,  1.3, 1.3, FACTOR, SENSFACTOR, "orange")
  
### TESTS
road_lsc = LineString(np.reshape(c_road.get_center_line(), (NPOINTS,2)))

t0 = t.time()
for i in range(0,100):

    # collision1 test
    collision1 = c_road.collision_check(car01)
    #print("COLLISION1 ", collision1)
    
    # distance test
    c02_data = Polygon(np.reshape(car01.get_car_polygon(), (5,2)))
    #print("Distance blue car <-> road ", road_lsc.distance(c02_data))

    # set car test
    car03.set_car_pos(rnd.uniform(0,WIDTH), rnd.uniform(0,HEIGHT), rnd.uniform(0,2*m.pi), rnd.uniform(0,2*m.pi))

    # car moving test
    car04._car_move_d(1.0,1.5,-0.10)

    # car sensor rotation test
    car05._sensor_rot(-0.7+i/100)
    
    # car rotation test
    car06._car_rot_d(-0.1)
    
    if VISUALIZE == True:
        win_env.update()
        t.sleep(0.005)

# car resume position and collide test
car01.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car02.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car03.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car04.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car05.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car06.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car07.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car08.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car09.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car10.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car11.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
car12.set_resume_pos(c_road.get_center_line(), c_road.get_right_line(), c_road.get_left_line())
collision8 = c_road.collision_check(car08) # test collision second time
#print("COLLISION8 ", collision8)

# car set start pos test
car07.set_start_pos(c_road.get_center_line())

# reset position test
car09.set_reset_pos()

# get sensordata of a car
s5_leftborder, s5_rightborder = c_road.get_sensordata(car03)
#print("sensor 5, distance to LEFT border: ", s5_leftborder)
#print("sensor 5, distance to RIGHT border: ", s5_rightborder)

if VISUALIZE == True:
    win_env.update()

t1 = t.time()-t0
print("elapsed time [s]: ", t1)  

if VISUALIZE == True:
    win_env.mainloop()


