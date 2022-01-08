# -*- coding: utf-8 -*-
"""
Created on Jan 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""

import pickle
import numpy as np
#import pandas as pd    # summarizing in dataframe is slow... 
                        # ... and maybe not necessary?
import warnings

def helper_load_logged_data(file: str):
    """
    
    Loads a stored stable_baselines3.her.her_replay_buffer.HerReplayBuffer and extracts epoch, observations, actions and rewards for each timestep. 
    Due to the limited length of the stable_baselines3.her.her_replay_buffer.HerReplayBuffer of 1,000,000 timesteps, 
    the function only works correctly if the replay_buffer is not full.

    ...
    
    Parameters
    ----------
    file : str
        Full file name (incl. path and file extension) of the stable_baselines3.her.her_replay_buffer.HerReplayBuffer.

    Returns
    -------
    epoch : float or int array
        Number of the epoch for each time step.
    observations : float or int array
        Observations for each time step.
    actions : float or int array
        Actions for each time step.
    rewards : float or int array
        Rewards for each time step.

    """
    
    # Load file
    with open(file, 'rb') as f:
        data = pickle.load(f)
    
    # Find number of logged timesteps
    timesteps = data.size()
    if timesteps >= 1_000_000: # 1_000_000 is the length of the stable_baselines3.her.her_replay_buffer.HerReplayBuffer
        warnings.warn("Maximum possible number of logged time steps was exceeded. The results are incomplete and the variable ""epoch"" is not correct.")
    
    # Get number of epoch and rewards
    epoch = np.cumsum(data.dones)[0:timesteps]
    rewards = data.rewards.squeeze()[0:timesteps]
    
    # Get observations
    if len(data.observation_space.shape) == 1:
        observations = data.observations.squeeze()[0:timesteps,:]
    elif len(data.observation_space.shape) == 0:
        observations = data.observations.squeeze()[0:timesteps]
    else:
        warnings.warn('Error in dimension of observations.')
      
    # Get actions
    if len(data.action_space.shape) == 1:
        actions = data.actions.squeeze()[0:timesteps,:]
    elif len(data.action_space.shape) == 0:
        actions = data.actions.squeeze()[0:timesteps]
    else:
        warnings.warn('Error in dimension of actions.')
        
    return epoch, observations, actions, rewards 


def helper_rendering():
    # Render using tkinter
    pass


if __name__ == "__main__":
    epoch, observations, actions, rewards = helper_load_logged_data('example_ReplayBuffer.pkl') # File to large for github...


