# -*- coding: utf-8 -*-
"""
Created on Dec 2021

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""


from gym.utils import seeding
import gym
import math
import numpy as np
import random

# Custom
from cls_Car import Car
from cls_Road import Road


class PaceRaceEnv(gym.Env):
    """
    
    Reinforcement learning environment 'Pace Race'. 
    All physical quantities are to be interpreted in Si base units.
    
    Objective: Minimize lap time.
    ---------
    
    Actions (continuous action space): 
    ---------------------------------
    
        Action				         |  min  |  max  |
        ----------------------------------------------                          
        Power 				        |  -1   |    1  |
        Change of steering angle    |  -1   |    1  |
        
    Observations (continuous observation space):
    -------------------------------------------
    
        Observation                 |  min  |  max  |
        ---------------------------------------------
        Longitudinal velocity       |   0   |  100 |
        Lateral velocity            | -100  |  100 |
        Angular velocity            | -inf  |  inf |
        Total steering angle        | -45°  |  45° |
        Sensor distance measurement |   0   |   1  |
        (5 sensors)

    Restrictions:
    ------------
        No collision with lane boarders.
        No exceeding of friction


    Reward: Define your own reward function in step-function.
    ------

    Assumptions: 
    -----------
    	The car moves in 2-dimensional plane.
         car has a minimum speed o 1e-5 m/s.
         There is friction on the wheels only.
         The wheelbase corresponds to the vehicle length.
         One road has the same width for whole length.

    """

    def __init__(self, CF=49_000, CR=49_000, M=1_000, LF=2, LR=2, CAR_WIDTH=2, SENS_SCALE=1, CT=0.1, MU=1.0, P=100_000, ROADLENGTH = 10, verbose = 0, custom_center_line = None, custom_roadwidth=None):
        """
        
        Initializes Pace-Race reinforcement leratning object.
        
        Parameters
        ----------
        CF : int or float, optional
            Cornering stiffness front wheel. Non-negative value. The default is 49_000.
        CR : int or float, optional
            Cornering stiffness rear wheel. Non-negative value. The default is 49_000.
        M : int or float, optional
            Mass of car. Non-negative value. The default is 1_000.
        LF : int or float, optional
            Distance from center to front wheel. Non-negative value. The default is 2.
        LR : int or float, optional
            Distance from center to rear wheel. Non-negative value. The default is 2.
        CAR_WIDTH : int or float, optional
            Width of car. Non-negative value. The default is 2.
        SENS_SCALE : int or float, optional
            Factor for scaling the length of cars sensors. Non-negative value. The default is 1.
        CT : int or float, optional
        	Time step for numerical integration of car dynamics. Non-negative value. The default is 0.1.
        MU : int or float, optional
            Coefficient of friction road-wheels. Non-negative value. The default is 1.0.
        P : int or float, optional
            Power of car (used for acceleration and braking). Non-negative value. The default is 100_000.
        ROADLENGTH : int, optional
            Discrete factor for length of random road. Valid inputs: {2, 3, 4, 5, 6, 7, 8, 9, 10}. The default is 10.
        verbose : int, optional
            Verbose mode. Valid inputs: {0, 1, 2}. The default is 0.
        custom_center_line : None or np.ndarray with size [nx2], optional
            Custom trajectory in R2 [x,y]-value-pairs. The default is None.
        custom_roadwidth : None or int or float, optional
            Width of the roadway. Non-negative value. The default is None.

        Returns
        -------
        None.

        """
        
        
        # Check inputs
        assert MU >= 0 , "MU has to be non-negative!"
        valid_verbose = {0, 1, 2}
        if verbose not in valid_verbose:
                raise ValueError("verbose must be one of %r." % valid_verbose)
        
        # Initialize and assign car
        self.car01 = Car(LF=LF, LR=LR, CF=CF, CR=CR, WIDTH=CAR_WIDTH, M=M, P=P,\
                             x=0, y=0, psi=0, delta=0, SENS_SCALE=SENS_SCALE, CT=CT)
                    
        # Assign further properties
        self.MU = MU
        self.roadwidth = custom_roadwidth
        self.ROADLENGTH = ROADLENGTH
        self.custom_center_line = custom_center_line
        self.verbose = verbose

        # Radius of traction circle            
        self.Fmax = M * 9.81 * MU 
        
        # Initialize counter
        self.num_episodes = -1
        self.counter = 0
        
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

        self.max_delta_steering_angle = 30*CT*np.pi/180 # Zeitabhängig. entspricht 3 Grad Lenkwinkel der Räder pro Sekunde => ###########
        self.min_delta_steering_angle = -30*CT*np.pi/180         ############### !!! DAS IST FALSCH !!! ############################
        
        self.max_total_steering_angle = 45*np.pi/180
        self.min_total_steering_angle = -45*np.pi/180   

        self.max_omega = np.finfo(np.float32).max   
        self.min_omega = np.finfo(np.float32).min

        self.sensordata_min = 0
        self.sensordata_max = 1

        # Normalized action Space [power, delta_steering_angle]
        self.action_space = gym.spaces.Box(
            low=-1, high=1, shape=(2,), dtype="float32")

        # Observation Space [vlon, vlat, omega, total_steering_angle, sensor1, sensor3, sensor5, sensor7, sensor9]
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
        
        # Rescale the normalized actions
        range_action_Power = self.max_power - self.min_power # b-a
        range_action_delta_delta = self.max_delta_steering_angle - self.min_delta_steering_angle
        range_actions = np.array([range_action_Power, range_action_delta_delta])
        action_scaled = np.asarray(action) * 0.5 * range_actions + 0.5 * np.array([self.max_power + self.min_power, self.max_delta_steering_angle + self.min_delta_steering_angle]) # x * (b-a)/2 + (b+a)/2, dot-wise multiplied

        # Unpacking and conversion
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
        elif P > 0 and self.car01.vlon == 0:                    ## DAS SOLLTEN WIR NOCH ANPASSEN, da gar nicht alle Fälle auftreten dürfen!
            a = 9.81*self.MU/math.sqrt(2)
        elif P < 0 and self.car01.vlon == 0:
            a = -9.81*self.MU/math.sqrt(2) # problematic?
        elif P > 0 and self.car01.vlon != 0:
            a = min(P/(self.car01.M*self.car01.vlon), 9.81*self.MU/math.sqrt(2)) 
        elif P < 0 and self.car01.vlon != 0:
            a = max(P/(self.car01.M*self.car01.vlon), -9.81*self.MU/math.sqrt(2)) 
        else:
            raise NotImplementedError('Error in calculation of acceleration.')
            
        # Move car via dynamic model
        inputs = (a, delta) # must be a tuple
        self.car01.set_next_car_position(inputs) # calculate next car position with diff. eq.
        
        # Check if car has crossed the finish line (99,9% of roadlength)
        curr_path_length = self.car01.get_path_length(self.road)
        done = bool(curr_path_length >= 0.999)
       
        # calculate Fres (regardless of whether done is False or True)
        F_ctfg = self.car01.M * self.car01.omega * self.car01.vlon 
        Fres = math.sqrt((self.car01.M * a)**2 + F_ctfg**2) # resulting force, Pythagoras not correct because not perpendicular
    
        # Check for chash
        if done == False:
            # Collision check
            collision_check = self.car01.collision_check(self.road)
            
            # Check whether centrifugal force to high
            force_exceeded = Fres > self.Fmax
            
            # Bool to check whether limits were violated
            violation = collision_check or force_exceeded 
            
            # Set car to resume-position, when violation
            if violation:
                # done = True
                resume_successful = self.car01.set_resume_pos(self.road)
                if self.verbose != 0:
                    print(f"--got resumed! at {self.num_iterations}")
                if resume_successful == False:
                    raise NotImplementedError(f"Calculation of psi failed: {self.num_iterations}")
        else:
            violation = False
            
        ######################################################################
        ####################### --- REWARD SECTION --- ####################### 
        ######################################################################
               
        reward = 0
        #1
        reward -= 3 # penalize time on track
        #2
        if done:
            reward += 2000
        #3                       
        if self.num_iterations > 2000 and not done: # stop after a maximum o n iterations, this implies a penalty of -3n from #1
            done = True
            reward += -100 + curr_path_length * 200 # if stopped by exceeding time limit, reward proportionally to achieved progress
        #4
        if violation: # penalize violation (collision or force-check)
            reward -= (50 + self.num_episodes/100)
        #5    
        # reward += 0.3*self.car01.vlon
            
        # if a < 0:
        #     reward = reward - 2
        
        # if curr_path_length - self.last_path_length > 0.2: # reward driving forward
        #     reward = reward + 3
        
        # if curr_path_length < self.last_path_length: # punish driving backward
        #     reward = reward - 5
        
        self.episode_reward += reward
        
        # Update path_length
        self.last_path_length = curr_path_length # NEWER USED! Delete later
        
        # Get sensordata of a car
        sensdist = self.car01.get_sensordata(self.road, normalized=True)
        
        # Summarize observations
        observation = np.concatenate((np.array([self.car01.vlon, self.car01.vlat, self.car01.omega, self.car01.delta]), np.min(sensdist, axis = 1)), axis=None) # add MU for param study
        
        # Update info-dict
        info = {"obs": observation,"act": action, "Fres": Fres}
        
        # Print to terminal
        if self.verbose == 1: 
            print(f"=== counter: {self.counter} === no-episode:  {self.num_episodes:04.0F}")
        elif self.verbose == 2:
            print(f"action_scaled: {action_scaled[0]:09.2F} || a: {a:06.2F} || v_lon: {self.car01.vlon:05.2F} || pos: {np.round(curr_path_length,4)} || epoch: {self.num_episodes:04.0F} || eprew: {self.episode_reward} || iter: {self.num_iterations}, || counter: {self.counter}")
        if self.verbose != 0:
            if self.num_iterations%10000 == 0:
                print(f"----> {self.num_iterations}")
            elif self.num_iterations%2000 == 0:
                print("--")
                
        # Update counter
        self.num_iterations += 1
        self.counter += 1
                
        return np.array([observation], dtype=np.float32).flatten(), reward, done, info


    def reset(self): 
        
        # Print to terminal
        if self.verbose != 0:
            print(10*"---" + "**reset**" + 10*"---")    
    
        # Reset counter        
        self.episode_reward = 0 # track cumulative reward per episode
        self.num_iterations = 0
        self.num_episodes += 1
         
        # self.MU = round(random.uniform(0.3,1.0),2) # variable friction coefficient
        
        # # Construct new road
        # if self.custom_center_line == None:
        #     self.roadwidth = round(random.uniform(self.car01.WIDTH*5,self.car01.WIDTH*10), 2)
        #     self.road = Road(ROADWIDTH=self.roadwidth, ROADLENGTH = self.ROADLENGTH, NPOINTS = 1000)
        # else:
        #     self.road = Road(ROADWIDTH=self.roadwidth, custom_center_line = self.custom_center_line)
            
        # Construct new road
        if np.any(self.custom_center_line) == None:
            self.roadwidth = round(random.uniform(self.car01.WIDTH*5,self.car01.WIDTH*10), 2)
            self.road = Road(ROADWIDTH=self.roadwidth, ROADLENGTH = self.ROADLENGTH, NPOINTS = 1000)
        else:
            self.road = Road(ROADWIDTH=self.roadwidth, custom_center_line = self.custom_center_line)

        # Set car to start-position
        self.car01.set_start_pos(self.road) 
        self.last_path_length = 0

        self.t0 = 0

        # Get sensordata
        sensdist = self.car01.get_sensordata(self.road) # reads distances for each sensor in an array
        
        # Pack up
        observation = np.concatenate((np.array([self.car01.vlon, self.car01.vlat, self.car01.omega, self.car01.delta]), np.min(sensdist, axis = 1)), axis=None) # add MU for param study
        return np.array([observation], dtype=np.float32).flatten()

    def render(self, mode='human'):
        raise NotImplementedError('Please use custom, external rendering.')
        pass            
            
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def close(self):
        print('End of training')


if __name__ == '__main__':
    
    g = PaceRaceEnv(CF=49_000, CR=49_000, CT=0.1, custom_roadwidth=30)
    g.reset()
    
    for i in range(500):
        g.step((0.3, 0.000))
