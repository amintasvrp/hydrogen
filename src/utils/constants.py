"""
Default Constants
"""

DEFAULT_NUMBER = 0

DEFAULT_STRING = ""

DEFAULT_ARRAY = []

DEFAULT_DICT = {}

DEFAULT_NODE_ID = "0"

DEFAULT_BLOCK = {
    'index': DEFAULT_NUMBER,
    'timestamp': DEFAULT_NUMBER,
    'transactions': DEFAULT_ARRAY,
    'proof': DEFAULT_NUMBER,
    'previous_hash': DEFAULT_STRING
}

"""
Endpoints Constants
"""

ENDPOINT_CHAIN = "/chain"
ENDPOINT_MINE = "/mine"
ENDPOINT_TRANSACTIONS = "/transactions/new"

ENDPOINT_NODES = "/nodes"
ENDPOINT_NODES_REGISTER = f"{ENDPOINT_NODES}/register"
ENDPOINT_NODES_RESOLVE = f"{ENDPOINT_NODES}/resolve"

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_BAD_REQUEST = 400
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404

"""
Files Constants
"""

SETTINGS_FILE = "settings.ini"

SETTINGS_REST = "REST"
SETTINGS_PROTOCOL = "PROTOCOL"
SETTINGS_HOST = "HOST"
SETTINGS_PORT = "PORT"

SETTINGS_ATTRIBUTES = "ATTRIBUTES"
SETTINGS_NODE_ID = "NODE_ID"

"""
Messages Constants
"""

MESSAGE_TRANSACTIONS_NOT_FOUND = "No transactions found"
MESSAGE_BLOCK_FORGED = "New block forged"
MESSAGE_MISSING_VALUES = "Some values are missing"
MESSAGE_INVALID_NODES = "Invalid list of nodes"
MESSAGE_ADD_NODES = "New nodes have been added"
MESSAGE_CHAIN_UPDATED = "Our chain was replaced"
MESSAGE_CHAIN_NOT_UPDATED = "Our chain is authoritative"


def MESSAGE_ADD_TRANSACTION(block_index):
    return f"Transaction will be added to block {block_index}"
