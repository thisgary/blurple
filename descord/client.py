import json
import asyncio
import requests
import threading
import websockets

uri = 'wss://gateway.discord.gg/?v=9&encoding=json'
conn = {'$os': 'linux','$browser': 'custom','$device': 'custom'}

def gateway_payload(op, **d):
    return json.dumps({'op': op, 'd': d})

async def gateway_heartbeat(cd, ws):
    while True:
        await asyncio.sleep(cd/1000)
        await ws.send(gateway_payload(1))

async def gateway_monitor(ws, hb, token):
    while True:
        recv = json.loads(await ws.recv())
        if recv['op'] == 7: 
            hb.stop()
            await gateway_resume(token, True)
        elif recv['op'] == 11: continue
        if 's' in recv: open('seq', 'w').write(str(recv['s'])) 
        print(recv)
        open('log.txt', 'a+').write(f'{recv}\n')

async def gateway_connect(token, resume=False):
    async with websockets.connect(uri) as ws:
        op10 = json.loads(await ws.recv())
        cd = op10['d']['heartbeat_interval']
        hb = threading.Thread(target=asyncio.run, 
                args=(gateway_heartbeat(cd,ws),))
        hb.start()
        if resume:
            op6 = gateway_payload(6, token=token,
                    session_id=open('session_id').read(), 
                    seq=int(open('seq').read()))
            await ws.send(op6)
        else:
            op2 = gateway_payload(2, token=token, 
                    intents=32509, properties=conn)
            await ws.send(op2)
            op0 = json.loads(await ws.recv())
            session_id = op0['d']['session_id']
            open('session_id', 'w').write(session_id)
        await gateway_monitor(ws, hb, token)

