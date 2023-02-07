from typing import Optional
from uuid import UUID

from pydantic import UUID4, BaseModel

from core.db.choices.users import UserTypes


class LocationSchema(BaseModel):
    id: UUID
    name: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    email: str
    website: Optional[str]

class LocationCreate(BaseModel):
    name: str
    address: str
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    email: str
    website: Optional[str]
    lead_contact: UUID4

class UserCreate(BaseModel):
    email: str
    type: UserTypes
    full_name: str
    language: Optional[str]

class UserUpdate(BaseModel):
    email: Optional[str]
    type: Optional[UserTypes]
    full_name: Optional[str]
    language: Optional[str]

class UserSchema(BaseModel):
    id: UUID4
    email: str
    full_name: str
    language: Optional[str]

    class Config:
        orm_mode = True
