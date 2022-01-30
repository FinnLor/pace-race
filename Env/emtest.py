import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import time as t

# jede Iteration einen Punkt setzen explizit bei Scatterplots!
# analog zu "Hold On"




fig, ax = plt.subplots()
scat = ax.scatter(rnd.random(),rnd.random(), c='black')
ax.set_xlim(-0,1)
ax.set_ylim(-0,1)
fig.canvas.draw()


for i in range(2000):
    
    data_old = scat.get_offsets()
    point_new = [rnd.random(),rnd.random()]
    data_new = np.concatenate([data_old,np.array(point_new, ndmin=2)])
    scat.set_offsets(data_new)
    
    scat.update_scalarmappable()
    scat.axes.figure.canvas.draw_idle()
    fig.canvas.flush_events() 
    # fig.canvas.draw()
    # t.sleep(0.01)
    


