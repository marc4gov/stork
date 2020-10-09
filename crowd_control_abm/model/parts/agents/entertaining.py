from ..location import nearby_agents, get_next_location, get_nearest_attraction_location
from ..utils import located_attraction, persons_in_attraction, select_persons, remove_from_bucket_list
import random

def p_entertain_people(params, substep, state_history, prev_state):
    """
    Entertains the person in the attraction.
    """
    print('p_entertain_people')
    agents = prev_state['agents']
    entertained_persons = {k: v for k, v in agents.items() if v['type'] == 'person' and v['locked'] == True }
    attractions = {k: v for k, v in agents.items() if v['type'] == 'attraction'}
 
    agent_delta_stay = {}
    agent_delta_locked = {}
    # agent_delta_bucket_list = {}
    agent_delta_capacity = {}
    

    for attraction_label, attraction_properties in attractions.items():
        location = attraction_properties['location']
        capacity = attractions[attraction_label]['capacity']
        persons = persons_in_attraction(location, entertained_persons)
        for person_label, person_properties in persons.items():
            print("Capacity at: ", attraction_label, " is: ", capacity)
            stay = person_properties['stay']
            stay += 1
            if stay >= params['attraction_max_stay']:
                agent_delta_stay[person_label] = 0
                agent_delta_locked[person_label] = False
                capacity += 1
                print("Capacity free: ", attraction_label, " now: ", capacity)
            else:
                agent_delta_stay[person_label] = stay
        agent_delta_capacity[attraction_label] = capacity

    return {'agent_delta_stay': agent_delta_stay,
            'agent_delta_locked': agent_delta_locked,
            'agent_delta_capacity': agent_delta_capacity
            }

def s_agent_entertainment(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta_stay in policy_input['agent_delta_stay'].items():
        updated_agents[label]['stay'] = delta_stay
    for label, delta_locked in policy_input['agent_delta_locked'].items():
        updated_agents[label]['locked'] = delta_locked
    for label, delta_capacity in policy_input['agent_delta_capacity'].items():
        updated_agents[label]['capacity'] = delta_capacity
    return ('agents', updated_agents)


