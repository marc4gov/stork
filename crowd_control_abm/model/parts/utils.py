import random
from typing import *
from .location import get_nearest_attraction_location

def located_attraction(location: tuple, attractions: Dict[str, dict]):
    for k, v in attractions.items():
        attraction_location = v['location']
        if attraction_location[0] == location[0] and attraction_location[1] == location[1]:
            return k
        else:
            continue

def remove_from_bucket_list(label, attractions: Dict[str, dict]):
    attr = attractions.copy()
    for k, v in attractions.items():
        if label == k:
            # print(str(k) + " popped")
            attr.pop(k)
        else:
            continue
    return attr

def entertaining_attraction(position: tuple, attractions: Dict[str, dict]):
    for k, v in attractions.items():
        if position[0] == v['location'][0] and position[1] == v['location'][1]:
            return k
        else:
            continue
    return False


def check_bucket_list(attraction_label, persons: Dict[str, dict]) -> Dict[str, dict]:
    people = {k: v for k, v in persons.items()
            if attraction_label in v['bucket_list'].keys()}
    # print(attraction_label, people)
    return people

def select_persons(number: int, candidates: Dict[str, dict]) -> Dict[str, dict]:
    selected = {}
    times = number
    while times > 0:
        try:
            (k, v) = random.choice(list(candidates.items()))
            selected[k] = v
            candidates.pop(k)
            times -= 1
        except IndexError:
            print('selected is popped')
            break
    return selected

def handle_queue(attraction_label, location: tuple, persons: Dict[str, dict], delta_money: int = 1):
    agent_delta_money = {}
    agent_delta_locked = {}
    agent_delta_queue = {}
    agent_delta_bucket_list = {}
    nearest_attraction_locations = {}

    for person_label, person_properties in persons.items():
        agent_delta_money[attraction_label] = delta_money
        agent_delta_money[person_label] = -1 * delta_money
        agent_delta_locked[person_label] = True
        agent_delta_queue[person_label] = False
        new_bucket_list = remove_from_bucket_list(attraction_label, person_properties['bucket_list'])
        agent_delta_bucket_list[person_label] = new_bucket_list
        if len(new_bucket_list) > 0:
            nearest_attraction_location = get_nearest_attraction_location(location, new_bucket_list)
        else:
            nearest_attraction_location = (0, 0)
        nearest_attraction_locations[person_label] = nearest_attraction_location
    return (agent_delta_money, agent_delta_locked, agent_delta_queue, agent_delta_bucket_list, nearest_attraction_locations)
