"""
Module responsible by constants defined in settings
"""

from uuid import uuid4
from configparser import ConfigParser
from utils.constants import SETTINGS_FILE, SETTINGS_HOST, SETTINGS_PORT, SETTINGS_REST, \
    SETTINGS_PROTOCOL, SETTINGS_ATTRIBUTES, SETTINGS_NODE_ID

settings = ConfigParser()
settings.read(SETTINGS_FILE)


def get_rest_protocol():
    return settings[SETTINGS_REST][SETTINGS_PROTOCOL]


def get_node_id():
    settings_node_id = settings[SETTINGS_ATTRIBUTES][SETTINGS_NODE_ID]

    if settings_node_id:
        return settings_node_id
    else:
        return str(uuid4()).replace('-', '')


def get_api_host():
    return settings[SETTINGS_REST][SETTINGS_HOST]


def get_api_port():
    return int(settings[SETTINGS_REST][SETTINGS_PORT])
