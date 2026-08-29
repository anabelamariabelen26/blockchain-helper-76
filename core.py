import hashlib
from functools import lru_cache
class Core:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 2
    @lru_cache(maxsize=128)
    def calculate_hash(self, index, previous_hash, transactions_str, timestamp, nonce):
        block_string = f"{index}{previous_hash}{transactions_str}{timestamp}{nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    def create_genesis(self):
        genesis_block = {"index": 0, "timestamp": 0.0, "transactions": [], "previous_hash": "0", "nonce": 0}
        tx_str = str(genesis_block["transactions"])
        genesis_block["hash"] = self.calculate_hash(genesis_block["index"], genesis_block["previous_hash"], tx_str, genesis_block["timestamp"], genesis_block["nonce"])
        self.chain.append(genesis_block)
    def add_transaction(self, sender, recipient, amount):
        transaction = {"sender": sender, "recipient": recipient, "amount": amount}
        self.pending_transactions.append(transaction)
    def mine_block(self, miner):
        if not self.chain:
            self.create_genesis()
        previous_block = self.chain[-1]
        tx_str = str(self.pending_transactions)
        new_block = {"index": len(self.chain), "timestamp": 1609459200.0, "transactions": self.pending_transactions[:], "previous_hash": previous_block["hash"], "nonce": 0}
        new_block["hash"] = self.calculate_hash(new_block["index"], new_block["previous_hash"], tx_str, new_block["timestamp"], new_block["nonce"])
        target = "0" * self.difficulty
        while new_block["hash"][:self.difficulty] != target:
            new_block["nonce"] += 1
            new_block["hash"] = self.calculate_hash(new_block["index"], new_block["previous_hash"], tx_str, new_block["timestamp"], new_block["nonce"])
        self.chain.append(new_block)
        reward = {"sender": "system", "recipient": miner, "amount": 10.0}
        self.pending_transactions = [reward]
        return new_block
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]
            if current_block["previous_hash"] != prev_block["hash"]:
                return False
            tx_str = str(current_block["transactions"])
            computed = self.calculate_hash(current_block["index"], current_block["previous_hash"], tx_str, current_block["timestamp"], current_block["nonce"])
            if current_block["hash"] != computed:
                return False
        return True
if __name__ == "__main__":
    c = Core()
    c.add_transaction("a", "b", 1)
    c.mine_block("m")
    print(c.validate_chain())