from typing import Dict, Any, Optional
class BlockchainError(Exception):
    pass

class InsufficientFundsError(BlockchainError):
    def __init__(self, address: str, required: float, available: float) -> None:
        self.address = address
        self.required = required
        self.available = available
        super().__init__(f"Insufficient funds for {address}: required {required}, available {available}")

class InvalidAddressError(BlockchainError):
    def __init__(self, address: str, reason: str) -> None:
        self.address = address
        self.reason = reason
        super().__init__(f"Invalid address {address}: {reason}")

class NetworkError(BlockchainError):
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint
        super().__init__(f"Network error at {endpoint}")

def validate_address(address: str) -> None:
    if not address or len(address) < 20:
        raise InvalidAddressError(address or "", "Address format invalid")
    if not address.startswith("0x"):
        raise InvalidAddressError(address, "Must start with 0x")

def check_funds(address: str, amount: float, balances: Dict[str, float]) -> None:
    if address not in balances or balances[address] < amount:
        raise InsufficientFundsError(address, amount, balances.get(address, 0))

def handle_transfer(sender: str, recipient: str, amount: float, balances: Dict[str, float]) -> Dict[str, Any]:
    try:
        validate_address(sender)
        validate_address(recipient)
        if amount <= 0:
            raise BlockchainError("Amount must be positive")
        check_funds(sender, amount, balances)
        updated = dict(balances)
        updated[sender] -= amount
        updated[recipient] = updated.get(recipient, 0) + amount
        return {"success": True, "balances": updated}
    except BlockchainError as e:
        return {"success": False, "error": str(e)}

def handle_network(endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    try:
        if not endpoint.startswith("https://"):
            raise NetworkError(endpoint)
        if data and data.get("fail"):
            raise NetworkError(endpoint)
        return {"success": True, "endpoint": endpoint}
    except BlockchainError as e:
        return {"success": False, "error": str(e)}

def process_edge_case(op: str, params: Dict[str, Any]) -> Dict[str, Any]:
    if op == "transfer":
        return handle_transfer(
            params.get("sender", ""),
            params.get("recipient", ""),
            params.get("amount", 0),
            params.get("balances", {})
        )
    elif op == "network":
        return handle_network(
            params.get("endpoint", ""),
            params.get("data")
        )
    return {"success": False, "error": "Invalid operation"}