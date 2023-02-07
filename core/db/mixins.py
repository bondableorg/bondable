import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


class TimestampsMixin:
    """Mixin that define timestamp columns."""

    __abstract__ = True

    created_at = sa.Column(
        "created_at", sa.TIMESTAMP(timezone=False), default=sa.func.now(), nullable=False
    )

    updated_at = sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=False),
        default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )


class PKUUIDMixin:
    """Mixin define id(primary key) as UUID field."""

    __abstract__ = True

    id = sa.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True)
