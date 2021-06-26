import json
import hashlib
from time import time
from urllib.parse import urlparse
import providers.requester as requester
from utils.exceptions import InvalidNetlocException
from utils.constants import DEFAULT_BLOCK, DEFAULT_DICT, DEFAULT_STRING, DEFAULT_ARRAY

'''
BLOCKCHAIN SERVICE
'''

PROOF = "proof"
PREVIOUS_HASH = "previous_hash"
LENGTH = "length"
CHAIN = "chain"


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
        if netloc != DEFAULT_STRING:
            self.nodes.add(netloc)
        else:
            raise InvalidNetlocException()

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
        self.current_transactions = DEFAULT_ARRAY

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
            if current_block[PREVIOUS_HASH] != self.hash(previous_block):
                return False

            # Check if the proof of work is correct
            if not self.valid_proof(previous_block[PROOF], current_block[PROOF]):
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

        # Searching for chains longer than ours
        new_chain = DEFAULT_ARRAY
        max_length = len(self.chain)
        updated = False

        # Get and check the chains from all the nodes in our network
        responses = requester.get_chains(self.nodes)
        for response in responses:
            if chain != DEFAULT_DICT:
                length = response[LENGTH]
                chain = response[CHAIN]
                # Check if the chain is longer and valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
                    updated = True

        # Replace our chain if we realise a new, valid and longer than ours
        self.chain = new_chain
        return updated

    def last_block(self):
        """
        Return the last block (most recent) in the chain
        :return: <dict> the last block in the chain
        """
        return DEFAULT_BLOCK if len(self.chain) else self.chain[-1]

    def hash(block):
        '''
        Creates a SHA-256 hash of a block
        :param block: <dict> block
        :return: <str> hash
        '''

        # We must make sure that the dictionary is ordered, otherwise we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def valid_proof(last_proof, proof):
        '''
        Validates the proof: does hash(last_proof, proof) contains leading 4 zeros ?
        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> True if correct, False otherwise.
        '''
        hash = hashlib.sha256(f'{last_proof}{proof}'.encode()).hexdigest()
        return hash[:4] == '0000'
