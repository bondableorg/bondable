from functools import cached_property

from core.db import AsyncDBSession
from core.entity_service.base.base import EntitiesService
from core.entity_service.user import UserEntityService
from core.entity_service.location import LocationEntityService

# from core.entity_service.location import LocationEntityService


class SQLAlchemyEntitiesService(EntitiesService):
    def __init__(self, session: AsyncDBSession):
        self.session = session

    @cached_property
    def user(self) -> UserEntityService:
        return UserEntityService(session=self.session)

    @cached_property
    def location(self) -> LocationEntityService:
        return LocationEntityService(session=self.session)
