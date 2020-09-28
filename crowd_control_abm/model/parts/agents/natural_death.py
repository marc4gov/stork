
def p_agent_remove(params, substep, state_history, prev_state):
    """
    Remove person agents which are done.
    """
    agents = prev_state['agents']
    leaving_persons = {k: v for k, v in agents.items() 
            if v['type'] == 'person' and len(v['bucket_list']) == 0 and v['location'][0] == 0 and v['location'][1] == 0}
    return {'remove_agents': leaving_persons}


def s_agent_remove(params, substep, state_history, prev_state, policy_input):
    agents_to_remove = policy_input['remove_agents']
    surviving_agents = {k: v for k, v in prev_state['agents'].items()
                        if k not in agents_to_remove}
    return ('agents', surviving_agents)
