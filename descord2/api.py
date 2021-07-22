import requests


class Url:
    usr = '/users'
    gld = '/guilds'
    chn = '/channels'
    msg = '/messages'

    @staticmethod
    def me(self):
        return usr + '/@me'

    @staticmethod
    def to_user(self, usr_id):
        return usr + '/' + str(usr_id)

    @staticmethod
    def to_dms(self):
        return Url.me() + chn

    @staticmethod
    def to_guilds(self):
        return Url.me() + gld

    @staticmethod
    def to_guild(self, gld_id):
        return gld + '/' + str(gld_id)

    @staticmethod
    def to_channels(self, gld_id):
        return Url.guild(gld_id) + chn

    @staticmethod
    def to_channel(self, chn_id):
        return chn + '/' + str(chn_id)

    @staticmethod
    def to_messages(self, chn_id):
        return Url.channel(chn_id) + msg

    @staticmethod
    def to_message(self, chn_id, msg_id):
        return Url.messages(chn_id) + '/' + str(msg_id)


class Access:
    def __init__(self, access_token, *, is_bot=True, api_version=9):
        auth_prefix = 'Bot' if is_bot else 'Bearer'
        self.auth = {'Authorization': f'{auth_prefix} {access_token.strip()}'}
        self.url = f'https://discord.com/api/v{api_version}'

    def get(self, path, obj=None):
        return requests.get(self.url+path, headers=self.auth, params=obj)

    def get_me(self):
        return self.get(Url.me())

    def get_user(self, user_id):
        return self.get(Url.user(user_id))

    def get_guilds(self):
        return self.get(Url.guilds())

    def get_guild(self, gld_id):
        return self.get(Url.guild(gld_id))

    def get_channels(self, gld_id):
        return self.get(Url.channels(gld_id))

    def get_channel(self, chn_id):
        return self.get(Url.channel(chn_id))

    def get_messages(self, chn_id, hx_obj=None):
        return self.get(Url.messages(chn_id), hx_obj)

    def get_message(self, chn_id, msg_id):
        return self.get(Url.message(chn_id, msg_id))

    def post(self, path, obj):
        return requests.post(self.url+path, headers=self.auth, json=obj)

    def create_dm(self, user_id):
        dm_obj = {'recipient_id': user_id}
        return self.post(Url.to_dms(), dm_obj)

    def create_guild(name, **kwargs):
        guild_obj = {'name': name}
        guild_obj.update(kwargs)
        return self.post(Url.gld, guild_obj)

    def create_channel(self, gld_id, chn_name, **kwargs):
        chn_obj = {'name': chn_name}
        chn_obj.update(kwargs)
        return self.post(Url.channels(gld_id), chn_obj)

    def create_message(self, chn_id, msg_con, **kwargs):
        msg_obj = {'content': msg_con}
        chn_obj.update(kwargs)
        return self.post(Url.messages(chn_id), msg_obj)

