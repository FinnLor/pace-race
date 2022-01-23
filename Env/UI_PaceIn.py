


from env_PaceRace import PaceRaceEnv
from our_render import Render
from stable_baselines3 import SAC
from shapely.geometry import LineString, Point
from PIL import Image,ImageTk
# import matplotlib.pyplot as plt
import numpy as np

# import random as rn
import tkinter as tk



class UIPace:
    def __init__(self,master):
  
        # preferences
        self.master = master
        self.canvas_width = 1596
        self.canvas_height = 864 
        self.road_width_min = 10
        self.road_width_max = 32
        self.road_width = int(np.round(0.5*(self.road_width_min+self.road_width_max)))
        self.width_ok = False
        self.length_ok = False
        self.points_x = []
        self.points_y = []
        self.line_data = [] # prepared to generate
        self.green = '#b3ffb3'
        self.orange = '#ff8844'
        
        # static text
        self.label_RoadWidthText = tk.Label(master, text =f'STRAßENBREITE als ganze Zahl in Meter eingeben. Wertebereich in Meter [{self.road_width_min}-{self.road_width_max}]:')
        self.label_RoadWidthText.grid(row=0, column=0, sticky = 'W')
        self.label_RoadPath = tk.Label(master, text = 'Mindestens zwei PUNKTE als Streckenverlauf erfassen (1 Pixel entspricht 1 Meter):')
        self.label_RoadPath.grid(row=1, column=0,sticky = 'W')
        self.label_CloseUI = tk.Label(master, text = 'Bei gültigen Daten werden diese übernommen und die GUI geschlossen:')
        self.label_CloseUI.grid(row=2, column=0,sticky = 'W')

        # create entry
        self.entry_RoadWidth = tk.Entry(master, width = 10)
        self.entry_RoadWidth.grid(row=0, column=1)
        self.entry_RoadWidth.insert('end', self.road_width)
        
        # buttons
        self.button_ApplyRoadWidth = tk.Button(self.master, text = 'übernehmen', command = self.apply_RoadWidth, width = 15)
        self.button_ApplyRoadWidth.grid(row=0, column=2)
        self.button_ResetRoadPath= tk.Button(self.master, text = 'neu', command = self.reset_RoadPath, width = 10)
        self.button_ResetRoadPath.grid(row=1, column=1)
        self.button_ApplyRoadPath = tk.Button(self.master, text = 'übernehmen', command = self.apply_RoadPath, width = 15)
        self.button_ApplyRoadPath.grid(row=1, column=2)
        self.button_CloseUI = tk.Button(self.master, text = 'schließen', command = self.closeUI, width = 15)
        self.button_CloseUI.grid(row=2, column=2)      
        
        # interactive text
        self.label_RoadWidthCheck = tk.Label(master, text = 'ungültig', width=25, background=self.orange)
        self.label_RoadWidthCheck.grid(row=0, column=3, sticky = 'W')
        self.label_RoadPathCheck = tk.Label(master, text = 'ungültig', width=25, background=self.orange)
        self.label_RoadPathCheck.grid(row=1, column=3, sticky = 'W')
        self.label_RoadOkCheck = tk.Label(master, text = 'Daten nicht vollständig', width=25, background=self.orange)
        self.label_RoadOkCheck.grid(row=2, column=3, sticky = 'W')
        
        # canvas
        self.canvas_pace = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, background='white', offset='s')
        self.canvas_pace.grid(row=3, column=0, columnspan=4)

        # left mouseclick action
        self.canvas_pace.bind('<Button-1>',self.extend_RoadPath)
    
    
    def apply_RoadWidth(self):
        try:
            self.road_width = int(self.entry_RoadWidth.get())
            if self.road_width >=self.road_width_min and self.road_width <=self.road_width_max:
                self.label_RoadWidthCheck.configure(text ='i.O.', background=self.green)
                self.width_ok = True
            else:
                self.label_RoadWidthCheck.configure(text ='ungültig. Vorgaben beachten.', background=self.orange)
                self.width_ok = False
        except:
            self.label_RoadWidthCheck.configure(text ='ungültig. Vorgaben beachten.', background=self.orange)
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
                self.label_RoadPathCheck.configure(text ='i.O.', background=self.green)
                self.length_ok = True
            else:
                self.label_RoadPathCheck.configure(text ='ungültig. Vorgaben beachten.', background=self.orange)
                self.length_ok = False
        except:
            self.label_RoadPathCheck.configure(text ='ungültig. Vorgaben beachten.', background=self.orange) 
            self.length_ok = False
        self.set_status()
            
    def set_status(self):
        if self.length_ok == False or self.width_ok == False:
            self.label_RoadOkCheck.configure(text = 'Daten nicht vollständig', background=self.orange)
        else:
            self.label_RoadOkCheck.configure(text = 'Daten vollständig', background=self.green)

    def closeUI(self):
        
            self.master.destroy() 

            if self.length_ok == True and self.width_ok == True:
                Y = self.canvas_height-4 # height of canvas, minus 4
                x = self.line_data[:,0]
                y = np.subtract(Y, self.line_data[:,1])
                data = np.transpose([x,y])
                # test road with a model
                env = PaceRaceEnv(P=1000, custom_center_line = data, custom_roadwidth=self.road_width)
                model = SAC.load("models/sac_pace_race_FS_02_210122.zip")
                #model = SAC.load("models/sac_pace_race_bad01.zip")
                print('Starting new game.')
                obs = env.reset() # get initial obs
                display = Render()
                display.update(env, done = False)
                # for i in range(1000):
                #     print(i)
                #     env.step((0.3, 0.000))
                #     display.update(env,False)
                # display.update(env,True)
                while True:
                    # c+=1
                    # print(c)
                    # action = env.action_space.sample() # random
                    # obs, reward, done, info = env.step((0.001,0.1)) # manual
                    action, _state = model.predict(obs) # agent, get next action from last obs
                    obs, reward, done, info = env.step(action) # input action, get next obs
                    done = False
                    display.update(env, done) # render that current obs



# create ui_pace
def main(): 
    ui_pace = tk.Tk()
    ui_pace.title('OKS_PaceRace_Streckeneingabemaske')
    ui_pace.geometry('1600x1000')
    ui_pace.resizable(width=False, height=False)
    app = UIPace(ui_pace)   
    ui_pace.mainloop()
    

if __name__ == '__main__':
    main()
    




# def ui_about():
#     print('ABOUT')
#     ui_about = tk.Tk()
#     ui_about.title('ABOUT')
#     ui_about.geometry('400x240')
#     ui_about.resizable(width=False, height=False)

# # items
# item_info = tk.Menu(ui_pace)
# item_about = tk.Menu(item_info)
# item_about.add_command(label='About', command=ui_about)
# item_info.add_cascade(label='Info', menu=item_about)
# ui_pace.config(menu=item_info)


