import hashlib
import json
from typing import Dict, List, Any

class BlockchainError(Exception):
    pass
class InvalidAddressError(BlockchainError):
    pass
class InvalidAmountError(BlockchainError):
    pass
class InsufficientBalanceError(BlockchainError):
    pass
class EmptyTransactionPoolError(BlockchainError):
    pass

def is_valid_address(address: str) -> bool:
    if not isinstance(address, str):
        return False
    if len(address) != 42:
        return False
    if not address.startswith("0x"):
        return False
    try:
        int(address[2:], 16)
    except ValueError:
        return False
    return True

def compute_hash(data: Dict[str, Any]) -> str:
    encoded = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()

class CryptoCore:
    def __init__(self) -> None:
        self.chain: List[Dict[str, Any]] = []
        self.balances: Dict[str, int] = {}
        self.pending: List[Dict[str, Any]] = []

    def add_transaction(self, sender: str, recipient: str, amount: int) -> bool:
        if not is_valid_address(sender):
            raise InvalidAddressError("Invalid sender address")
        if not is_valid_address(recipient):
            raise InvalidAddressError("Invalid recipient address")
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        current_balance = self.balances.get(sender, 0)
        if current_balance < amount:
            raise InsufficientBalanceError("Insufficient balance for transaction")
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }
        self.pending.append(transaction)
        self.balances[sender] = current_balance - amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount
        return True

    def mine_pending_transactions(self) -> Dict[str, Any]:
        if not self.pending:
            raise EmptyTransactionPoolError("No pending transactions to mine")
        block = {
            "index": len(self.chain) + 1,
            "transactions": self.pending[:],
            "previous_hash": self.chain[-1]["hash"] if self.chain else "0" * 64,
            "hash": ""
        }
        block["hash"] = compute_hash(block)
        self.chain.append(block)
        self.pending = []
        return block

    def get_balance(self, address: str) -> int:
        if not is_valid_address(address):
            raise InvalidAddressError("Invalid address")
        return self.balances.get(address, 0)

    def get_chain(self) -> List[Dict[str, Any]]:
        return self.chain