import random
from typing import *

def located_attraction(location: tuple, attractions: Dict[str, dict]) -> str:
    for k, v in attractions.items():
        if v['location'] == location:
            return k
        else:
            continue

def check_bucket_list(attraction_label: str, persons: Dict[str, dict]) -> Dict[str, dict]:
    people = {k: v for k, v in persons.items()
            if attraction_label in v['bucket_list'].keys()}
    return people

def select_persons(number: int, candidates: Dict[str, dict]) -> (Dict[str, dict], Dict[str, dict]):
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