import requests

__all__ = ['Request']

class Request:
    def __init__(self, access_token, *, api_version=9):
        h = {'Authorization': f'Bot {access_token}'} 
        u = f'https://discord.com/api/v{api_version}'

        self.get = lambda p, d=None : requests.get(u+p, headers=h, params=d)
        self.post = lambda p, j : requests.post(u+p, headers=h, json=j)
    
    def get_dms(self):
        return self.get('/users/@me/channels')

    def get_guilds(self):
        return self.get('/users/@me/guilds')

    def get_guild(self, guild_id: int):
        return self.get(f'/guilds/{guild_id}')

    def get_channels(self, guild_id: int):
        return self.get(f'/guilds/{guild_id}/channels')

    def get_channel(self, channel_id: int):
        return self.get(f'/channels/{channel_id}')

    def get_messages(self, channel_id: int, history_object: dict):
        return self.get(f'/channels/{channel_id}', history_object)
    
    def post_message(self, channel_id: int, message_object: dict):
        return self.post(f'/channels/{channel_id}/messages', message_object)
