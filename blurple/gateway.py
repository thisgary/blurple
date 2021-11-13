import asyncio
from datetime import datetime
import json

from .object import Payload
import websockets


__all__ = ['Gateway']


class Gateway:
    events = []
    
    def __init__(self, access_token: str, *, 
                 version: int = 9, debug: bool = False) -> None:
        self.token  = access_token
        self.uri = f'wss://gateway.discord.gg/?v={version}&encoding=json'
        self.debug = debug

    async def heartbeat(self, i: int) -> None:
        op1 = Payload(1)
        while True:
            await asyncio.sleep(i)
            op1.load['d'] = self.seq
            await self.ws.send(op1)

    async def recv(self) -> dict:
        pl = json.loads(await self.ws.recv())
        if self.debug: 
            print(pl)
            log = f'[{datetime.now()}] {pl}\n'
            open('blurple.log', 'a+', encoding='utf-8').write(log)
        return pl

    async def identify(self) -> None:
        PROP = {'$os': 'linux', '$browser': 'IE', '$device': 'ta-1077'}
        op2 = Payload(2, token=self.token, intents=32509, properties=PROP)
        await self.ws.send(op2.load)
        op0 = await self.recv()
        self.id = op0['d']['session_id'] # TODO: 429

    async def resume(self) -> None:
        OP6 = Payload(6, token=self.token, session_id=self.id, seq=self.seq)
        await self.ws.send(OP6.load)

    # USAGE: @Gateway().event
    def event(self, func: callable) -> callable:
        if asyncio.iscoroutinefunction(func):
            self.events.append(func)
        return func

    async def handle(self, r: dict):
        for event in self.events:
            try:
                await event(r)
            except Exception as e:
                print(e)
                if self.debug: # debug error logging
                    open('error.log', 'a+').write(f'{e}\n')

    async def connect(self) -> None:
        async with websockets.connect(self.uri) as self.ws:
            while True:
                pl = await self.recv()
                if (op := pl['op']) == 0:
                    self.seq = pl['s']
                    await self.handle(pl)
                elif op == 7: # reconnect
                    await self.resume()
                elif op == 9: # invalid session
                    await asyncio.sleep(3)
                    await self.identify()
                elif op == 10: # new session
                    i = pl['d']['heartbeat_interval']/1000
                    self.hb = asyncio.create_task(self.heartbeat(i))
                    await self.identify()
        self.hb.cancel()

    def start(self) -> None:
        while True:
            try:
                asyncio.run(self.connect())
            except Exception as e:
                print(e)
                if self.debug: 
                    open('pl.log', 'a+').write(f'{e}\n')
