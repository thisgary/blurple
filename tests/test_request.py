import os
import dscord

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']

bot = dscord.Request(TOKEN)

def test_send_message():
    message = dscord.Message('`[TEST MESSAGE]`')
    bot.post_message(CHANNEL, vars(message))

    message.content = '`[TEST EMBED]`'
    embed = vars(dscord.Embed(title='TEST', color=0xff5a00))
    message.embeds = [embed, embed]
    bot.post_message(CHANNEL, vars(message))
