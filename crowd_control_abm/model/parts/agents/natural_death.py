
def p_natural_death(params, substep, state_history, prev_state):
    """
    Remove person agents which are done.
    """
    agents = prev_state['agents']
    agents_to_remove = []
    for agent_label, agent_properties in agents.items():
        to_remove = len(agent_properties['bucket_list']) == 0 
        if to_remove:
          agents_to_remove.append(agent_label)
    return {'remove_agents': agents_to_remove}


def s_agent_remove(params, substep, state_history, prev_state, policy_input):
    agents_to_remove = policy_input['remove_agents']
    surviving_agents = {k: v for k, v in prev_state['agents'].items()
                        if k not in agents_to_remove}
    return ('agents', surviving_agents)
