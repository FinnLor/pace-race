# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 20:52:18 2021

@author: felix
"""

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import math


# parameters
cf = 0.7
cr = 0.7
m = 1
Jz = 1
lf = 1
lr = 1
par = [cf, cr, m, Jz, lf, lr]

# inputs
vlon = 1
delta = 0.0

# initial conditions
vlat0 = 0
omega0 = 0
psi0 = 0

# current states
vlat = 0
omega = 0
psi = 0
x = 0
y = 0
states = np.array([vlat, omega, psi, x, y])

def model(t, states, vlon, delta):
    cf = 0.7
    cr = 0.7
    m = 1
    Jz = 1
    lf = 1
    lr = 1
    vlat, omega, psi, x, y = states
    dvlatdt = -omega*vlon + 1/m* (-cr*math.atan2(vlat-omega*lr, vlon) -math.cos(delta)*cf*math.atan2(-vlon*math.sin(delta)+math.cos(delta)*vlat+math.cos(delta)*omega*lf, vlon*math.cos(delta)+math.sin(delta)*vlat+math.sin(delta)*omega*lf))
    domegadt = 1/Jz * (cr*lr*math.atan2(vlat-omega*lr, vlon) -cf*lf*math.atan2(-vlon*math.sin(delta)+math.cos(delta)*vlat+math.cos(delta)*omega*lf ,vlon*math.cos(delta)+math.sin(delta)*vlat+math.sin(delta)*omega*lf))
    dpsidt = omega
    dxdt = vlon*math.cos(psi) - vlat*math.sin(psi)
    dydt = vlon*math.sin(psi) + vlat*math.cos(psi)
    return dvlatdt, domegadt, dpsidt, dxdt, dydt





t0 = 0
tmax = 10
n_steps = int((tmax-t0)/0.01)
t = np.linspace(t0,tmax,n_steps)

res = integrate.solve_ivp(fun=model, t_span=(t0, tmax), y0=states, args=(vlon, delta), t_eval=t)

# %matplotlib qt
# plt.plot(res.t, res.y[0:2].T) # plot vlat, omega
plt.plot(res.y[3].T, res.y[4].T)

##############################################################################
# Workflow implementation example
##############################################################################

# n = 100 # number of steps
# t0 = 0 # starting point in time
# step = 0.05 # cycle time
# invlon = 1
# indelta = 0
# inp = (invlon, indelta)
# logger = np.zeros((5, n))

# for i in range(n):
#     # inp = tuple(np.random.randn(2)*0.05 + inp)
#     # inp = tuple(np.array([0.0,0.5])+ inp)
#     inp = (1,0)
#     res = integrate.solve_ivp(fun=model, t_span=(t0, t0+step), y0=states, args=inp, t_eval=np.linspace(t0,t0+step, 10))
#     vlat = res.y[0, -1]
#     omega = res.y[1, -1]
#     psi = res.y[2, -1]
#     x = res.y[3, -1]
#     y = res.y[4, -1]
#     states = np.array([vlat, omega, psi, x, y])
#     t0 += step
#     logger[0:5, i] = res.y[0:5, -1]
    
# plt.plot(logger[3], logger[4])