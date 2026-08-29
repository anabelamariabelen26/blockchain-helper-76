import hashlib
import json
from functools import lru_cache

class BlockchainCore:
    def __init__(self):
        self.chain = []
        self.pending = []
        self.create_genesis()

    def create_genesis(self):
        block = {
            'index': 1,
            'transactions': [],
            'proof': 1,
            'previous_hash': '0' * 64
        }
        self.chain.append(block)

    def add_transaction(self, sender, recipient, amount):
        self.pending.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    def create_block(self, proof):
        previous_hash = self.hash(self.chain[-1])
        block = {
            'index': len(self.chain) + 1,
            'transactions': self.pending,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        self.pending = []
        return block

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        return self._cached_hash(block_string)

    @lru_cache(maxsize=128)
    def _cached_hash(self, block_string):
        return hashlib.sha256(block_string.encode()).hexdigest()

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            if not self.proof_of_work(previous_block['proof'], current_block['proof']):
                return False
        return True

    def proof_of_work(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'