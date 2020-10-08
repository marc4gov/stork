from ..location import nearby_agents, get_next_location, get_nearest_attraction_location
from ..utils import located_attraction, located_person, check_bucket_list, select_persons, rearrange_persons, remove_from_bucket_list
import random

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
        i = 0
        waiting_line = attraction_properties['waiting_line']
        candidates = persons.copy()
        location = attraction_properties['location']
        nearby_persons = nearby_agents(location, persons)
        nearby_persons2 = check_bucket_list(attraction_label, nearby_persons)
        removed_candidates = []
        # accomodate in queue (put them in line: first one 2 postions next to location and next one queueing up)
        for queued_person_label, queued_person_properties in nearby_persons2.items():
            agent_delta_queued[queued_person_label] = True
            print("Queued at " + str(attraction_label) + ": " + str(queued_person_label))
            queued_location = tuple(map(lambda x, y: x + y, location, (2 + i, 1)))
            agent_delta_location[queued_person_label] = queued_location
            if 'test' in waiting_line:
                waiting_line.pop('test')
            waiting_line[queued_person_label] = queued_location
            i += 1
            # remove person from candidates
            removed_candidates.append(queued_person_label)
        # remove accomodated persons from search
        for candidate in removed_candidates:
            persons.pop(candidate)
        agent_delta_waiting_line[attraction_label] = waiting_line
            
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


def p_empty_queue(params, substep, state_history, prev_state):
    """
    Empty the queue and get waiting persons into the attraction.
    """
    print('p_empty_queue')
    agents = prev_state['agents']
    # capacity_threshold = params['capacity_treshold']
    attractions = {k: v for k, v in agents.items()
                 if v['type'] == 'attraction' and v['capacity'] > 0 and 'test' not in v['waiting_line']}
    persons = {k: v for k, v in agents.items()
                 if v['type'] == 'person' and v['queued'] == True} 
    agent_delta_money = {}
    agent_delta_location = {}
    agent_delta_locked = {}
    agent_delta_queue = {}
    agent_delta_waiting_line = {}
    agent_delta_capacity = {}
    agent_delta_bucket_list = {}
    nearest_attraction_locations = {}

    print("Attractions: ", attractions)
    for attraction_label, attraction_properties in attractions.items():
        location = attraction_properties['location']
        waiting_line = attraction_properties['waiting_line']
        print("Waiting: ", waiting_line)
        delta_money = params['attraction_money']
        capacity = attraction_properties['capacity']
        selected_persons = {}

        if capacity < len(waiting_line):
            # select people until full
            (selected_persons, queued_persons) = select_persons(capacity, waiting_line)
            # print("Queued_persons: ", queued_persons)
            agent_delta_waiting_line[attraction_label] = rearrange_persons(location, queued_persons)
            agent_delta_capacity[attraction_label] = 0
        else:
            #accomodate everyone in queue
            agent_delta_waiting_line[attraction_label] = {'test': (0,0)}
            selected_persons = waiting_line
            agent_delta_capacity[attraction_label] = capacity - len(waiting_line)
        print("Selected: ", selected_persons)
        for person_label in selected_persons:
            agent_delta_money[attraction_label] = delta_money
            agent_delta_money[person_label] = -1 * delta_money
            agent_delta_location[person_label] = location
            agent_delta_locked[person_label] = True
            agent_delta_queue[person_label] = False
            print("Locked at " + str(attraction_label) + ": " + str(person_label))
            person = located_person(person_label, persons)
            # print(person)
            new_bucket_list = remove_from_bucket_list(attraction_label, person['bucket_list'])
            agent_delta_bucket_list[person_label] = new_bucket_list
            if len(new_bucket_list) > 0:
                nearest_attraction_location = get_nearest_attraction_location(location, new_bucket_list)
            else:
                nearest_attraction_location = (0, 0)
            nearest_attraction_locations[person_label] = nearest_attraction_location
    

    return {
            'agent_delta_money': agent_delta_money,
            'agent_delta_location': agent_delta_location,
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
    for label, delta_location in policy_input['agent_delta_location'].items():
        updated_agents[label]['location'] = delta_location
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
