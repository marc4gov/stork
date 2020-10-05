"""
Helper functions associated with location
"""

import numpy as np
import random
from typing import *

def busy_locations(agents: Dict[str, dict]) -> List[tuple]:
    return [properties['location'] for properties in agents.values()]

# def check_location(position: tuple,
#                    max_distance: int,
#                    all_sites: np.matrix,
#                    busy_locations: List[tuple]) -> List[tuple]:
#     """
#     Returns an list of available location tuples neighboring an given
#     position location.
#     """
#     N, M = all_sites.shape
#     potential_sites = [(position[0], position[1] + max_distance),
#                        (position[0], position[1] - max_distance),
#                        (position[0] + max_distance, position[1]),
#                        (position[0] - max_distance, position[1])]
#     potential_sites = [(site[0] % N, site[1] % M) for site in potential_sites]
#     valid_sites = [site for site in potential_sites if site not in busy_locations]
#     return valid_sites

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
                        (position[0] + 1, position[1] + 1),
                       (position[0] - 1, position[1] - 1),                   
                        (position[0] + 1, position[1] - 1),
                       (position[0] - 1, position[1] + 1), 
                       ]
    potential_sites = [(site[0] % N, site[1] % M) for site in potential_sites]
    
    valid_sites = [site for site in potential_sites if site not in busy_locations]
    return valid_sites


# def get_free_location(position: tuple,
#                       all_sites: np.matrix,
#                       used_sites: List[tuple]) -> tuple:
#     """
#     Gets an random free location neighboring an position. Returns False if
#     there aren't any location available.
#     """
#     available_locations = check_location(position, all_sites, used_sites)
#     if len(available_locations) > 0:
#         return random.choice(available_locations)
#     else:
#         return False

def get_next_location(position: tuple, attraction_location: tuple,
                      all_sites: np.matrix,
                      busy_locations: List[tuple],
                     ):
    """
    Gets a free location neighboring an position. Returns False if
    there aren't any location available.
    """
    available_locations = check_next_location(position, all_sites, busy_locations)
    if len(available_locations) > 0:
        max_distance = 1000
        best_location = (0,0)
        for location in available_locations:
            distance = np.abs(attraction_location[0] - location[0]) + np.abs(attraction_location[1] - location[1])
            if distance < max_distance:
                max_distance = distance
                best_location = location
        return best_location
    else:
        return False


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

def nearby_agents(location: tuple, agents: Dict[str, dict]) -> Dict[str, dict]:
    """
    Filter the non-nearby agents.
    """
    neighbors = {label: agent for label, agent in agents.items()
                 if is_neighbor(agent['location'], location, 2)}
    return neighbors

def is_neighbor(location_1: tuple, location_2: tuple, max_distance: int) -> bool:
    dx = np.abs(location_1[0] - location_2[0])
    dy = np.abs(location_1[1] - location_2[1])
    distance = dx + dy
    if distance <= max_distance:
        return True
    else:
        return False
