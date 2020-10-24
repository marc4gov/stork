# Crowd Control demo

cadCAD crowd agent-based modelling approaches.

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

There are 2 types of agents: person and attraction. The goal is to balance the capacity of the attractions to the amount of visiting persons. Every person agent has a bucket list of attractions they want to enter. When persons are getting queued up, they will go to another attraction (not implemented yet)