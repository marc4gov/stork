from ..location import nearby_agents
from ..utils import located_attraction, check_bucket_list, select_persons, remove_from_bucket_list
import random

def p_entertain_people(params, substep, state_history, prev_state):
    """
    Entertains the person in the attraction.
    """
    agents = prev_state['agents']
    entertained_persons = {k: v for k, v in agents.items() if v['type'] == 'person' and v['locked'] == True }

    agent_delta_stay = {}
    agent_delta_locked = {}
    # agent_delta_bucket_list = {}
    agent_delta_capacity = {}
    
    for label, properties in entertained_persons.items():
        stay = properties['stay']
        location = properties['location']
        entertaining_attractions = {k: v for k, v in agents.items() 
                if v['type'] == 'attraction' and v['location'][0] == location[0] and v['location'][1] == location[1] }
        attraction_label = list(entertaining_attractions.keys())[0]
        # bucket_list = properties['bucket_list']
        # print('p_entertain_people', bucket_list)
        agent_delta_stay[label] = stay + 1
        if agent_delta_stay[label] >= params['attraction_max_stay']:
            agent_delta_stay[label] = 0
            agent_delta_locked[label] = False
            # agent_delta_bucket_list[label] = remove_from_bucket_list(attraction_label, bucket_list)
            agent_delta_capacity[attraction_label] = 1

    return {'agent_delta_stay': agent_delta_stay,
            'agent_delta_locked': agent_delta_locked,
            # 'agent_delta_bucket_list': agent_delta_bucket_list,
            'agent_delta_capacity': agent_delta_capacity
            }

def s_agent_entertainment(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta_stay in policy_input['agent_delta_stay'].items():
        updated_agents[label]['stay'] = delta_stay
    for label, delta_locked in policy_input['agent_delta_locked'].items():
        updated_agents[label]['locked'] = delta_locked
    # for label, delta_bucket_list in policy_input['agent_delta_bucket_list'].items():
    #     updated_agents[label]['bucket_list'] = delta_bucket_list
    for label, delta_capacity in policy_input['agent_delta_capacity'].items():
        updated_agents[label]['capacity'] += delta_capacity
    return ('agents', updated_agents)


def p_empty_queue(params, substep, state_history, prev_state):
    """
    Empty the queue and get waiting persons into the attraction.
    """
    agents = prev_state['agents']
    # capacity_threshold = params['capacity_treshold']
    persons = {k: v for k, v in agents.items()
             if v['type'] == 'person' and v['queued'] == True}
    attractions = {k: v for k, v in agents.items()
                 if v['type'] == 'attraction'}
    luring_attractions = {k: v for k, v in attractions.items()
                        if v['capacity'] > 0 and v['waiting_line'] > 0}
    agent_delta_money = {}
    agent_delta_locked = {}
    agent_delta_queue = {}
    agent_delta_waiting_line = {}
    agent_delta_capacity = {}
    agent_delta_bucket_list = {}
    nearest_attraction_locations = {}

    for attraction_label, attraction_properties in luring_attractions.items():
        location = attraction_properties['location']
        waiting_line = attraction_properties['waiting_line']
        delta_money = attraction_properties['money']
        capacity = attraction_properties['capacity']
        waiting_persons = {k: v for k, v in persons.items()
                if v['location'] == location}
        if capacity < waiting_line:
            # select people until full
            selected_persons = select_persons(capacity, waiting_persons)
            agent_delta_waiting_line[attraction_label] = waiting_line - capacity
            agent_delta_capacity[attraction_label] = 0
            # selected persons get entrance
            for person_label, person_properties in selected_persons.items():
                agent_delta_money[attraction_label] = delta_money
                agent_delta_money[person_label] = -1 * delta_money
                agent_delta_locked[person_label] = True
                agent_delta_queue[person_label] = False
                new_bucket_list = remove_from_bucket_list(attraction_label, person_properties['bucket_list'])
                agent_delta_bucket_list[person_label] = new_bucket_list
                nearest_attraction_location = get_nearest_attraction_location(location, new_bucket_list)
                nearest_attraction_locations[person_label] = nearest_attraction_location
            # not selected still wait in line
        else:
            #accomodate everyone in queue
            agent_delta_waiting_line[attraction_label] = 0
            agent_delta_capacity[attraction_label] = capacity - waiting_line
            for person_label, person_properties in waiting_persons.items():
                agent_delta_money[attraction_label] = delta_money
                agent_delta_money[person_label] = -1 * delta_money
                agent_delta_locked[person_label] = True
                agent_delta_queue[person_label] = False
                agent_delta_bucket_list[person_label] = new_bucket_list
                nearest_attraction_location = get_nearest_attraction_location(location, new_bucket_list)
                nearest_attraction_locations[person_label] = nearest_attraction_location
    return {
            'agent_delta_money': agent_delta_money,
            'agent_delta_locked': agent_delta_locked,
            'agent_delta_queue': agent_delta_queue,
            'agent_delta_capacity': agent_delta_capacity,
            'agent_delta_waiting_line': agent_delta_waiting_line, 
            'agent_delta_bucket_list': agent_delta_bucket_list,
            'update_attraction_location': nearest_attraction_locations        
    }

def s_empty_queue(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta_queue in policy_input['agent_delta_queue'].items():
        updated_agents[label]['queued'] = delta_queue
    for label, delta_money in policy_input['agent_delta_money'].items():
        updated_agents[label]['money'] += delta_money
    for label, delta_locked in policy_input['agent_delta_locked'].items():
        updated_agents[label]['locked'] = delta_locked
    for label, delta_capacity in policy_input['agent_delta_capacity'].items():
        updated_agents[label]['capacity'] = delta_capacity
    for label, delta_waiting_line in policy_input['agent_delta_waiting_line'].items():
        updated_agents[label]['waiting_line'] = delta_waiting_line
    for label, delta_bucket_list in policy_input['agent_delta_bucket_list'].items():
        updated_agents[label]['bucket_list'] = delta_bucket_list
    for label, location2 in policy_input['update_attraction_location'].items():
        updated_agents[label]['nearest_attraction_location'] = location2
    return ('agents', updated_agents)

def p_accomodate_persons(params, substep, state_history, prev_state):
    """
    Accomodate the nearby and willing persons into the attraction.
    """
    agents = prev_state['agents']
    persons = {k: v for k, v in agents.items()
             if v['type'] == 'person' and v['queued'] == False and v['locked'] == False}
    attractions = {k: v for k, v in agents.items()
                 if v['type'] == 'attraction'}
    luring_attractions = {k: v for k, v in attractions.items()
                        if v['capacity'] > 0}
    agent_delta_location = {}
    agent_delta_waiting_line = {}
    agent_delta_queued = {}
    attraction = {}
    for attraction_label, attraction_properties in luring_attractions.items():
        attraction[attraction_label] = attraction_properties
        location = attraction_properties['location']
        waiting_line = attraction_properties['waiting_line']
        nearby_persons = nearby_agents(location, persons)
        nearby_persons2 = check_bucket_list(attraction, nearby_persons)
        # accomodate in queue
        agent_delta_waiting_line[attraction_label] = waiting_line + len(nearby_persons2)
        for queued_person_label, queued_person_properties in nearby_persons2.items():
            bucket_list = queued_person_properties['bucket_list']
            agent_delta_queued[queued_person_label] = True
            agent_delta_location[queued_person_label] = location
            
    return {
            'agent_delta_location': agent_delta_location,
            'agent_delta_queued': agent_delta_queued,
            'agent_delta_waiting_line': agent_delta_waiting_line,
    }

def s_accomodate_persons(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta_location in policy_input['agent_delta_location'].items():
        updated_agents[label]['location'] = delta_location
    for label, delta_queue in policy_input['agent_delta_queued'].items():
        updated_agents[label]['queued'] = delta_queue
    for label, delta_waiting_line in policy_input['agent_delta_waiting_line'].items():
        updated_agents[label]['waiting_line'] = delta_waiting_line
    return ('agents', updated_agents)

