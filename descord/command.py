import json
import requests

cmd = {'list': []}
json.dump(cmd, open('command.json','w'))

def create(name, description, *options):
    cmd_obj = {'name': name, 'description': description, 'options': options}
    cmd = json.load(open('command.json'))
    cmd['list'].append(cmd_obj)
    json.dump(cmd, open('command.json','w'))

def option(opt_type: int, name, description, **optional):
    opt_obj = {'type': opt_type, 'name': name, 'description': description}
    opt_obj.update(optional) # required, choices, options
    return opt_obj

def choice(name, value):
    ch_obj = {'name': name, 'value': value}
    return ch_obj
