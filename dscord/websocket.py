import json
import asyncio
import requests
import threading
from typing import Callable

import dscord
import websockets

__all__ = ['Gateway']


class Heartbeat:
    def __init__(self, interval: int, connection):
        self.interval = interval/1000
        self.connection = connection
        self.active = True
        threading.Thread(target=asyncio.run, args=(self.start(),)).start()

    async def start(self):
        op1 = dscord.Payload(1)
        await asyncio.sleep(self.interval)
        while self.active:
            await self.connection.send(op1.json())
            await asyncio.sleep(self.interval)

    def stop(self):
        self.active = False


class Gateway:
    def __init__(self, access_token: str, *, api_version: int = 9):
        self.token = access_token
        self.uri   = f'wss://gateway.discord.gg/?v={api_version}&encoding=json'
        self.active, self.resuming = True, False
        self.events = []

    def event(self, f: Callable) -> Callable:
        self.events.append(f)
        return f

    async def connect(self):
        async with websockets.connect(self.uri) as self.ws:
            op10 = json.loads(await self.ws.recv())
            interval = op10['d']['heartbeat_interval']
            self.hb = Heartbeat(interval, self.ws)
            await self.resume() if self.resuming else await self.identify()
            await self.monitor()
 
    async def resume(self):
        session = json.load(open('session.json'))
        op6 = dscord.Payload(6, token=self.token, 
                session_id=session['session_id'], seq=session['seq'])
        await self.ws.send(op6.json())

    async def identify(self):
        properties = {
                '$os': 'linux',
                '$browser': 'IE',
                '$device': 'ta-1077'}
        op2 = dscord.Payload(2, token=self.token, 
                intents=32509, properties=properties)
        await self.ws.send(op2.json())
        READY = json.loads(await self.ws.recv())
        session = {'session_id': READY['d']['session_id']}
        json.dump(session, open('session.json', 'w'))

    async def monitor(self):
        while self.active:
            payload = json.loads(await self.ws.recv())
            if self.debug:
                print(payload)
                open('dscord.log', 'a+').write(f'{payload}\n') 
            op = payload['op']
            if op == 0:
                session = json.load(open('session.json'))
                session['seq'] = payload['s']
                json.dump(session, open('session.json', 'w'))
                await self.handle(payload)
            elif op == 7:
                self.resuming = True
                break
            elif op == 9:
                self.resuming = False
                break
        self.hb.stop()

    async def handle(payload: dict):
        for event in self.events:
            try:
                event(payload)
            except Exception as e:
                print(e)
                if self.debug:
                    open('error.log', 'w').write(e+'\n')

    def start(self, *, debug: bool = False):
        self.debug = debug
        while self.active:
            asyncio.run(self.connect())
        os.remove('session.json')

    def stop(self):
        self.active = False
