"""
Helper functions associated with location
"""


import numpy as np
import random
from typing import *

def busy_locations(agents: Dict[str, dict]) -> List[tuple]:
    return [properties['location'] for properties in agents.values()]

def check_location(position: tuple,
                   max_distance: int,
                   all_sites: np.matrix,
                   busy_locations: List[tuple]) -> List[tuple]:
    """
    Returns an list of available location tuples neighboring an given
    position location.
    """
    N, M = all_sites.shape
    potential_sites = [(position[0], position[1] + max_distance),
                       (position[0], position[1] - max_distance),
                       (position[0] + max_distance, position[1]),
                       (position[0] - max_distance, position[1])]
    potential_sites = [(site[0] % N, site[1] % M) for site in potential_sites]
    valid_sites = [site for site in potential_sites if site not in busy_locations]
    return valid_sites

def check_next_location(position: tuple,
                   all_sites: np.matrix,
                   busy_locations: List[tuple]) -> tuple:
    """
    Returns an list of available location tuples neighboring an given
    position location.
    """
    N, M = all_sites.shape
    potential_sites = [(position[0], position[1] + 1),
                       (position[0], position[1] - 1),
                       (position[0] + 1, position[1]),
                       (position[0] - 1, position[1]),
                        (position[0] - 1, position[1] + 1),
                       (position[0] - 1, position[1] - 1),
                       (position[0] + 1, position[1] + 1),
                       (position[0] + 1, position[1] - 1)]
    potential_sites = [(site[0] % N, site[1] % M) for site in potential_sites]
    valid_sites = [site for site in potential_sites if site not in busy_locations]
    return valid_sites


def get_free_location(position: tuple,
                      all_sites: np.matrix,
                      used_sites: List[tuple]) -> tuple:
    """
    Gets an random free location neighboring an position. Returns False if
    there aren't any location available.
    """
    available_locations = check_location(position, all_sites, used_sites)
    if len(available_locations) > 0:
        return random.choice(available_locations)
    else:
        return False

def get_next_location(position: tuple,
                      all_sites: np.matrix,
                      busy_locations: List[tuple],
                      attractions: Dict[str, dict]) -> tuple:
    """
    Gets an random free location neighboring an position. Returns False if
    there aren't any location available.
    """
    available_locations = check_next_location(position, all_sites, busy_locations)
    if len(available_locations) > 0:
        max_distance = 1000
        best_location = (0,0)
        label, d_vector = get_nearest_attraction(position, attractions)
        for location in available_locations:
            distance = np.abs(d_vector[0] - location[0]) + np.abs(d_vector[1] - location[1])
            if distance < max_distance:
                max_distance = distance
                best_location = location
        return best_location
    else:
        return False


def distance_vector(location_1: tuple, location_2: tuple) -> tuple:
    dx = location_1[0] - location_2[0]
    dy = location_1[1] - location_2[1]
    return (dx, dy)

def get_nearest_attraction(location: tuple, attractions: Dict[str, dict]) -> (str, tuple):
    distance_to_attraction = 1000
    nearest_d_vector = (0,0)
    nearest_label = ''
    for label, properties in attractions.items():
        d_vector = distance_vector(location, properties['location'])
        distance = np.abs(d_vector[0]) + np.abs(d_vector[1])
        if distance < distance_to_attraction:
            distance_to_attraction = distance
            nearest_d_vector = d_vector
            nearest_label = label
        else:
            continue
    return (nearest_label, nearest_d_vector)

def nearby_agents(location: tuple, agents: Dict[str, dict]) -> Dict[str, dict]:
    """
    Filter the non-nearby agents.
    """
    neighbors = {label: agent for label, agent in agents.items()
                 if is_neighbor(agent['location'], location, 2)}
    return neighbors

def is_neighbor(location_1: tuple, location_2: tuple, max_distance: int) -> bool:
    dx = np.abs(location_1[0] - location_2[0])
    dy = (location_1[1] - location_2[1])
    distance = dx + dy
    if distance <= max_distance:
        return True
    else:
        return False
