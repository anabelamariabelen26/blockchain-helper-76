# blockchain-helper-76

`blockchain-helper-76` is a lightweight Python toolkit designed to streamline interactions with EVM-compatible blockchains. It simplifies common tasks such as gas estimation, balance tracking, and secure transaction signing for developers building decentralized applications.

## Features

*   **Gas Oracle Integration:** Automatically fetches current network gas prices and suggests optimal priority fees to minimize transaction latency.
*   **Encrypted Wallet Management:** Securely handle private keys using local AES-256 encryption to prevent exposure in application logs.
*   **Batch Balance Scanner:** Efficiently query token balances for multiple addresses in a single RPC call to reduce latency and API overhead.
*   **Smart Contract Wrapper:** Provides a high-level interface to interact with deployed contracts without manually decoding ABI inputs.

## Installation

Ensure you have Python 3.8+ installed. Install the package via pip:

```bash
pip install blockchain-helper-76
```

For development requirements, clone the repository and run:

```bash
git clone https://github.com/Developer/blockchain-helper-76.git
cd blockchain-helper-76
pip install -r requirements.txt
```

## Usage

Here is a quick example of how to fetch the native balance of an address using the helper:

```python
from blockchain_helper import Web3Client

# Initialize client with your RPC endpoint
client = Web3Client(rpc_url="https://eth.llamarpc.com")

# Get balance in Ether
balance = client.get_balance("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
print(f"Current Balance: {balance} ETH")

# Estimate gas for a transaction
gas_price = client.get_recommended_gas()
print(f"Recommended Gas Price: {gas_price} Gwei")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.