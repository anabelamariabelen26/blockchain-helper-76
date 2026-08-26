import os
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "network": "mainnet",
    "rpc_url": "https://mainnet.infura.io/v3/default",
    "gas_limit": 21000,
    "timeout_seconds": 30,
    "max_retries": 3,
}


class ConfigLoader:
    def __init__(self, env_prefix: str = "BC_HELP_") -> None:
        self.env_prefix = env_prefix
        self._config = DEFAULT_CONFIG.copy()
        self._load_from_env()

    def _load_from_env(self) -> None:
        for key in self._config:
            env_name = f"{self.env_prefix}{key.upper()}"
            env_value = os.getenv(env_name)
            if env_value is not None:
                self._config[key] = self._cast_value(
                    env_value, type(self._config[key])
                )

    @staticmethod
    def _cast_value(value: str, target_type: type) -> Any:
        if target_type == bool:
            return value.lower() in ("true", "1", "yes", "on")
        try:
            return target_type(value)
        except (ValueError, TypeError):
            return value

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return self._config.copy()


config = ConfigLoader()
