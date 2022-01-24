



from env_PaceRace import PaceRaceEnv
from our_render import Render
from stable_baselines3 import SAC
import tkinter as tk 
import numpy as np

env = PaceRaceEnv()
done = False
i=0
# model = SAC.load("models/sac_pace_race_FS_02_210122.zip")
model = SAC.load("models/sac_pace_race_em01.zip")

obs = env.reset() # get initial obs
display = Render()
display.update(env, done)
while True:
    i+=1
    # action = env.action_space.sample() # random
    # obs, reward, done, info = env.step((0.001,0.1)) # manual
    action, _state = model.predict(obs) # agent, get next action from last obs
    obs, reward, done, info = env.step(action) # input action, get next obs
    print(f'STEP: {i}')
    display.update(env, done) # render that current obs
