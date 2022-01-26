# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 19:06:30 2022

@author: felix
"""
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from shapely.geometry import LineString

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class Render():
    def __init__(self):
        
        self.render_gui = tk.Tk() # parent window for canvas
        tk.Button(self.render_gui, text="Quit", command=self.render_gui.destroy).pack()
        self.CANVAS_WIDTH = 1600
        self.CANVAS_HEIGHT = 900
        self.RENDER_ANY = 1
        self.canvas = tk.Canvas(self.render_gui, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT) # canvas is the rendering area
        self.canvas.pack() # required to visualize the canvas    
        self.render_step = 0
        self.render_step_array = []
        self.F_ctfg = []
        self.P = []
        self.delete_old = True

    def update(self, env, done, info=None, plot_performance=False, color="blue"):
        
        if self.render_step == 0:  # NEU ERSETZT
            
            # get canvas height for up-down-flipping
            self.Y = self.canvas.winfo_reqheight()-4 # height of canvas, minus 4 is necessary
            self.X = self.canvas.winfo_reqwidth()-4 # width of canvas, minus 4 is necessary
    
            # extract road data
            x, y   = LineString(env.road.center_line).xy
            xl, yl = LineString(env.road.left_line).xy
            xr, yr = LineString(env.road.right_line).xy
            y = np.subtract(self.Y, y)
            yl = np.subtract(self.Y, yl)
            yr = np.subtract(self.Y, yr)
            
            # get data for best adaption of the road into the canvas
            self.min_x = min(min(x)-env.roadwidth, min(x)+env.roadwidth)
            max_x = max(max(x)-env.roadwidth, max(x)+env.roadwidth)
            self.min_y = min(min(y)-env.roadwidth, min(y)+env.roadwidth)
            max_y = max(max(y)-env.roadwidth, max(y)+env.roadwidth)
            delta_x = max_x - self.min_x
            delta_y = max_y - self.min_y
            self.factor_x = self.CANVAS_WIDTH / delta_x
            self.factor_y = self.CANVAS_HEIGHT / delta_y
            self.factor = min(self.factor_x, self.factor_y) # resizing self.factor, e.g. FAKTOR=10 => 10pixel==1m
    
            # align road data to render_gui
            x = self.factor * np.add(x, -self.min_x)
            y = self.factor * np.add(y, -self.min_y)
            xl = self.factor * np.add(xl, -self.min_x)
            yl = self.factor * np.add(yl, -self.min_y)                
            xr = self.factor * np.add(xr, -self.min_x)
            yr = self.factor * np.add(yr, -self.min_y)
            
            # generate road lines
            center_line_data = list((np.ravel(([x,y]),'F'))) # list is neccessary for a correct separation with comma             
            self.canvas.create_line(center_line_data, dash=(4), fill="grey", width=1)
            left_line_data   = list((np.ravel(([xl,yl]),'F'))) # list is neccessary for a correct separation with comma
            self.canvas.create_line(left_line_data, fill="brown", width=2)
            right_line_data  = list((np.ravel(([xr,yr]),'F'))) # list is neccessary for a correct separation with comma
            self.canvas.create_line(right_line_data, fill="brown", width=2)
    
            # generate 10m-measure-line
            x_m = [self.X/2-(5*self.factor), self.X/2+(5*self.factor)]
            y_m = [self.Y-10, self.Y-10]
            measure_line_data = list((np.ravel(([x_m,y_m]),'F')))
            self.canvas.create_line(measure_line_data, width=5)
      
            # generate measurement text
            meter_pro_pixel = 1/self.factor
            self.canvas_id = self.canvas.create_text(10 + self.X/2+(5*self.factor), self.Y-25, anchor="nw")
            self.canvas.itemconfig(self.canvas_id, text="=10m  (1 Pixel entspr.  m)")
            str_meter_pro_pixel = '{:.2f}'.format(meter_pro_pixel)
            self.canvas.insert(self.canvas_id, 23, str_meter_pro_pixel)
            
            if plot_performance == True:
                
                # create figure that will contain the plots
                self.plot_fig = Figure(figsize = (12.5, 3.9),dpi = 100)
                
                # adding the subplots            
                self.plot1 = self.plot_fig.add_subplot(121,xlabel='Iteration (Step)',ylabel='F_ctfg [N]', title='Centrifugal Force', box_aspect=1/1.5)
                self.plot2 = self.plot_fig.add_subplot(122,xlabel='Iteration (Step)',ylabel='P [Nm/s]', title = 'Absolute amount of power', box_aspect=1/1.5)
    
                # creating the Tkinter canvas which contains the Matplotlib figures
                self.plot_canvas = FigureCanvasTkAgg(self.plot_fig,master = self.render_gui)  
                self.plot_canvas.get_tk_widget().pack()
            
        # generate the performance efficiency data arrays like power and centrifugal force
        if plot_performance == True: 
            if info != None:
                P = env.car01.vlon * info['Fres']
                self.P.append(P)
                F_ctfg = env.car01.M * env.car01.omega * env.car01.vlon
                self.F_ctfg.append(F_ctfg)
      
                # plot the performance efficiency data
                if self.render_step % 100 == 0:
                    self.render_step_array = np.arange(0,self.render_step+1,1)
                    # self.plot1.plot(self.render_step_array,self.F_ctfg, color = 'blue', linewidth = 0.5)
                    self.plot1.scatter(self.render_step_array,self.F_ctfg, marker='.', color='blue', s=0.5,linewidth = 0.5)
                    self.plot1.plot(self.render_step_array,np.repeat(0,np.shape(self.render_step_array)[0]), color = 'black', linewidth = 0.5)
                    self.plot2.plot(self.render_step_array,self.P, color = 'blue', linewidth = 0.5)
                    # self.plot2.scatter(self.render_step_array,self.P, marker='.', color='blue', s=0.5,linewidth = 0.5)
                    self.plot2.plot(self.render_step_array,np.repeat(env.max_power,np.shape(self.render_step_array)[0]), color = 'red', linewidth = 0.5)
                    self.plot_canvas.draw()
                    # self.plot_canvas.flush_events()
            else:
                pass
                # print('These are the values of interest')
                # print()
                # print(f'render_step: {self.render_step}')
                # print(f' Fctfg: {env.car01.M * env.car01.omega * env.car01.vlon}')  
                # print(f'P: {P}')

        # extract and align car data
        x_car = env.car01.corners[:,0]
        y_car = np.subtract(self.Y, env.car01.corners[:,1])
        x_car = self.factor * np.add(x_car, -self.min_x)
        y_car = self.factor * np.add(y_car, -self.min_y)
        car01_data = list((np.ravel(([x_car,y_car]),'F'))) # list is neccessary for a correct separation with comma
        
        # extract and align sensor data
        x_s01 = [env.car01.corners[3,0], env.car01.sensors[0,0]]
        y_s01 = [self.Y-env.car01.corners[3,1], self.Y-env.car01.sensors[0,1]]
        x_s01 = self.factor * np.add(x_s01, -self.min_x)
        y_s01 = self.factor * np.add(y_s01, -self.min_y)
        s01_line_data = list((np.ravel(([x_s01,y_s01]),'F'))) # list is neccessary for a correct separation with comma
        x_s03 = [env.car01.corners[3,0], env.car01.sensors[1,0]]
        y_s03 = [self.Y-env.car01.corners[3,1], self.Y-env.car01.sensors[1,1]]
        x_s03 = self.factor * np.add(x_s03, -self.min_x)
        y_s03 = self.factor * np.add(y_s03, -self.min_y)
        s03_line_data = list((np.ravel(([x_s03,y_s03]),'F'))) # list is neccessary for a correct separation with comma
        x_s05 = [env.car01.corners[3,0], env.car01.sensors[2,0]]
        y_s05 = [self.Y-env.car01.corners[3,1], self.Y-env.car01.sensors[2,1]]
        x_s05 = self.factor * np.add(x_s05, -self.min_x)
        y_s05 = self.factor * np.add(y_s05, -self.min_y)
        s05_line_data = list((np.ravel(([x_s05,y_s05]),'F'))) # list is neccessary for a correct separation with comma
        x_s07 = [env.car01.corners[3,0], env.car01.sensors[3,0]]
        y_s07 = [self.Y-env.car01.corners[3,1], self.Y-env.car01.sensors[3,1]]
        x_s07 = self.factor * np.add(x_s07, -self.min_x)
        y_s07 = self.factor * np.add(y_s07, -self.min_y)
        s07_line_data = list((np.ravel(([x_s07,y_s07]),'F'))) # list is neccessary for a correct separation with comma
        x_s09 = [env.car01.corners[3,0], env.car01.sensors[4,0]]
        y_s09 = [self.Y-env.car01.corners[3,1], self.Y-env.car01.sensors[4,1]]
        x_s09 = self.factor * np.add(x_s09, -self.min_x)
        y_s09 = self.factor * np.add(y_s09, -self.min_y)
        s09_line_data = list((np.ravel(([x_s09,y_s09]),'F'))) # list is neccessary for a correct separation with comma
        
        
        # generate car and sensor data
        # if iteration !=0 and delete_old == True: 
        if self.render_step !=0 and self.delete_old == True: # NEU ERSETZT
            self.canvas.delete(self.car_polygon)
            self.canvas.delete(self.car_s01)
            self.canvas.delete(self.car_s03)
            self.canvas.delete(self.car_s05)
            self.canvas.delete(self.car_s07)
            self.canvas.delete(self.car_s09)
        self.car_polygon = self.canvas.create_polygon(car01_data, fill=color, width=1)
        self.car_s01 = self.canvas.create_line(s01_line_data, fill="black", width=1)
        self.car_s03 = self.canvas.create_line(s03_line_data, fill="black", width=1) 
        self.car_s05 = self.canvas.create_line(s05_line_data, fill="black", width=1) 
        self.car_s07 = self.canvas.create_line(s07_line_data, fill="black", width=1) 
        self.car_s09 = self.canvas.create_line(s09_line_data, fill="black", width=1) 
      
        self.render_step += 1 # NEU
        
        if done:
            print("End of race")
            self.render_gui.destroy()
        else:
            self.render_gui.update()