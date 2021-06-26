"""
Module responsible by http requests
"""

import requests
from providers.settings import get_rest_protocol
from utils.constants import DEFAULT_DICT, ENDPOINT_CHAIN, STATUS_OK

PROTOCOL = get_rest_protocol()

"""
Get chains from all nodes neighbours
"""


def get_chains(nodes):
    results = []
    for node in nodes:
        response = requests.get(f'{PROTOCOL}://{node}{ENDPOINT_CHAIN}')
        if response.status_code == STATUS_OK:
            results.append(response.json())
        else:
            results.append(DEFAULT_DICT)
    return results
