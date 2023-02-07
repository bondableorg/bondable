from core.business_cases.location.schemas import LocationCreate

# from core.controllers.schemas.user import RequestAuthData
from core.common.utils.utils import BondableBusinessCase
from core.db.models.location import Location
from logger import logger


class CreateLocationBusinessCase(BondableBusinessCase):
    async def run(
        self,
        data: LocationCreate,
    ) -> Location:
        try:
            location_id = await self.entities_service.location.create(
                **data.dict()
            )

        except Exception as e:
            logger.exception(
                f"{self.__class__.__name__}.run | IntegrityError",
                extra={"data": data, "error": str(e)},
            )
            raise Exception(e)

        location = await self.entities_service.location.select_one(id=location_id)
        print(location.users)
        return location
