import hashlib
import json


def hash_transaction(transaction):
    transaction_string = json.dumps(transaction, sort_keys=True).encode()
    return hashlib.sha256(transaction_string).hexdigest()


def validate_address(address):
    return len(address) == 42 and address.startswith('0x')


def calculate_gas_fee(gas_price, gas_limit):
    return gas_price * gas_limit


def format_transaction_for_broadcast(transaction):
    return {
        'to': transaction['to'],
        'value': transaction['value'],
        'gas': transaction['gas'],
        'gasPrice': transaction['gasPrice'],
        'nonce': transaction['nonce'],
        'data': transaction.get('data', ''),
    }