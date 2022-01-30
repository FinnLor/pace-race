


from env_PaceRace import PaceRaceEnv
from our_render import Render
from stable_baselines3 import SAC
from shapely.geometry import LineString, Point
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np



class UIPace:
    def __init__(self,master):

        # preferences
        self.master = master
        self.canvas_width = 1596
        self.canvas_height = 864
        self.road_width_min = 8
        self.road_width_max = 40
        self.road_width = int(np.round(0.5*(self.road_width_min+self.road_width_max)))
        self.width_ok = False
        self.length_ok = False
        self.points_x = []
        self.points_y = []
        self.line_data = [] # prepared to generate
        self.green = '#b3ffb3'
        self.orange = '#ff8844'

        # static text
        self.label_RoadWidthText = tk.Label(self.master, text =f'STRASSENBREITE als ganze Zahl in Meter eingeben. Wertebereich in Meter [{self.road_width_min}-{self.road_width_max}]:')
        self.label_RoadWidthText.grid(row=0, column=0, sticky = 'W')
        self.label_RoadPath = tk.Label(self.master, text = 'Mindestens zwei PUNKTE als Streckenverlauf erfassen (1 Pixel entspricht 1 Meter):')
        self.label_RoadPath.grid(row=1, column=0,sticky = 'W')
        self.label_CloseUI = tk.Label(self.master, text = 'Bei gueltigen Daten werden diese uebernommen und die GUI geschlossen:')
        self.label_CloseUI.grid(row=2, column=0,sticky = 'W')

        # create entry
        self.entry_RoadWidth = tk.Entry(self.master, width = 10)
        self.entry_RoadWidth.grid(row=0, column=1)
        self.entry_RoadWidth.insert('end', self.road_width)

        # buttons
        self.button_ApplyRoadWidth = tk.Button(self.master, text = 'uebernehmen', command = self.apply_RoadWidth, width = 15)
        self.button_ApplyRoadWidth.grid(row=0, column=2)
        self.button_ResetRoadPath= tk.Button(self.master, text = 'neu', command = self.reset_RoadPath, width = 10)
        self.button_ResetRoadPath.grid(row=1, column=1)
        self.button_ApplyRoadPath = tk.Button(self.master, text = 'uebernehmen', command = self.apply_RoadPath, width = 15)
        self.button_ApplyRoadPath.grid(row=1, column=2)
        self.button_CloseUI = tk.Button(self.master, text = 'schliessen', command = self.closeUI, width = 15)
        self.button_CloseUI.grid(row=2, column=2)

        # interactive text
        self.label_RoadWidthCheck = tk.Label(self.master, text = 'ungueltig', width=25, background=self.orange)
        self.label_RoadWidthCheck.grid(row=0, column=3, sticky = 'W')
        self.label_RoadPathCheck = tk.Label(self.master, text = 'ungueltig', width=25, background=self.orange)
        self.label_RoadPathCheck.grid(row=1, column=3, sticky = 'W')
        self.label_RoadOkCheck = tk.Label(self.master, text = 'Daten nicht vollstaendig', width=25, background=self.orange)
        self.label_RoadOkCheck.grid(row=2, column=3, sticky = 'W')

        # canvas
        self.canvas_pace = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, background='white', offset='s')
        self.canvas_pace.grid(row=3, column=0, columnspan=4)

        # items
        self.item_info = tk.Menu(self.master)
        self.item_about = tk.Menu(self.item_info)
        self.item_about.add_command(label='About', command=self.ui_about)
        self.item_info.add_cascade(label='Info', menu=self.item_about)
        self.master.config(menu=self.item_info) # self.master

        # left mouseclick action
        self.canvas_pace.bind('<Button-1>',self.extend_RoadPath)


    def apply_RoadWidth(self):
        try:
            self.road_width = int(self.entry_RoadWidth.get())
            if self.road_width >=self.road_width_min and self.road_width <=self.road_width_max:
                self.label_RoadWidthCheck.configure(text ='i.O.', background=self.green)
                self.width_ok = True
            else:
                self.label_RoadWidthCheck.configure(text ='ungueltig. Vorgaben beachten.', background=self.orange)
                self.width_ok = False
        except:
            self.label_RoadWidthCheck.configure(text ='ungueltig. Vorgaben beachten.', background=self.orange)
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
                self.label_RoadPathCheck.configure(text ='ungueltig. Vorgaben beachten.', background=self.orange)
                self.length_ok = False
        except:
            self.label_RoadPathCheck.configure(text ='ungueltig. Vorgaben beachten.', background=self.orange)
            self.length_ok = False
        self.set_status()


    def set_status(self):
        if self.length_ok == False or self.width_ok == False:
            self.label_RoadOkCheck.configure(text = 'Daten nicht vollstaendig', background=self.orange)
        else:
            self.label_RoadOkCheck.configure(text = 'Daten vollstaendig', background=self.green)


    def ui_about(self):
        ui_about = tk.Toplevel()
        image = Image.open("splash_OKS.png")
        photo = ImageTk.PhotoImage(image)
        width = photo.width()
        ui_about.config(width=photo.width()+4, height=photo.height()+4)
        label_photo = ttk.Label(ui_about, image=photo)
        label_photo.pack()
        button_ok = tk.Button(ui_about, text = 'ok', command = ui_about.destroy, width = 10)
        button_ok.pack()
        ui_about.mainloop()


    def closeUI(self):

            self.master.destroy()

            if self.length_ok == True and self.width_ok == True:
                Y = self.canvas_height-4 # height of canvas, minus 4
                x = self.line_data[:,0]
                y = np.subtract(Y, self.line_data[:,1])
                data = np.transpose([x,y])

                # test road with a model
                env1 = PaceRaceEnv(P=1000, custom_center_line = data, custom_roadwidth=self.road_width)
                env2 = PaceRaceEnv(P=1000, custom_center_line = data, custom_roadwidth=self.road_width)
                # model = SAC.load("models/sac_pace_race_bad_01.zip")
                model1 = SAC.load("models/sac_pace_race_EM_01_230122.zip")
                model2 = SAC.load("models/sac_pace_race_FS_02_210122.zip")
                obs1 = env1.reset() # get initial obs
                obs2 = env2.reset() # get initial obs
                display1 = Render()
                display2 = Render()
                vlon1_max=0
                vlon2_max=0
                vsum1=0
                vsum2=0
                c=0
                # for i in range(1000):
                #     print(i)
                #     env.step((0.3, 0.000))
                #     display.update(env,False, info)
                while True:
                    c+=1
                    # print(c)
                    # action = env.action_space.sample() # random
                    # obs, reward, done, info = env.step((0.001,0.1)) # manual
                    action1, _state1 = model1.predict(obs1) # agent, get next action from last obs
                    action2, _state2 = model2.predict(obs2) # agent, get next action from last obs
                    obs1, reward1, done, info1 = env1.step(action1) # input action, get next obs
                    obs2, reward2, done, info2 = env2.step(action2) # input action, get next obs
                    done = False
                    if obs1[0] > vlon1_max:
                        vlon1_max=obs1[0]
                    if obs2[0] > vlon2_max:
                        vlon2_max=obs2[0]
                    vsum1 = vsum1+obs1[0]
                    vsum2 = vsum2+obs2[0]
                    print(f'vmax car1={vlon1_max} vmax car2={vlon2_max}')
                    print(f'vsum car1={vsum1} vsum car2={vsum2}')


                    display1.update(env1, done, info1, plot_performance=True, color='blue') # render that current obs
                    display2.update(env2, done, info2, color='red') # render that current obs



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
