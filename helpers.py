import hashlib
import re
from typing import Union


def double_sha256(data: bytes) -> str:
    first = hashlib.sha256(data).digest()
    return hashlib.sha256(first).hexdigest()


def wei_to_eth(wei_val: int) -> float:
    return wei_val / 10**18


def eth_to_wei(eth_val: Union[int, float]) -> int:
    return int(eth_val * 10**18)


def is_valid_evm_address(address: str) -> bool:
    return bool(re.match('^0x[0-9a-fA-F]{40}$', address))


def is_valid_tx_hash(tx_hash: str) -> bool:
    return bool(re.match('^0x[0-9a-fA-F]{64}$', tx_hash))
