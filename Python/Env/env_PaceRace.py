import math
# from typing import Optional
import numpy as np
# from scipy import integrate
from matplotlib import pyplot as plt
import gym
# import tkinter as tk
# from gym import spaces
from gym.utils import seeding
from cls_Car import Car
from cls_Road import Road


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


    def __init__(self, CF=0.7, CR=0.7, M=1_000, LF=2, LR=2, CAR_WIDTH=2, CT=0.1, MU=1.0, P=100_000, ROADWIDTH=8):

 
        self.MU = MU # Reibzahl, trockener Asphalt
        self.ROADWIDTH = ROADWIDTH

        self.car01 = Car(LF=LF, LR=LR, WIDTH=CAR_WIDTH, M=M, P=P,\
                     x=0, y=0, psi=0, delta=0, SENS_SCALE=1)

        # Numerical timestamp
        self.cycletime = CT
        self.t0 = 0

        # # Actions and Observations
        # SOLLTE NORMALISIERT WERDEN?

        self.max_x_position = np.finfo(np.float32).max
        self.min_x_position = np.finfo(np.float32).min

        self.max_y_position = np.finfo(np.float32).max
        self.min_y_position = np.finfo(np.float32).min

        self.max_yaw_angle = np.finfo(np.float32).max
        self.min_yaw_angle =  np.finfo(np.float32).min                                 # DAS IST KOMPLIZIERT ZU BEHANDELN !!! -> Modulo

        self.max_velocity_lon = np.finfo(np.float32).max
        self.min_velocity_lon = np.finfo(np.float32).min

        self.max_velocity_lat = np.finfo(np.float32).max
        self.min_velocity_lat = np.finfo(np.float32).min

        # self.max_acceleration = np.finfo(np.float32).max
        # self.min_acceleration = np.finfo(np.float32).min
        
        self.max_power = P # for accelerating
        self.min_power = -P # for decelerating

        self.max_delta_steering_angle = np.finfo(np.float32).max
        self.min_delta_steering_angle = np.finfo(np.float32).min
        
        self.max_total_steering_angle = np.finfo(np.float32).max
        self.min_total_steering_angle = np.finfo(np.float32).min    

        self.max_omega = np.finfo(np.float32).max
        self.min_omega = np.finfo(np.float32).min

        self.sensordata_min = 0
        self.sensordata_max = 1

        # Action Space
        self.low_action = np.array(
            [self.min_power, self.min_delta_steering_angle], dtype=np.float32
        )
        self.high_action= np.array(
            [self.max_power, self.max_delta_steering_angle], dtype=np.float32
        )

        self.action_space = gym.spaces.Box(
            low=self.low_action, high=self.high_action, dtype=np.float32 # changes FS: low_action instead low_state etc.
        )

        # Observation Space
        # observation: [x, y, psi, vlon, vlat, omega, total_steering_angle, sensor1, sensor3, sensor5, sensor7, sensor9]
        self.low_state = np.array(
            [self.min_x_position, self.min_y_position, self.min_yaw_angle, \
             self.min_velocity_lon, self.min_velocity_lat, \
             self.min_omega, self.sensordata_min, self.sensordata_min, \
             self.sensordata_min, self.sensordata_min, self.sensordata_min], dtype=np.float32
        )
        self.high_state = np.array(
            [self.max_x_position, self.max_y_position, self.max_yaw_angle, \
             self.max_velocity_lon, self.max_velocity_lat, \
             self.max_omega, self.sensordata_max, self.sensordata_max, \
             self.sensordata_max, self.sensordata_max, self.sensordata_max], dtype=np.float32
        )

        self.observation_space = gym.spaces.Box(
            low=self.low_state, high=self.high_state, dtype=np.float32
        )

        # FOR OLD VERSION OF GYM
        self.seed()

    def step(self, action):

        # unpacking and conversion
        P, delta_delta = action # unpack RL action variables
        delta = self.car01.delta + delta_delta # calculate new total steering angle
        # ERROR HERE: if vlon is very small, a becomes Inf! not fixable with try/except, because not continiuous!
        a = P/(self.car01.M*self.car01.vlon) # calculate feasable acceleceration
        
        # move car via dynamic model
        states = np.concatenate(self.car01.center, np.array([self.car01.psi, self.car01.vlon, self.car01.vlat, self.car01.omega])) # states before moving
        inputs = (a, delta) # must be a tuple
        self.car01.get_next_car_position(self.car01._car_dynamics, states, inputs) # calculate next car position with diff. eq.

        # calculate centrifugal force
        omega_after_int = self.car01.omega # get current angle velocity
        try:
            R = (self.LF+self.LR)/math.tan(delta) * 1/(math.atan(math.tan(delta) * self.LR/(self.LF+self.LR)))
            F_ctfg = self.M * omega_after_int**2 * R # centrifugal force
        except ZeroDivisionError:
            F_ctfg = 0

        # get sensordata of a car
        sensdist = self.car01.get_sensordata(self.road, normalized=True)

        collision_check = self.car01.collision_check(self.road)
        if collision_check:
            self.car01.set_resume_pos(self.road)

        # check critical centrifugal force
        Fmax = self.car01.M * 9.81 * self.MU # radius of traction circle
        Fres = math.sqrt((self.car01.M * a)**2 + F_ctfg**2) # resulting force
        if Fres > Fmax:
            self.car01.set_resume_pos(self.road)
            self.car01.vlon = 0
            self.car01.vlat = 0
            # self.state[3:6] = 0, 0, 0 # set velocities and psi to zero # old code, but why did we reset psi?

        ######################################################################
        # REWARD SECTION
        # Convert a possible numpy bool to a Python bool
        done = bool(self.road.get_path_length(self.car01) >= 0.99)
        reward = 0 # reward wird in jedem step() ausgerechnet? Oder ist das eine Objektvariable, die kumuliert wird? -> Recherche!

        if not done:
            # if self.road.get_path_length(self.car01)%0.1 == 0: # jede 10 Prozentpunkte ein Extra-Leckerli ...
            #     reward += 10
            reward -= 1.0
        else:
            reward = 1000.0

        info = dict()
        states = np.concatenate(self.car01.center, np.array([self.car01.psi, self.car01.vlon, self.car01.vlat, self.car01.omega])) # states after moving
        observation = np.concatenate([np.append(states,delta), sensdist])
        return np.array([observation], dtype=np.float32).flatten(), reward, done, info

    # Current Version of gym
    # def reset(self, seed: Optional[int] = None):
    #     super().reset(seed=seed)

    def reset(self): # FOR OLD VERSION OF GYM
        ### CONSTRUCT NEW ROAD
        self.road = Road(ROADWIDTH=self.ROADWIDTH, NPOINTS = 1000)

        ### SET BACK CAR TO START POSITION
        self.car01.set_start_pos(self.road) # this sets x, y, psi and delta
        self.car01.vlon = 0
        self.car01.vlat = 0
        self.car01.omega = 0

        self.t0 = 0

        # read sensordata
        sensdist = self.car01.get_sensordata(self.road) # reads distances for each sensor in an array
        
        # pack up
        states = np.concatenate((self.car01.center, np.array([self.car01.psi, self.car01.vlon, self.car01.vlat, self.car01.omega])), axis=None)
        # append delta to states and concatenate the sensdist array to its end (compare with the setup/order of an 'observation' array, line 106)
        observation = np.concatenate((np.append(states, self.car01.delta), sensdist), axis=None) 
        return np.array([observation], dtype=np.float32)

    def render(self, mode='human'):
        pass
        # if mode == 'human':
            # tkinter Visualisierung
        # elif mode == '...'
        #     plt.scatter(self.state[0], self.state[1], s=20, marker='o', color='g')

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
    g = PaceRaceEnv()
    g.reset()
    g.render(mode='human')
    for i in range(50):
        g.step((0, 0))
        g.render(mode='human')
    plt.show()
