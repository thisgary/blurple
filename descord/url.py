usr = '/users'
gld = '/guilds'
chn = '/channels'
msg = '/messages'

def me():
    return usr + '/@me'

def user(usr_id):
    return usr + '/' + str(usr_id)

def dms():
    return me() + chn

def guilds():
    return me() + gld

def guild(gld_id):
    return gld + '/' + str(gld_id)

def channels(gld_id):
    return guild(gld_id) + Url.chn

def channel(chn_id):
    return chn + '/' + str(chn_id)

def messages(chn_id):
    return channel(chn_id) + Url.msg

def message(chn_id, msg_id):
    return messages(chn_id) + '/' + str(msg_id)


