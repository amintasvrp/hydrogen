from flask import Flask, jsonify, request
from providers.settings import get_node_id
from controllers.blockchain import Blockchain
from utils.constants import DEFAULT_NODE_ID, ENDPOINT_CHAIN, ENDPOINT_MINE, ENDPOINT_NODES, ENDPOINT_NODES_REGISTER, \
    ENDPOINT_NODES_RESOLVE, ENDPOINT_TRANSACTIONS, MESSAGE_ADD_NODES, MESSAGE_ADD_TRANSACTION, MESSAGE_BLOCK_FORGED, MESSAGE_CHAIN_NOT_UPDATED, MESSAGE_CHAIN_UPDATED, MESSAGE_INVALID_NODES, \
    MESSAGE_MISSING_VALUES, MESSAGE_TRANSACTIONS_NOT_FOUND, STATUS_BAD_REQUEST, STATUS_CREATED, \
    STATUS_NOT_FOUND, STATUS_OK

'''
API REST
'''

PROOF = "proof"
INDEX = "index"
TRANSACTIONS = "transactions"
PREVIOUS_HASH = "previous_hash"

SENDER = "sender"
RECIPIENT = "recipient"
AMOUNT = "amount"
NODES = "nodes"

# Instantiate our node
app = Flask(__name__)

# Generate a globally unique address for this node
NODE_ID = get_node_id()

# Instantiate blockchain
blockchain = Blockchain()


# Mine a new block

@app.route(ENDPOINT_MINE, methods=['GET'])
def mine():
    height = len(blockchain.current_transactions)
    if not height:
        response = {
            'message': MESSAGE_TRANSACTIONS_NOT_FOUND
        }
        return response, STATUS_NOT_FOUND

    # We run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block()
    proof = blockchain.proof_of_work(last_block[PROOF])

    # We must recieve a reward for find the proof.
    # The sender "0" to means that this node has mined a new coin

    blockchain.new_transaction(
        sender=DEFAULT_NODE_ID,
        recipient=NODE_ID,
        amount=height
    )

    # Forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        "message": MESSAGE_BLOCK_FORGED,
        "index": block[INDEX],
        "transactions": block[TRANSACTIONS],
        "proof": block[PROOF],
        "previous_hash": block[PREVIOUS_HASH]
    }

    return jsonify(response), STATUS_OK


# Create a new transaction to a block


@app.route(ENDPOINT_TRANSACTIONS, methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in request data
    required = [SENDER, RECIPIENT, AMOUNT]
    if not all(attribute in values for attribute in required):
        response = {
            'message': MESSAGE_MISSING_VALUES
        }
        return response, STATUS_BAD_REQUEST

    # Creating a new transaction
    index = blockchain.new_transaction(
        values[SENDER], values[RECIPIENT], values[AMOUNT]
    )

    response = {
        'message': MESSAGE_ADD_TRANSACTION(index)
    }
    return jsonify(response), STATUS_CREATED


# Return the full Blockchain


@app.route(ENDPOINT_CHAIN, methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), STATUS_OK


# Return the network nodes set


@app.route(ENDPOINT_NODES, methods=['GET'])
def get_nodes():
    response = {
        'nodes': list(blockchain.nodes),
        'length': len(blockchain.nodes)
    }
    return jsonify(response), STATUS_OK


# Register networks nodes to this node
# Needed to run consensus algorithim


@app.route(ENDPOINT_NODES_REGISTER, methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values['nodes']
    if not nodes:
        response = {
            'message': MESSAGE_INVALID_NODES
        }
        return jsonify(response), STATUS_BAD_REQUEST

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': MESSAGE_ADD_NODES,
        'nodes': list(blockchain.nodes)
    }
    return jsonify(response), STATUS_CREATED


@app.route(ENDPOINT_NODES_RESOLVE, methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conficts()

    if replaced:
        response = {
            'message': MESSAGE_CHAIN_UPDATED,
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': MESSAGE_CHAIN_NOT_UPDATED,
            'chain': blockchain.chain
        }

    return jsonify(response), STATUS_OK


# Run API
def run_server(host, port):
    app.run(host=host, port=port)
