import os
import descord

bot = descord.Request(os.environ['TOKEN'])

def test_message_create():
    bot.message_create(os.environ['CHANNEL'], '`[TEST MESSAGE]`')

