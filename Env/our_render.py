# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 19:06:30 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from shapely.geometry import LineString
import numpy as np
import tkinter as tk


class Render():
    """
    Class to render the car with sensors and the street. 
    The size of the street is fitted into the Canvas.
    
    ...
    
    Attributes
    ----------
    render_gui : tkinter.Tk
        parent window for the canvas.
    CANVAS_WIDTH: int
        Width of the canvas.
    CANVAS_HEIGHT: int
        Height of the canvas.
    RENDER_ANY: int
        Steps between each render-process.
    canvas : tkinter.Canvas
        The canvas window.
    render_step : int
        Counter for the number of update-calls.
    render_step_array : np.ndarray with size [ ,2]
        Array of steps.
    num_Resumes : int
        Counter for the number of resumes.
    F_res : int or float
        Resulting tire forces.
    P : int or float
        Current power amount of car.
    done : bool
        Detects whether the rendering steps are finished.
    stop : bool
        Detects whether user would like to stop the rendering.

    Methods
    -------
    def update(self, env, done, info=None, plot_performance=False, delete_old = True, color="blue"):
        Initiates update process of render window, 
        regarding all corresponding properties.
    def close_render(self):   
        Initiates the closing process of render window.
    """
    
    
    def __init__(self):
        """
        
        Initializes object.
        Creates a canvas in which the road, the car and other 
        (partially optional) information will be rendered.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        
        # self.render_gui = render_gui
        self.render_gui = tk.Tk() # parent window for canvas
        self.render_gui.title('our_render')
        tk.Button(self.render_gui, text="Quit", command=self.close_render, width=10).pack()
        self.CANVAS_WIDTH = 1725
        self.CANVAS_HEIGHT = 700
        self.xmax = 2000
        self.GREY = '#aaaaaa'
        self.BLACK = '#000000'
        self.RENDER_ANY = 1
        self.canvas = tk.Canvas(self.render_gui, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg='white') # canvas is the rendering area
        self.canvas.pack() # required to visualize the canvas
        self.render_step = 0
        self.render_step_array = []
        self.num_Resumes = 0
        self.F_res = []
        self.P = []
        self.RewardCheck = []
        self.done = False
        self.stop = False
        self.F_data = []
        self.P_data = []
        self.R_data = []


    def update(self, env, done, info=None, plot_performance=False, delete_old = True, color="blue"):
        """
        
        Returns the relative (default) or absolute distance from the first point of the road to a specified point, 
        measured along the lane centerline.

        Parameters
        ----------
        env : env_PaceRace.PaceRaceEnv
            The whole Reinforcement learning environment.
        done : bool, optional
            Detects whether the rendering steps are finished.
        plot_performance : bool, optional
            Detects whether performance info should be plotted during
            the rendering process.
        delete_old : bool, optional
            Detects whether old car position should be deleted
            before the next rendering.
        color: str, optional
            Color of the car.
        
        Returns
        -------
        None.
        
        """

        self.done = done
        if self.render_step == 0:  # NEU ERSETZT
        
            # set whether old car should be deleted
            self.delete_old = delete_old
            
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
            x_m = [-100 + self.X/2-(5*self.factor), -100 + self.X/2+(5*self.factor)]
            y_m = [self.Y-10, self.Y-10]
            measure_line_data = list((np.ravel(([x_m,y_m]),'F')))
            self.canvas.create_line(measure_line_data, width=6)

            # generate measurement text
            self.canvas_text_pixel= self.canvas.create_text(-92 + self.X/2+(5*self.factor), self.Y-25, anchor="nw")
            self.canvas.itemconfig(self.canvas_text_pixel, text="=10m (1 Pixel:  m),")
            str_meter_pro_pixel = '{:.2f}'.format(1/self.factor)
            self.canvas.insert(self.canvas_text_pixel, 15, str_meter_pro_pixel)
           
            # generate resume-counter 
            self.canvas_text_resumes = self.canvas.create_text(95 + self.X/2+(5*self.factor), self.Y-25, anchor="nw")
            self.canvas.itemconfig(self.canvas_text_resumes, text="amount of resumes: ")
            str_num_resumes = '{:.0f}'.format(self.num_Resumes)
            self.canvas.insert(self.canvas_text_resumes, 19, str_num_resumes)
            
            if plot_performance == True:

                # prepare the subplots
                self.plot_fig = Figure(figsize = (11.5, 2.4),dpi = 100)
                self.plot_fig.tight_layout()
                x = np.linspace(0, self.xmax, self.xmax+1)
                
                # adding subplot1
                self.plot1 = self.plot_fig.add_subplot(131,xlabel='Iteration (Step)',ylabel='F_res [N]', title='Resulting Force', box_aspect=1/2.3)
                self.plot1.plot(x,np.ones((self.xmax+1,1))*env.Fmax, color = 'red', linewidth = 0.5)
                self.plot1.set_xlim(0,self.xmax)
                self.plot1.set_ylim(0,1.05*env.Fmax)
                self.scat1 = self.plot1.scatter(0,0, marker='.', color='blue', s=0.5,linewidth = 0.7)
                
                # adding subplot2
                self.plot2 = self.plot_fig.add_subplot(132,xlabel='Iteration (Step)',ylabel='P [Nm/s/norm]', title = 'Absolute amount of Power', box_aspect=1/2.3)
                self.plot2.plot(x,np.ones((self.xmax+1,1))*(-1), color = 'red', linewidth = 0.5)
                self.plot2.plot(x,np.zeros((self.xmax+1,1)), color = 'black', linewidth = 0.5)
                self.plot2.plot(x,np.ones((self.xmax+1,1))*1, color = 'red', linewidth = 0.5)
                self.plot2.set_xlim(0,self.xmax)
                self.plot2.set_ylim(-1.10,1.10)
                self.scat2 = self.plot2.scatter(0,0, marker='.', color='blue', s=0.5,linewidth = 0.7)
                
                # adding subplot3
                self.plot3 = self.plot_fig.add_subplot(133,xlabel='Iteration (Step)',ylabel='SumRewards [1]', title = 'RewardCheck', box_aspect=1/2.3)
                self.plot3.plot(x,np.zeros((self.xmax+1,1)), color = 'black', linewidth = 0.5)
                self.plot3.set_xlim(0,self.xmax)
                self.plot3.set_ylim(-1.10,1.10)
                self.scat3 = self.plot3.scatter(0,0, marker='.', color='blue', s=0.5,linewidth = 0.7)

                self.plot_fig.tight_layout()
                
                # creating the Tkinter canvas which contains the Matplotlib figures
                self.plot_canvas = FigureCanvasTkAgg(self.plot_fig,master = self.render_gui)
                self.plot_canvas.get_tk_widget().pack()

        # generate resume-counter
        if info['num_Resumes']> self.num_Resumes:
            self.num_Resumes = info['num_Resumes']
            str_num_resumes = '{:.0f}'.format(self.num_Resumes)
            self.canvas.delete(self.canvas_text_resumes)
            self.canvas_text_resumes = self.canvas.create_text(95 + self.X/2+(5*self.factor), self.Y-25, anchor="nw")
            self.canvas.itemconfig(self.canvas_text_resumes, text="amount of resumes: ")
            self.canvas.insert(self.canvas_text_resumes, 19, str_num_resumes)
            
        # generate the performance efficiency data arrays like power and centrifugal force
        if plot_performance == True:
            if info != None:

                # get resolution forces
                F_res = info['Fres']
                self.F_res.append(F_res)
                
                # get power
                P = info['act'][0]
                self.P.append(P)
                
                # get sum_rewards
                RewardCheck = info['RewardCheck']
                self.RewardCheck.append(RewardCheck)
                
                # set it together
                self.render_step_array.append(np.shape(self.render_step_array)[0])
                self.F_data.append([np.shape(self.render_step_array)[0],F_res])
                self.P_data.append([np.shape(self.render_step_array)[0],P])
                self.R_data.append([np.shape(self.render_step_array)[0],RewardCheck])
                min_R_data = np.min(self.R_data)
                max_R_data = np.max(self.R_data)
                
                # plot the performance efficiency data
                if self.render_step % 100 == 0:
                    
                    self.scat1.set_offsets(self.F_data)
                    self.plot1.set_xlim(0,self.render_step)
                    # self.scat1.update_scalarmappable()
                    self.scat1.axes.figure.canvas.draw_idle()
                    
                    self.scat2.set_offsets(self.P_data)
                    self.plot2.set_xlim(0,self.render_step)
                    # self.scat2.update_scalarmappable()
                    self.scat2.axes.figure.canvas.draw_idle()

                    self.scat3.set_offsets(self.R_data)
                    self.plot3.set_xlim(0,self.render_step)
                    self.plot3.set_ylim(min_R_data,max_R_data)
                    self.scat3.update_scalarmappable()
                    self.scat3.axes.figure.canvas.draw_idle()
                    
                    # self.plot_fig.canvas.flush_events() 
            else:
                print('No Info loaded')

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
        if self.render_step !=0 and self.delete_old == True: # NEU ERSETZT
            sensor_color = self.BLACK
            self.canvas.delete(self.car_polygon)
            self.canvas.delete(self.car_s01)
            self.canvas.delete(self.car_s03)
            self.canvas.delete(self.car_s05)
            self.canvas.delete(self.car_s07)
            self.canvas.delete(self.car_s09)
        else:
            sensor_color = self.GREY
        self.car_polygon = self.canvas.create_polygon(car01_data, fill=color, width=1)
        self.car_s01 = self.canvas.create_line(s01_line_data, fill=sensor_color, width=1)
        self.car_s03 = self.canvas.create_line(s03_line_data, fill=sensor_color, width=1)
        self.car_s05 = self.canvas.create_line(s05_line_data, fill=sensor_color, width=1)
        self.car_s07 = self.canvas.create_line(s07_line_data, fill=sensor_color, width=1)
        self.car_s09 = self.canvas.create_line(s09_line_data, fill=sensor_color, width=1)

        self.render_step += 1 # NEU
        
        if self.done == False:
            self.render_gui.update()
        if self.stop == True:
            self.render_gui.destroy()
        if self.done == True:
            print(f'End of race, {self.render_step} steps needed.')
            self.render_gui.mainloop()

        return self.stop

    
    def close_render(self):
        """
        
        Initiates the closing process of render window.

        Parameters
        ----------
        None.
        
        Returns
        -------
        None.
        
        """
        self.stop = True
        if self.done:
            self.render_gui.destroy()



