# -*- coding: utf-8 -*-
"""
Created on Jan 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""


from env_PaceRace import PaceRaceEnv
from LogTraining import CustomTrainingLogCallback, load_Log 
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3 import SAC, A2C


### CONFIGURATION
config = {'total_timesteps': 500,
          'log_keys': ('obs', 'act', 'Fres'),           # custom Logger
          'log_freq_epoch': 10,                         # custom Logger
          'log_freq_step': 10,                          # custom Logger
          'monitor_log_path': 'TrainLog/DefaultLog',    # integrated Logger
          'save_path_models': "models//sac_pace_race"}


### ENV SETUP
env = Monitor(PaceRaceEnv(verbose = 0), filename=config['monitor_log_path'])
check_env(env, warn=True)


### MODEL SETUP
model = SAC("MlpPolicy",
            env,
            verbose=1,
            seed=0
            )

# Load pre-trained model
# model = SAC.load("models/sac_pace_race_FL_01_20220122.zip")
# model = SAC.load("models/sac_pace_race_FS_02_210122.zip")
# model = SAC.load("models/sac_pace_race_EM_01_230122.zip")

# Check validity of environment
model.set_env(env)


### TRAINING
print('Start training')
callback=CustomTrainingLogCallback(info_keywords = config['log_keys'], 
                                   log_freq_epoch=config['log_freq_epoch'], 
                                   log_freq_step=config['log_freq_step'])
model.learn(config['total_timesteps'], callback=callback)
print('End of training')
env.close()
model.save(config['save_path_models'])


# Load Log
#Log = load_Log('TrainLog/CustomLog')
