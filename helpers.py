import hashlib
import hmac
import json
from typing import Any, Dict


def generate_signature(secret: str, payload: Dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True)
    signature = hmac.new(
        secret.encode("utf-8"),
        serialized.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature


def verify_signature(secret: str, payload: Dict[str, Any], signature: str) -> bool:
    expected = generate_signature(secret, payload)
    return hmac.compare_digest(expected, signature)


def sanitize_tx_data(data: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {}
    for key, value in data.items():
        if value is not None:
            if isinstance(value, str):
                cleaned[key] = value.strip()
            else:
                cleaned[key] = value
    return cleaned


def format_wei_to_ether(wei_value: int) -> float:
    if wei_value < 0:
        raise ValueError("Wei value cannot be negative")
    return wei_value / 10**18
