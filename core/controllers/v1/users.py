from typing import Optional
import traceback
from fastapi import APIRouter, Depends, Request, Query
from pydantic import UUID4, BaseModel

from core.business_cases.user import (
    CreateUserBusinessCase,
    GetUserBusinessCase,
    ListUserBusinessCase,
)
from core.business_cases.user.schemas import UserCreate, UserSchema, UserUpdate
from core.business_cases.user.update import UpdateUserBusinessCase
from core.controllers.deps.db import get_db_session
from core.db import AsyncDBSession
from config.settings import Settings, get_settings

user_v1_router = APIRouter()


@user_v1_router.get(
    path="/",
    response_model=list[UserSchema],
    description="Get list of users.",
)
async def list_of_users(
    db_session: AsyncDBSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    """Retrieve list of users."""
    business_cases = ListUserBusinessCase(db_session=db_session, settings=settings)

    users = await business_cases.run()
    return users


@user_v1_router.post(path="/", response_model=UserSchema)
async def create_user(
    data: UserCreate,
    db_session: AsyncDBSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    """
    Create account for user.
    """
    business_cases = CreateUserBusinessCase(db_session=db_session, settings=settings)
    user = await business_cases.run(data=data)

    return user


@user_v1_router.get(
    path="/{user_id}/",
    response_model=UserSchema,
)
async def retrieve_user(
    user_id: UUID4,
    db_session: AsyncDBSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    """Retrieve user by ID."""
    business_cases = GetUserBusinessCase(db_session=db_session, settings=settings)
    user = await business_cases.run(user_id=user_id)

    return user


@user_v1_router.patch(path="/{user_id}/", response_model=UserSchema)
async def update_user(
    user_id: UUID4,
    data: UserUpdate,
    db_session: AsyncDBSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    business_cases = UpdateUserBusinessCase(db_session=db_session, settings=settings)
    user = await business_cases.run(user_id=user_id, data=data)
    return user
