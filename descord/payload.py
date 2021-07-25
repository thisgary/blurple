import json

def get(pl, attr): # get attr from payload data
    d = json.loads(pl)['d']
    if attr in d: return d[attr]

def create(op: int, **d): # return json
    pl = {'op': op, 'd': d}
    return json.dumps(pl)

def heartbeat():
    return create(1)

def identify(token: str):
    prop = {
            '$os': 'linux', 
            '$browser': 'IE', 
            '$device': 'Nokia-3310'
            }
    return create(2, token=token, intents=32509, properties=prop)

def resume(token: str, session_id: str, seq: int):
    return create(6, token=token, session_id=session_id, seq=seq)

