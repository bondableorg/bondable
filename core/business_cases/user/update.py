from typing import Optional
from pydantic import UUID4

from sqlalchemy.exc import IntegrityError

from core.business_cases.user.schemas import UserUpdate

# from core.controllers.schemas.user import RequestAuthData
from core.common.utils.utils import BondableBusinessCase
from core.db.models.user import User
from logger import logger


class UpdateUserBusinessCase(BondableBusinessCase):
    async def run(
        self,
        data: UserUpdate,
        user_id: UUID4,
    ) -> User:
        try:
            updated = await self.entities_service.user.update(
                id=user_id, update_dict=data.dict(exclude_none=True)
            )

        except IntegrityError as e:
            logger.exception(
                f"{self.__class__.__name__}.run | IntegrityError",
                extra={"error": str(e)},
            )
            raise Exception

        if not updated:
            raise Exception

        user = await self.entities_service.user.select_one(id=user_id)
        return user
