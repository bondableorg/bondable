from core.db.models.user import User
from core.entity_service.base.sqlalchemy import BaseSQLAlchemyEntityService


class UserEntityService(BaseSQLAlchemyEntityService):
    model = User