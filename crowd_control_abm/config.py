"""
Simulation configuration object.
"""


MONTE_CARLO_RUNS = 1 # N monte carlo runs

from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim
from .model.state_variables import genesis_states
from .model.partial_state_update_block import partial_state_update_block
from .model.sys_params import sys_params as sys_params
from .sim_params import SIMULATION_TIME_STEPS


sim_config = config_sim (
    {
        'N': MONTE_CARLO_RUNS,
        'T': range(SIMULATION_TIME_STEPS), # number of timesteps
        'M': sys_params,
    }
)

exp = Experiment()

exp.append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    partial_state_update_blocks=partial_state_update_block
)
