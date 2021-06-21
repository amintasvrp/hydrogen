import json
import hashlib
import requests
from time import time
from uuid import uuid4
from urllib.parse import urlparse

from textwrap import dedent
from flask import Flask, jsonify, request
from werkzeug.wrappers import response


'''
BLOCKCHAIN SERVICE
'''

DEFAULT_BLOCK = {
    'index': 0,
    'timestamp': 0,
    'transactions': [],
    'proof': 0,
    'previous_hash': ""
}


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

    def register_node(self, address):
        '''
        Add a new node to the set of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: <str> Node netloc (IP:Port)
        '''

        parsed_url = urlparse(address)
        netloc = parsed_url.netloc
        if netloc != "":
            self.nodes.add(netloc)

        return parsed_url.netloc

    def new_block(self, proof, previous_hash=None):
        '''
        Create a new block in blockchain
        :param proof: <int> The proof given by the 'proof of work' algorithm
        :param previous_hash: (Optional) <str> hash of previous block
        :return: <dict> New block
        '''
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        '''
        Creates a new transaction to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount
        :return: <int> The index of the block tha will hold this transaction
        '''

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        '''
        Simples proof of work algorithm:
        - p1 is the previous proof and p2 is the new proof
        - Find a number p2 such that hash(p1p2) contains leading 4 zeros (0000)
        :param last_proof: <int> previous proof
        :return: <int> new proof
        '''

        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1

        return proof

    def valid_chain(self, chain):
        '''
        Validate chain
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        '''
        previous_index = 0
        current_index = 1
        chain_size = len(self.chain)
        while current_index < chain_size:
            previous_block = chain[previous_index]
            current_block = chain[current_index]

            # Check if the hash of the block is correct
            if current_block['previous_hash'] != self.hash(previous_block):
                return False

            # Check if the proof of work is correct
            if not self.valid_proof(previous_block['proof'], current_block['proof']):
                return False

            previous_index += 1
            current_index += 1

        return True

    def resolve_conficts(self):
        '''
        This is our Consensus Algorithm. It resolves conficts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        '''

        neighbours = self.nodes
        new_chain = None

        # Searching for chains longer than ours
        max_length = len(self.chain)

        # Get and check the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the chain is longer and valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we realise a new, valid and longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    @property
    def last_block(self):
        if len(self.chain):
            return self.chain[-1]
        return DEFAULT_BLOCK

    @staticmethod
    def hash(block):
        '''
        Creates a SHA-256 hash of a block
        :param block: <dict> block
        :return: <str> hash
        '''

        # We must make sure that the dictionary is ordered, otherwise we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        Validates the proof: does hash(last_proof, proof) contains leading 4 zeros ?
        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> True if correct, False otherwise.
        '''
        hash = hashlib.sha256(f'{last_proof}{proof}'.encode()).hexdigest()
        return hash[:4] == '0000'


'''
API
'''

# Instantiate our node
app = Flask(__name__)

# Generate a globally unique address for this node
node_id = str(uuid4()).replace('-', '')

# Instantiate blockchain
blockchain = Blockchain()


# Mine a new block

@app.route('/mine', methods=['GET'])
def mine():
    if not len(blockchain.current_transactions):
        response = {
            'message': 'No transactions found'
        }
        return response, 404

    # We run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])

    # We must recieve a reward for find the proof.
    # The sender "0" to means that this node has mined a new coin

    blockchain.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1
    )

    # Forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        "message": "New block forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]
    }

    return jsonify(response), 200


# Create a new transaction to a block


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in request data
    required = ['sender', 'recipient', 'amount']
    if not all(attribute in values for attribute in required):
        response = {
            'message': 'Missing values'
        }
        return response, 400

    # Creating a new transaction
    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount']
    )

    response = {
        'message': f'Transaction will be added to block {index}'
    }
    return jsonify(response), 201


# Return the full Blockchain


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values['nodes']
    if not nodes:
        response = {
            'message': 'Invalid list of nodes'
        }
        return jsonify(response), 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conficts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


# Run API
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
