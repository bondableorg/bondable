from typing import Optional
from pydantic import UUID4

from sqlalchemy.exc import IntegrityError

# from core.controllers.schemas.user import RequestAuthData
from core.common.utils.utils import BondableBusinessCase
from core.db.models.location import Location
from logger import logger


class ListLocationsBusinessCase(BondableBusinessCase):
    async def run(
        self,
    ) -> list[Location]:
        try:
            locations: list[Location] = await self.entities_service.location.select(
                limit=100, offset=0
            )
        except IntegrityError as e:
            logger.exception(
                f"{self.__class__.__name__}.run | IntegrityError",
                extra={"error": str(e)},
            )
            raise Exception

        return locations
