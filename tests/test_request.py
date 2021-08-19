import os
import dscord

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']

bot = dscord.Request(TOKEN)
message = dscord.Message('`[TEST MESSAGE]`')

def test_send_message():
    bot.send_message(CHANNEL, message.__dict__)

    embed = dscord.Embed(title='TEST', color=0xff5a00).__dict__
    message.embeds = [embed, embed]
    bot.send_message(CHANNEL, '`[TEST EMBED]`', message.__dict__)
