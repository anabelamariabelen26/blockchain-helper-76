from typing import Dict, Any

class Config:
    def __init__(self, settings: Dict[str, Any]) -> None:
        self.settings = settings

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value

    def __repr__(self) -> str:
        return f"Config(settings={self.settings})"

config = Config(settings={
    'api_key': 'your_api_key',
    'api_secret': 'your_api_secret',
    'network': 'mainnet'
})