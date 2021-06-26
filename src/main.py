"""
Responsible to run this node
"""
from services.server import run_server
from providers.settings import get_api_port, get_api_host

if __name__ == '__main__':
    host = get_api_host()
    port = get_api_port()
    run_server(host, port)
