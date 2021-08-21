import asyncio
from typing import Callable, List

import dscord

TOKEN = input("Bot Token: ")

gateway = dscord.Gateway(TOKEN)
request = dscord.Request(TOKEN)


def guild_list() -> List[dict]:
    return [d for d in request.get_guilds().json()]


def scope(header: str, dicts: List[dict]) -> str:
    s, i = '\n' + header + '\n', 0
    for d in dicts:
        s += f"[{i}] {d['name']} ({d['id']}) \n"
        i += 1
    return s


@gateway.event
async def message_create(p):
    if p.t == 'MESSAGE_CREATE':
        content = p.d['content']
        if content == '': return
        author, timestamp = p.d['author'], p.d['timestamp']
        g, c = p.d['guild_id'][:3], p.d['channel_id'][:3]
        t = timestamp.split('T')[1][:8]
        a = f"{author['username']}#{author['discriminator']}"
        print(f'{t} ({g}..,{c}..) {a}: {content}')


print(scope("Guilds: ", guild_list()))

gateway.start()
