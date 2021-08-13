import os
import dscord

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']

bot = dscord.Request(TOKEN)

def test_message_create():
    bot.message_create(CHANNEL, '`[TEST MESSAGE]`')

def test_embed_message():
    embed = dscord.Embed(title='TEST')
    bot.message_create(CHANNEL, '`[TEST EMBED]`', embed=embed)
