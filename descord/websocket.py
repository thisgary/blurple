import json
import asyncio
import requests
import threading
import websockets
from descord import payload

__all__ = ['Gateway']


class Gateway:
    class Heartbeat:
        def __init__(self, interval, connection):
            self.alive      = True
            self.interval   = interval/1000
            self.connection = connection

        async def heartbeating(self):
            while self.alive:
                await asyncio.sleep(self.interval)
                await self.connection.send(payload.heartbeat())
            print('Stopped heartbeating')

        def start(self): 
            threading.Thread(target=asyncio.run, args=(self.heartbeating(),)).start()

        def stop(self):
            self.alive = False


    def __init__(self, token, *, version=9):
        self.token = token
        self.uri   = f'wss://gateway.discord.gg/?v={version}&encoding=json'

    async def connection(self, resume=False):
        async with websockets.connect(self.uri) as ws:
            hello   = await ws.recv() # Hello
            hb_intv = payload.data(hello, 'heartbeat_interval')
            self.hb = self.Heartbeat(hb_intv, ws)
            self.hb.start()
            if not resume:
                await ws.send(payload.identify(self.token))
                ready = await ws.recv()
                ss = {
                        'session_id': payload.data(ready, 'session_id'),
                        'seq': None}
                json.dump(ss, open('session.json', 'w'))
            else:
                ss = json.load(open('session.json'))
                session_id, seq = ss['session_id'], ss['seq']
                await ws.send(payload.resume(self.token, session_id, seq))
            await self.monitor(ws)

    async def monitor(self, ws, debug=True):
        while True:
            event = json.loads(await ws.recv())
            if event['op'] == 7:
                self.hb.stop()
                await self.connection(True)
            elif event['op'] == 11:
                if not debug: continue # Ignoring logging
            if 's' in event: 
                ss = json.load(open('session.json'))
                ss['seq'] = event['s']
                json.dump(ss, open('session.json', 'w'))
            print(event)
            if debug: open('log.txt', 'a+').write(f'{event}\n') # Debugging purpose

    def connect(self):
        asyncio.run(self.connection())

