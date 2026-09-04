import hashlib
import json
from typing import Dict, Any, Optional

class BlockchainHelper:
    def __init__(self, chain_id: int = 1):
        self.chain_id = chain_id

    @staticmethod
    def generate_keccak256(data: bytes) -> str:
        sha = hashlib.sha3_256()
        sha.update(data)
        return f'0x{sha.hexdigest()}'

    def prepare_transaction(self, nonce: int, to_address: str, value_wei: int, gas_limit: int, gas_price_gwei: int, data: Optional[str] = None) -> Dict[str, Any]:
        if not to_address.startswith('0x') or len(to_address) != 42:
            raise ValueError('Invalid recipient address format')
        
        return {
            'chainId': self.chain_id,
            'nonce': nonce,
            'to': to_address.lower(),
            'value': value_wei,
            'gas': gas_limit,
            'gasPrice': gas_price_gwei * (10**9),
            'data': data or '0x'
        }

    def hash_transaction(self, tx: Dict[str, Any]) -> str:
        serialized = json.dumps(tx, sort_keys=True).encode('utf-8')
        return self.generate_keccak256(serialized)