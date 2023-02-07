from typing import Optional
from uuid import UUID

from pydantic import UUID4, BaseModel
from core.business_cases.user.schemas import UserSchema

class LocationSchema(BaseModel):
    id: UUID4
    name: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    email: str
    website: Optional[str]
    users: Optional[list[UserSchema]]
    class Config:
        orm_mode = True

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
    

class LocationUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    email: Optional[str]
    lead_contact: Optional[UUID]