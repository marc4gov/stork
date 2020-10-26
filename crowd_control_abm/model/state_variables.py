"""
Model initial state.
"""

# Dependences

import random
import uuid
import numpy as np
from typing import Tuple, List, Dict
from itertools import cycle
from enum import Enum

import matplotlib.pyplot as plt
import matplotlib.animation as animation

### World size
N = 200
M = 20
INITIAL_CROWD = 1

### Initial agent count
PERSON_COUNT = 200
ATTRACTION_COUNT = 5
MAX_ATTRACTION_CAPACITY = 3

## yet to be implemented
agent_probabilities = [0.5,1/3,0.25,1/5,3/4,0.8]

class Person(Enum):
    parent = 1
    child = 2
    youngster = 3
    aged = 4
    single = 5
    groupie = 6

class Behaviour(Enum):
    clumper = 1
    conformist = 2
    bowler = 3
    maverick = 4
    wallhugger = 5

## Helper functions

def select_agent_behaviour(person_id, behaviour_id) -> tuple:
    return (Person(person_id), Behaviour(behaviour_id))


def get_nearest_attraction_location(position: tuple, bucket_list: dict) -> tuple:
    distance_to_attraction = 1000
    nearest_location = (0,0)
    for label in bucket_list.keys():
        attraction_location = bucket_list[label]
        x = attraction_location[0]
        y = attraction_location[1]
        distance = np.abs(x - position[0]) + np.abs(y - position[1])
        if distance < distance_to_attraction:
            distance_to_attraction = distance
            nearest_location = attraction_location
        else:
            continue
    return nearest_location

def new_person_agent(agent_type: str, location: Tuple[int, int], person_type: Tuple[int, int], attractions: [str] = [''],
              nearest_attraction_location: Tuple[int, int] = (0,0), money: int=100, queued: bool=False, locked: bool=False, stay: int=0) -> dict:
    agent = {'type': agent_type,
             'location': location,
             'person_type': person_type,
             'money': money,
             'bucket_list' : attractions,
             'nearest_attraction_location': nearest_attraction_location,
             'queued': queued,
             'locked': locked,
             'stay': stay,
             'probability': random.choice(agent_probabilities)}
    return agent

def new_attraction_agent(agent_type: str, location: Tuple[int, int],
               waiting_line: [str] = [''], money: int=0, capacity: int=MAX_ATTRACTION_CAPACITY) -> dict:
    agent = {'type': agent_type,
             'location': location,
             'money': money,
             'waiting_line': waiting_line,
             'capacity': capacity}
    return agent

def select_attractions(attrs: dict, number: int) -> dict:
    selected = {}
    times = number
    while times > 0:
        try:
            k, v = random.choice(list(attrs.items()))
            selected[k] = v
            attrs.pop(k)
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
    i = 0
#   attractions
    for agent_type in attraction_queue:
        i = i + 1
        location = (20 + 30 * i, 3 + 3 * i)
        available_locations.remove(location)
        created_agent = new_attraction_agent(agent_type, location, {'test': (0,0)})
        initial_agents[uuid.uuid4()] = created_agent
#   people
    attraction_agents = initial_agents.copy()
    attractions = {k: v['location'] for k, v in attraction_agents.items()}
    for agent_type in person_queue:
        person_type = select_agent_behaviour(random.choice([e.value for e in Person]), random.choice([e.value for e in Behaviour]) )
        location = random.choice(available_locations)
        available_locations.remove(location)
#       select attractions (3 in total)

        selected_attractions = select_attractions(attractions.copy(), 3)
        nearest_attraction_location = get_nearest_attraction_location(location, selected_attractions)
        created_agent = new_person_agent(agent_type, location, person_type, selected_attractions, nearest_attraction_location)
        # print(created_agent)
        # print("\n")
        initial_agents[uuid.uuid4()] = created_agent
    return initial_agents


## Generate initial state

sites = np.zeros((N, M)) * INITIAL_CROWD
locations = [(n, m) for n in range(N) for m in range(M)]
initial_agents = generate_agents(locations, ATTRACTION_COUNT, PERSON_COUNT)

persons = {k: v for k, v in initial_agents.items() if v['type'] == 'person' }
attrs = {k: v for k, v in initial_agents.items() if v['type'] == 'attraction' }
attr = list(attrs.values())[0]
person = list(persons.values())[23]
print(person)

# label = list(person['bucket_list'].keys())[0]
# person['bucket_list'].pop(label)
# print(list(person['bucket_list'].keys()))

genesis_states = {
    'agents': initial_agents,
    'sites': sites
}
