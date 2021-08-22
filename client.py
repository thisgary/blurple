import threading
from typing import Callable, List

import dscord


class Cli:
    def __init__(self, access_token: str):
        self.gate = dscord.Gateway(access_token)
        self.req = dscord.Request(access_token)

    def guild_list(self):
        guilds = [(g['name'], g['id']) for g in self.req.get_guilds().json()]
        s = '\nGUILDS\n'
        for g in guilds:
            s += f'{g[0]} - {g[1]} \n'
        return s

    def listen(self):
        while True:
            inp = input()
            if inp in ['/help', '/h']:
                print('WIP')
            elif inp in ['/quit', '/exit', '/q']:
                print('Exiting..')
                self.gate.stop()
                break

    def start(self):
        print(self.guild_list())
        threading.Thread(target=self.gate.start).start()
        print('Enter /help for more info!')
        self.listen()


client = Cli(input('Bot token: '))


@client.gate.event
async def on_message(p):
    if p.t == 'MESSAGE_CREATE':
        content = p.d['content']
        if content == '': return
        t = p.d['timestamp'].split('T')[1][:8]
        gld_id, chn_id = p.d['guild_id'], p.d['channel_id']
        if gld_id[:3] == chn_id[:3]:
            g, c = f'..{gld_id[-3:]}', f'..{chn_id[-3:]}'
        else:
            g, c = f'{gld_id[:3]}..', f'{chn_id[:3]}..'
        author = p.d['author']
        a = f"{author['username']}#{author['discriminator']}"
        print(f'{t} ({g}, {c}) {a}: {content}')


client.start()
