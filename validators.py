from typing import Dict, Any, Optional


class ValidationError(Exception):
    pass


def validate_transaction(tx: Dict[str, Any]) -> Optional[str]:
    required_fields = {'sender', 'recipient', 'amount', 'nonce'}
    
    if not isinstance(tx, dict):
        raise ValidationError("Transaction payload must be a dictionary")
        
    missing = required_fields - tx.keys()
    if missing:
        raise ValidationError(f"Missing required transaction fields: {missing}")
        
    if not isinstance(tx['sender'], str) or len(tx['sender']) != 42:
        raise ValidationError("Invalid sender address format")
        
    if not isinstance(tx['recipient'], str) or len(tx['recipient']) != 42:
        raise ValidationError("Invalid recipient address format")
        
    try:
        amount = float(tx['amount'])
        if amount <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise ValidationError("Transaction amount must be a positive number")
        
    if not isinstance(tx['nonce'], int) or tx['nonce'] < 0:
        raise ValidationError("Transaction nonce must be a non-negative integer")
        
    return None
