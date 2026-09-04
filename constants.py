from typing import Final

CURRENCIES: Final[list[str]] = ['BTC', 'ETH', 'SOL', 'DOT', 'ADA']

RPC_TIMEOUT: Final[int] = 30

DEFAULT_DECIMALS: Final[int] = 8

API_BASE_URL: Final[str] = 'https://api.blockchain.org/v1'

STATUS_CODES: Final[dict[int, str]] = {
    200: 'SUCCESS',
    400: 'BAD_REQUEST',
    401: 'UNAUTHORIZED',
    404: 'NOT_FOUND',
    429: 'RATE_LIMITED',
    500: 'SERVER_ERROR'
}

RETRY_ATTEMPTS: Final[int] = 3

DEFAULT_HEADERS: Final[dict[str, str]] = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'blockchain-helper-76-client'
}

MIN_CONFIRMATIONS: Final[int] = 6

SUPPORTED_NETWORKS: Final[set[str]] = {'mainnet', 'testnet', 'devnet'}