from sqlalchemy import Column, ForeignKey, String

from core.db import Base
from core.db.mixins import PKUUIDMixin, TimestampsMixin
from sqlalchemy.orm import relationship


class Location(Base, PKUUIDMixin, TimestampsMixin):
    """DB model for Location."""

    __tablename__ = "location"
    
    name = Column(String, nullable=False)
    address = Column(String, nullable=True, default="")
    city = Column(String, nullable=True, default="")
    state = Column(String, nullable=True, default="")
    zip_code = Column(String, nullable=True, default="")
    country = Column(String, nullable=True, default="")
    phone = Column(String, nullable=True, default="")
    email = Column(String, nullable=True, default="")
    website = Column(String, nullable=True, default="")

    users = relationship("User", back_populates="location", cascade="delete", lazy="select")
