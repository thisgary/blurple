import requests


class Access:
    def __init__(self, access_token, *, is_bot=True, api_version=9):
        auth_prefix = 'Bot' if is_bot else 'Bearer'
        self.auth = {'Authorization': f'{auth_prefix} {access_token.strip()}'}
        self.url = f'https://discord.com/api/v{api_version}'

    def get(self, path, obj=None): return requests.get(self.url+path, headers=self.auth, params=obj)

    def get_user(user_id): return self.get(f'/users/{user_id}')

    def get_me(self): return self.get('/users/@me')

    def get_guilds(self): return self.get('/users/@me/guilds')

    def get_guild(self, guild_id): return self.get(f'/guilds/{guild_id}')

    def get_channels(self, guild_id): return self.get(f'/guilds/{guild_id}/channels')

    def get_channel(self, chn_id): return self.get(f'/channels/{chn_id}')

    def get_messages(self, chn_id, hx_obj=None):
        return self.get(f'/channels/{chn_id}/messages', hx_obj)

    def get_message(self, chn_id, msg_id):
        return self.get(f'/channels/{chn_id}/messages/{msg_id}')

    def post(self, path, obj):
        return requests.post(self.url+path, headers=self.auth, json=obj)

    def create_dm(self, dm_obj):
        return self.post(f'/users/@me/channels', dm_obj)

    def create_channel(self, guild_id, chn_name, *, chn_type=None):
        chn_obj = {'name': chn_name}
        if chn_type: chn_obj['type'] = chn_type
        return self.post(f'/guilds/{guild_id}/channels', chn_obj)

    def create_message(self, chn_id, msg_con):
        msg_obj = {'content': msg_con}
        return self.post(f'/channels/{chn_id}/messages', msg_obj)


class Obj:
    @staticmethod
    def dm(usr_id): # direct message channel object
        obj = {'recipient_id': usr_id} # user id
        return obj

    @staticmethod
    def guild(name, *, 
            icon=None, 
            verification=None, 
            notifications=None, 
            explicit=None, 
            roles=None, 
            channels=None, 
            afk_channel=None, 
            afk_timeout=None, 
            system_channel=None, 
            system_channel_flags=None):
        obj = {'name': name}
        if icon: obj['icon'] = icon # byte-like object
        if verification: obj['verification_level'] = verification # 0-4
        if notifications: obj['default_message_notifications'] = notifications # 0-1
        if explicit: obj['explicit_content_filter'] = explicit
        if roles: obj['roles'] = roles
        if channels: obj['channels'] = channels
        if afk_channel: obj['afk_channel_id'] = afk_channel
        if afk_timeout: obj['afk_timeout'] = afk_timeout
        if system_channel: obj['system_channel_id'] = system_channel
        if system_channel_flags = obj['system_channel_flags'] = system_channel_flags
        return obj

    @staticmethod
    def channel(name, *, 
            chn_type=None, 
            topic=None, 
            bitrate=None, 
            user_limit=None, 
            rate_limit_per_user=None, 
            position=None, 
            permission_overwrites=None, 
            parent_id=None, 
            nsfw=None):
        obj = {'name': name}
        if chn_type: obj['type'] = chn_type # 0-12
        if topic: obj['topic'] = topic # strings
        if bitrate: obj['bitrate'] = bitrate # (voice only)
        if user_limit: obj['user_limit'] = user_limit # 0-99 (voice only)
        if rate_limit: obj['rate_limit_per_user'] = rate_limit # 0-21600
        if position: obj['position'] = position # int
        if permission_overwrites: obj['permission_overwrites'] = permission_overwrites
        if parent_id: obj['parent_id'] = parent_id # category channel id
        if nsfw: obj['nsfw'] = nsfw 
        return obj        

    @staticmethod
    def hx(hx_type, msg_id, limit:int=None): # messages history object
        obj = {hx_type: msg_id} # type: around, before, after; id: user id
        if limit: obj['limit'] = limit # 1-100
        return obj

