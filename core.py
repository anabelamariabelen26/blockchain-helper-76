import hashlib
from functools import lru_cache
from typing import List, Dict, Any


class BlockProcessor:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.target = "0" * difficulty

    @lru_cache(maxsize=1024)
    def calculate_hash(self, block_data: str) -> str:
        return hashlib.sha256(block_data.encode("utf-8")).hexdigest()

    def batch_process_transactions(self, transactions: List[Dict[str, Any]]) -> List[str]:
        processed_hashes = []
        for tx in transactions:
            tx_string = f"{tx.get('sender')}:{tx.get('recipient')}:{tx.get('amount')}:{tx.get('nonce')}"
            tx_hash = self.calculate_hash(tx_string)
            processed_hashes.append(tx_hash)
        return processed_hashes

    def verify_proof_of_work(self, block_header: str, nonce: int) -> bool:
        candidate = f"{block_header}:{nonce}"
        block_hash = self.calculate_hash(candidate)
        return block_hash.startswith(self.target)

    def find_nonce(self, block_header: str, max_iterations: int = 1000000) -> int:
        for nonce in range(max_iterations):
            if self.verify_proof_of_work(block_header, nonce):
                return nonce
        return -1
