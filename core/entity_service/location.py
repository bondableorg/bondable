from core.db.models.location import Location
from core.entity_service.base.sqlalchemy import BaseSQLAlchemyEntityService


class LocationEntityService(BaseSQLAlchemyEntityService):
    model = Location