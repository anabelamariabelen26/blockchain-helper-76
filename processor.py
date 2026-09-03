from typing import Dict, Any, List

class TransactionProcessor:
    """Processes blockchain transaction data for analysis and formatting."""

    def __init__(self, decimals: int = 18) -> None:
        self.decimals = decimals

    def to_wei(self, value: float) -> int:
        """Convert a float ether value to wei."""
        return int(value * (10 ** self.decimals))

    def from_wei(self, value: int) -> float:
        """Convert a wei integer value to ether."""
        return float(value / (10 ** self.decimals))

    def extract_transfer_events(
        self, tx_receipts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract and normalize standard ERC20 transfer events from receipts."""
        transfers: List[Dict[str, Any]] = []
        transfer_topic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

        for receipt in tx_receipts:
            for log in receipt.get("logs", []):
                topics = log.get("topics", [])
                if topics and topics[0] == transfer_topic and len(topics) == 3:
                    try:
                        transfers.append({
                            "token": log.get("address"),
                            "from": "0x" + topics[1][-40:],
                            "to": "0x" + topics[2][-40:],
                            "value": int(log.get("data", "0x0"), 16)
                        })
                    except (ValueError, IndexError):
                        continue
        return transfers

    def calculate_total_fees(self, txs: List[Dict[str, Any]]) -> int:
        """Calculate total gas fees spent in a list of transactions."""
        total_fee = 0
        for tx in txs:
            gas_used = tx.get("gas_used") or tx.get("gas", 0)
            gas_price = tx.get("effective_gas_price") or tx.get("gas_price", 0)
            total_fee += gas_used * gas_price
        return total_fee