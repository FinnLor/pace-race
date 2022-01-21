# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 18:43:40 2022

@author: felix
"""
from stable_baselines3 import SAC
from env_PaceRace import PaceRaceEnv
from our_render import Render

env = PaceRaceEnv()
# model = load("SAC_model")
c = 0
done = False
model = SAC.load("models//sac_pace_race_FS_02_210122.zip")
# model = SAC.load("C://Users//felix//sciebo2//General//Studium Master//M.Sc. Maschinenbau//3. Semester//OKS//pace-race//Env//sac_pace_race.zip")
print('Starting new game.')
obs = env.reset() # get initial obs
display = Render()
display.update(env, done)
while True:
    # c+=1
    # print(c)
    # action = env.action_space.sample() # random
    # obs, reward, done, info = env.step((0.001,0.1)) # manual
    action, _state = model.predict(obs) # agent, get next action from last obs
    obs, reward, done, info = env.step(action) # input action, get next obs
    display.update(env, done) # render that current obs
