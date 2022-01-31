# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 18:43:40 2022

@author: felix
"""
from stable_baselines3 import SAC
from env_PaceRace import PaceRaceEnv
from our_render import Render, load_model

filename = load_model()

env = PaceRaceEnv(verbose =1)
c = 0
done = False
model = SAC.load(filename)
print('Starting new game.')
obs = env.reset() # get initial obs
display = Render()
while True:
    # c+=1
    # print(c)
    # action = env.action_space.sample() # random
    # obs, reward, done, info = env.step((0.001,0.1)) # manual
    action, _state = model.predict(obs) # agent, get next action from last obs
    obs, reward, done, info = env.step(action) # input action, get next obs
    display.update(env, done, info, plot_performance=True) # render that current obs
