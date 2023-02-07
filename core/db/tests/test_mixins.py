from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects.postgresql import UUID

from core.db.mixins import PKUUIDMixin, TimestampsMixin


def test_timestamps_mixin():
    assert TimestampsMixin.__abstract__
    assert isinstance(TimestampsMixin.created_at, Column)
    assert isinstance(TimestampsMixin.created_at.type, TIMESTAMP)
    assert isinstance(TimestampsMixin.updated_at, Column)
    assert isinstance(TimestampsMixin.updated_at.type, TIMESTAMP)


def test_pkuuid_mixin():
    assert PKUUIDMixin.__abstract__
    assert isinstance(PKUUIDMixin.id, Column)
    assert isinstance(PKUUIDMixin.id.type, UUID)
