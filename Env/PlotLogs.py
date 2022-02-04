# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:34:19 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""

import LogTraining
import matplotlib.pyplot as plt

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
path = r'TrainLog\CustomLog'
df = LogTraining.load_Log(path)

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
