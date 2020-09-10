from ..location import get_free_location


def p_move_agents(params, substep, state_history, prev_state):
    """
    Move agents.
    """
    agents = prev_state['agents']
    sites = prev_state['sites']
    moving_persons = {k: v for k, v in agents.items() if v['type'] == 'person' and v['locked'] == False}
    attractions = {k: v for k, v in agents.items() if v['type'] == 'attraction'}
    busy_locations = [agent['location'] for agent in agents.values()]
    new_locations = {}
    for label, properties in moving_persons.items():
        new_location = get_next_location(properties['location'], sites, attractions)
        if new_location is not False:
            new_locations[label] = new_location
            busy_locations.append(new_location)
        else:
            continue
    return {'update_agent_location': new_locations}


def s_agent_location(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, location in policy_input['update_agent_location'].items():
        updated_agents[label]['location'] = location
    return ('agents', updated_agents)
