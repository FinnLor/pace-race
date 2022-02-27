# -*- coding: utf-8 -*-
"""
Created on Feb 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""

import cb_LogTraining as LogTraining
import matplotlib.pyplot as plt
# %matplotlib qt # run in console to externalize figures

def my_plotter(ax, xData, yData, title, xlabel, ylabel, param_dict):
    """
    A helper function to make a graph.
    """
    if xData == None:
        out = ax.plot(yData, **param_dict)
    else:
        out = ax.plot(xData, yData, **param_dict)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.tight_layout()
    return out

### Load data into dataframe
path = r'..\TrainLog\CustomLog'
df = LogTraining.load_Log(path)

### Load data into dataframe
path_def = r'..\TrainLog\DefaultLog'
df_def = LogTraining.load_Log(path)

### Plot

# example 1
fig, ax = plt.subplots()
ax.plot(df["Fres"], label="Fres")
ax.set_title(r'$\sigma_i=15$')
ax.set_xlabel('Iterations')
ax.set_ylabel('Force in N')
ax.legend()

# example 2
fig, (ax1,ax2) = plt.subplots(2,1)
my_plotter(ax1, None, df["obs0"], "Plot1", "xAxis", "yAxis", {'marker': '.', 'label': 'obs0'})
my_plotter(ax2, None, df["obs1"], "Plot2", "xAxis", "yAxis", {'marker': 'x', 'label': 'obs1'})

# example 3
fig, (ax3,ax4,ax5) = plt.subplots(3,1)
my_plotter(ax3, None, df_def["r"], "Rewards", "xAxis", "rew", {'marker': '', 'label': ''})
my_plotter(ax4, None, df_def["l"], "Length of episodes", "xAxis", "len", {'marker': '', 'label': ''})
my_plotter(ax5, None, df_def["t"], "Number of episodes", "xAxis", "num_ep", {'marker': '', 'label': ''})

