from abc import ABC, abstractmethod
from typing import Optional, Union
from uuid import UUID


class BaseEntityService(ABC):
    default_limit = 100

    @abstractmethod
    async def select_one(self, **filter_kwargs):
        """Select one item."""

    @abstractmethod
    async def select(
        self, limit: Optional[int] = None, offset: Optional[int] = None, **filter_kwargs
    ) -> list:
        """Select items."""

    @abstractmethod
    async def create(self, retrieve: bool = False, **create_kwargs) -> Union[UUID, str]:
        """Create item"""

    @abstractmethod
    async def update(self, update_dict: dict, **filter_kwargs):
        """Create items"""

    @abstractmethod
    async def delete(self, **filter_kwargs) -> int:
        """Delete items"""

    @abstractmethod
    async def update_or_create(self, defaults, **filter_kwargs):
        """Update or create"""

    @abstractmethod
    async def exists(self, **filter_kwargs) -> bool:
        """Exists item"""


class EntitiesService:
    @property
    @abstractmethod
    def location(self) -> BaseEntityService:
        """location entity service"""

    @property
    @abstractmethod
    def user(self) -> BaseEntityService:
        """User entity service"""
