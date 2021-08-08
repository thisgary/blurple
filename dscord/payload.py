import json

conn_prop = { # Connection properties
        '$os': 'linux', 
        '$browser': 'IE', 
        '$device': 'Nokia-3310'}

def create(op, **d):
    pl = {'op': op, 'd': d}
    return json.dumps(pl)

def heartbeat(): return create(1)

def identify(token):
    return create(2, token=token, intents=32509, properties=conn_prop)

def resume(token, session_id, seq):
    return create(6, token=token, session_id=session_id, seq=seq)


class Read:
    def __init__(self, pl_str): # Payload string
        self.obj = obj = json.loads(pl_str)
    
    def d(self, attr):
        data = self.obj['d']
        if attr in data: return data[attr]

