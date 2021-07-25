import json
import asyncio
import requests
import threading
import websockets
from descord import payload

uri = 'wss://gateway.discord.gg/?v=9&encoding=json'

async def gateway_heartbeat(cd, ws):
    while True:
        await asyncio.sleep(cd/1000)
        await ws.send(payload.heartbeat())

async def gateway_monitor(ws, hb, token):
    while True:
        recv = json.loads(await ws.recv())
        if recv['op'] == 7: 
            hb.stop()
            await gateway_connect(token, True)
        elif recv['op'] == 11: continue
        if 's' in recv: open('seq', 'w').write(str(recv['s'])) 
        print(recv)
        open('log.txt', 'a+').write(f'{recv}\n')

async def gateway_connect(token, resume=False):
    async with websockets.connect(uri) as ws:
        cd = payload.get(await ws.recv(), 'heartbeat_interval')
        hb = threading.Thread(target=asyncio.run, 
                args=(gateway_heartbeat(cd,ws),))
        hb.start()
        if resume:
            session_id = open('session_id').read() 
            seq = int(open('seq').read()) 
            await ws.send(payload.resume(token, session_id, seq))
        else:
            await ws.send(payload.identify(token))
            session_id = payload.get(await ws.recv(), 'session_id')
            open('session_id', 'w').write(session_id)
        await gateway_monitor(ws, hb, token)

