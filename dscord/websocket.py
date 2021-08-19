import json
import asyncio
import requests
import threading
import websockets
from dscord import payload

__all__ = ['Gateway']


class Heartbeat:
    def __init__(self, intervals: int, connection):
        self.beat = True
        self.intv = intervals/1000
        self.conn = connection
        threading.Thread(target=asyncio.run, args=(self.start(),)).start()

    async def start(self):
        await asyncio.sleep(self.intv)
        while self.beat:
            await self.conn.send(payload.heartbeat())
            await asyncio.sleep(self.intv)

    def stop(self):
        self.beat = False


class Gateway:
    def __init__(self, access_token: str, *, api_version: int = 9):
        self.token = access_token
        self.uri   = f'wss://gateway.discord.gg/?v={api_version}&encoding=json'
        self.active = True

    async def connect(self):
        async with websockets.connect(self.uri) as self.ws:
            op10 = payload.Read(await self.ws.recv())
            inertvals = op10.d('heartbeat_interval')
            self.hb = Heartbeat(intervals, self.ws)
            try: self.resume()
            except: self.identify()
            await self.monitor()
        
    async def resume(self):
        session = json.load(open('session.json'))
        op6 = payload.resume(self.token, session['session_id'], session['seq'])
        await self.ws.send(op6)

    async def identify(self):
        op2 = payload.identify(self.token)
        await self.ws.send(op2)
        ready = payload.Read(await self.ws.recv())
        session = {'session_id': ready.d('session_id')}
        json.dump(session, open('session.json', 'w'))

    async def monitor(self, *, debug: bool = True):
        while self.active:
            pl = payload.Read(await self.ws.recv())
            if debug:
                open('dscord.log', 'a+').write(f'{pl.obj}\n')
            op = pl['op']
            if op == 0:
                session = json.load(open('session.json'))
                session['seq'] = pl['s']
                json.dump(session, open('session.json', 'w'))
            elif op == 7: break
        self.hb.stop()

    def start(self):
        while self.active:
            asyncio.run(self.connect())

    def stop(self):
        self.active = False
