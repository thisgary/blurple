import requests


class Abreaction:
    def __init__(self, access_token, *, is_bot=True, api_version=None):
        auth_prefix = 'Bot' if is_bot else 'Bearer'
        self.auth = {'Authorization': f'{auth_prefix} {access_token}'}
        base_url = 'https://discord.com/api'
        self.url = f'{base_url}/v{api_version}' if api_version else base_url

    def get(self, path):
        return requests.get(self.url+path, headers=self.auth)

    def get_guilds(self):
        return self.get('/users/@me/guilds').json()

    def get_guild(self, guild_id):
        return self.get(f'/guilds/{guild_id}')

    def get_channels(self, guild_id):
        return self.get(f'/guilds/{guild_id}/channels')

    def get_channel(self, chn_id):
        return self.get(f'/channels/{chn_id}')

    def get_message(self, msg_id):
        return self.get(f'/messages/{msg_id}')

    def post(self, path, obj):
        return requests.post(self.url+path, headers=self.auth, json=obj)

    def create_channel(self, guild_id, chn_name, *, chn_type=None):
        chn_obj = {'name': chn_name}
        if chn_type: chn_obj['type'] = chn_type
        return self.post(f'/guilds/{guild_id}/channels', chn_obj)

    def create_message(self, chn_id, msg_con):
        msg_obj = {'content': msg_con}
        return self.post(f'/channels/{chn_id}/messages', msg_obj)

