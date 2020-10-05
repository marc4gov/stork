from ..location import nearby_agents, get_next_location, get_nearest_attraction_location
from ..utils import located_attraction, select_persons, remove_from_bucket_list
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
    
    for label, properties in entertained_persons.items():
        stay = properties['stay']
        location = properties['location']
        attraction_label = located_attraction(location, attractions)
        capacity = attractions[attraction_label]['capacity']
        agent_delta_stay[label] = stay + 1
        if agent_delta_stay[label] >= params['attraction_max_stay']:
            agent_delta_stay[label] = 0
            agent_delta_locked[label] = False
            if attraction_label:
                agent_delta_capacity[attraction_label] = capacity + 1

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


