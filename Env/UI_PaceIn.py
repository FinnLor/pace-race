# -*- coding: utf-8 -*-
"""
Created on Jan 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""



from env_PaceRace import PaceRaceEnv
from our_render import Render
from stable_baselines3 import SAC
from shapely.geometry import LineString, Point
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
from tkinter import filedialog as fd # für fd.askopenfilename



class UIPace():
    def __init__(self,master):

        # preferences
        self.master = master
        self.canvas_width = 1396
        self.canvas_height = 664
        self.road_width_min = 8
        self.road_width_max = 40
        self.road_width = int(np.round(0.5*(self.road_width_min+self.road_width_max)))
        self.width_ok = False
        self.length_ok = False
        self.model_ok = False
        self.points_x = []
        self.points_y = []
        self.line_data = [] # prepared to generate
        self.green = '#b3ffb3'
        self.yellow = '#ffff44'
        self.orange = '#ff8844'

        # static text
        self.label_LoadModelText = tk.Label(self.master, text ='UI FOR THE OKS-RL-PACERACE-PROJECT', font=('Arial 12 bold'))
        self.label_LoadModelText.grid(row=0, column=0, sticky = 'W')
        self.label_RoadWidthText = tk.Label(self.master, text =f'Enter width of road as integer. Value range in meter [{self.road_width_min}-{self.road_width_max}]:')
        self.label_RoadWidthText.grid(row=1, column=0, sticky = 'W')
        self.label_RoadPath = tk.Label(self.master, text = 'Set ad least two points as the course of the route (1 pixel equals 1 meter):')
        self.label_RoadPath.grid(row=2, column=0,sticky = 'W')
        self.label_CloseUI = tk.Label(self.master, text = 'If data is valid, the data will be commited for rendering:')
        self.label_CloseUI.grid(row=3, column=0,sticky = 'W')

        # create entry
        self.entry_RoadWidth = tk.Entry(self.master, width = 10)
        self.entry_RoadWidth.grid(row=1, column=1)
        self.entry_RoadWidth.insert('end', self.road_width)

        # checkbutton
        self.cb = tk.IntVar()
        self.check_PlotPerformance = tk.Checkbutton(self.master, text = 'Plot performance', variable=self.cb, onvalue = 1, offvalue = 0)
        self.check_PlotPerformance.grid(row=0, column=1)      
        
        
        # buttons
        self.button_LoadModel = tk.Button(self.master, text = 'Load Model', command = self.load_Model, width = 15)
        self.button_LoadModel.grid(row=0, column=2)
        self.button_ApplyRoadWidth = tk.Button(self.master, text = 'Apply', command = self.apply_RoadWidth, width = 15)
        self.button_ApplyRoadWidth.grid(row=1, column=2)
        self.button_ResetRoadPath= tk.Button(self.master, text = 'Reset', command = self.reset_RoadPath, width = 15)
        self.button_ResetRoadPath.grid(row=2, column=1)
        self.button_RandomTrack = tk.Button(self.master, text = 'Apply', command = self.apply_RoadPath, width = 15)
        self.button_RandomTrack.grid(row=2, column=2)
        self.button_UserTrack = tk.Button(self.master, text = 'Take Random Track', command = self.random_Track, width = 15)
        self.button_UserTrack.grid(row=3, column=1)
        self.button_UserTrack = tk.Button(self.master, text = 'Take User Track', command = self.user_Track, width = 15)
        self.button_UserTrack.grid(row=3, column=2)

        # interactive text
        self.label_LoadModelCheck = tk.Label(self.master, text = 'No Model loaded', width=25, background=self.orange)
        self.label_LoadModelCheck.grid(row=0, column=3, sticky = 'W')
        self.label_RoadWidthCheck = tk.Label(self.master, text = 'Not valid', width=25, background=self.orange)
        self.label_RoadWidthCheck.grid(row=1, column=3, sticky = 'W')
        self.label_RoadPathCheck = tk.Label(self.master, text = 'Not valid', width=25, background=self.orange)
        self.label_RoadPathCheck.grid(row=2, column=3, sticky = 'W')
        self.label_RoadOkCheck = tk.Label(self.master, text = 'Data not complete', width=25, background=self.orange)
        self.label_RoadOkCheck.grid(row=3, column=3, sticky = 'W')

        # canvas
        self.canvas_pace = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, background='white', offset='s')
        self.canvas_pace.grid(row=5, column=0, columnspan=4)

        # items
        self.item_info = tk.Menu(self.master)
        self.item_about = tk.Menu(self.item_info)
        self.item_about.add_command(label='About', command=self.ui_about)
        self.item_about.add_command(label='Close', command=self.ui_close)
        self.item_info.add_cascade(label='Info', menu=self.item_about)
        self.master.config(menu=self.item_info) # self.master

        # left mouseclick action
        self.canvas_pace.bind('<Button-1>',self.extend_RoadPath)


    def apply_RoadWidth(self):
        try:
            self.road_width = int(self.entry_RoadWidth.get())
            if self.road_width >=self.road_width_min and self.road_width <=self.road_width_max:
                self.label_RoadWidthCheck.configure(text ='Good', background=self.green)
                self.width_ok = True
            else:
                self.label_RoadWidthCheck.configure(text ='Not valid | Follow instructions', background=self.orange)
                self.width_ok = False
        except:
            self.label_RoadWidthCheck.configure(text ='Not valid |Follow instructions', background=self.orange)
            self.width_ok = False
        self.set_status()


    def extend_RoadPath(self,event):
        self.points_x = np.append(self.points_x, event.x)
        self.points_y = np.append(self.points_y, event.y)
        self.canvas_pace.create_line(event.x-5,event.y+5,event.x+5,event.y-5)
        self.canvas_pace.create_line(event.x-5,event.y-5,event.x+5,event.y+5)


    def reset_RoadPath(self):
        self.points_x = []
        self.points_y = []
        self.line_data = []
        self.canvas_pace.delete('all')
        self.length_ok = False
        self.apply_RoadPath()


    def apply_RoadPath(self):
        try:
            self.line_data = np.transpose([self.points_x,self.points_y])
            if np.shape(self.line_data)[0]>1:
                self.label_RoadPathCheck.configure(text ='Good', background=self.green)
                self.length_ok = True
            else:
                self.label_RoadPathCheck.configure(text ='Not valid | Follow instructions', background=self.orange)
                self.length_ok = False
        except:
            self.label_RoadPathCheck.configure(text ='Not valid | Follow instructions', background=self.orange)
            self.length_ok = False
        self.set_status()


    def set_status(self):
        if self.length_ok == False or self.width_ok == False or self.model_ok == False:
            if self.model_ok == True:
                self.label_RoadOkCheck.configure(text = 'Random Track ready', background=self.yellow)
            else:    
                self.label_RoadOkCheck.configure(text = 'Not valid | Follow instructions', background=self.orange)
        else:
            self.label_RoadOkCheck.configure(text = 'Both Ready', background=self.green)
        
        
    def ui_about(self):
        ui_about = tk.Toplevel()
        image = Image.open("splash_OKS.png")
        photo = ImageTk.PhotoImage(image)
        width = photo.width()
        ui_about.config(width=photo.width()+4, height=photo.height()+4)
        label_photo = ttk.Label(ui_about, image=photo)
        label_photo.pack()
        button_ok = tk.Button(ui_about, text = 'Good', command = ui_about.destroy, width = 10)
        button_ok.pack()
        ui_about.mainloop()
        
    
    def load_Model(self):
        model_name = fd.askopenfilename(filetypes=[('SAC-Model', '.zip')]) 
        if not model_name:
            return
        else:
            self.model = SAC.load(model_name)
            self.label_LoadModelCheck.configure(text ='Good', background=self.green)
            self.model_ok = True
            self.set_status()
       
            
    def random_Track(self):

            if self.model_ok == True:
                env = PaceRaceEnv(verbose =1)
                obs = env.reset() # get initial obs
                display = Render()
                while True:
                    # action = env.action_space.sample() # random
                    # obs, reward, done, info = env.step((0.001,0.1)) # manual
                    action, _state = self.model.predict(obs) # agent, get next action from last obs
                    obs, reward, done, info = env.step(action) # input action, get next obs
                    if self.cb.get() == 1:
                        plot_performance = True
                    else:
                        plot_performance = False
                    display.update(env, done, info, plot_performance, color='blue') # render that current obs


    def user_Track(self):

            if self.length_ok == True and self.width_ok == True and self.model_ok == True:
                Y = self.canvas_height-4 # height of canvas, minus 4
                x = self.line_data[:,0]
                y = np.subtract(Y, self.line_data[:,1])
                data = np.transpose([x,y])

                # test road with the loaded model
                env = PaceRaceEnv(P=1000, custom_center_line = data, custom_roadwidth=self.road_width)
                obs = env.reset() # get initial obs
                display = Render()
                # for i in range(1000):
                #     print(i)
                #     env.step((0.3, 0.000))
                #     display.update(env,False, info)
                while True:
                    # action = env.action_space.sample() # random
                    # obs, reward, done, info = env.step((0.001,0.1)) # manual
                    action, _state = self.model.predict(obs) # agent, get next action from last obs
                    obs, reward, done, info = env.step(action) # input action, get next obs
                    if self.cb.get() == 1:
                        plot_performance = True
                    else:
                        plot_performance = False
                    display.update(env, done, info, plot_performance, color='blue') # render that current obs
    
    def ui_close(self):

            self.master.destroy()



# create ui_pace
def main():
    ui_pace = tk.Tk()
    ui_pace.title('UI_PaceIn')
    ui_pace.geometry('1400x800')
    ui_pace.resizable(width=False, height=False)
    app = UIPace(ui_pace)
    ui_pace.mainloop()


if __name__ == '__main__':
    main()
