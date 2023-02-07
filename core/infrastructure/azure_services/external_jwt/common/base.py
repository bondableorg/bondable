from abc import ABC, abstractmethod
from typing import Optional


class ExternalJWT(ABC):
    @abstractmethod
    async def get_token(self, payload: Optional[dict] = None):
        """Get external JWT"""
