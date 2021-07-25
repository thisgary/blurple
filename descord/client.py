import json
import asyncio
import requests
import threading
import websockets
from descord import payload

uri = 'wss://gateway.discord.gg/?v=9&encoding=json'
cli = {}

async def gateway_heartbeat(intv, ws):
    while True:
        await asyncio.sleep(intv/1000)
        await ws.send(payload.heartbeat())

# Monitor incoming gateway events
async def gateway_monitor(ws, hb, token):
    while True:
        event = json.loads(await ws.recv())
        if event['op'] is 7: 
            hb.stop()
            await gateway_connect(token, True)
        elif event['op'] is 11: continue
        if 's' in event: 
            cli = json.load(open('client.json'))
            cli['seq'] = event['s']
            json.dump(cli, open('client.json', 'w'))
        print(event)
        open('log.txt', 'a+').write(f'{event}\n')

# Establish websocket connection with Gateway API
# Alternatively, resume disconnected session
async def gateway_connect(token, resume=False):
    async with websockets.connect(uri) as ws:
        hello = await ws.recv()
        hb_intv = payload.data(hello, 'heartbeat_interval')
        hb = threading.Thread(target=asyncio.run,
                args=(gateway_heartbeat(hb_intv, ws), ))
        hb.start()
        if resume:
            cli = json.load(open('client.json'))
            session_id, seq = cli['session_id'], cli['seq']
            await ws.send(payload.resume(token, session_id, seq))
        else:
            await ws.send(payload.identify(token))
            ready = await ws.recv()
            cli['session_id'] = payload.data(ready, 'session_id')
            json.dump(cli, open('client.json', 'w'))
        await gateway_monitor(ws, hb, token)

def connect(token):
    asyncio.run(gateway_connect(token))

