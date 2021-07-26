import json
import asyncio
import requests
import threading
import websockets
from descord import payload


class Request:
    class Path:
        usr = '/users'
        gld = '/guilds'
        chn = '/channels'
        msg = '/messages'

        def user(self, user_id):
            return self.url + self.usr + '/' + str(user_id)

        def me(self):
            return self.url + '/@me'

        def dms(self):
            return self.me() + self.chn

        def guilds(self):
            return self.me() + self.gld

        def guild(self, guild_id):
            return self.url + self.gld + '/' + str(guild_id)

        def channels(self, guild_id):
            return self.guild(guild_id) + self.chn

        def channel(self, channel_id):
            return self.url + self.chn + '/' + str(channel_id)

        def messages(self, channel_id):
            return self.channel(channel_id) + self.msg

        def message(self, channel_id, message_id):
            return self.messages(channel_id) + '/' + str(message_id)


    def __init__(self, access_token, *, is_bot=True, api_version=9):
        auth_prefix = 'Bot' if is_bot else 'Bearer'
        self.auth = {'Authorization': f'{auth_prefix} {access_token.strip()}'}
        self.url = f'https://discord.com/api/v{api_version}'
        self.p = self.Path()

    def get(self, path, obj=None):
        return requests.get(self.url+path, headers=self.auth, params=obj)

    def get_me(self):
        return self.get(self.p.me())

    def get_user(self, user_id):
        return self.get(self.p.user(user_id))

    def get_dms(self):
        return self.get(self.p.dms())

    def get_guilds(self):
        return self.get(self.p.guilds())

    def get_guild(self, gld_id):
        return self.get(self.p.guild(gld_id))

    def get_channels(self, gld_id):
        return self.get(self.p.channels(gld_id))

    def get_channel(self, chn_id):
        return self.get(self.p.channel(chn_id))

    def get_messages(self, chn_id, hx_obj=None):
        return self.get(self.p.messages(chn_id), hx_obj)

    def get_message(self, chn_id, msg_id):
        return self.get(self.p.message(chn_id, msg_id))

    def post(self, path, obj):
        return requests.post(path, headers=self.auth, json=obj)

    def create_dm(self, user_id):
        dm_obj = {'recipient_id': user_id}
        return self.post(self.p.dms(), dm_obj)

    def create_guild(name, **kwargs):
        guild_obj = {'name': name}
        guild_obj.update(kwargs)
        return self.post(self.p.gld, guild_obj)

    def create_channel(self, gld_id, chn_name, **kwargs):
        chn_obj = {'name': chn_name}
        chn_obj.update(kwargs)
        return self.post(self.p.channels(gld_id), chn_obj)

    def create_message(self, chn_id, msg_con, **kwargs):
        msg_obj = {'content': msg_con}
        chn_obj.update(kwargs)
        return self.post(self.p.messages(chn_id), msg_obj)


class Gateway:
    class Heartbeat:
        def __init__(self, interval, connection):
            self.alive = True
            self.interval = interval/1000
            self.connection = connection

        async def async_start(self):
            while self.alive:
                await asyncio.sleep(self.interval)
                await self.connection.send(payload.heartbeat())
            print('Stopped heartbeating')

        def start(self):
            threading.Thread(target=asyncio.run, args=(self.async_start(),)).start()

        def stop(self):
            self.alive = False


    def __init__(self, token, *, version=9):
        self.token = token
        self.uri = f'wss://gateway.discord.gg/?v={version}&encoding=json'
        self.hb = None

    async def async_connect(self, resume=False):
        async with websockets.connect(self.uri) as ws:
            hello = await ws.recv() # Hello
            hb_intv = payload.data(hello, 'heartbeat_interval')
            self.hb = self.Heartbeat(hb_intv, ws)
            self.hb.start()
            if not resume:
                await ws.send(payload.identify(self.token)) # Identify
                ready = await ws.recv() # Ready
                ss = {
                        'session_id': payload.data(ready, 'session_id'),
                        'seq': None}
                json.dump(ss, open('session.json', 'w'))
            else:
                ss = json.load(open('session.json'))
                session_id, seq = ss['session_id'], ss['seq']
                await ws.send(payload.resume(self.token, session_id, seq)) # Resume
            await self.monitor(ws)

    async def monitor(self, ws):
        while True:
            event = json.loads(await ws.recv())
            if event['op'] is 7:
                self.hb.stop()
                await self.bridge(True)
            elif event['op'] is 11: continue
            if 's' in event: 
                ss = json.load(open('session.json'))
                ss['seq'] = event['s']
                json.dump(ss, open('session.json', 'w'))
            print(event)
            open('log.txt', 'a+').write(f'{event}\n')

    def connect(self):
        asyncio.run(self.async_connect())

