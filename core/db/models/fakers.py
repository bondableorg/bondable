import datetime
import random
from typing import Optional

import faker
from pydantic import UUID4, BaseModel, Field

from core.db.choices.users import UserTypes

faker_instance = faker.Faker()


class FakerFactory:
    def __init__(self, provider_name: str, *args, **kwargs):
        self._provider_name = provider_name
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        # global faker
        provider = getattr(faker_instance, self._provider_name)
        return provider(*self._args, **self._kwargs)


class UserFactory(BaseModel):
    id: UUID4 = Field(default_factory=FakerFactory("uuid4"))
    full_name: str = Field(default_factory=FakerFactory("name"))
    email: str = Field(default_factory=FakerFactory("email"))


class LocationFactory(BaseModel):
    id: UUID4 = Field(default_factory=FakerFactory("uuid4"))
    name: str = Field(default_factory=FakerFactory("city"))
    address: str = Field(default_factory=FakerFactory("address"))
    postcode: str = Field(default_factory=FakerFactory("postcode"))
    phone: str = Field(default_factory=FakerFactory("phone_number"))
