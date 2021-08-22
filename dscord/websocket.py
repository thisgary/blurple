import asyncio
import inspect
import json
import os
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
        self.active = True
        self.events = []

    def event(self, f: Callable) -> Callable:
        if inspect.isfunction(f):
            self.events.append(f)
        return f

    async def connect(self):
        async with websockets.connect(self.uri) as self.ws:
            op10 = json.loads(await self.ws.recv())
            interval = op10['d']['heartbeat_interval']
            self.hb = Heartbeat(interval, self.ws)
            await self.identify()
            asyncio.create_task(self.monitor())
            while self.active: pass
 
    async def resume(self):
        sesh = json.load(open('session.json'))
        op6 = dscord.Payload(6, token=self.token, 
                session_id=sesh['id'], seq=sesh['s'])
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
        sesh = {'id': READY['d']['session_id']}
        json.dump(sesh, open('session.json', 'w'))

    async def monitor(self):
        while True:
            payload = json.loads(await self.ws.recv())
            if self.debug:
                print(payload)
                open('dscord.log', 'a+').write(f'{payload}\n')
            p = dscord.Payload()
            p.read(payload)
            if p.op == 0:
                sesh = json.load(open('session.json'))
                sesh['s'] = p.s
                json.dump(sesh, open('session.json', 'w'))
                await self.handle(p)
            elif p.op == 7:
                await self.resume()
            elif p.op == 9:
                await asyncio.sleep(3)
                await self.identify()

    async def handle(self, payload):
        for event in self.events:
            try: 
                if inspect.iscoroutinefunction(event):
                    await event(payload)
                else: event(payload)
            except Exception as e: print(e)

    def start(self, *, debug: bool = False):
        self.debug = debug
        while self.active:
            try: asyncio.run(self.connect())
            except Exception as e: print(e)
            self.hb.stop()
        os.remove('session.json')

    def stop(self):
        self.active = False
