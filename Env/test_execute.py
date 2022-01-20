# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 18:43:40 2022

@author: felix
"""
from stable_baselines3 import SAC
from env_PaceRace import PaceRaceEnv
from our_render import Render

env = PaceRaceEnv(P=1000)
# model = load("SAC_model")
c = 0
done = False
model = SAC.load("C://Users//felix//Desktop//sac_pace_race.zip")
# model = SAC.load("C://Users//felix//sciebo2//General//Studium Master//M.Sc. Maschinenbau//3. Semester//OKS//pace-race//Env//sac_pace_race.zip")
print('Starting new game.')
obs = env.reset() # get initial obs
# display = Render()
# display.update(env)
while True:
    c += 1
    print(c)    
    # action, _state = model.predict(obs) # get next action from last obs
    # print(action[0], obs[3])
    # action = env.action_space.sample()
    # print(action[0], obs[3])
    # obs, reward, done, info = env.step(action) # input action, get next obs
    obs, reward, done, info = env.step((0.001,0.1))
    if done:
        # display.show()
        print("End of race")
        break # end if done
    # display.update(env) # render that current obs