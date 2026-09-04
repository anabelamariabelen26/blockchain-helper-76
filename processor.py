import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class TransactionError(Exception):
    pass


class InsufficientBalanceError(TransactionError):
    pass


class InvalidNonceError(TransactionError):
    pass


class BlockProcessor:
    def __init__(self, max_gas_limit: int = 15_000_000) -> None:
        self.max_gas_limit = max_gas_limit

    def validate_transaction(self, tx: Dict[str, Any]) -> None:
        if not isinstance(tx, dict):
            raise TransactionError("Transaction payload must be a dictionary")

        required_fields = {"sender", "recipient", "value", "nonce", "gas_limit"}
        missing = required_fields - tx.keys()
        if missing:
            raise TransactionError(f"Missing required fields: {missing}")

        if not isinstance(tx["value"], (int, float)) or tx["value"] < 0:
            raise TransactionError("Invalid transaction value")

        if not isinstance(tx["nonce"], int) or tx["nonce"] < 0:
            raise InvalidNonceError("Nonce must be a non-negative integer")

        if tx["gas_limit"] > self.max_gas_limit:
            raise TransactionError(
                f"Gas limit {tx['gas_limit']} exceeds maximum {self.max_gas_limit}"
            )

    def process_transaction(
        self, tx: Dict[str, Any], sender_balance: int, expected_nonce: int
    ) -> Optional[Dict[str, Any]]:
        try:
            self.validate_transaction(tx)

            if tx["nonce"] != expected_nonce:
                raise InvalidNonceError(
                    f"Nonce mismatch: expected {expected_nonce}, got {tx['nonce']}"
                )

            total_cost = tx["value"] + (tx.get("gas_price", 0) * tx["gas_limit"])
            if sender_balance < total_cost:
                raise InsufficientBalanceError(
                    f"Balance {sender_balance} insufficient for cost {total_cost}"
                )

            return {
                "status": "success",
                "tx_hash": f"0x{hash(str(tx)):x}",
                "remaining_balance": sender_balance - total_cost,
            }
        except (TransactionError, InvalidNonceError, InsufficientBalanceError) as e:
            logger.error("Transaction failed edge check: %s", str(e))
            raise
        except Exception as e:
            logger.critical("Unexpected error during tx processing: %s", str(e))
            raise TransactionError("System failure processing transaction") from e