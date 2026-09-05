import hashlib
import hmac
import json
from typing import Any, Dict

def calculate_sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def generate_hmac_signature(secret: str, message: str) -> str:
    return hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def format_payload(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def validate_checksum(data: str, expected_hash: str) -> bool:
    return hmac.compare_digest(calculate_sha256(data), expected_hash)

def parse_hex(hex_string: str) -> bytes:
    return bytes.fromhex(hex_string.lstrip('0x'))

def to_wei(amount: float, decimals: int = 18) -> int:
    return int(amount * (10**decimals))