import os
import dscord

bot = dscord.Request(os.environ['TOKEN'])

def test_message_create():
    bot.message_create(os.environ['CHANNEL'], '`[TEST MESSAGE]`')

