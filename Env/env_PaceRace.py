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




    def __init__(self, CF=49_000, CR=49_000, M=1_000, LF=2, LR=2, CAR_WIDTH=2, CT=0.1, MU=1.0, P=100_000, ROADWIDTH=8):

        # super(PaceRaceEnv, self).__init__() # FS: have seen this in other code ... purpose?
        
        self.MU = MU # Reibzahl, trockener Asphalt
        self.ROADWIDTH = ROADWIDTH

        self.car01 = Car(LF=LF, LR=LR, CF=CF, CR=CR, WIDTH=CAR_WIDTH, M=M, P=P,\
                     x=0, y=0, psi=0, delta=0, SENS_SCALE=1, CT=CT)

        # Actions and Observations

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
        # observation: [vlon, vlat, omega, total_steering_angle, sensor1, sensor3, sensor5, sensor7, sensor9]
        self.low_state = np.array(
            [self.min_velocity_lon, self.min_velocity_lat, \
             self.min_omega, self.min_total_steering_angle,
             self.sensordata_min, self.sensordata_min,
             self.sensordata_min, self.sensordata_min, self.sensordata_min], dtype=np.float32
        )
        self.high_state = np.array(
            [self.max_velocity_lon, self.max_velocity_lat, \
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
        inputs = (a, delta) # must be a tuple
        self.car01.set_next_car_position(inputs) # calculate next car position with diff. eq.
        
        # check if car has crossed the finish line
        curr_path_length = self.car01.get_path_length(self.road)
        done = bool(curr_path_length >= 0.999)

        if done == False:

            # collision check
            collision_check = self.car01.collision_check(self.road)
            if collision_check:
                print(f"--got resumed! at {self.counter}")
                psi_error = self.car01.set_resume_pos(self.road)
                if psi_error == False:
                    print(f"Collision: {self.counter}")
    
            # calculate centrifugal force
            F_ctfg = self.car01.M * self.car01.omega * self.car01.vlon 
    
            # check critical centrifugal force
            Fmax = self.car01.M * 9.81 * self.MU # radius of traction circle
            Fres = math.sqrt((self.car01.M * a)**2 + F_ctfg**2) # resulting force, Pythagoras not correct because not perpendicular
            force_exceeded = Fres > Fmax
            if force_exceeded:
                print(f"--got resumed! at {self.counter}")
                #print("Haftkraft überschritten!")
                psi_error = self.car01.set_resume_pos(self.road)
                if psi_error == False:
                    print(f"MaxAcc: {self.counter}") # probably reset() would be a better penalty
            
            violation = collision_check or force_exceeded # a bool to check if limits were violated
        else:
            violation = False
            
        ######################################################################
        # REWARD SECTION
        reward = 0

        reward = reward - 3 # penalize time on track
        
        if done:
            reward += 2500
        
        if self.counter > 4000 and not done: # stop after a maximum of 2000 iterations, this implies a penalty of -2000 from #1
            done = True
            reward += curr_path_length * 2000 # if stopped by exceeding time limit, reward proportionally to achieved progress
        
        if violation: # penalize violation (collision or force-check)
            reward -= 60
            
        # if a < 0:
        #     reward = reward - 2
        
        # if curr_path_length - self.last_path_length > 0.2: # reward driving forward
        #     reward = reward + 3
        
        # if curr_path_length < self.last_path_length: # punish driving backward
        #     reward = reward - 5
        
        self.episode_reward += reward
        
        print(f"input: {action_scaled[0]:09.2F} ||  acceleration: {a:06.2F} || v_lon: {self.car01.vlon:05.2F} || pos: {np.round(curr_path_length,4)} || done: {done} || eprew: {self.episode_reward} || iter: {self.counter}")

        # update path_length
        self.last_path_length = curr_path_length
        
        # get sensordata of a car
        sensdist = self.car01.get_sensordata(self.road, normalized=True)

        states = np.array([self.car01.vlon, self.car01.vlat, self.car01.omega])
        observation = np.concatenate((np.append(states, self.car01.delta), np.min(sensdist, axis = 1)), axis=None)
        info = {"obs": observation,"act": action}
        return np.array([observation], dtype=np.float32).flatten(), reward, done, info

    # Current Version of gym
    # def reset(self, seed: Optional[int] = None):
    #     super().reset(seed=seed)

    def reset(self): # FOR OLD VERSION OF GYM
        self.episode_reward = 0
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
        states = np.array([self.car01.vlon, self.car01.vlat, self.car01.omega])
        observation = np.concatenate((np.append(states, self.car01.delta), np.min(sensdist, axis = 1)), axis=None) 
        return np.array([observation], dtype=np.float32).flatten()

    def render(self, mode='human'):
        pass            
            
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
    
    for i in range(500):
        g.step((0.3, 0.000))
