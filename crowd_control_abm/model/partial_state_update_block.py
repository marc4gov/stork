"""
Model logic structure.
"""


# from .parts.environment.food_regeneration import *
from .parts.agents.entertaining import *
from .parts.agents.movement import *
from .parts.agents.natural_death import *


partial_state_update_block = [
    {
        'policies': {
            'move_agent': p_move_agents
        },
        'variables': {
            'agents': s_agent_location,
        }
    },
    {
        'policies': {
            'accomodate_persons': p_accomodate_persons
        },
        'variables': {
            'agents': s_accomodate_persons,
        }
    },
    {
        'policies': {
            'empty_queue': p_empty_queue
        },
        'variables': {
            'agents': s_empty_queue,
        }
    },
    {
        'policies': {
            'entertain_people': p_entertain_people
        },
        'variables': {
            'agents': s_agent_entertainment
        }
    },
    # {
    #     'policies': {
    #         'natural_death': p_natural_death
    #     },
    #     'variables': {
    #         'agents': s_agent_remove
    #     }
    # }
]
