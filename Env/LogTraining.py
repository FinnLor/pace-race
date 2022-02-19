# -*- coding: utf-8 -*-
"""
Created on Jan 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""


from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import DummyVecEnv, VecEnv
import gym

from typing import Tuple, Union
import csv
import json
import os
import warnings
import pandas
import numpy as np


class CustomTrainingLogCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: (int) Verbosity level 0: not output 1: info 2: debug
    """
    def __init__(self,  info_keywords: Tuple[str, ...], log_dir: str = 'TrainLog', log_name: str = 'CustomLog', 
                 log_freq_epoch: int = 1_000, log_freq_step: int = 1, verbose=0):
        
        super(CustomTrainingLogCallback, self).__init__(verbose)
        
        self.log_freq_epoch = log_freq_epoch
        self.log_freq_step = log_freq_step
        
        self.log_name = log_name
        self.log_dir = log_dir
        
        self.info_keywords = info_keywords
        
        # Create folder if needed
        save_path = os.path.join(self.log_dir)
        if save_path is not None:
            os.makedirs(save_path, exist_ok=True)

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
        
        filename = os.path.join(self.log_dir, self.log_name +".monitor.csv")
        
        header = {}
        # Open file
        self.file_handler = open(filename, "wt", newline="\n")
        self.file_handler.write("#%s\n" % json.dumps(header))
        # self.logger = csv.DictWriter(self.file_handler, fieldnames=("epoch","iter") + self.info_keywords)
        # self.logger.writeheader()
        self.file_handler.flush()
        
        # Initialize counter
        self.iter = 0
        
        # 
        self.before_first_step = True

    def _on_rollout_start(self) -> None:
        pass

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: (bool) If the callback returns False, training is aborted early.
        """

        # Now the length of the info_dict entries is known, so we update the headers accordingly
        if self.before_first_step:
            updated_fieldnames = ["epoch","iter"]
            for key in self.info_keywords:
                try: # works only for a sequence (string, tuple, list ...) or collection (dict, set...)
                    for i in range(len(self.model.env.buf_infos[0][key])):
                        subkey = key + str(i)   
                        updated_fieldnames.append(subkey)
                except TypeError:
                    updated_fieldnames.append(key)
            
            self.logger = csv.DictWriter(self.file_handler, fieldnames=updated_fieldnames)
            self.logger.writeheader()
            
            self.before_first_step = False
            

        # Write to file 
        if (self.model._episode_num % self.log_freq_epoch) == 0:  
            if self.iter % self.log_freq_step == 0:
                
                ret = {'epoch': self.model._episode_num,'iter': self.iter}
                for key in self.info_keywords:
                    try: # works only for a sequence (string, tuple, list ...) or collection (dict, set...)
                        for i in range(len(self.model.env.buf_infos[0][key])):
                            subkey = key + str(i)
                            ret[subkey] = self.model.env.buf_infos[0][key][i]
                    except TypeError:
                        ret[key] = self.model.env.buf_infos[0][key]
                            
                self.logger.writerow(ret)
                self.file_handler.flush()

        if self.model.env.buf_dones[0]:
            self.iter = 0
        else: 
            self.iter += 1 

        return True

    def _on_rollout_end(self) -> None:
        pass

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        # Close file
        self.file_handler.close()
        
  
        
  
class CustomEvalLogCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: (int) Verbosity level 0: not output 1: info 2: debug
    """
    def __init__(self,  eval_env: Union[gym.Env, VecEnv], 
                 eval_center_lines, 
                 eval_roadwidths, 
                 log_dir: str = 'TrainLog', 
                 log_name: str = 'EvalLog', 
                 log_freq_epoch: int = 10, 
                 verbose=0):
        
        super(CustomEvalLogCallback, self).__init__(verbose)
        
        # Convert to VecEnv for consistency
        if not isinstance(eval_env, VecEnv):
            eval_env = DummyVecEnv([lambda: eval_env])
        self.eval_env = eval_env
  
        # Check and set eval-roads
        assert len(eval_center_lines) == len(eval_roadwidths)
        self.n_eval_roads = len(eval_center_lines)
        for i in range(self.n_eval_roads):
            assert eval_roadwidths[i] > 0, "All eval_roadwidths has to be non-negative!"
            assert (isinstance(eval_center_lines[i],np.ndarray) and
                    eval_center_lines[i].ndim == 2 and
                    eval_center_lines[i].shape[1] == 2) , "All eval_center_lines has to be [nx2] np.ndarray!"
        self.eval_center_lines = eval_center_lines
        self.eval_roadwidths = eval_roadwidths
        
        # Logger
        self.log_freq_epoch = log_freq_epoch
        self.log_name = log_name
        self.log_dir = log_dir
        
        # Create folder if needed
        save_path = os.path.join(self.log_dir)
        if save_path is not None:
            os.makedirs(save_path, exist_ok=True)
        

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
               
            
        if not isinstance(self.model.env, type(self.eval_env)):
            warnings.warn("Training and eval env are not of the same type" f"{self.model.env} != {self.eval_env}")
        
        
        filename = os.path.join(self.log_dir, self.log_name +".monitor.csv")
        
        header = {}
        # Open file
        self.file_handler = open(filename, "wt", newline="\n")
        self.file_handler.write("#%s\n" % json.dumps(header))
        
        fieldnames=["epoch"]
        for i in range(self.n_eval_roads):
            subkey1 = "num_iter_road_" + str(i)
            subkey2 = "reward_road_" + str(i)
            fieldnames.append(subkey1)
            fieldnames.append(subkey2)
    
        self.logger = csv.DictWriter(self.file_handler, fieldnames=fieldnames)
        self.logger.writeheader()
        self.file_handler.flush()
        

    def _on_rollout_start(self) -> None:
        pass

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: (bool) If the callback returns False, training is aborted early.
        """
         

        # Write to file 
        if (self.model._episode_num % self.log_freq_epoch) == 0 and self.model.env.buf_dones[0]:  

            ret = {'epoch': self.model._episode_num}
            for i in range(self.n_eval_roads): 
                self.eval_env.envs[0].env.custom_center_line = self.eval_center_lines[i]
                self.eval_env.envs[0].env.roadwidth = self.eval_roadwidths[i]
                episode_rewards = 0
                episode_lengths = 0
                obs = self.eval_env.reset() # get initial obs
                done = False
                while done == False:
                    action, _state = self.model.predict(obs, deterministic=True) 
                    obs, reward, done, info = self.eval_env.step(action)
                    episode_rewards += reward
                    episode_lengths += 1
                ret.update({"num_iter_road_"+ str(i): episode_lengths, "reward_road_" + str(i): episode_rewards[0]})
                
            self.logger.writerow(ret)
            self.file_handler.flush()

        return True

    def _on_rollout_end(self) -> None:
        pass

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        # Close file
        self.file_handler.close()
        
        
        
        
def load_Log(file_name: str):
    file_name = file_name + ".monitor.csv"
    with open(file_name, "rt") as file_handler:
        first_line = file_handler.readline()
        assert first_line[0] == "#"
        data_frame = pandas.read_csv(file_handler, index_col=None)
    return data_frame
        
