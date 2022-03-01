# PaceRace

Welcome to PaceRace, a student project to optimize the laptime of a 2D vehicle on randomly generated tracks based on reinforcement learning.

## Description

In Progress.

## Getting Started
In this work we aim to optimize the lap time of a vehicle on randomly generated tracks. A two dimensional, dynamical vehicle model is derived and a simple generator of random 2D-tracks is developed. We show one way to define a useful reward function for the problem and then apply reinforcement learning algorithms to solve the optimization task. The implementation of equations and frameworks is presented. The results are validated by performing a parameter study on the friction coefficient concerning tire and track, where an agent is trained in various settings and the resulting performances are examined.


### Dependencies

* csv
* gym
* json
* math
* matplotlib   
* numpy  
* os  
* pandas
* pickle
* pillow   
* random  
* scipy  
* shapely  
* stable_baselines3  
* tkinter  

For a Windows operating system, install the conda environment from folder ```condaEnv/```.

### Installing

```
git clone https://github.com/FinnLor/pace-race.git
```

### Executing program

* Use train.py to train an agent for a specified number of iterations
* GUI.py opens a GUI where you can load a SAC model and run it either on randomized tracks or on a track that you individually specify by width and path points

### Models
* Trained agents of a parameter study and a algorithm benchmarking study can be found in ```models/```.


## Authors

Contributors names and contact info

Finn Lorenzen  
Eliseo Milonia  
Felix Schönig  


## Version History


* Pre-Alpha
    * work-in-progress
