"""
Parse configuration file
"""
import json

def parse(config_file, key):
    config_name = str(key)
    conf = json.load(open(config_file))[config_name]
    return conf


