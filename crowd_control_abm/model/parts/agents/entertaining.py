from ..location import nearby_agents
from ..utils import located_attraction, check_bucket_list, select_persons
import random

def p_entertain_people(params, substep, state_history, prev_state):
    """
    Entertains the person in the attraction.
    """
    agents = prev_state['agents']
    persons = {k: v for k, v in agents.items() if v['type'] == 'person'}
    entertained_persons = {label: properties for label, properties in persons.items()
                    if properties['locked'] == True}
    agent_delta_stay = {}
    for label, properties in entertained_persons.items():
        stay = properties['stay']
        agent_delta_stay[label] = stay + 1

    return {'agent_delta_stay': agent_delta_stay}

def s_agent_entertainment(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta_stay in policy_input['agent_delta_stay'].items():
        updated_agents[label]['stay'] = delta_stay
        if updated_agents[label]['stay'] > params['attraction_max_stay']:
            updated_agents[label]['stay'] = 0
            updated_agents[label]['locked'] = False
            attraction_label = located_attraction(updated_agents[label]['location'], updated_agents[label]['bucket_list'])
            updated_agents[label]['bucket_list'].pop(attraction_label)
    return ('agents', updated_agents)


def p_empty_queue(params, substep, state_history, prev_state):
    """
    Empty the queue and get waiting persons into the attraction.
    """
    agents = prev_state['agents']
    # capacity_threshold = params['capacity_treshold']
    persons = {k: v for k, v in agents.items()
             if v['type'] == 'person'}
    attractions = {k: v for k, v in agents.items()
                 if v['type'] == 'attraction'}
    luring_attractions = {k: v for k, v in attractions.items()
                        if v['capacity'] > 0 and v['queued'] > 0}
    agent_delta_money = {}
    agent_delta_locked = {}
    agent_delta_queue = {}
    agent_delta_capacity = {}

    for attraction_label, attraction_properties in luring_attractions.items():
        location = attraction_properties['location']
        queued = attraction_properties['queued']
        delta_money = attraction_properties['money']
        capacity = attraction_properties['capacity']
        waiting_persons = {k: v for k, v in persons.items()
                if v['queued'] == True and v['location'] == location}
        if capacity < queued:
            # select people until full
            (selected_persons, queued_persons) = select_persons(capacity, waiting_persons)
            agent_delta_queue[attraction_label] = queued - capacity
            agent_delta_capacity[attraction_label] = 0
            # selected persons get entrance
            for person_label, person_properties in selected_persons.items():
                agent_delta_money[attraction_label] = delta_money
                agent_delta_money[person_label] = -1 * delta_money
                agent_delta_locked[person_label] = True
                agent_delta_queue[person_label] = False
            # not selected still wait in line
            for queued_person_label, queued_person_properties in queued_persons.items():
                agent_delta_queue[queued_person_label] = True
        else:
            #accomodate everyone in queue
            agent_delta_queue[attraction_label] = 0
            agent_delta_capacity[attraction_label] = capacity - queued
            for person_label, person_properties in waiting_persons.items():
                agent_delta_money[attraction_label] = delta_money
                agent_delta_money[person_label] = -1 * delta_money
                agent_delta_locked[person_label] = True
                agent_delta_queue[person_label] = False

    return {
            'agent_delta_money': agent_delta_money,
            'agent_delta_locked': agent_delta_locked,
            'agent_delta_queue': agent_delta_queue,
            'agent_delta_capacity': agent_delta_capacity,
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
    return ('agents', updated_agents)

def p_accomodate_persons(params, substep, state_history, prev_state):
    """
    Accomodate the nearby and willing persons into the attraction.
    """
    agents = prev_state['agents']
    persons = {k: v for k, v in agents.items()
             if v['type'] == 'person'}
    attractions = {k: v for k, v in agents.items()
                 if v['type'] == 'attraction'}
    luring_attractions = {k: v for k, v in attractions.items()
                        if v['capacity'] > 0}
    agent_delta_location = {}
    agent_delta_queue = {}

    for attraction_label, attraction_properties in luring_attractions.items():
        location = attraction_properties['location']
        queued = attraction_properties['queued']
        nearby_persons = nearby_agents(location, persons)
        nearby_persons = check_bucket_list(attraction_label, nearby_persons)
        # wait in line
        agent_delta_queue[attraction_label] = queued + len(nearby_persons)
        for queued_person_label, queued_person_properties in nearby_persons.items():
            agent_delta_queue[queued_person_label] = True
            agent_delta_location[queued_person_label] = location
            
    return {
            'agent_delta_location': agent_delta_location,
            'agent_delta_queue': agent_delta_queue
    }

def s_accomodate_persons(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta_location in policy_input['agent_delta_location'].items():
        updated_agents[label]['location'] = delta_location
    for label, delta_queue in policy_input['agent_delta_queue'].items():
        updated_agents[label]['queued'] = delta_queue
    return ('agents', updated_agents)

