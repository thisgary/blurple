import json
import asyncio
import requests
import threading
import websockets
import .payload

__all__ = ['Gateway']


class Heartbeat:
    def __init__(self, intv, conn):
        self.beat = True
        self.intv = intv/1000
        self.conn = conn
        threading.Thread(target=asyncio.run, args=(self.op1(),)).start()

    async def op1(self):
        print('[OP1 START]')
        await asyncio.sleep(self.intv)
        while self.beat:
            await self.conn.send(payload.heartbeat())
            await asyncio.sleep(self.intv)
        print('[OP1 STOPPED]')

    def stop(self): self.beat = False


class Gateway:
    def __init__(self, token, *, version=9):
        self.token = token
        self.uri   = f'wss://gateway.discord.gg/?v={version}&encoding=json'

    async def connect(self, res=False):
        async with websockets.connect(self.uri) as self.ws:
            await self.hello()
            if not res: await self.identify()
            else: await self.resume()
            await self.monitor()

    async def hello(self):
        op10 = payload.Read(await self.ws.recv())
        intv = op10.d('heartbeat_interval')
        print('[OP10 RECEIVED]')
        self.hb = Heartbeat(intv, self.ws)

    async def identify(self):
        op2 = payload.identify(self.token)
        await self.ws.send(op2)
        print('[OP2 SENT]')
        ready = payload.Read(await self.ws.recv())
        ss_id = ready.d('session_id')
        ss = {'session_id': ss_id}
        json.dump(ss, open('session.json', 'w'))

    async def resume(self):
        ss = json.load(open('session.json'))
        op6 = payload.resume(self.token, ss['session_id'], ss['seq'])
        await self.ws.send(op6)
        print('[OP6 SENT]')

    async def monitor(self, debug=True):
        while True:
            pl = payload.Read(await self.ws.recv())
            op = pl['op']
            if op == 0:
                ss = json.load(open('session.json'))
                ss['seq'] = pl['s']
                json.dump(ss, open('session.json', 'w'))
            elif op == 7: 
                print('[OP7 RECEIVED]')
                break
            elif op == 11 and not debug: continue
            print(pl.obj)
            if debug: open('log.txt', 'a+').write(f'{pl.obj}\n')
        self.hb.stop()
        await self.connect(True)

    def start(self): asyncio.run(self.connect())

