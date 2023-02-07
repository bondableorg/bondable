from typing import Optional
from pydantic import UUID4

from sqlalchemy.exc import IntegrityError


# from core.controllers.schemas.user import RequestAuthData
from core.common.utils.utils import BondableBusinessCase
from core.db.models.location import Location
from logger import logger


class GetLocationBusinessCase(BondableBusinessCase):
    async def run(
        self,
        user_id: UUID4,
    ) -> Location:
        try:
            location = await self.entities_service.location.select_one(id=user_id)
        except IntegrityError as e:
            logger.exception(
                f"{self.__class__.__name__}.run | IntegrityError",
                extra={"error": str(e)},
            )
            raise Exception

        return location
