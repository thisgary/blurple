import json

def data(pl, attr): # get from payload data
    d = json.loads(pl)['d']
    if attr in d: return d[attr]

def create(op, **d):
    pl = {'op': op, 'd': d}
    return json.dumps(pl)

def heartbeat():
    return create(1)

def identify(token):
    prop = {
            '$os': 'linux', 
            '$browser': 'IE', 
            '$device': 'Nokia-3310'}
    return create(2, token=token, intents=32509, properties=prop)

def resume(token, session_id, seq):
    return create(6, token=token, session_id=session_id, seq=seq)


