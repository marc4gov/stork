import random
from typing import *

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

def check_bucket_list(attraction: Dict[str, dict], persons: Dict[str, dict]) -> Dict[str, dict]:
    attraction_label = list(attraction.keys())[0] 
    people = {k: v for k, v in persons.items()
            if attraction_label in v['bucket_list'].keys()}
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