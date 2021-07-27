import json
import asyncio
import requests
import threading
import websockets
from descord import payload

__all__ = ['Gateway']


class Heartbeat:
    def __init__(self, intv, conn):
        self.beat = True
        self.intv = intv/1000
        self.conn = conn
        threading.Thread(target=asyncio.run, args=(self.op1(),)).start()

    async def op1(self):
        print('[OP1 STARTED]')
        while self.beat:
            await self.conn.send(payload.heartbeat())
            await asyncio.sleep(self.intv)
        print('[OP1 STOPPED]')

    def stop(self): self.beat = False


class Gateway:
    def __init__(self, token, *, version=9):
        self.token = token
        self.uri   = f'wss://gateway.discord.gg/?v={version}&encoding=json'

    async def connection(self, res=False):
        async with websockets.connect(self.uri) as ws:
            await self.hello(ws)
            if not res: await self.identify(ws)
            else: await self.resume(ws)
            await self.monitor(ws)

    async def hello(self, ws):
        op10 = await ws.recv()
        intv = payload.data(op10, 'heartbeat_interval')
        self.hb = Heartbeat(intv, ws)

    async def identify(self, ws):
        op2 = payload.identify(self.token)
        print(0)
        await ws.send(op2)
        print(1)
        ready = await ws.recv()
        print(ready)
        ss_id = payload.data(ready, 'session_id')
        ss = {'session_id': ss_id}
        json.dump(ss, open('session.json', 'w'))

    async def resume(self, ws):
        ss = json.load(open('session.json'))
        op6 = payload.resume(self.token, ss['session_id'], ss['seq'])
        await ws.send(op6)

    async def monitor(self, ws, debug=True):
        while True:
            pls = await ws.recv()
            print(pls)
            # Illegal, personal debug use only
            if debug: open('log.txt', 'a+').write(pls+'\n')
            pl = json.loads(pls)
            op = pl['op']
            if op == 0:
                ss = json.load(open('session.json'))
                ss['seq'] = event['s']
                json.dump(ss, open('session.json', 'w'))
            elif op == 7: break
            elif op == 11 and debug: continue
        self.hb.stop()
        await self.connection(True)
    def connect(self):
        asyncio.run(self.connection())

