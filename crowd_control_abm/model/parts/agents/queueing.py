from ..location import nearby_agents, get_next_location, get_nearest_attraction_location
from ..utils import located_attraction, check_bucket_list, select_persons, remove_from_bucket_list, handle_queue, entertaining_attraction
import random

def p_empty_queue(params, substep, state_history, prev_state):
    """
    Empty the queue and get waiting persons into the attraction.
    """
    print('p_empty_queue')
    agents = prev_state['agents']
    # capacity_threshold = params['capacity_treshold']
    persons = {k: v for k, v in agents.items()
             if v['type'] == 'person' and v['queued'] == True}
    attractions = {k: v for k, v in agents.items()
                 if v['type'] == 'attraction' and if v['capacity'] > 0 and len(v['waiting_line']) > 0}
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
        delta_money = params['attraction_money']
        capacity = attraction_properties['capacity']
        if capacity < len(waiting_line):
            # select people until full
            selected_persons = waiting_line[:capacity]
            print("Selected persons: " + str(selected_persons)
            agent_delta_waiting_line[attraction_label] = waiting_line[capacity:]
            agent_delta_capacity[attraction_label] = 0
            # selected persons get entrance
            agent_delta_money, agent_delta_locked, agent_delta_queue, agent_delta_bucket_list, nearest_attraction_locations = handle_queue(attraction_label, location, selected_persons, delta_money)
            # not selected still wait in line
        else:
            #accomodate everyone in queue
            agent_delta_waiting_line[attraction_label] = 0
            agent_delta_capacity[attraction_label] = capacity - waiting_line
            agent_delta_money, agent_delta_locked, agent_delta_queue, agent_delta_bucket_list, nearest_attraction_locations = handle_queue(attraction_label, location, waiting_persons, delta_money)

    print("Queued persons: " + str(agent_delta_queue.items()))
    

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
    print('p_accomodate_persons')
    agents = prev_state['agents']
    persons = {k: v for k, v in agents.items()
             if v['type'] == 'person' and v['queued'] == False and v['locked'] == False}
    luring_attractions = {k: v for k, v in agents.items()
                        if v['type'] == 'attraction' and v['capacity'] > 0}
    # print(luring_attractions.items())
    agent_delta_location = {}
    agent_delta_waiting_line = {}
    agent_delta_queued = {}
    attraction = {}
    for attraction_label, attraction_properties in luring_attractions.items():

        attraction[attraction_label] = attraction_properties
        location = attraction_properties['location']
        waiting_line = attraction_properties['waiting_line']
        nearby_persons = nearby_agents(location, persons)
        nearby_persons2 = check_bucket_list(attraction_label, nearby_persons)
        # accomodate in queue
        # agent_delta_waiting_line[attraction_label] = waiting_line + len(nearby_persons2)
        for queued_person_label, queued_person_properties in nearby_persons2.items():
            bucket_list = queued_person_properties['bucket_list']
            agent_delta_queued[queued_person_label] = True
            agent_delta_location[queued_person_label] = location
            agent_delta_waiting_line[attraction_label] = waiting_line.append(queued_person_label)
        print("Attraction Waiting line: " + str(agent_delta_waiting_line), " Capacity: " + str(attraction_properties['capacity']))
            
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

