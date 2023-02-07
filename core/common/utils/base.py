from abc import ABC, abstractmethod

from core.entity_service.base.base import EntitiesService


class BaseBusinessCase(ABC):
    @property
    @abstractmethod
    def entities_service(self) -> EntitiesService:
        """Entities service"""