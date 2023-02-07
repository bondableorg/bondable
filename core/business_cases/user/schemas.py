from typing import Optional
from uuid import UUID

from pydantic import UUID4, BaseModel

from core.db.choices.users import UserTypes


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
    type: UserTypes
    locations: Optional[UUID4]

    class Config:
        orm_mode = True
