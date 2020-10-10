
import uuid

def person_data(length, dims=2):
    persons = {}
    for k, agent in agent_ds[0].items():
        if agent['type'] == 'person':
            persons[k] = []
    
    for i in range(0,length*5,5):
        for k, agent in agent_ds[i].items():

            if agent['type'] == 'person':
                persons[k] = agent['location']
    return persons

def person(timestep, key):
    person = {}
    for k, agent in agent_ds[timestep*5].items():
        if agent['type'] == 'person' and k == key:
            return agent
    return person

def persons_queued(length):
    persons = {}
    for k, agent in agent_ds[0].items():
        if agent['type'] == 'person':
            persons[k] = ""
    
    for i in range(0,length*5,5):
        for k, agent in agent_ds[i].items():
            if agent['type'] == 'person' and agent['queued']:
                persons[k] = 'queued'
    return persons

def persons_locked(length):
    persons = {}
    for k, agent in agent_ds[0].items():
        if agent['type'] == 'person':
            persons[k] = ""
    
    for i in range(0,length*5,5):
        for k, agent in agent_ds[i].items():
            if agent['type'] == 'person' and agent['locked']:
                persons[k] = 'locked'
    return persons

def attraction_location(length, dims=2):
    attrs = {}
    for k, agent in agent_ds[0].items():
        if agent['type'] == 'attraction':
            attrs[k] = []
    
    for i in range(0,length*5,5):
        for k, agent in agent_ds[i].items():
            if agent['type'] == 'attraction':
                attrs[k] = agent['location']
    return attrs

def attraction_capacity(length, dims=2):
    attrs = {}
    for k, agent in agent_ds[0].items():
        if agent['type'] == 'attraction':
            attrs[k] = []
    
    for i in range(0,length*5,5):
        for k, agent in agent_ds[i].items():
            if agent['type'] == 'attraction':
                attrs[k] = agent['capacity']
    return attrs

def persons(timestep):
    persons = {}
    for k, agent in agent_ds[timestep*5].items():
        if agent['type'] == 'person':
            persons[k] = str(agent['location']) + ' To: ' + str(agent['nearest_attraction_location']) + ' queued: ' + str(agent['queued']) + ' locked: ' + str(agent['locked']) + ' stay: '+ str(agent['stay'])
    return persons

def attractions(timestep):
    persons = {}
    for k, agent in agent_ds[timestep*5].items():
        if agent['type'] == 'attraction':
            persons[k] = 'Location: ' + str(agent['location']) + ' Capacity: ' + str(agent['capacity']) + ' waiting: ' + str(agent['waiting_line'])
    return persons

def get_attraction_locations(timestep):
    locations = []
    for key, value in attractions(timestep).items():
        locations.append(value)
    return locations

def get_locations(timestep):
    locations = []
    for key, value in person_data(timestep).items():
        locations.append(value)
    return locations