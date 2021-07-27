import os
import descord

bot = descord.Request(os.environ['TOKEN'])

def test_create_message():
    bot.create_message(os.environ['CHANNEL'], '`[TEST MESSAGE]`')

