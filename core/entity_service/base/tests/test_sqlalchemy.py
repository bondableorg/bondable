import uuid
from typing import Type

import pytest
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from core.db.models import Customer
from core.entity_service.base.sqlalchemy import BaseSQLAlchemyEntityService


class TestBaseSQLAlchemyEntityService:
    @property
    def entity_service_class(self) -> Type[BaseSQLAlchemyEntityService]:
        class TestClass(BaseSQLAlchemyEntityService):
            model = Customer

        return TestClass

    @pytest.mark.asyncio
    async def test_select_one_without_filter(self, db_session):
        entity_service = self.entity_service_class(session=db_session)

        with pytest.raises(ValueError):
            await entity_service.select_one()

    @pytest.mark.asyncio
    async def test_select_one_with_filter(self, db_session):
        entity_service = self.entity_service_class(session=db_session)

        customer_id1 = await entity_service.create(
            retriever_id=1, company_name="company_name", display_name="display_name"
        )

        await entity_service.create(
            retriever_id=2, company_name="company_name", display_name="display_name"
        )

        with pytest.raises(NoResultFound):
            await entity_service.select_one(id=uuid.uuid4())

        with pytest.raises(MultipleResultsFound):
            await entity_service.select_one(company_name="company_name")

        result = await entity_service.select_one(id=customer_id1)
        assert result.id == customer_id1

    @pytest.mark.asyncio
    async def test_create_without_fields(self, db_session):
        entity_service = self.entity_service_class(session=db_session)

        customer_id = await entity_service.create()
        assert customer_id

        customer_id = await entity_service.create()
        assert customer_id

    @pytest.mark.asyncio
    async def test_select(self, db_session):
        entity_service = self.entity_service_class(session=db_session)

        customer_id1 = await entity_service.create(
            retriever_id=1, company_name="company_name", display_name="display_name"
        )

        customer_id2 = await entity_service.create(
            retriever_id=2, company_name="company_name", display_name="display_name"
        )

        customer_id3 = await entity_service.create(
            retriever_id=3, company_name="company_name2", display_name="display_name"
        )

        result = await entity_service.select(id=customer_id1)
        assert len(result) == 1
        assert result[0].id == customer_id1

        result = await entity_service.select(company_name="company_name")
        assert len(result) == 2
        assert set(customer.id for customer in result) == {customer_id1, customer_id2}

        result = await entity_service.select(display_name="display_name")
        assert len(result) == 3
        assert set(customer.id for customer in result) == {customer_id1, customer_id2, customer_id3}

        result = await entity_service.select(display_name="display_name", limit=1, offset=1)
        assert len(result) == 1
        assert result[0].id == customer_id2

    @pytest.mark.asyncio
    async def test_delete(self, db_session):
        entity_service = self.entity_service_class(session=db_session)

        await entity_service.create(
            retriever_id=1, company_name="company_name", display_name="display_name"
        )

        await entity_service.create(
            retriever_id=2, company_name="company_name", display_name="display_name"
        )

        await entity_service.create(
            retriever_id=3, company_name="company_name2", display_name="display_name"
        )

        result = await entity_service.delete(company_name="company_name")
        assert result == 2

        result = await entity_service.delete(display_name="display_name")
        assert result == 1

        result = await entity_service.delete(display_name="display_name")
        assert result == 0

    @pytest.mark.asyncio
    async def test_update(self, db_session):
        entity_service = self.entity_service_class(session=db_session)

        await entity_service.create(
            retriever_id=1, company_name="company_name", display_name="display_name"
        )

        await entity_service.create(
            retriever_id=2, company_name="company_name", display_name="display_name"
        )

        await entity_service.create(
            retriever_id=3, company_name="company_name2", display_name="display_name"
        )

        result = await entity_service.update(
            company_name="company_name", update_dict={"company_name": "new_company_name"}
        )
        assert result == 2

        result = await entity_service.update(
            company_name="company_name", update_dict={"company_name": "new_company_name"}
        )
        assert result == 0

    @pytest.mark.asyncio
    async def test_exists(self, db_session):
        entity_service = self.entity_service_class(session=db_session)

        await entity_service.create(
            retriever_id=1, company_name="company_name", display_name="display_name"
        )

        await entity_service.create(
            retriever_id=2, company_name="company_name", display_name="display_name"
        )

        await entity_service.create(
            retriever_id=3, company_name="company_name2", display_name="display_name"
        )

        result = await entity_service.exists(company_name="company_name")
        assert result

        result = await entity_service.exists(company_name="company_name3")
        assert not result

    @pytest.mark.asyncio
    async def update_or_create(self, db_session):
        entity_service = self.entity_service_class(session=db_session)

        customer_id = await entity_service.create(
            retriever_id=1, company_name="company_name", display_name="display_name"
        )

        customer = await entity_service.update_or_create(
            company_name="company_name", defaults={"display_name": "new_display_name"}
        )
        assert customer_id == customer.id
        assert customer.display_name == "new_display_name"

        customer = await entity_service.update_or_create(
            company_name="new_company_name", defaults={"display_name": "display_name"}
        )
        assert customer_id != customer.id
        assert customer.company_name == "new_company_name"
        assert customer.display_name == "display_name"
