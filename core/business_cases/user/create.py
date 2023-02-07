from typing import Optional

from sqlalchemy.exc import IntegrityError

from core.business_cases.user.schemas import UserCreate
# from core.controllers.schemas.user import RequestAuthData
from core.common.utils.utils import BondableBusinessCase
from core.db.models.user import User
from logger import logger


class CreateUserBusinessCase(BondableBusinessCase):
    async def run(
        self,
        data: UserCreate,
    ) -> User:
        try:
            user_id = await self.entities_service.user.create(**data.dict())
        except Exception as e:
            logger.exception(
                f"{self.__class__.__name__}.run | IntegrityError",
                extra={"data": data, "error": str(e)},
            )
            raise Exception(e)
        
        user = await self.entities_service.user.select_one(id=user_id)
        return user


