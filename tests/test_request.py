import os
import dscord

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']

bot = dscord.Request(TOKEN)

def test_message_create():
    bot.message_create(CHANNEL, '`[TEST MESSAGE]`')

def test_message_create_embed():
    embed = dscord.Embed(title='TEST', color=0xff5a00)
    bot.message_create(CHANNEL, '`[TEST EMBED]`', embed=embed.__dict__)
