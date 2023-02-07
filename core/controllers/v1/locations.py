from typing import Optional
import traceback
from fastapi import APIRouter, Depends, Request, Query
from pydantic import UUID4, BaseModel

from core.business_cases.location import (
    CreateLocationBusinessCase,
    GetLocationBusinessCase,
    ListLocationsBusinessCase,
    UpdateLocationBusinessCase,
)
from core.business_cases.location.schemas import LocationCreate, LocationSchema, LocationUpdate

from core.controllers.deps.db import get_db_session
from core.db import AsyncDBSession
from config.settings import Settings, get_settings

location_v1_router = APIRouter()


@location_v1_router.get(
    path="/",
    response_model=list[LocationSchema],
    description="Get list of locations.",
)
async def list_of_locations(
    db_session: AsyncDBSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    """Retrieve list of locations."""
    business_cases = ListLocationsBusinessCase(db_session=db_session, settings=settings)

    locations = await business_cases.run()
    return locations


@location_v1_router.post(path="/", response_model=LocationSchema)
async def create_location(
    data: LocationCreate,
    db_session: AsyncDBSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    """
    Create account for location.
    """
    business_cases = CreateLocationBusinessCase(db_session=db_session, settings=settings)
    location = await business_cases.run(data=data)

    return location


@location_v1_router.get(
    path="/{location_id}/",
    response_model=LocationSchema,
)
async def retrieve_location(
    location_id: UUID4,
    db_session: AsyncDBSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    """Retrieve location by ID."""
    business_cases = GetLocationBusinessCase(db_session=db_session, settings=settings)
    location = await business_cases.run(location_id=location_id)

    return location


@location_v1_router.patch(path="/{location_id}/", response_model=LocationSchema)
async def update_location(
    location_id: UUID4,
    data: LocationUpdate,
    db_session: AsyncDBSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    business_cases = UpdateLocationBusinessCase(db_session=db_session, settings=settings)
    location = await business_cases.run(location_id=location_id, data=data)
    return user
