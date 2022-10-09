"""
Responsible to run this node
"""
from sys import argv as args
from services.server import run_server
from providers.settings import get_api_port, get_api_host, get_node_id

if __name__ == '__main__':
    if len(args) > 1:
        host = args[1]
        port = int(args[2])
        node_id = args[3]
    else:    
        host = get_api_host()
        port = get_api_port()
        node_id = get_node_id()

    run_server(host, port, node_id)
