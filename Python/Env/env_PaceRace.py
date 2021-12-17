import math
from typing import Optional

import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt

import gym
from gym import spaces
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
    

    def __init__(self, CF=0.7, CR=0.7, M=1, JZ=1, LF=1, LR=1, CT=0.1):
        
        # Car-Design
        self.CF = CF
        self.CR = CR
        self.M = M
        self.JZ = JZ
        self.LF = LF
        self.LR = LR
        
        # Numerical timestamp
        self.cycletime = CT
        self.t0 = 0
        
        # # Road
        # self.road_path = lambda x,slope,bias : x*slope+bias
                
        # Actions and Observations
        self.max_x_position = np.finfo(np.float32).max
        self.min_x_position = 0
        
        self.max_y_position = np.finfo(np.float32).max
        self.min_y_position = np.finfo(np.float32).min
        
        self.max_yaw_angle = 2*np.pi
        self.min_yaw_angle = 0                                      # DAS IST KOMPLIZIERT ZU BEHANDELN !!! -> Modulo
        
        self.max_velocity_lon = 10
        self.min_velocity_lon = 0
        
        self.max_velocity_lat = 10
        self.min_velocity_lat = 0
    
        self.max_acceleration = 10
        self.min_acceleration = -self.max_acceleration
        
        self.max_steering_angle = 60
        self.min_steering_angle = -self.max_steering_angle
        
        self.max_omega = 2*np.pi
        self.min_omega = 0
        
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
                 self.min_omega], dtype=np.float32
        )
        self.high_state = np.array(
            [self.max_x_position, self.min_y_position, self.max_yaw_angle, \
             self.max_velocity_lon, self.max_velocity_lat, \
                 self.max_omega], dtype=np.float32
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
        x, y, psi, a, vlat, omega = self.state
        res = integrate.solve_ivp(fun=model, t_span=(self.t0, self.t0+self.cycletime), \
                                  y0=np.array(self.state), args=[action], \
                                  t_eval=np.linspace(self.t0, self.t0+self.cycletime, 10))
        self.state = tuple(res.y[0:6,-1])    # UPDATE STATES
        self.t0 = self.t0+self.cycletime
        
        # Convert a possible numpy bool to a Python bool
        done = bool(self.state[0] >= self.goal_position)
        
        # Reward
        reward = 0
        # TODO: hier Kollisionsabfrage zwischen fzg u strecke abfragen
        # TODO: hier F-Kritisch abfragen (aus der Kurve fliegen)
        if not done:
            reward -= 1.0
        else:
            reward = 100.0
            
        info = dict()
        return self.state, reward, done, info
    
    # Current Version of gym
    # def reset(self, seed: Optional[int] = None):
    #     super().reset(seed=seed)
    def reset(self): # FOR OLD VERSION OF GYM
    # hier Streckeninitialisierung implementieren
        self.road_slope = self.np_random.randint(low=-10, high=10)*self.np_random.random()
        self.road_bias  = self.np_random.randint(low=-10, high=10)*self.np_random.random()
        self.state = (0,self.road_bias,0,0,0,0)
        self.t0 = 0
        return np.array(self.state, dtype=np.float32)

    def render(self, mode='human'):
        if mode == 'human':
            plt.scatter(self.state[0], self.state[1], s=20, marker='o', color='g') 

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

