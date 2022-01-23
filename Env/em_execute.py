



from env_PaceRace import PaceRaceEnv
from our_render import Render
from stable_baselines3 import SAC
import tkinter as tk 
import numpy as np



env = PaceRaceEnv(P=1000, custom_roadwidth=20)
env.reset()
display = Render()
display.update(env, done=False)
for i in range(1000):
    env.step((0.3, 0.000))
    display.update(env, False)

display.update(env, True)

# display.main(env)

    