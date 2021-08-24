import asyncio
import os
import threading
from typing import Callable

import dscord
import dscord.object
import websockets

__all__ = ['Gateway']


class Gateway:
    def event(self, func: callable) -> callable:
        if asyncio.iscoroutinefunction(func):
            self.events.append(func)
        return func

    def __init__(self, access_token: str, *, 
            version: int = 9, debug: bool = True) -> None:
        self.token  = access_token
        self.uri = f'wss://gateway.discord.gg/?v={version}&encoding=json'
        self.debug = debug
        self.events = []

    def start(self) -> None:
        self.active = True
        while self.active:
            try:
                asyncio.run(self.connect(), 
                        debug=self.debug)
            except Exception as e:
                print(e)
        else:
            os.remove('session.json')

    def stop(self) -> None:
        self.active = False

    async def connect(self) -> None:
        async with websockets.connect(self.uri) as self.ws:
            await self.monitor()
            self.hb.cancel()

    async def monitor(self) -> None:
        while True:
            payload = await self.ws.recv()
            if self.debug:
                print(payload)
                open('dscord.log', 'a+').write(f'{payload}\n')
            pl = dscord.Payload()
            pl.load(payload)
            op = pl.op
            if op == 10:
                intv = pl.d['heartbeat_interval']
                self.hb = asyncio.create_task(self.heartbeat(intv))
                await self.identify()
            elif op == 9:
                await asyncio.sleep(3)
                await self.identify()
            elif op == 7:
                await self.resume()
            elif op == 0:
                self.seq = pl.s
                await self.handle(pl)

    async def heartbeat(self, interval: int) -> None:
        i = interval // 1000
        op1 = dscord.Payload(1).dump()
        while True:
            await asyncio.sleep(i)
            await self.ws.send(op1)

    async def identify(self):
        prop = {
                '$os': 'linux',
                '$browser': 'IE',
                '$device': 'ta-1077'
        }
        op2 = dscord.Payload(2, 
                token=self.token, 
                intents=32509, 
                properties=prop
        ).dump()
        await self.ws.send(op2)
        ready = await self.ws.recv()
        pl = dscord.Payload()
        pl.load(ready)
        self.sesh_id = pl.d['session_id']

    async def resume(self):
        op6 = dscord.Payload(6, 
                token=self.token, 
                session_id=self.sesh_id, 
                seq=self.seq).dump()
        await self.ws.send(op6)

    async def handle(self, pl: dscord.object.Payload):
        for event in self.events:
            try:
                await event(pl)
            except Exception as e:
                print(e)

