import requests

__all__ = ['Request']

api  = 'https://discord.com/api'

usr = '/users'
gld = '/guilds'
chn = '/channels'
msg = '/messages'

prv = '/preview'
mem = '/members'

src = '/search'

me     = usr + '/@me'
dms    = me  + chn
guilds = me  + gld

def user    (usr_id): return f'{usr}/{usr_id}'
def guild   (gld_id): return f'{gld}/{gld_id}'
def channel (chn_id): return f'{chn}/{chn_id}'

def channels(gld_id): return guild(gld_id)   + chn
def preview (gld_id): return guild(gld_id)   + prv
def members (gld_id): return guild(gld_id)   + mem
def messages(chn_id): return channel(chn_id) + msg

def mem_src (gld_id): return members(gld_id) + src

def member  (gld_id, usr_id): return members(gld_id) + f'/{usr_id}'

def message (chn_id, msg_id): return messages(chn_id) + f'/{msg_id}'


class Request:
    def __init__(self, token, *, bot=True, version=9):
        self.url  = f'{api}/v{version}'
        prefix    = 'Bot' if bot else 'Bearer'
        self.auth = {'Authorization': f'{prefix} {token.strip()}'} 

    def get(self, path, params=None): 
        return requests.get(self.url+path, headers=self.auth, params=params)

    def me_get    (self): return self.get(me)
    def dms_get   (self): return self.get(dms)
    def guilds_get(self): return self.get(guilds)

    def user_get    (self, usr_id): return self.get(user(usr_id))
    def guild_get   (self, gld_id): return self.get(guild(gld_id))
    def channels_get(self, gld_id): return self.get(channels(gld_id))
    def channel_get (self, chn_id): return self.get(channel(chn_id))

    def members_get(self, gld_id, **mem_ls_obj): # Require intent
        return self.get(members (gld_id), mem_ls_obj)

    def messages_get(self, chn_id, **msg_hx_obj):
        return self.get(messages(chn_id), msg_hx_obj)

    def members_search(self, gld_id, **mem_src_obj):
        return self.get(mem_src (gld_id), mem_src_obj)


    def member_get (self, gld_id, usr_id): 
        return self.get(member(gld_id, usr_id))

    def message_get(self, chn_id, msg_id): 
        return self.get(message(chn_id, msg_id))

    def post(self, path, json):
        return requests.post(self.url+path, headers=self.auth, json=json)

    def dm_create(self, usr_id):
        dm_obj = {'recipient_id': usr_id}
        return self.post(dms, dm_obj)

    def guild_create(self, gld_name, **kwargs):
        gld_obj = {'name': gld_name}
        gld_obj.update(kwargs)
        return self.post(guilds, gld_obj)

    def channel_create(self, gld_id, chn_name, **kwargs):
        chn_obj = {'name': chn_name}
        chn_obj.update(kwargs)
        return self.post(channels(gld_id), chn_obj)

    def message_create(self, chn_id, msg_con, **kwargs):
        msg_obj = {'content': msg_con}
        msg_obj.update(kwargs)
        return self.post(messages(chn_id), msg_obj)
    
    def patch(self, path, json):
        return requests.post(self.url+path, headers=self.auth, json=json)

    def guild_modify(self, gld_id, **gld_obj):
        return self.patch(guild(gld_id), gld_obj)

    def channel_modify_position(self, gld_id, chn_id, **kwargs):
        pos_obj = {'id': chn_id}
        pos_obj.update(kwargs)
        return self.patch(guild(gld_id), pos_obj)

    def put(self, path, json):
        return requests.post(self.url+path, headers=self.auth, json=json)
    
    def guild_member_add(self, gld_id, usr_id, access_token, **kwargs):
        join_obj = {'access_token': access_token}
        join_obj.update(kwargs)
        return self.put(member(gld_id, usr_id), join_obj)

    def delete(self, path, json=None): 
        return requests.get(self.url+path, headers=self.auth, json=json)

    def guild_delete(self, gld_id):
        return self.delete(guild(gld_id))

