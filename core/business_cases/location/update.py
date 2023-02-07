from typing import Optional
from pydantic import UUID4

from sqlalchemy.exc import IntegrityError

from core.business_cases.user.schemas import LocationUpdate

# from core.controllers.schemas.user import RequestAuthData
from core.common.utils.utils import BondableBusinessCase
from core.db.models.location import Location
from logger import logger


class UpdateLocationBusinessCase(BondableBusinessCase):
    async def run(
        self,
        data: LocationUpdate,
        user_id: UUID4,
    ) -> Location:
        try:
            updated = await self.entities_service.location.update(
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

        location = await self.entities_service.location.select_one(id=user_id)
        return location
