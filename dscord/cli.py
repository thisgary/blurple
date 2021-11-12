from getpass import getpass
import sys
import threading
from typing import List, Tuple

import dscord

help_general = '''
Dscord Cli Client
A cursed cli bot client for Discord, it is by chance illegal.

[COMMANDS]
/channels - list text channels in a guilds by partial guild ids.
/send - send messages to a channel, to last active channel by default.
/quit - you know... (;-;)
'''

help_send = '''
/send
[DESCRIPTION]
Send message to a channel, to last active channel by default.

[ALIASES] 
s, say, send

[FLAGS]
-l {n}
Set the scope to last n + 1 th active channel.

-c {x}
Set the scope by first/last n th length of channel ids.
'''

cmds = {
        'help': ['help', 'h'],
        'send': ['send', 'say', 's'],
        'quit': ['quit', 'q', 'exit'],
        'chns': ['channels', 'chns', 'cs']
}

flgs = {
        'send': ['-l', '-c']
}

usage = {
        'send': '[USAGE] /s {?flag} {?arg} {context}',
        'chns': '[USAGE] /cs {guild_id_part}',
}

cache_guilds = cache_history = []


def match_part(x: str, ys: List[Tuple[str, str]]) -> List[str]:
    ms = []
    i = len(x) - 2
    for y in ys:
        if ((x[:2] == '..' and y[1][-i:] == x[2:]) or
                (x[-2:] == '..' and y[1][:i] == x[:-2])):
            ms.append(y)
    return ms


def read_list(header: str, xs: List[str], *, 
        f = None) -> str:
    txt = '\n' + header + '\n'
    if f:
        xs = [f(x) for x in xs]
    for x in xs:
        txt += (x + '\n')
    return txt

class Cli:
    def __init__(self, access_token: str) -> None:
        self.gate = dscord.Gateway(access_token, debug=True)
        self.req = dscord.Request(access_token)

    def start(self) -> None:
        threading.Thread(target=self.gate.start).start()
        self.read_guilds()
        print('Enter /help for more info!')
        self.listen()

    def read_guilds(self):
        guilds = self.req.get_guilds().json()
        gs = [(g['name'], g['id']) for g in guilds]
        f = lambda g : f'{g[0]} - {g[1]}'
        print(read_list('[GUILDS]', gs, f=f))

    def read_channels(self, gld_id: str, *, h: str = None):
        channels = self.req.get_channels(gld_id).json()
        cs = [(c['name'], c['id']) for c in channels]
        f = lambda c : f'{c[0]} - {c[1]}'
        if not h: h = 'channels'
        print(read_list(f'[{h.upper()}]', cs, f=f))

    def listen(self) -> None:
        while True:
            user_input = input()
            if user_input[0] != '/': continue
            args = user_input[1:].split(' ')
            cmd = args.pop(0).lower()
            if cmd in cmds['help']:
                print(help_general)
            elif cmd in cmds['send']:
                self.command_send(args)
            elif cmd in cmds['chns']:
                if len(args) < 1: 
                    print(usage['chns'])
                    continue
                arg = args.pop(0)
                global cache_guilds
                if not cache_guilds:
                    cache_guilds = self.req.get_guilds().json()
                glds = [(g['name'], g['id']) for g in cache_guilds]
                res = match_part(arg, glds)
                if res:
                    r = len(res)
                    if r == 1:
                        self.read_channels(res[0][1], h=res[0][0])
                    elif r > 1:
                        f = lambda g : f'{g[0]} - {g[1]}'
                        read_list('[POSSIBLITY]', res, f=f)
                else:
                    print('[NO MATCH]')
            elif cmd in cmds['quit']:
                sys.exit()

    def command_send(self, args: List[str]) -> tuple:
        if len(args) < 1:
            print(usage['send'])
            return
        if args[0] in flgs['send']:
            flag = args.pop(0)[1:]
            if flag == 'l':
                h = len(cache_history)
                if h == 0:
                    print('[NO HISTORY]')
                    return
                elif h == 1:
                    pos = 0
                elif h > 1:
                    if args[0].isnumeric():
                        p = abs(int(args.pop(0))) + 1
                        pos = -p if h < p else 0
                    else:
                        pos = -2
                    if len(args) < 1:
                        print(usage['send'])
                        return
        else:
            if cache_history:
                pos = -1
            else:
                print('[NO HISTORY]')
                return
        chn_id = cache_history[pos][1]
        msg = vars(dscord.Message(' '.join(args)))
        self.req.post_message(chn_id, msg)


client = Cli(sys.argv[1])


@client.gate.event
async def on_message(p):
    if p.t == 'MESSAGE_CREATE':
        content = p.d['content']
        if content == '': return
        t = p.d['timestamp'].split('T')[1][:8]
        scope = (p.d['guild_id'], p.d['channel_id'])
        global cache_history
        if scope in cache_history:
            cache_history.remove(scope)
        cache_history.append(scope)
        if scope[0][:3] == scope[1][:3]:
            s = f'(..{scope[0][-3:]}, ..{scope[1][-3:]})'
        else:
            s = f'({scope[0][:3]}.., {scope[1][:3]}..)'
        author = p.d['author']
        a = f"{author['username']}#{author['discriminator']}"
        print(f'{t} {s} {a}: {content}')

client.start()
