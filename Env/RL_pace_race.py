
from env_PaceRace import PaceRaceEnv
from stable_baselines3 import SAC, A2C
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from LogTraining import CustomTrainingLogCallback, load_Log 

### CONFIGURATION
config = {'total_timesteps': 100_000,
          'log_keys': ('obs', 'act'),                   # custom Logger
          'log_freq_epoch': 10,                         # custom Logger
          'log_freq_step': 1,                           # custom Logger
          'monitor_log_path': 'TrainLog/DefaultLog',    # integrated Logger
          'save_path_models': "models//sac_pace_race"}


### ENV SETUP
env = Monitor(PaceRaceEnv(verbose = 1), filename=config['monitor_log_path'])
check_env(env, warn=True)


### MODEL SETUP
model = SAC("MlpPolicy",
            env,
            verbose=1,
            )

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
#Log = load_Log('TrainLog/myLog')
