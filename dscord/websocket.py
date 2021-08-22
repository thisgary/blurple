import asyncio
import inspect
import json
import os
import threading
from typing import Callable

import dscord
import websockets
from websockets.exceptions import ConnectionClosedOK

__all__ = ['Gateway']


class Gateway:
    def __init__(self, access_token: str, *, v: int = 9):
        self.token = access_token
        self.uri = f'wss://gateway.discord.gg/?v={v}&encoding=json'
        self.active, self.events = True, []

    def event(self, f: Callable) -> Callable:
        if inspect.isfunction(f):
            self.events.append(f)
        return f
 
    async def connect(self):
        async with websockets.connect(self.uri) as self.ws:
            op10 = json.loads(await self.ws.recv())
            intv = op10['d']['heartbeat_interval']
            task = await asyncio.gather(
                    self.heartbeat(intv),
                    self.monitor()
                    )

    async def heartbeat(self, interval: int):
        hb, i = dscord.Payload(1).json(), interval//1000
        while True:
            await asyncio.sleep(i)
            await self.ws.send(hb)

    async def identify(self):
        prop = {
                '$os': 'linux',
                '$browser': 'IE',
                '$device': 'ta-1077'
                }
        op2 = dscord.Payload(2, 
                token=self.token, 
                intents=32509, 
                properties=prop).json()
        await self.ws.send(op2)
        op0 = json.loads(await self.ws.recv())
        sesh = {
                'id': op0['d']['session_id']
                }
        json.dump(sesh, open('session.json', 'w'))

    async def resume(self):
        sesh = json.load(open('session.json'))
        op6 = dscord.Payload(6, 
                token=self.token, 
                session_id=sesh['id'], 
                seq=sesh['s'])
        await self.ws.send(op6.json())

    async def monitor(self):
        try:
            await self.identify()
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
        except ConnectionClosedOK: 
            print('[DISCONNECTED]')

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
        os.remove('session.json')

    def stop(self):
        self.active = False
