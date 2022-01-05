
import os
import random
from matplotlib import pyplot as plt
import numpy as np

def plot_returns(returns, filename):
    def moving_average(x, window_size):
        # https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
        return np.hstack([np.empty(window_size//2,)*np.nan, 
                          np.convolve(x, np.ones(window_size), 'valid') / window_size,
                          np.empty(window_size//2,)*np.nan])
    
    plt.ioff()
    plt.plot(returns, label='Return', alpha=0.7)
    plt.plot(moving_average(returns, 100), label='Average return (window_size=100)', lw=3)
    plt.plot(moving_average(returns, 1_000), label='Average return (window_size=1000)', lw=3)
    plt.ylabel('Return')
    plt.xlabel('Episode')
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.cla()
    plt.clf()
    plt.close()
    
    
    
### PLOTTING
plot_returns(random(), filename=os.path.join('best', 'env_return_history.png'))
