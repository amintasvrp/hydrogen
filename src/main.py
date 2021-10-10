"""
Responsible to run this node
"""
from sys import argv as args
from services.server import run_server
from providers.settings import get_api_port, get_api_host

if __name__ == '__main__':
    if len(args) > 1:
        host = args[1]
        port = int(args[2])
    else:    
        host = get_api_host()
        port = get_api_port()
    
    run_server(host, port)
