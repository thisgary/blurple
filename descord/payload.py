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
        self.str = pl_str
        self.obj = json.loads(pl_str)
        self.op  = self.obj['op']
        self.s   = self.obj['s']
        self.t   = self.obj['t']
    
    def d(self, attr=None):
        d = self.obj['d']
        if attr:
            if attr in d: return d[attr]
        else: return d

