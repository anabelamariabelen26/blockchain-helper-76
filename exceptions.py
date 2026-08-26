class BlockchainHelperError(Exception):
    pass

class ConfigurationError(BlockchainHelperError):
    pass

class InvalidAddressError(BlockchainHelperError):
    pass

class NetworkConnectionError(BlockchainHelperError):
    pass

class TransactionFailedError(BlockchainHelperError):
    pass

class InsufficientFundsError(BlockchainHelperError):
    pass

def handle_blockchain_exception(error: Exception) -> dict:
    if isinstance(error, InvalidAddressError):
        return {"error": "InvalidAddress", "message": str(error), "code": 400}
    elif isinstance(error, InsufficientFundsError):
        return {"error": "InsufficientFunds", "message": str(error), "code": 402}
    elif isinstance(error, NetworkConnectionError):
        return {"error": "NetworkError", "message": str(error), "code": 503}
    elif isinstance(error, TransactionFailedError):
        return {"error": "TransactionFailed", "message": str(error), "code": 422}
    elif isinstance(error, ConfigurationError):
        return {"error": "ConfigurationError", "message": str(error), "code": 500}
    return {"error": "InternalError", "message": str(error), "code": 500}
