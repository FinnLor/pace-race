# -*- coding: utf-8 -*-
"""
Created on Jan 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""


from PIL import ImageTk, Image
from stable_baselines3 import SAC
from tkinter import filedialog as fd # für fd.askopenfilename
from tkinter import ttk
import numpy as np
import tkinter as tk

# Custom
from Env.env_PaceRace import PaceRaceEnv
from Env.cls_Render import Render


class UIPace():
    """
    
    Class to provide a user interface to try out some Pace_Race models 
    on a randomly or user generated road.
    
    ...
    
    Attributes
    ----------
    master: tkinter.Tk
        Master parent for the UI.
    CANVAS_WIDTH: int
        Width of the canvas.
    CANVAS_HEIGHT: int
        Height of the canvas.
    ROAD_WIDTH_MIN: int
        Minimal allowed road width.
    ROAD_WIDTH_MAX: int
        Maximal allowed road width.
    road_width: int
        Current road width.
    width_ok: bool
        Checks whether the UI-input of the width is within the allowed range.
    length_ok: bool
        Checks whether the UI-input of the length includes
        at least two points.   
    model_ok: bool
        Checks whether a model is loaded.
    RESOLUTION: int or float 
        The current resolution of the user-road-canvas
        Please do not change this value because changes are not implemented yet.
    points_x : np.ndarray with size [npoints, ]
        Array of x-values of the UI-road-centerpoints.
    points_y : np.ndarray with size [npoints, ]
        Array of y-values of the UI-road-centerpoints.    
    line_data : np.ndarray with size [npoints,2]
        Array of x-y-values of the UI-road-centerpoints.
    GREEN : str
        Predefined color for green background.
    YELLOW : str
        Predefined color for yellow background.
    ORANGE : str
        Predefined color for orange background.
    
    Other UI Widgets which are not listed in detail.
    
    Methods
    -------
 
    apply_RoadWidth(self):
        Applies the user input for the road width.
    extend_RoadPath(self,event):
        Extends the user input for the road width.
    clear_RoadPath(self):
        Deletes the user input of the road.
    apply_RoadPath(self):
        Applies the user input road path.
    _set_status(self): 
        Controls and set the status of the current model and road input data.
    ui_help(self):
        Calls a short Manual for UI_PaceIn.py
    ui_about(self):
        Splash screen with basic information about the project.
    load_Model(self):
        Opens an Interface to load a model.
    random_Track(self):
        Generates a random track and starts the rendering process.
    user_Track(self):
        Applies the user input as a center-line of a track,
        generates that one and starts the rendering process.
    ui_quit(self):
        Closes and quits the UI_Pacein.
    """
    
    def __init__(self,master):
        """
        
        Initializes object.
        Creates an Interface which gives the user the possibility to
        - load a desired model (currently only compatible with SAC-models),
        - apply a desired road width (for the user track),
        - to optionally generate or clear a track, designed from a user,
        - to start a rendering process with a random track or a user track.
        ...

        Parameters
        ----------
        master: tkinter.Tk
            Master parent for the UI.

        Returns
        -------
        None.

        """
        
        # preferences
        self.master = master
        self.CANVAS_WIDTH = 1296
        self.CANVAS_HEIGHT = 584
        self.ROAD_WIDTH_MIN = 8
        self.ROAD_WIDTH_MAX = 40
        self.road_width = int(np.round(0.5*(self.ROAD_WIDTH_MIN+self.ROAD_WIDTH_MAX)))
        self.width_ok = False
        self.length_ok = False
        self.model_ok = False
        self.points_x = []
        self.points_y = []
        self.RESOLUTION = 1 # dont change this 
        self.line_data = []
        self.GREEN = '#B3FFB3'
        self.YELLOW = '#FFFF44'
        self.ORANGE = '#FF8844'

        # static text
        self.label_LoadModelText = tk.Label(self.master, text ='OKS-RL-PACERACE-PROJECT', font=('Arial 12 bold'))
        self.label_LoadModelText.grid(row=0, column=0, sticky = 'W')
        self.label_RoadWidthText = tk.Label(self.master, text =f'Enter width of road as integer. Value range in meter [{self.ROAD_WIDTH_MIN}:{self.ROAD_WIDTH_MAX}]:')
        self.label_RoadWidthText.grid(row=1, column=0, sticky = 'W')
        self.label_RoadPath = tk.Label(self.master, text = f'Set min two points as course of the route (1 pixel = {self.RESOLUTION} meter):')
        self.label_RoadPath.grid(row=2, column=0,sticky = 'W')
        self.label_CloseUI = tk.Label(self.master, text = 'If data is valid so far, the data will be commited for rendering:')
        self.label_CloseUI.grid(row=3, column=0,sticky = 'W')

        # checkbuttons
        self.cb_old = tk.IntVar()
        self.check_PlotOld = tk.Checkbutton(self.master, text = 'Maintain Car Pos', variable=self.cb_old, onvalue = 1, offvalue = 0)
        self.check_PlotOld.grid(row=0, column=1)  
        self.cb_perf = tk.IntVar()
        self.check_PlotPerformance = tk.Checkbutton(self.master, text = 'Plot Performance', variable=self.cb_perf, onvalue = 1, offvalue = 0)
        self.check_PlotPerformance.grid(row=0, column=2)  
        
        # create entry
        self.entry_RoadWidth = tk.Entry(self.master, width = 8)
        self.entry_RoadWidth.grid(row=1, column=2)
        self.entry_RoadWidth.insert('end', self.road_width)
        
        # buttons
        self.button_LoadModel = tk.Button(self.master, text = 'Load Model', command = self.load_Model, width = 15)
        self.button_LoadModel.grid(row=0, column=3)
        self.button_ApplyRoadWidth = tk.Button(self.master, text = 'Apply Width', command = self.apply_RoadWidth, width = 15)
        self.button_ApplyRoadWidth.grid(row=1, column=3)
        self.button_ClearRoadPath= tk.Button(self.master, text = 'Clear Track', command = self.clear_RoadPath, width = 15)
        self.button_ClearRoadPath.grid(row=2, column=2)
        self.button_RandomTrack = tk.Button(self.master, text = 'Apply Track', command = self.apply_RoadPath, width = 15)
        self.button_RandomTrack.grid(row=2, column=3)
        self.button_UserTrack = tk.Button(self.master, text = 'Take Random Track', command = self.random_Track, width = 15)
        self.button_UserTrack.grid(row=3, column=2)
        self.button_UserTrack = tk.Button(self.master, text = 'Take User Track', command = self.user_Track, width = 15)
        self.button_UserTrack.grid(row=3, column=3)

        # interactive text
        self.label_LoadModelCheck = tk.Label(self.master, text = 'No Model loaded', width=25, background=self.ORANGE)
        self.label_LoadModelCheck.grid(row=0, column=4, sticky = 'W')
        self.label_RoadWidthCheck = tk.Label(self.master, text = 'Not valid', width=25, background=self.ORANGE)
        self.label_RoadWidthCheck.grid(row=1, column=4, sticky = 'W')
        self.label_RoadPathCheck = tk.Label(self.master, text = 'Not valid', width=25, background=self.ORANGE)
        self.label_RoadPathCheck.grid(row=2, column=4, sticky = 'W')
        self.label_RoadOkCheck = tk.Label(self.master, text = 'Data not complete', width=25, background=self.ORANGE)
        self.label_RoadOkCheck.grid(row=3, column=4, sticky = 'W')

        # canvas
        self.canvas_pace = tk.Canvas(self.master, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, background='white', offset='s')
        self.canvas_pace.grid(row=5, column=0, columnspan=5)

        # items
        self.item_more = tk.Menu(self.master)
        self.item_about = tk.Menu(self.item_more)
        self.item_about.add_command(label='Help', command=self.ui_help)
        self.item_about.add_command(label='About', command=self.ui_about)
        
        self.item_more.add_command(label='Quit', command=self.ui_quit)
        
        self.item_more.add_cascade(label='More', menu=self.item_about)
        self.master.config(menu=self.item_more) # self.master 

        # left mouseclick action
        self.canvas_pace.bind('<Button-1>',self.extend_RoadPath)


    def apply_RoadWidth(self):
        """
        
        Applies the user input for the road width.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        
        try:
            self.road_width = int(self.entry_RoadWidth.get())
            if self.road_width >=self.ROAD_WIDTH_MIN and self.road_width <=self.ROAD_WIDTH_MAX:
                self.label_RoadWidthCheck.configure(text ='Good', background=self.GREEN)
                self.width_ok = True
            else:
                self.label_RoadWidthCheck.configure(text ='Not valid | Follow Instructions', background=self.ORANGE)
                self.width_ok = False
        except:
            self.label_RoadWidthCheck.configure(text ='Not valid | Follow Instructions', background=self.ORANGE)
            self.width_ok = False
        self._set_status()


    def extend_RoadPath(self,event):
        """
        
        Extends the user input for the road width.
        ...

        Parameters
        ----------
        event : tkinter.Event
            Click-event, created from the mouse-button.

        Returns
        -------
        None.
        
        """
        
        self.points_x = np.append(self.points_x, event.x)
        self.points_y = np.append(self.points_y, event.y)
        self.canvas_pace.create_line(event.x-5,event.y+5,event.x+5,event.y-5)
        self.canvas_pace.create_line(event.x-5,event.y-5,event.x+5,event.y+5)


    def clear_RoadPath(self):
        """
        
        Deletes the user input of the road.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        
        self.points_x = []
        self.points_y = []
        self.line_data = []
        self.canvas_pace.delete('all')
        self.length_ok = False
        self.apply_RoadPath()


    def apply_RoadPath(self):
        """
        
        Applies the user input road path.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        
        try:
            self.line_data = np.transpose([self.points_x,self.points_y])
            if np.shape(self.line_data)[0]>1:
                self.label_RoadPathCheck.configure(text ='Good', background=self.GREEN)
                self.length_ok = True
            else:
                self.label_RoadPathCheck.configure(text ='Not valid | Follow Instructions', background=self.ORANGE)
                self.length_ok = False
        except:
            self.label_RoadPathCheck.configure(text ='Not valid | Follow Instructions', background=self.ORANGE)
            self.length_ok = False
        self._set_status()


    def _set_status(self):
        """
        
        Controls and set the status of the current model and road input data.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        
        if self.length_ok == False or self.width_ok == False or self.model_ok == False:
            if self.model_ok == True:
                self.label_RoadOkCheck.configure(text = 'Random Track ready', background=self.YELLOW)
            else:    
                self.label_RoadOkCheck.configure(text = 'Not valid | Follow Instructions', background=self.ORANGE)
        else:
            self.label_RoadOkCheck.configure(text = 'Both ready', background=self.GREEN)
      
        
    def ui_help(self):
        """
        
        Short Manual for the UI_Pacein
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        
        ui_help = tk.Toplevel()
        ui_help.title("Help")
        ui_help.config(width=650, height=950)
        ui_help_canvas = tk.Canvas(ui_help,width=646, height=946, bg="white")
        
        ui_file = open('Env/UI_PaceIn_help_en.txt', 'r')
        ui_help_text = ui_file.read()
        
        ui_help_canvas.create_text(40,25, text = ui_help_text, anchor="nw", font=('Arial','7'))
        ui_help_canvas.pack()
    
        button_ok = tk.Button(ui_help, text = 'o.k.', command = ui_help.destroy, width = 10)
        button_ok.pack()
        ui_help.mainloop()
        
        
    def ui_about(self):
        """
        
        Splash screen with basic information about the project.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        
        ui_about = tk.Toplevel()
        ui_about.title("About")
        image = Image.open("Env/splash_OKS_en.png")
        photo = ImageTk.PhotoImage(image)
        ui_about.config(width=photo.width()+4, height=photo.height()+4)
        label_photo = ttk.Label(ui_about, image=photo)
        label_photo.pack()
        button_ok = tk.Button(ui_about, text = 'o.k.', command = ui_about.destroy, width = 10)
        button_ok.pack()
        ui_about.mainloop()
        
    
    def load_Model(self):
        """
        
        Opens an Interface to load a model.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        
        model_name = fd.askopenfilename(filetypes=[('SAC-Model', '.zip')]) 
        if not model_name:
            return
        else:
            self.model = SAC.load(model_name)
            self.label_LoadModelCheck.configure(text ='Good', background=self.GREEN)
            self.model_ok = True
            self._set_status()
       
            
    def random_Track(self):
        """
        
        Generates a random track and starts the rendering process.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        
        if self.model_ok == True:
            
            # test road with a random model
            env = PaceRaceEnv(custom_roadwidth=self.road_width, max_iter_per_epoch = 10e10, verbose =1)
            obs = env.reset() # get initial obs
            display = Render()
            done = False
            while done == False:
                action, _state = self.model.predict(obs, deterministic=True) # agent, get next action from last obs
                obs, reward, done, info = env.step(action) # input action, get next obs
                if self.cb_old.get() == 1:
                    delete_old = False
                else:
                    delete_old = True
                if self.cb_perf.get() == 1:
                    plot_performance = True
                else:
                    plot_performance = False    
                print(reward)
                done = display.update(env, done, info, plot_performance, delete_old, color='blue') # render that current obs


    def user_Track(self):
        """
        
        Applies the user input as a center-line of a track,
        generates that one and starts the rendering process.
        ...

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """

        if self.length_ok == True and self.width_ok == True and self.model_ok == True:
            Y = self.CANVAS_HEIGHT-4 # height of canvas, minus 4
            x = self.line_data[:,0]
            y = np.subtract(Y, self.line_data[:,1])
            data = np.transpose([x,y])

            # test road with the loaded model
            env = PaceRaceEnv(custom_center_line = data, custom_roadwidth=self.road_width, max_iter_per_epoch = 10e10, verbose =1)
            obs = env.reset() # get initial obs
            display = Render()  
            done = False
            while done == False:
                action, _state = self.model.predict(obs, deterministic=True) # agent, get next action from last obs
                obs, reward, done, info = env.step(action) # input action, get next obs
                if self.cb_old.get() == 1:
                    delete_old = False
                else:
                    delete_old = True
                if self.cb_perf.get() == 1:
                    plot_performance = True
                else:
                    plot_performance = False
                display.update(env, done, info, plot_performance, delete_old, color='blue') # render that current obs

    
    def ui_quit(self):
        """
        
        Closes and quits the UI_Pacein.
        ...
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        None.
        
        """

        self.master.destroy()


# create ui_pace
def main():

    ui_pace = tk.Tk()
    ui_pace.title('UI_PaceIn')
    ui_pace.geometry('1300x700')
    ui_pace.resizable(width=False, height=False)
    app = UIPace(ui_pace) # must remain here
    ui_pace.mainloop()


if __name__ == '__main__':
    main()
