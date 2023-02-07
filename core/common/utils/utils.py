from functools import cached_property

from config.settings import Settings
from core.common.utils.base import BaseBusinessCase
from core.db.db import AsyncDBSession
from core.entity_service import SQLAlchemyEntitiesService


class BondableBusinessCase(BaseBusinessCase):
    def __init__(self, db_session: AsyncDBSession, settings: Settings):
        self.db_session = db_session
        self.settings = settings

    @cached_property
    def entities_service(self) -> SQLAlchemyEntitiesService:
        return SQLAlchemyEntitiesService(session=self.db_session)
