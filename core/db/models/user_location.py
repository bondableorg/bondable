from sqlalchemy import Column, ForeignKey

from core.db.mixins import PKUUIDMixin, TimestampsMixin
from .user import User
from .location import Location
from core.db import Base
from sqlalchemy.orm import relationship


class UserLocation(Base, PKUUIDMixin, TimestampsMixin):
    """DB model for UserLocation."""

    __tablename__ = "user_location"

    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    location_id = Column(ForeignKey("location.id", ondelete="CASCADE"), primary_key=True)

