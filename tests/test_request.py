import os
import blurple

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']

bot = blurple.Request(TOKEN)

def test_send_message():
    message = blurple.Message('`[TEST MESSAGE]`')
    bot.post_message(CHANNEL, vars(message))

    message.content = '`[TEST EMBED]`'
    embed = vars(blurple.Embed(title='TEST', color=0x5865f2))
    message.embeds = [embed, embed]
    bot.post_message(CHANNEL, vars(message))
