"""
Module responsible by http requests
"""

import threading
import concurrent.futures as executors

import requests
from providers.settings import get_rest_protocol
from utils.constants import DEFAULT_DICT, ENDPOINT_CHAIN, STATUS_OK

PROTOCOL = get_rest_protocol()
results = []
lock = threading.Lock()

"""
Get chains from all nodes neighbours
"""

def get_chain(node):
    response = requests.get(f'{PROTOCOL}://{node}{ENDPOINT_CHAIN}')
    with lock:
        if response.status_code == STATUS_OK:
            results.append(response.json())
        else:
            results.append(DEFAULT_DICT)

def get_chains(nodes):
    with executors.ThreadPoolExecutor(max_workers=len(nodes)) as executor:
        executor.map(get_chain, nodes)        
    return results
