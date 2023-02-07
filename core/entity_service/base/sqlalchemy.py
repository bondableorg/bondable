from abc import ABC, abstractmethod
from typing import Optional, Union

import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound

from core.db import AsyncDBSession, Base
from core.entity_service.base.base import BaseEntityService
from logger import logger


class BaseSQLAlchemyEntityService(BaseEntityService, ABC):
    default_order_by: Optional[str] = None
    ordering_function: Union[sa.asc, sa.desc] = sa.asc

    @property
    @abstractmethod
    def model(self) -> Base:
        pass

    def __init__(self, session: AsyncDBSession):
        self.session = session

    def _get_query(self):
        return sa.select(self.model)

    async def get_count(self, **filter_kwargs):
        query = self._get_query()
        query = self._apply_filters_to_query(query=query, filter_kwargs=filter_kwargs)
        result = await self.session.execute(query.with_only_columns([sa.func.count()]))
        return result.scalar_one()

    def _apply_filters_to_query(self, query, filter_kwargs: dict):
        """Apply filters for query.
        Using this, SQL Alchemy in_ filter may be applied using "{some_field}__in"
        clause in the filter kwargs.
        """

        if not filter_kwargs:
            return query

        in__filters = []
        not__filters = []
        gt__filters = []
        lt__filters = []
        filter_without_in = {}
        # retrieve model class from query
        model = query._propagate_attrs["plugin_subject"].class_  # noqa
        # separate in_ clauses and usual clauses
        for key, value in filter_kwargs.items():
            if key.endswith("__in"):
                # Project.key.in_(value)
                in__filters.append(getattr(getattr(model, key.removesuffix("__in")), "in_")(value))
            elif key.endswith("__not"):
                not__filters.append(
                    getattr(
                        getattr(model, key.removesuffix("__not")),
                        "isnot" if value is None else "not",
                    )(value)
                )
            elif key.endswith("__gt"):
                gt__filters.append(getattr(model, key.removesuffix("__gt")) > value)
            elif key.endswith("__lt"):
                lt__filters.append(getattr(model, key.removesuffix("__lt")) < value)
            else:
                filter_without_in[key] = value

        # apply in_ clauses
        if in__filters:
            query = query.filter(*in__filters)

        if not__filters:
            query = query.filter(*not__filters)

        if filter_without_in:
            query = query.filter_by(**filter_without_in)

        if gt__filters:
            query = query.filter(*gt__filters)

        if lt__filters:
            query = query.filter(*lt__filters)

        return query

    def _transform_select_items(self, select_items):
        return [self._transform_select_item(row=row) for row in select_items]

    @staticmethod
    def _transform_select_item(row):
        obj, *_ = row
        return obj

    async def select_one(self, **filter_kwargs):
        if not filter_kwargs:
            raise ValueError("Specify at least one parameter")

        query = self._get_query()
        query = self._apply_filters_to_query(query=query, filter_kwargs=filter_kwargs)
        result = await self.session.execute(query)
        row = result.one()
        return self._transform_select_item(row)

    async def create(self, **create_kwargs):
        query = sa.insert(self.model).values(**create_kwargs)
        insert_result = await self.session.execute(query)

        return insert_result.inserted_primary_key[0]

    async def select(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        ordering: Optional[list[str]] = None,
        **filter_kwargs,
    ) -> list:

        query = self._get_query()
        query = self._apply_filters_to_query(query=query, filter_kwargs=filter_kwargs)

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        if ordering:
            # transform ordering from list to the str
            # e.g. from ["-display_name", "active_users_number"] to the ordering string
            # which will be used in ordering query: "display_name desc, active_users_number acs"
            order_by_values_list = []
            for order_value in ordering:
                desc = order_value.startswith("-")
                field = order_value.lstrip("-").strip().lower()
                if not hasattr(self.model, field):
                    logger.warning(
                        f"Trying to order `{self.model.__name__}` model by field=`{field}`. "
                        f"Ordering field is not exists in model."
                    )
                    continue
                order_value = f"{field} {'desc' if desc else 'asc'}"
                order_by_values_list.append(order_value)
            order_by_str = ", ".join(order_by_values_list)
            query = query.order_by(sa.text(order_by_str))
        elif self.default_order_by is not None:
            column = getattr(self.model, self.default_order_by, None)
            if column:
                query = query.order_by(self.ordering_function.__func__(column))

        items = await self.session.execute(query)

        return self._transform_select_items(select_items=items)

    async def delete(self, **filter_kwargs):
        query = sa.delete(self.model)
        query = self._apply_filters_to_query(query=query, filter_kwargs=filter_kwargs)
        result = await self.session.execute(query)
        return result.rowcount

    async def update(self, update_dict: dict, **filter_kwargs):
        """Update objects in DB."""

        query = sa.update(self.model)
        query = self._apply_filters_to_query(query=query, filter_kwargs=filter_kwargs)
        query = query.values(**update_dict)
        result = await self.session.execute(query)
        return result.rowcount

    async def update_or_create(self, defaults, **filter_kwargs):
        query = self._get_query()
        query = self._apply_filters_to_query(query=query, filter_kwargs=filter_kwargs)
        result = await self.session.execute(query)

        try:
            obj = result.scalar_one()
        except NoResultFound:
            insert_result = await self.session.execute(
                sa.insert(self.model).values(filter_kwargs | defaults)
            )

            obj = await self.select_one(id=insert_result.inserted_primary_key[0])
        else:
            for key, value in defaults.items():
                setattr(obj, key, value)

        return obj

    async def exists(self, **filter_kwargs) -> bool:
        query = self._get_query()
        query = self._apply_filters_to_query(query=query, filter_kwargs=filter_kwargs)
        query = query.exists()
        result = await self.session.execute(sa.select(query))
        result = result.scalar()
        return result

    async def change_position(self, prev_position: int, new_position: int, **filter_kwargs):
        # in case, position not changing, do nothing
        if prev_position == new_position:
            return 0

        # item moving lower in the list -> raise up items between old position and new one
        if new_position > prev_position:
            filter_kwargs["position__gt"] = prev_position
            filter_kwargs["position__lt"] = new_position + 1
            update_dict = {"position": self.model.position - 1}
        else:
            filter_kwargs["position__gt"] = new_position - 1
            filter_kwargs["position__lt"] = prev_position
            update_dict = {"position": self.model.position + 1}

        query = sa.update(self.model)
        query = self._apply_filters_to_query(query=query, filter_kwargs=filter_kwargs)
        query = query.values(**update_dict)
        result = await self.session.execute(query)
        return result.rowcount
