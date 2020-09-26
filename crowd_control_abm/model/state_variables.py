"""
Model initial state.
"""

# Dependences

import random
import uuid
import numpy as np
from typing import Tuple, List, Dict
from itertools import cycle

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# fig, ax = plt.subplots()
# line, = ax.plot(np.random.rand(10))
# ax.set_ylim(0, 1)
## Input parameters

### World size & initial food
N = 200
M = 20
INITIAL_CROWD = 1

### Initial agent count
PERSON_COUNT = 10
ATTRACTION_COUNT = 5
MAX_ATTRACTION_CAPACITY = 10

## Helper functions

def new_person_agent(agent_type: str, location: Tuple[int, int], attractions: Dict[str, dict],
              nearest_attraction_location: Tuple[int, int] = (0,0), money: int=100, queued: bool=False, locked: bool=False, stay: int=0) -> dict:
    agent = {'type': agent_type,
             'location': location,
             'money': money,
             'bucket_list' : attractions,
             'nearest_attraction_location': nearest_attraction_location,
             'queued': queued,
             'locked': locked,
             'stay': stay}
    return agent

def new_attraction_agent(agent_type: str, location: Tuple[int, int],
              money: int=0, waiting_line: int=0, capacity: int=MAX_ATTRACTION_CAPACITY) -> dict:
    agent = {'type': agent_type,
             'location': location,
             'money': money,
             'waiting_line': waiting_line,
             'capacity': capacity}
    return agent

def select_attractions(attractions: Dict[str, dict]) -> Dict[str, dict]:
    selected = {}
    times = 3
    while times > 0:
        try:
            (k, v) = random.choice(list(attractions.items()))
            selected[k] = v
            attractions.pop(k)
            times -= 1
        except IndexError:
            print('item is popped')
            break
    return selected


def generate_agents(available_locations: List[Tuple[int, int]],
                    n_attractions: int,
                    n_person: int) -> Dict[str, dict]:
    initial_agents = {}
    person_queue = ['person'] * n_person
    attraction_queue = ['attraction'] * n_attractions
#   attractions
    for agent_type in attraction_queue:
        location = random.choice(available_locations)
        available_locations.remove(location)
        created_agent = new_attraction_agent(agent_type, location)
        initial_agents[uuid.uuid4()] = created_agent
#   people
    attraction_agents = initial_agents.copy()
    for agent_type in person_queue:
        location = random.choice(available_locations)
        available_locations.remove(location)
#       select attractions (7 in total)
        selected_attractions = select_attractions(attraction_agents.copy())
        created_agent = new_person_agent(agent_type, location, selected_attractions)
        # print(created_agent)
        # print("\n")
        initial_agents[uuid.uuid4()] = created_agent
    return initial_agents


## Generate initial state

sites = np.zeros((N, M)) * INITIAL_CROWD
locations = [(n, m) for n in range(N) for m in range(M)]
initial_agents = generate_agents(locations, ATTRACTION_COUNT, PERSON_COUNT)

persons = {k: v for k, v in initial_agents.items() if v['type'] == 'person' }
person = list(persons.values())[0]
print(person)
# label = list(person['bucket_list'].keys())[0]
# person['bucket_list'].pop(label)
# print(list(person['bucket_list'].keys()))

genesis_states = {
    'agents': initial_agents,
    'sites': sites
}
