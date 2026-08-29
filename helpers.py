import hashlib
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_string(self):
        return f"{self.sender}{self.recipient}{self.amount}"

class BlockchainHelper:
    def __init__(self):
        pass

    @lru_cache(maxsize=512)
    def calculate_block_hash(self, index, previous_hash, transactions_str, timestamp):
        block_string = f"{index}{previous_hash}{transactions_str}{timestamp}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def process_transactions_batch(self, transactions):
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(self.validate_tx, tx) for tx in transactions]
            validated = []
            for future in as_completed(futures):
                result = future.result()
                if result:
                    validated.append(result)
            return validated

    def validate_tx(self, tx):
        if not isinstance(tx, Transaction):
            return None
        if tx.amount > 0 and len(tx.sender) > 0:
            return tx
        return None

    def optimize_chain_validation(self, chain):
        previous_hash = '0'
        for block in chain:
            if block.get('previous_hash') != previous_hash:
                return False
            tx_str = ''.join([t.to_string() for t in block.get('transactions', [])])
            computed = self.calculate_block_hash(
                block.get('index', 0),
                block.get('previous_hash', ''),
                tx_str,
                block.get('timestamp', 0)
            )
            if computed != block.get('hash'):
                return False
            previous_hash = block.get('hash')
        return True

    def get_block_by_hash(self, chain, hash_value):
        hash_map = {b.get('hash'): b for b in chain}
        return hash_map.get(hash_value)