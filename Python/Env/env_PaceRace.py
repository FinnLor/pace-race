import math
# from typing import Optional
import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
import road_car
import gym
import tkinter as tk
# from gym import spaces
from gym.utils import seeding


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


    def __init__(self, CF=0.7, CR=0.7, M=1, JZ=1, LF=1, LR=1, CT=0.1, MU=1.0):

        # Car-Design
        self.CF = CF
        self.CR = CR
        self.M = M
        self.JZ = JZ
        self.LF = LF
        self.LR = LR
        self.MU = MU # Reibzahl, trockener Asphalt

        #######################################################################
        # initialize Car() object?
        ### CONFIGURE ENVIRONMENT BASICS
        self.win_env = tk.Tk() # parent window for the canvas
        self.WIDTH = 1800
        self.HEIGHT = 900
        self.VISUALIZE = True
        self.NPOINTS = 1000 # no of points of the central road line
        self.ROADWIDTH = 8
        self.FACTOR = 10 # resizing FACTOR, e.g. FAKTOR=10 => 10pixel==1m
        self.SENSFACTOR = 1 # resizing factor for sensors 1 = standard
        self.canvas = tk.Canvas(self.win_env, width= self.WIDTH, height= self.HEIGHT) # rendering area in GUI for s, theirs sensors and a road
        self.canvas.pack() # ist required to visualize the canvas
        self.button = tk.Button(self.win_env, text='enough', command = lambda:self.win_env.destroy()).pack(expand=True) # EXPERIMENTAL added button for closing GUI

        #######################################################################

        # Numerical timestamp
        self.cycletime = CT
        self.t0 = 0

        # # Road
        # self.road_path = lambda x,slope,bias : x*slope+bias

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

        self.max_acceleration = np.finfo(np.float32).max
        self.min_acceleration = np.finfo(np.float32).min

        self.max_steering_angle = np.finfo(np.float32).max
        self.min_steering_angle = np.finfo(np.float32).min

        self.max_omega = np.finfo(np.float32).max
        self.min_omega = np.finfo(np.float32).min

        self.sensordata_min = 0
        self.sensordata_max = 1

        # Action Space
        self.low_action = np.array(
            [self.min_acceleration, self.min_steering_angle], dtype=np.float32
        )
        self.high_action= np.array(
            [self.max_acceleration, self.max_steering_angle], dtype=np.float32
        )

        self.action_space = gym.spaces.Box(
            low=self.low_action, high=self.high_action, dtype=np.float32 # changes FS: low_action instead low_state etc.
        )

        # Observation Space
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

        # Finish-Line
        self.goal_position = 10

        # FOR OLD VERSION OF GYM
        self.seed()

    def step(self, action):

        # Das gefällt mit nicht, dass das hier steht... /FL
        def model(t, states, action):
            a, delta = action
            x, y, psi, vlon, vlat, omega = states

            dxdt = vlon*math.cos(psi) - vlat*math.sin(psi)
            dydt = vlon*math.sin(psi) + vlat*math.cos(psi)
            dpsidt = omega
            dvlondt = a
            dvlatdt = -omega*vlon + 1/self.M* (-self.CR*math.atan2(vlat-omega*self.LR, vlon) -math.cos(delta)*self.CF*math.atan2(-vlon*math.sin(delta)+math.cos(delta)*vlat+math.cos(delta)*omega*self.LF, vlon*math.cos(delta)+math.sin(delta)*vlat+math.sin(delta)*omega*self.LF))
            domegadt = 1/self.JZ * (self.CR*self.LR*math.atan2(vlat-omega*self.LR, vlon) -self.CF*self.LF*math.atan2(-vlon*math.sin(delta)+math.cos(delta)*vlat+math.cos(delta)*omega*self.LF, vlon*math.cos(delta)+math.sin(delta)*vlat+math.sin(delta)*omega*self.LF))

            return dxdt, dydt, dpsidt, dvlondt, dvlatdt, domegadt

        # Run one timestep of the environment's dynamics
        # x, y, psi, a, vlat, omega = self.state # überflüssige Zeile
        res = integrate.solve_ivp(fun=model, t_span=(self.t0, self.t0+self.cycletime), \
                                  y0=np.array(self.state), args=[action], \
                                  t_eval=np.linspace(self.t0, self.t0+self.cycletime, 10))
        self.state = np.array(res.y[0:6,-1], dtype=np.float32)    # UPDATE STATES
        self.t0 = self.t0+self.cycletime

        # return forces
        a, delta = action # unpack the action variables, because delta is needed
        omega_after_int = res.y[5,-1] # get current angle velocity
        try:
            R = (self.LF+self.LR)/math.tan(delta) * 1/(math.atan(math.tan(delta) * self.LR/(self.LF+self.LR)))
            F_ctfg = self.M * omega_after_int**2 * R # centrifugal force
        except ZeroDivisionError:
            F_ctfg = 0

        # set car to new position
        self.car01.set_car_pos(self.state[0], self.state[1], self.state[2], delta) # inputs: x,y,psi,delta

        # Convert a possible numpy bool to a Python bool
        done = bool(self.state[0] >= self.goal_position)
        done = False

        # Reward
        reward = 0

        # get sensordata of a car
        s1_rightborder, s1_leftborder = self.road.get_sensordata(self.car01.c4, self.car01.s01)
        s3_rightborder, s3_leftborder = self.road.get_sensordata(self.car01.c4, self.car01.s03)
        s5_rightborder, s5_leftborder = self.road.get_sensordata(self.car01.c4, self.car01.s05)
        s7_rightborder, s7_leftborder = self.road.get_sensordata(self.car01.c4, self.car01.s07)
        s9_rightborder, s9_leftborder = self.road.get_sensordata(self.car01.c4, self.car01.s09)
        sensordata = [s1_leftborder, s1_rightborder, s3_leftborder, s3_rightborder, s5_leftborder, s5_rightborder, s7_leftborder, s7_rightborder, s9_leftborder, s9_rightborder]

        collision_check = self.road.collision_check(self.car01)
        if collision_check:
            self.car01.set_resume_pos(self.road.get_center_line(), self.road.get_right_line(), self.road.get_left_line())

        # check critical centrifugal force
        Fmax = self.M * 9.81 * self.MU # radius of traction circle
        Fres = math.sqrt((self.M * a)**2 + F_ctfg**2) # resulting force
        if Fres > Fmax:
            self.car01.set_resume_pos(self.road.get_center_line(), self.road.get_right_line(), self.road.get_left_line())
            self.state[3:6] = 0, 0, 0 # set velocities and psi to zero


        if not done:
            reward -= 1.0
        else:
            reward = 100.0

        info = dict()
        observation = np.concatenate([self.state, sensordata])
        return np.array([observation], dtype=np.float32).flatten(), reward, done, info


    # Current Version of gym
    # def reset(self, seed: Optional[int] = None):
    #     super().reset(seed=seed)

    def reset(self): # FOR OLD VERSION OF GYM
        ### CONSTRUCT ROAD
        self.road = road_car.Road(self.canvas,self.FACTOR,self.WIDTH,self.HEIGHT,self.NPOINTS, self.ROADWIDTH)

        ### CONSTRUCT S
        self.car01 = road_car.Car(self.canvas, 140, 20,  0, 0, self.FACTOR, self.SENSFACTOR, "yellow")
        # self.car02 = env_road_car.Car(self.canvas, 140, 20,  0, 0, self.FACTOR, self.SENSFACTOR, "red")
        # etc.

    # hier Streckeninitialisierung implementieren
        # self.road_slope = self.np_random.randint(low=-10, high=10)*self.np_random.random()
        self.road_bias  = self.np_random.randint(low=-10, high=10)*self.np_random.random()
        self.state = (0,self.road_bias,0,0,0,0)
        self.t0 = 0
        return np.array(self.state, dtype=np.float32)

    def render(self, mode='human'):
        pass
        # if mode == 'human':
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
