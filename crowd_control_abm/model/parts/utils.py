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
    return ''

def persons_in_attraction(location: tuple, persons: Dict[str, dict]) -> Dict[str, dict]:
    persons_in_attraction = {}
    for k, v in persons.items():
        person_location = v['location']
        if person_location[0] == location[0] and person_location[1] == location[1]:
            persons_in_attraction[k] = v
        else:
            continue
    return persons_in_attraction

def located_person(label, persons: Dict[str, dict]):
    for k, v in persons.items():
        if k == label:
            return v
        else:
            continue
    return {}

def remove_from_bucket_list(label, attractions: dict):
    attr = attractions.copy()
    for k in attractions.keys():
        if label == k:
            # print(str(k) + " popped")
            attr.pop(k)
        else:
            continue
    return attr

def check_bucket_list(attraction_label, persons: Dict[str, dict]) -> Dict[str, dict]:
    people = {k: v for k, v in persons.items()
            if attraction_label in v['bucket_list'].keys()}
    # print(attraction_label, people)
    return people

def select_persons(number: int, candidates: dict) -> (dict, dict):
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
    return (selected, candidates)

def rearrange_persons(attraction_location: tuple, persons: dict) -> dict:
    rearranged = {}
    i = 0
    for person_label, person_properties in persons.items():
        position = tuple(map(lambda x, y: x + y, attraction_location, (2 + i, 1)))
        rearranged[person_label] = position
        i += 1
    return rearranged

def empty_queue(attraction_label, location: tuple, persons: Dict[str, dict], delta_money: int = 1):
    agent_money = {}
    agent_locked = {}
    agent_queue = {}
    agent_bucket_list = {}
    nearest_attraction_locations = {}

    for person_label, person_properties in persons.items():
        agent_money[attraction_label] = delta_money
        agent_money[person_label] = -1 * delta_money
        agent_locked[person_label] = True
        agent_queue[person_label] = False
        new_bucket_list = remove_from_bucket_list(attraction_label, person_properties['bucket_list'])
        agent_bucket_list[person_label] = new_bucket_list
        if len(new_bucket_list) > 0:
            nearest_attraction_location = get_nearest_attraction_location(location, new_bucket_list)
        else:
            nearest_attraction_location = (0, 0)
        nearest_attraction_locations[person_label] = nearest_attraction_location
    return (agent_money, agent_locked, agent_queue, agent_bucket_list, nearest_attraction_locations)
