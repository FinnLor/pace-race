# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:18:33 2021

@author: emilo
"""


import random as rnd
import numpy as np
import math as m
import matplotlib.pyplot as plt


n = np.linspace(0.5, 2*m.pi, 400)
x = m.pow((-1),rnd.randrange(1,3,1)) * (n + 3*rnd.uniform(0,1)*np.tan(0.2*n))
y = 1./n + rnd.uniform(0,1)*3.*np.cos(n)*np.power(np.sin(n),2)
plt.plot(x,y)
