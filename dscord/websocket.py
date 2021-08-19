import json
import asyncio
import requests
import threading

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
        self.active, self.resume = True, False

    async def connect(self, debug: bool):
        async with websockets.connect(self.uri) as self.ws:
            op10 = json.loads(await self.ws.recv())
            interval = op10['d']['heartbeat_interval']
            self.hb = Heartbeat(interval, self.ws)
            if self.resume: await self.resume()
            else: await self.identify()
            await self.monitor(debug)
        
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

    async def monitor(self, debug: bool):
        while self.active:
            payload = json.loads(await self.ws.recv())
            if debug:
                print(payload)
                open('dscord.log', 'a+').write(f'{payload}\n') 
            op = payload['op']
            if op == 0:
                session = json.load(open('session.json'))
                session['seq'] = payload['s']
                json.dump(session, open('session.json', 'w'))
            elif op == 7:
                self.resume = True
                break
            elif op == 9:
                self.resume = False
                break
        self.hb.stop()

    def start(self, *, debug: bool = False):
        while self.active:
            asyncio.run(self.connect(debug))
        os.remove('session.json')

    def stop(self):
        self.active = False
