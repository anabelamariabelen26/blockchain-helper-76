import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

@dataclass
class BlockchainSettings:
    """Dataclass holding blockchain network settings."""
    rpc_url: str
    chain_id: int
    gas_limit: int = 21000
    timeout: int = 30

class ConfigManager:
    """Manages configuration settings for blockchain interactions."""
    def __init__(self, env_prefix: str = "BLOCKCHAIN") -> None:
        """Initialize the configuration manager."""
        self.env_prefix: str = env_prefix
        self._settings: Dict[str, BlockchainSettings] = self._initialize_settings()

    def _initialize_settings(self) -> Dict[str, BlockchainSettings]:
        """Set up default settings loaded from environment."""
        return {
            "ethereum": BlockchainSettings(
                rpc_url=os.getenv(f"{self.env_prefix}_ETH_RPC", "https://eth.llamarpc.com"),
                chain_id=1
            ),
            "polygon": BlockchainSettings(
                rpc_url=os.getenv(f"{self.env_prefix}_POLY_RPC", "https://polygon-rpc.com"),
                chain_id=137,
                gas_limit=30000
            ),
            "bsc": BlockchainSettings(
                rpc_url=os.getenv(f"{self.env_prefix}_BSC_RPC", "https://bsc-dataseed.binance.org"),
                chain_id=56
            )
        }

    def get_network_settings(self, network: str) -> Optional[BlockchainSettings]:
        """Fetch settings object for the given network name."""
        return self._settings.get(network.lower())

    def get_rpc_url(self, network: str) -> str:
        """Return the RPC URL for the specified network."""
        settings = self.get_network_settings(network)
        if settings is None:
            raise ValueError(f"Unsupported network: {network}")
        return settings.rpc_url

    def get_chain_id(self, network: str) -> int:
        """Return the chain ID for the specified network."""
        settings = self.get_network_settings(network)
        if settings is None:
            raise ValueError(f"Unsupported network: {network}")
        return settings.chain_id

    def list_supported_networks(self) -> List[str]:
        """Provide list of all supported networks."""
        return list(self._settings.keys())

    def update_setting(self, network: str, key: str, value: Any) -> None:
        """Modify a setting for a network if it exists."""
        if network not in self._settings:
            raise ValueError(f"Network {network} not supported")
        settings_obj = self._settings[network]
        if not hasattr(settings_obj, key):
            raise AttributeError(f"Invalid setting key: {key}")
        setattr(settings_obj, key, value)

    def get_all_settings(self) -> Dict[str, BlockchainSettings]:
        """Return a copy of all configured settings."""
        return self._settings.copy()