# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:34:19 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""

import LogTraining
import matplotlib as mpl
import matplotlib.pyplot as plt

# Load data into dataframe
path = r'TrainLog\CustomLog'
df = LogTraining.load_Log(path)

# Plot
fig, ax = plt.subplots()
ax.plot(df["Fres"])
ax.set_title("Test")
ax.set_xlabel('entry a')
ax.set_ylabel('entry b');