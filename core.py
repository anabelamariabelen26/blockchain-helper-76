import hashlib
import json
import time
from typing import Any, Dict, List

def hash_data(data: Dict[str, Any]) -> str:
    json_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(json_str.encode()).hexdigest()

def validate_address(address: str) -> bool:
    if len(address) != 42 or not address.startswith('0x'):
        return False
    try:
        int(address[2:], 16)
        return True
    except ValueError:
        return False

def to_wei(ether: float) -> int:
    return int(ether * 10 ** 18)

def from_wei(wei: int) -> float:
    return wei / 10 ** 18

def create_transaction(sender: str, recipient: str, amount: float, gas: int = 21000) -> Dict[str, Any]:
    tx = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        'gas': gas,
        'timestamp': int(time.time())
    }
    tx['hash'] = hash_data(tx)
    return tx

def verify_transaction(tx: Dict[str, Any]) -> bool:
    if 'hash' not in tx:
        return False
    original_hash = tx['hash']
    tx_copy = {k: v for k, v in tx.items() if k != 'hash'}
    computed_hash = hash_data(tx_copy)
    return original_hash == computed_hash

def mine_block(previous_hash: str, transactions: List[Dict[str, Any]], difficulty: int = 4) -> Dict[str, Any]:
    block = {
        'previous_hash': previous_hash,
        'transactions': transactions,
        'timestamp': int(time.time()),
        'nonce': 0
    }
    while True:
        block_without_hash = {k: v for k, v in block.items() if k != 'hash'}
        block['hash'] = hash_data(block_without_hash)
        if block['hash'].startswith('0' * difficulty):
            return block
        block['nonce'] += 1