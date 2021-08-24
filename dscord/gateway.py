import asyncio
import os
import threading
from typing import Callable

import dscord
import websockets
from websockets.exceptions import ConnectionClosedOK

__all__ = ['Gateway']


class Gateway:
    def __init__(self, access_token: str, *, 
            version: int = 9, debug: bool = False) -> None:
        self.token  = access_token
        self.uri = f'wss://gateway.discord.gg/?v={version}&encoding=json'
        self.debug = debug

    def start(self) -> None:
        self.active = True
        while self.active:
            try:
                asyncio.run(self.connect())
            except Exception as e:
                print(e)
        else:
            os.remove('session.json')

    def stop(self) -> None:
        self.active = False

    async def connect(self) -> None:
        async with websockets.connect(self.uri) as self.ws:
            monitor = asyncio.create_task(self.monitor())
            while self.active:
                await asyncio.sleep(0.5)
            else:
                self.hb.cancel()
                monitor.cancel()

    async def monitor(self):
        while True:
            payload = await self.ws.recv()
            if self.debug:
                print(payload)
                open('dscord.log', 'a+').write(f'{payload}\n')
            pl = dscord.Payload()
            pl.load(payload)
            op = pl.op
            if op == 10:
                intv = payload.d['heartbeat_interval']
                self.hb = asyncio.create_task(self.heartbeat(intv))
                await self.identify()
            elif op == 9:
                await asyncio.sleep(3)
                await self.identify()
            elif op == 7:
                await self.resume()
            elif op == 0:
                self.seq = pl.s
                yield pl

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

