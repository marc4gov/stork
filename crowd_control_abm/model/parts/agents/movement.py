from ..location import get_next_location, get_nearest_attraction_location

def p_move_agents(params, substep, state_history, prev_state):
    """
    Move agents.
    """
    print('p_move_agents')
    agents = prev_state['agents']
    sites = prev_state['sites']
    moving_persons = {k: v for k, v in agents.items() 
            if v['type'] == 'person' and v['locked'] == False and v['queued'] == False}
    busy_locations = [agent['location'] for agent in agents.values()]
    new_locations = {}
    nearest_attraction_locations = {}
    for label, properties in moving_persons.items():
        probability = properties['probability']
        bucket_list = properties['bucket_list']
        location = properties['location']
        if len(bucket_list) > 0:
            nearest_attraction_location = get_nearest_attraction_location(location, bucket_list)
        else:
            nearest_attraction_location = (0,0)
        nearest_attraction_locations[label] = nearest_attraction_location
        new_location = get_next_location(location, nearest_attraction_location, sites, busy_locations, probability)
        if new_location is not False:
            new_locations[label] = new_location
            busy_locations.append(new_location)
        else:
            continue

    return {'update_agent_location': new_locations, 
            'update_attraction_location': nearest_attraction_locations}

def s_agent_location(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, location in policy_input['update_agent_location'].items():
        updated_agents[label]['location'] = location
    for label, location2 in policy_input['update_attraction_location'].items():
        updated_agents[label]['nearest_attraction_location'] = location2
    return ('agents', updated_agents)
