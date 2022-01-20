# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 18:43:40 2022

@author: felix
"""

from env_PaceRace import PaceRaceEnv
from our_render import Render

env = PaceRaceEnv()
# model = load("SAC_model")
counter = 0
done = False

print('Starting new game.')
obs = env.reset() # get initial obs
display = Render()
while True:
        
    # action, _state = model.predict(obs) # get next action from last obs
    # obs, reward, done, info = env.step(action) # input action, get next obs
    obs, reward, done, info = env.step((1,0))
    display.update(env) # render that current obs
    
    if done:
        display.show()
        print("End of race")
        break # end if done