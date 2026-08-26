import logging
import sys
from typing import Optional


class BlockchainLogger:
    _instance: Optional['BlockchainLogger'] = None
    
    def __new__(cls, name: str = 'blockchain-helper-76') -> 'BlockchainLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger(name)
        return cls._instance

    def _initialize_logger(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str, **kwargs: Any) -> None:
        extra_str = f" | {kwargs}" if kwargs else ""
        self.logger.info(f"{message}{extra_str}")

    def error(self, message: str, **kwargs: Any) -> None:
        extra_str = f" | {kwargs}" if kwargs else ""
        self.logger.error(f"{message}{extra_str}")

    def warning(self, message: str, **kwargs: Any) -> None:
        extra_str = f" | {kwargs}" if kwargs else ""
        self.logger.warning(f"{message}{extra_str}")


def get_logger(name: str = 'blockchain-helper-76') -> BlockchainLogger:
    return BlockchainLogger(name)
