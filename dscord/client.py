from getpass import getpass
import sys
import threading
from typing import Callable, List

import dscord

history = []


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
        for char in sys.stdin.read():
            global stdin
            stdin += char
            print(stdin)
#            if line[0] != '/': continue
#            cmd, *tail = line[1:].split(' ')
#            if cmd in ['help', 'h']:
#                print('[KYS]')
#            elif cmd in ['send', 's']:
#                if tail[0][0] == '-':
#                    flag, arg, *tail = tail
#                    if flag == '-l' and arg.isnumeric():
#                        pos = 0 - (int(arg) + 1)
#                        scope = history[pos]
#                else:
#                    scope = history[-1]
#                msg = vars(dscord.Message(' '.join(tail)))
#                self.req.post_message(scope[1], msg)
#            elif cmd in ['quit', 'exit', 'q']:
#                print('Quitting..')
#                self.gate.stop()
#                break

    def start(self):
        print(self.guild_list())
        threading.Thread(target=self.gate.start).start()
        print('Enter /help for more info!')
        self.listen()


client = Cli(getpass('Bot token: '))


@client.gate.event
async def on_message(p):
    if p.t == 'MESSAGE_CREATE':
        content = p.d['content']
        if content == '': return
        t = p.d['timestamp'].split('T')[1][:8]
        scope = (p.d['guild_id'], p.d['channel_id'])
        global history
        if scope in history:
            history.remove(scope)
        history.append(scope)
        if scope[0][:3] == scope[1][:3]:
            s = f'(..{scope[0][-3:]}, ..{scope[1][-3:]})'
        else:
            s = f'({scope[0][:3]}.., {scope[1][:3]}..)'
        author = p.d['author']
        a = f"{author['username']}#{author['discriminator']}"
        print(f'{t} {s} {a}: {content}')


client.start()
