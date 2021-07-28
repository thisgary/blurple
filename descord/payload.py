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
        self.pl = json.loads(pl_str)
        self.is_op0 = self.pl['op'] == 0

    def op(self): return self.pl['op']
    
    def data(self, attr=None):
        d = self.pl['d']
        if attr and 'attr' in d: return d[attr]
        else: return d

    def seq(self):
        if self.is_op0: return self.pl['s']

    def name(self):
        if self.is_op0: return self.pl['t']

