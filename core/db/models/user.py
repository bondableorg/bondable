from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import PKUUIDMixin, TimestampsMixin


class User(Base, PKUUIDMixin, TimestampsMixin):
    """DB model for User."""

    __tablename__ = "user"

    email = Column(String, nullable=True, unique=True)
    type = Column(String)
    last_login = Column("last_login", TIMESTAMP(timezone=False))

    # User Personal data
    full_name = Column(String, nullable=False, default="")
    language = Column(String(2), nullable=True, default="EN")
