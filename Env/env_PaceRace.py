import math
import random
# from typing import Optional
import numpy as np
# from scipy import integrate
from matplotlib import pyplot as plt
import gym
# import time as t
import tkinter as tk
# from gym import spaces
from gym.utils import seeding
from cls_Car import Car
from cls_Road import Road
from shapely.geometry import LineString, Point, Polygon


### alles in SI-Basiseinheiten
## ToDo:    realistischen Default-Wert für JZ
##          Quelle für MU und CF/CR


### alles in SI-Basiseinheiten
## ToDo:    realistischen Default-Wert für JZ
##          Quelle für MU und CF/CR


class PaceRaceEnv(gym.Env):
    """
    Description:

    Observation:
        Type: Box(2)
        Num    Observation               Min            Max
        0
        1
    Actions:
        Type: Box(1)
        Num    Action                    Min            Max
        0
    Reward:

    Starting State:

    Episode Termination:
         The car position is more than  XXXX
         Episode length is greater than XXXX
    """

    metadata = {"render.modes": ["human"]}




    def __init__(self, CF=49_000, CR=49_000, M=1_000, LF=2, LR=2, CAR_WIDTH=2, CT=0.1, MU=1.0, P=50_000, ROADWIDTH=8):

        # super(PaceRaceEnv, self).__init__() # FS: have seen this in other code ... purpose?
        
        self.render_step = 0 # NEU
        self.delete_old = True # NEU    
 
        self.MU = MU # Reibzahl, trockener Asphalt
        self.ROADWIDTH = ROADWIDTH

        self.car01 = Car(LF=LF, LR=LR, CF=CF, CR=CR, WIDTH=CAR_WIDTH, M=M, P=P,\
                     x=0, y=0, psi=0, delta=0, SENS_SCALE=1, CT=CT)

        # Actions and Observations

        #### Reicht es diese Variablen lokal anzulegen? /FL
        self.max_x_position = 10_000
        self.min_x_position = -10_000

        self.max_y_position = 10_000
        self.min_y_position = -10_000

        self.max_yaw_angle = 2*np.pi
        self.min_yaw_angle = -2*np.pi

        self.max_velocity_lon = 100
        self.min_velocity_lon = 0

        self.max_velocity_lat = 100
        self.min_velocity_lat = -100
        
        self.max_power = P # for accelerating
        self.min_power = -P # for decelerating

        self.max_delta_steering_angle = 30*CT*np.pi/180 # Zeitabhängig. entspricht 3 Grad Lenkwinkel der Räder pro Sekunde
        self.min_delta_steering_angle = -30*CT*np.pi/180
        
        self.max_total_steering_angle = 45*np.pi/180
        self.min_total_steering_angle = -45*np.pi/180   

        self.max_omega = np.finfo(np.float32).max   # ist implizit vorhanden durch v_max u delta_max. kann raus, muss überall angepasst werden.
        self.min_omega = np.finfo(np.float32).min

        self.sensordata_min = 0
        self.sensordata_max = 1

        # Action Space
        self.action_space = gym.spaces.Box(
            low=-1, high=1, shape=(2,), dtype="float32")

        # Observation Space
        # observation: [psi, vlon, vlat, omega, total_steering_angle, sensor1, sensor3, sensor5, sensor7, sensor9]
        self.low_state = np.array(
            [self.min_yaw_angle, \
             self.min_velocity_lon, self.min_velocity_lat, \
             self.min_omega, self.min_total_steering_angle,
             self.sensordata_min, self.sensordata_min,
             self.sensordata_min, self.sensordata_min, self.sensordata_min], dtype=np.float32
        )
        self.high_state = np.array(
            [self.max_yaw_angle, \
             self.max_velocity_lon, self.max_velocity_lat, \
             self.max_omega, self.max_total_steering_angle,
             self.sensordata_max, self.sensordata_max, \
             self.sensordata_max, self.sensordata_max, self.sensordata_max], dtype=np.float32
        )

        self.observation_space = gym.spaces.Box(
            low=self.low_state, high=self.high_state, dtype=np.float32
        )

        # FOR OLD VERSION OF GYM
        self.seed()

    def step(self, action):
        got_resumed = False
        
        self.counter += 1
        if self.counter%10000 == 0:
            print(f"----> {self.counter}")
        elif self.counter%2000 == 0:
            print("--")

        # rescale the normalized actions
        range_action_Power = self.max_power - self.min_power # b-a
        range_action_delta_delta = self.max_delta_steering_angle - self.min_delta_steering_angle
        range_actions = np.array([range_action_Power, range_action_delta_delta])
        action_scaled = np.asarray(action) * 0.5 * range_actions + 0.5 * np.array([self.max_power + self.min_power, self.max_delta_steering_angle + self.min_delta_steering_angle]) # x * (b-a)/2 + (b+a)/2, dot-wise multiplied

        # unpacking and conversion
        P, delta_delta = action_scaled # unpack RL action variables
        delta = self.car01.delta + delta_delta # calculate new total steering angle
        
        # Clip steering angle if necessary
        if delta > self.max_total_steering_angle:
            delta = self.max_total_steering_angle
        elif delta < self.min_total_steering_angle:
            delta = self.min_total_steering_angle  

        # Calculate acceleration
        if P == 0:
            a = 0
        elif P > 0 and self.car01.vlon == 0:
            a = 9.81*self.MU/math.sqrt(2)
        elif P < 0 and self.car01.vlon == 0:
            a = -9.81*self.MU/math.sqrt(2) # problematic?
        elif P > 0 and self.car01.vlon != 0:
            a = min(P/(self.car01.M*self.car01.vlon), 9.81*self.MU/math.sqrt(2)) 
        elif P < 0 and self.car01.vlon != 0:
            a = max(P/(self.car01.M*self.car01.vlon), -9.81*self.MU/math.sqrt(2)) 
        else:
            print('Error in calculation of acceleration.')
            
        # # new clip acceleration if velocity small or zero
        # if self.car01.vlon < 1:
        #     if self.car01.vlon <= 0: # alt: == 0 # vlat hier ggf mitkorrigieren
        #         self.car01.vlon = 0.1 # ORIGINAL: 0.001
        #     a = max(P/(float(self.car01.M*abs(self.car01.vlon))), 0.1) # ORIGINAL 0
      
        # move car via dynamic model
        states = np.concatenate((self.car01.center, np.array([self.car01.psi, self.car01.vlon, self.car01.vlat, self.car01.omega]))) # states before moving
        inputs = (a, delta) # must be a tuple
        self.car01.set_next_car_position(inputs) # calculate next car position with diff. eq.

        # check if car has crossed the finish line
        done = bool(self.car01.get_path_length(self.road) >= 0.999)

        if done == False:

            # collision check
            collision_check = self.car01.collision_check(self.road)
            if collision_check:
                got_resumed = True
                print(f"--got resumed! at {self.counter}")
                psi_error = self.car01.set_resume_pos(self.road)
                if psi_error == False:
                    print(f"Collision: {self.counter}")
    
            # calculate centrifugal force
            F_ctfg = self.car01.M * self.car01.omega * self.car01.vlon 
    
            # check critical centrifugal force
            Fmax = self.car01.M * 9.81 * self.MU # radius of traction circle
            Fres = math.sqrt((self.car01.M * a)**2 + F_ctfg**2) # resulting force, Pythagoras not correct because not perpendicular
            if Fres > Fmax:
                got_resumed = True
                print(f"--got resumed! at {self.counter}")
                #print("Haftkraft überschritten!")
                psi_error = self.car01.set_resume_pos(self.road)
                if psi_error == False:
                    print(f"MaxAcc: {self.counter}") # probably reset() would be a better penalty

        ######################################################################
        # REWARD SECTION
        reward = 0
        
        # Convert a possible numpy bool to a Python bool
        curr_path_length = self.car01.get_path_length(self.road)
        
        if curr_path_length > self.last_path_length: # reward driving forward
            reward = reward + 3
        
        if curr_path_length < self.last_path_length: # punish driving backward
            reward = reward - 5

        reward = reward - 1 # punish time on track
            
        if got_resumed: # punish violation (collision or force-check)
            reward = reward - 4

        # update path_length
        self.last_path_length = curr_path_length
        
        # get sensordata of a car
        sensdist = self.car01.get_sensordata(self.road, normalized=True)

        info = dict()
        # states = np.concatenate((self.car01.center, np.array([self.car01.psi, self.car01.vlon, self.car01.vlat, self.car01.omega]))) # states after moving
        states = np.array([self.car01.psi, self.car01.vlon, self.car01.vlat, self.car01.omega])
        observation = np.concatenate((np.append(states, self.car01.delta), np.min(sensdist, axis = 1)), axis=None)
        return np.array([observation], dtype=np.float32).flatten(), reward, done, info

    # Current Version of gym
    # def reset(self, seed: Optional[int] = None):
    #     super().reset(seed=seed)

    def reset(self): # FOR OLD VERSION OF GYM

        self.counter = 0
        print("**reset**")
        ### CONSTRUCT NEW ROAD
        self.ROADWIDTH = round(random.uniform(self.car01.WIDTH*5,self.car01.WIDTH*10), 2)
        self.road = Road(ROADWIDTH=self.ROADWIDTH, NPOINTS = 1000)

        ### SET BACK CAR TO START POSITION
        self.car01.set_start_pos(self.road) # this sets x, y, psi and delta
        self.last_path_length = 0

        self.t0 = 0

        # read sensordata
        sensdist = self.car01.get_sensordata(self.road) # reads distances for each sensor in an array
        
        # pack up
        states = np.concatenate((self.car01.center, np.array([self.car01.psi, self.car01.vlon, self.car01.vlat, self.car01.omega])), axis=None)
        # append delta to states and concatenate the sensdist array to its end (compare with the setup/order of an 'observation' array, line 106)
        # observation = np.concatenate((np.append(states, self.car01.delta), sensdist), axis=None) 
        states = np.array([self.car01.psi, self.car01.vlon, self.car01.vlat, self.car01.omega])
        observation = np.concatenate((np.append(states, self.car01.delta), np.min(sensdist, axis = 1)), axis=None) 
        return np.array([observation], dtype=np.float32).flatten()

    def render(self, mode='human'):
        pass

    # def render2(self, mode='human'):
    #     if mode == 'human':    
    #         if self.render_step == 0:  # NEU ERSETZT
            

                
    #             # get canvas height for up-down-flipping
    #             self.canvas = canvas
    #             self.Y = canvas.winfo_reqheight()-4 # height of canvas, minus 4 is necessary
    #             self.X = canvas.winfo_reqwidth()-4 # width of canvas, minus 4 is necessary

    #             # extract road data
    #             x, y   = LineString(self.road.center_line).xy
    #             xl, yl = LineString(self.road.left_line).xy
    #             xr, yr = LineString(self.road.right_line).xy
    #             y = np.subtract(self.Y, y)
    #             yl = np.subtract(self.Y, yl)
    #             yr = np.subtract(self.Y, yr)
                
    #             # get data for best adaption of the road into the canvas
    #             self.min_x = min(min(x)-self.ROADWIDTH, min(x)+self.ROADWIDTH)
    #             self.max_x = max(max(x)-self.ROADWIDTH, max(x)+self.ROADWIDTH)
    #             self.min_y = min(min(y)-self.ROADWIDTH, min(y)+self.ROADWIDTH)
    #             self.max_y = max(max(y)-self.ROADWIDTH, max(y)+self.ROADWIDTH)
    #             delta_x = self.max_x - self.min_x
    #             delta_y = self.max_y - self.min_y
    #             factor_x = CANVAS_WIDTH / delta_x
    #             factor_y = CANVAS_HEIGHT / delta_y
    #             self.factor = min(factor_x, factor_y) # resizing FACTOR, e.g. FAKTOR=10 => 10pixel==1m
    
    #             # align road data to render_gui
    #             x = self.factor * np.add(x, -self.min_x)
    #             y = self.factor * np.add(y, -self.min_y)
    #             xl = self.factor * np.add(xl, -self.min_x)
    #             yl = self.factor * np.add(yl, -self.min_y)                
    #             xr = self.factor * np.add(xr, -self.min_x)
    #             yr = self.factor * np.add(yr, -self.min_y)
                
    #             # generate road lines
    #             center_line_data = list((np.ravel(([x,y]),'F'))) # list is neccessary for a correct separation with comma             
    #             self.canvas.create_line(center_line_data, dash=(4), fill="grey", width=1)
    #             left_line_data   = list((np.ravel(([xl,yl]),'F'))) # list is neccessary for a correct separation with comma
    #             self.canvas.create_line(left_line_data, fill="brown", width=2)
    #             right_line_data  = list((np.ravel(([xr,yr]),'F'))) # list is neccessary for a correct separation with comma
    #             self.canvas.create_line(right_line_data, fill="brown", width=2)

    #             # generate 10m-measure-line
    #             x_m = [self.X/2-(5*self.factor), self.X/2+(5*self.factor)]
    #             y_m = [self.Y-10, self.Y-10]
    #             measure_line_data = list((np.ravel(([x_m,y_m]),'F')))
    #             self.canvas.create_line(measure_line_data, width=5)
      
    #             # generate measurement text
    #             meter_pro_pixel = 1/self.factor
    #             canvas_id = self.canvas.create_text(10 + self.X/2+(5*self.factor), self.Y-25, anchor="nw")
    #             canvas.itemconfig(canvas_id, text="=10m  (1 Pixel entspr.  m)")
    #             canvas.insert(canvas_id, 23, "%f" % meter_pro_pixel)
                
    #         # extract and align car data
    #         x_car = self.car01.corners[:,0]
    #         y_car = np.subtract(self.Y, self.car01.corners[:,1])
    #         x_car = self.factor * np.add(x_car, -self.min_x)
    #         y_car = self.factor * np.add(y_car, -self.min_y)
    #         car01_data = list((np.ravel(([x_car,y_car]),'F'))) # list is neccessary for a correct separation with comma
            
    #         # extract and align sensor data
    #         x_s01 = [self.car01.corners[3,0], self.car01.sensors[0,0]]
    #         y_s01 = [self.Y-self.car01.corners[3,1], self.Y-self.car01.sensors[0,1]]
    #         x_s01 = self.factor * np.add(x_s01, -self.min_x)
    #         y_s01 = self.factor * np.add(y_s01, -self.min_y)
    #         s01_line_data = list((np.ravel(([x_s01,y_s01]),'F'))) # list is neccessary for a correct separation with comma
    #         x_s03 = [self.car01.corners[3,0], self.car01.sensors[1,0]]
    #         y_s03 = [self.Y-self.car01.corners[3,1], self.Y-self.car01.sensors[1,1]]
    #         x_s03 = self.factor * np.add(x_s03, -self.min_x)
    #         y_s03 = self.factor * np.add(y_s03, -self.min_y)
    #         s03_line_data = list((np.ravel(([x_s03,y_s03]),'F'))) # list is neccessary for a correct separation with comma
    #         x_s05 = [self.car01.corners[3,0], self.car01.sensors[2,0]]
    #         y_s05 = [self.Y-self.car01.corners[3,1], self.Y-self.car01.sensors[2,1]]
    #         x_s05 = self.factor * np.add(x_s05, -self.min_x)
    #         y_s05 = self.factor * np.add(y_s05, -self.min_y)
    #         s05_line_data = list((np.ravel(([x_s05,y_s05]),'F'))) # list is neccessary for a correct separation with comma
    #         x_s07 = [self.car01.corners[3,0], self.car01.sensors[3,0]]
    #         y_s07 = [self.Y-self.car01.corners[3,1], self.Y-self.car01.sensors[3,1]]
    #         x_s07 = self.factor * np.add(x_s07, -self.min_x)
    #         y_s07 = self.factor * np.add(y_s07, -self.min_y)
    #         s07_line_data = list((np.ravel(([x_s07,y_s07]),'F'))) # list is neccessary for a correct separation with comma
    #         x_s09 = [self.car01.corners[3,0], self.car01.sensors[4,0]]
    #         y_s09 = [self.Y-self.car01.corners[3,1], self.Y-self.car01.sensors[4,1]]
    #         x_s09 = self.factor * np.add(x_s09, -self.min_x)
    #         y_s09 = self.factor * np.add(y_s09, -self.min_y)
    #         s09_line_data = list((np.ravel(([x_s09,y_s09]),'F'))) # list is neccessary for a correct separation with comma
            
            
    #         # generate car and sensor data
    #         # if iteration !=0 and delete_old == True: 
    #         if self.render_step !=0 and self.delete_old == True: # NEU ERSETZT
    #             self.canvas.delete(self.car_polygon)
    #             self.canvas.delete(self.car_s01)
    #             self.canvas.delete(self.car_s03)
    #             self.canvas.delete(self.car_s05)
    #             self.canvas.delete(self.car_s07)
    #             self.canvas.delete(self.car_s09)
    #         self.car_polygon = self.canvas.create_polygon(car01_data, fill="blue", width=1)
    #         self.car_s01 = self.canvas.create_line(s01_line_data, fill="black", width=1)
    #         self.car_s03 = self.canvas.create_line(s03_line_data, fill="black", width=1) 
    #         self.car_s05 = self.canvas.create_line(s05_line_data, fill="black", width=1) 
    #         self.car_s07 = self.canvas.create_line(s07_line_data, fill="black", width=1) 
    #         self.car_s09 = self.canvas.create_line(s09_line_data, fill="black", width=1) 
  
    #         self.render_step += 1 # NEU
            
    #     else:
    #     #elif mode == '...'
    #         pass
    #         # plt.scatter(self.state[0], self.state[1], s=20, marker='o', color='g')
            
            
    # Current Version of gym
    # def seed(self):
    #     pass

    # FOR OLD VERSION OF GYM
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def close(self):
        pass


if __name__ == '__main__':
    
    g = PaceRaceEnv(CF=49_000, CR=49_000, CT=0.1, ROADWIDTH=30)
    g.reset()
    RENDER_ANY = 1
    # set up render environment
    render_gui = tk.Tk() # parent window for canvas
    CANVAS_WIDTH = 1600
    CANVAS_HEIGHT = 1000
    canvas = tk.Canvas(render_gui, width=CANVAS_WIDTH, height=CANVAS_HEIGHT) # canvas is the rendering area
    canvas.pack() # required to visualize the canvas
    
    for i in range(500):
        g.step((0.3, 0.000))
        # print(i)
        if i % RENDER_ANY == 0:
            g.render2(mode='human')
            render_gui.update()     
    # for i in range(500):
    #     g.step((-0.3, 0.00))
    #     print(500+i)
    #     if i % RENDER_ANY == 0:
    #         g.render(mode='human')
    #         render_gui.update()
    # plt.show()
    render_gui.mainloop()
