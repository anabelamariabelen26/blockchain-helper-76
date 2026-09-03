import re

EVM_ADDRESS_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")
TX_HASH_PATTERN = re.compile(r"^0x[a-fA-F0-9]{64}$")
PRIVATE_KEY_PATTERN = re.compile(r"^(0x)?[a-fA-F0-9]{64}$")


class ValidationError(ValueError):
    """Raised when a cryptographic input fails validation."""


def validate_evm_address(address: str) -> str:
    if not isinstance(address, str):
        raise ValidationError("Address must be a string")
    clean_address = address.strip()
    if not EVM_ADDRESS_PATTERN.match(clean_address):
        raise ValidationError(f"Invalid EVM address format: {address}")
    return clean_address


def validate_tx_hash(tx_hash: str) -> str:
    if not isinstance(tx_hash, str):
        raise ValidationError("Transaction hash must be a string")
    clean_hash = tx_hash.strip()
    if not TX_HASH_PATTERN.match(clean_hash):
        raise ValidationError(f"Invalid transaction hash format: {tx_hash}")
    return clean_hash


def validate_private_key(private_key: str) -> str:
    if not isinstance(private_key, str):
        raise ValidationError("Private key must be a string")
    clean_key = private_key.strip()
    if not PRIVATE_KEY_PATTERN.match(clean_key):
        raise ValidationError("Invalid private key format")
    return clean_key
