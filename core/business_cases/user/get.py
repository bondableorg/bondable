from typing import Optional
from pydantic import UUID4

from sqlalchemy.exc import IntegrityError

from core.business_cases.user.schemas import UserCreate

# from core.controllers.schemas.user import RequestAuthData
from core.common.utils.utils import BondableBusinessCase
from core.db.models.user import User
from logger import logger


class GetUserBusinessCase(BondableBusinessCase):
    async def run(
        self,
        user_id: UUID4,
    ) -> User:
        try:
            user = await self.entities_service.user.select_one(id=user_id)
        except IntegrityError as e:
            logger.exception(
                f"{self.__class__.__name__}.run | IntegrityError",
                extra={"error": str(e)},
            )
            raise Exception

        return user
