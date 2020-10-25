# Crowd Control demo

cadCAD crowd agent-based modelling approaches. Originally forked from prey-predator demo cadCAD model https://github.com/cadCAD-org/demos/tree/master/demos/Agent_Based_Modeling/prey_predator_abm

## File Structure

* lab_odyssey.ipynb - The notebook for experimenting and visualizing
* main.py - main script derivate of notebook
* helpers.py - helper scripts for main.py
* run.py - Script for running all configurated experiments
* crowd_control_abm/ - Folder for the ABM simulation and model 
* {simulation}/sim_params.py - Simulation parameters
* {simulation}/model/partial_state_update_block.py - The structure of the logic behind the model
* {simulation}/model/state_variables.py - Model initial state
* {simulation}/model/sys_params.py - Model parameters
* {simulation}/model/parts/ - Model logic

## Simulation goal

There are 2 types of agents: person and attraction. The goal is to balance the capacity of the attractions to the amount of visiting persons. Every person agent has a bucket list of attractions they want to enter. When persons are getting queued up, they will go to another attraction from their bucket list (not implemented yet). Persons staying for 3 timesteps and then leave the attraction, removing it from their bucket list.

## Parameters

In state_variables.py. Making use of an N x M grid, where attractions and persons are randomly plotted in. At the moment person agents will move to the nearest attraction of their bucket list. Each attraction agent has a MAX_ATTRACTION_CAPACITY set in state_variables.py. When full, person agents are queued in line.

## Performance

Run main.py or using the Jupyter notebook. Simulation results given in about 20 sec, but is visualization, takes about 15-20 min for 300 timesteps with ATTRACTION_COUNT = 5 and PERSON_COUNT = 200.

## TBD

* Stochastic movement of person agents via propbabilities
* Monte Carlo simulations and parameter sweeps
* Person class agents modeling different behaviours (family, youngsters, elderly etc. )
* Tokenization of incentives via Ocean Protocol-like attraction tokens, art NFTs or likewise