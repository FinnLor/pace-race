import os
# import numpy as np
from env_PaceRace import PaceRaceEnv
from stable_baselines3 import SAC, A2C
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback, CallbackList, BaseCallback, EveryNTimesteps
from stable_baselines3.common.env_checker import check_env
# from stable_baselines3.common.vec_env import DummyVecEnv, VecCheckNan
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
#from plotting import plot_returns

from LogTraining import CustomTrainingLogCallback, load_Log # Logging

### CONFIGURATION
config = {'total_timesteps': 40000,
          'learning_rate': 3E-3,
          'n_eval_episodes': 20,
          'eval_freq': 5000,
          'checkpoint_freq': 5000}


### ENV SETUP
env = Monitor(PaceRaceEnv())
check_env(env, warn=True)
# env = DummyVecEnv([lambda: PaceRaceEnv()])
# env = VecCheckNan(env, raise_exception=True)   

### MODEL SETUP
model = SAC("MlpPolicy",
            env,
            verbose=1,
            )

# ### EVAL INIT MODEL
# print('Random Agent, before training')
# mean_reward, std_reward = evaluate_policy(model,
#                                           env,
#                                           n_eval_episodes=config['n_eval_episodes'],
#                                           deterministic=True,
#                                           render=True)
# print(f'mean_reward={mean_reward:.2f} +/- {std_reward}')

### CALLBACKS
eval_callback = EvalCallback(eval_env=env,
                              best_model_save_path="best",
                              eval_freq=config['eval_freq'],
                              n_eval_episodes=config['n_eval_episodes'],
                              deterministic=True,
                              render=False)

checkpoint_callback = CheckpointCallback(save_freq=config['checkpoint_freq'],
                                         save_path=os.path.join('best', 'checkpoints'),
                                         name_prefix='rl_model')



# callbacks = CallbackList([checkpoint_callback, eval_callback])
# callback = SaveOnBestTrainingRewardCallback(check_freq=2000, log_dir=log_dir)

### TRAINING
print('Start training')
model.learn(10, callback=CustomTrainingLogCallback(info_keywords = ('obs', 'act'), log_freq_epoch=10_000, log_freq_step=2))
# model.learn(total_timesteps=config['total_timesteps'],
#             callback=[eval_callback, checkpoint_callback])
print('End of training')

env.close()
model.save("models//sac_pace_race") # save model like this


# Load Log
Log = load_Log('TrainLog/myLog')

''' 
model.save("a2c_pace_race") # save model like this
model = A2C.load("a2c_pace_race") # load model like this
# test model like this:
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    if done:
        break
    env.render()
'''