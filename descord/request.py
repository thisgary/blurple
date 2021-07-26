import requests

__all__ = ['Request']

api  = 'https://discord.com/api'

usr = '/users'
gld = '/guilds'
chn = '/channels'
msg = '/messages'

me     = usr + '/@me'
dms    = me + chn
guilds = me + gld

def user    (usr_id): return f'{usr}/{usr_id}'
def guild   (gld_id): return f'{gld}/{gld_id}'
def channel (chn_id): return f'{chn}/{chn_id}'

def channels(gld_id): return guild  (gld_id) + chn
def messages(chn_id): return channel(chn_id) + msg

def message (chn_id, msg_id): return messages(chn_id) + f'/{msg_id}'


class Request:
    def __init__(self, token, *, bot=True, version=9):
        self.url  = f'{api}/v{version}'
        prefix    = 'Bot' if bot else 'Bearer'
        self.auth = {'Authorization': f'{prefix} {token.strip()}'} 

    def get(self, path, params=None): 
        return requests.get(self.url+path, headers=self.auth, params=params)

    def get_me    (self): return self.get(me)
    def get_dms   (self): return self.get(dms)
    def get_guilds(self): return self.get(guilds)

    def get_user    (self, usr_id): return self.get(user    (usr_id))
    def get_guild   (self, gld_id): return self.get(guild   (gld_id))
    def get_channels(self, gld_id): return self.get(channels(gld_id))
    def get_channel (self, chn_id): return self.get(channel (chn_id))

    def get_messages(self, chn_id, hx_obj=None):
        return self.get(messages(chn_id), hx_obj)

    def get_message(self, chn_id, msg_id):
        return self.get(message(chn_id, msg_id))

    def post(self, path, json):
        return requests.post(self.url+path, headers=self.auth, json=json)

    def create_dm(self, usr_id):
        dm_obj = {'recipient_id': usr_id}
        return self.post(dms, dm_obj)

    def create_guild(self, gld_name, **kwargs):
        gld_obj = {'name': gld_name}
        gld_obj.update(kwargs)
        return self.post(guilds, gld_obj)

    def create_channel(self, gld_id, chn_name, **kwargs):
        chn_obj = {'name': chn_name}
        chn_obj.update(kwargs)
        return self.post(channels(gld_id), chn_obj)

    def create_message(self, chn_id, msg_con, **kwargs):
        msg_obj = {'content': msg_con}
        msg_obj.update(kwargs)
        return self.post(messages(chn_id), msg_obj)

