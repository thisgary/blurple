import dscord

TOKEN = input("Bot Token: ")
client = dscord.Gateway(TOKEN)


@client.event
async def message_create(p: dict):
    if p.t == 'MESSAGE_CREATE':
        a, c, t = p.d['author'], p.d['content'], p.d['timestamp']
        if c == '': return
        time = t.split('T')[1][:8]
        author = f"{a['username']}#{a['discriminator']}"
        print(f'{time} {author}: {c}')


client.start()
