from core.entity_service.base.base import BaseEntityService


def test_base_entity_service():
    assert BaseEntityService.__abstractmethods__ == {
        "select_one",
        "select",
        "create",
        "update",
        "delete",
        "update_or_create",
        "exists",
    }
