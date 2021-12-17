import os
import env_PaceRaceV2
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from plotting import plot_returns


### CONFIGURATION
config = {'total_timesteps': 300_000,
          'learning_rate': 3E-3,
          'network_size': [128, 128],
          'exploration_final_eps': 0.05,
          'exploration_fraction': 0.8,
          'n_eval_episodes': 20,
          'eval_freq': 25_000,
          'checkpoint_freq': 50_000}


### ENV SETUP
env = Monitor(env_PaceRaceV2.PaceRaceEnv())
check_env(env, warn=True)

### MODEL SETUP
model = DQN('MlpPolicy',
            env,
            verbose=0,
            gamma=1.0,
            exploration_final_eps=config['exploration_final_eps'],
            exploration_fraction=config['exploration_fraction'],
            learning_rate=config['learning_rate'],
            policy_kwargs={'net_arch': config['network_size']})

### EVAL INIT MODEL
print('Random Agent, before training')
mean_reward, std_reward = evaluate_policy(model,
                                          env,
                                          n_eval_episodes=config['n_eval_episodes'],
                                          deterministic=True)
print(f'mean_reward={mean_reward:.2f} +/- {std_reward}')

### CALLBACKS
eval_callback = EvalCallback(env,
                             best_model_save_path='best',
                             eval_freq=config['eval_freq'],
                             n_eval_episodes=config['n_eval_episodes'],
                             deterministic=True,
                             render=False)

checkpoint_callback = CheckpointCallback(save_freq=config['checkpoint_freq'],
                                         save_path=os.path.join('best', 'checkpoints'),
                                         name_prefix='rl_model')

### TRAINING
print('Start training')
model.learn(total_timesteps=config['total_timesteps'],
            callback=[eval_callback, checkpoint_callback])

### PLOTTING
plot_returns(env.get_episode_rewards(), filename=os.path.join('best', 'env_return_history.png'))

### TEST GAMES
print('Play 5 games')
game_counter = 0
done = True
while True:
    if done:
        game_counter += 1
        if game_counter > 5:
            break
        print()
        print('Starting new game.')
        obs = env.reset()
        
    action, _state = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render(mode='console')
    print()

env.close()