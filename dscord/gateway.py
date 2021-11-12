import asyncio
import json

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
        while True:
            await asyncio.sleep(i)
            OP1 = json.dumps({'op': 1, 'd': self.seq})
            await self.ws.send(OP1)

    async def identify(self) -> None:
        OP2 = json.dumps({
            'op': 2, 
            'd': {
                'token': self.token, 
                'intents': 32509, 
                'properties': {
                    '$os': 'linux', '$browser': 'IE', '$device': 'ta-1077'
                }
            }
        })
        await self.ws.send(OP2)
        r = json.loads(await self.ws.recv())
        self.id = r['d']['session_id']

    async def resume(self) -> None:
        OP6 = json.dumps({
            'op': 6,
            'd': {'token': self.token, 'session_id': self.id, 'seq': self.seq}
        })
        await self.ws.send(OP6)

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
                r = json.loads(await self.ws.recv())

                if self.debug: 
                    print(r)
                    open('pl.log', 'a+', encoding='utf-8').write(f'{r}\n')

                if (op := r['op']) == 0:
                    self.seq = r['s']
                    await self.handle(r)
                elif op == 7: # reconnect
                    await self.resume()
                elif op == 9: # invalid session
                    await asyncio.sleep(3)
                    await self.identify()
                elif op == 10: # new session
                    i = r['d']['heartbeat_interval']/1000
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
