import hashlib
from functools import lru_cache
from typing import List, Dict
import time

class Core:
    def __init__(self):
        self.chain: List[Dict] = []

    @lru_cache(maxsize=256)
    def _hash_data(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def create_block(self, data: str, previous_hash: str = None) -> Dict:
        if previous_hash is None:
            previous_hash = self.chain[-1]['hash'] if self.chain else '0' * 64
        block_data = data + previous_hash
        block_hash = self._hash_data(block_data)
        block = {
            'data': data,
            'previous_hash': previous_hash,
            'hash': block_hash,
            'timestamp': time.time()
        }
        self.chain.append(block)
        return block

    def validate_blockchain(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current['previous_hash'] != prev['hash']:
                return False
            expected_hash = self._hash_data(current['data'] + current['previous_hash'])
            if current['hash'] != expected_hash:
                return False
        return True

    def get_latest_block(self) -> Dict:
        return self.chain[-1] if self.chain else {}

    def process_transactions(self, transactions: List[str]) -> List[Dict]:
        blocks = []
        prev_hash = self.get_latest_block().get('hash', '0' * 64)
        for transaction in transactions:
            block = self.create_block(transaction, prev_hash)
            blocks.append(block)
            prev_hash = block['hash']
        return blocks