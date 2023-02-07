# import asyncio
# import uuid
# from typing import Awaitable, Callable, Optional, Union

# import pytest_asyncio
# import sqlalchemy as sa
# from core.controllers.common.enums import CustomerRolesEnum, ProjectRolesEnum
# from core.controllers.schemas.user import RequestAuthData
# from core.db.choices.notification import NotificationTypeEnum
# from core.db.choices.search import SearchTypes
# from core.db.choices.users import UserTypes
# from core.db.models import (
#     Customer,
#     CustomerRole,
#     Notification,
#     NotificationSearchAssociation,
#     NotificationSubscription,
#     Project,
#     ProjectRole,
#     SearchGroup,
#     SearchItem,
#     User,
# )
# from core.db.models.fakers import (
#     CustomerFactory,
#     CustomerRoleFactory,
#     NotificationFactory,
#     NotificationSubscriptionFactory,
#     ProjectFactory,
#     ProjectRoleFactory,
#     SearchGroupFactory,
#     SearchItemFactory,
#     SearchItemHistoryFactory,
#     UserFactory,
# )
# from core.db.models.search import SearchItemHistory
# from core.entity_service import SearchGroupEntityService
# from pydantic import UUID4
# from some_common.messages.topic.factories.payload.payload import TopicPayloadCreateSchemaFactory


# @pytest_asyncio.fixture(scope="function")
# async def customer_factory(db_session):
#     async def factory(**kwargs):
#         customer_data = CustomerFactory(**kwargs)
#         query = sa.insert(Customer).values(**customer_data.dict())
#         await db_session.execute(query)

#         query = sa.select(Customer).filter_by(id=customer_data.id)
#         result = await db_session.execute(query)
#         return result.scalar_one()

#     return factory


# @pytest_asyncio.fixture(scope="function")
# async def user_factory(db_session, customer_factory: Callable) -> Callable:
#     async def factory(
#         customer_id: Optional[UUID4] = None,
#         type: UserTypes = UserTypes.CUSTOMER,
#         **kwargs,
#     ):
#         if customer_id is None:
#             customer = await customer_factory()
#             customer_id = customer.id

#         user_data = UserFactory(customer=customer_id, type=type, **kwargs)
#         query = sa.insert(User).values(**user_data.dict())
#         await db_session.execute(query)

#         query = sa.select(User).filter_by(id=user_data.id)
#         result = await db_session.execute(query)
#         return result.scalar_one()

#     return factory


# @pytest_asyncio.fixture(scope="function")
# async def project_factory(customer_factory: Callable, db_session):
#     async def create_project(
#         customer_id: Optional[UUID4] = None,
#         **kwargs,
#     ) -> Awaitable[Project]:
#         if customer_id is None:
#             customer = await customer_factory()
#             customer_id = customer.id

#         project_data = ProjectFactory(customer=customer_id, **kwargs)
#         query = sa.insert(Project).values(**project_data.dict())
#         await db_session.execute(query)

#         query = sa.select(Project).filter_by(id=project_data.id)
#         result = await db_session.execute(query)
#         return result.scalar_one()

#     return create_project


# @pytest_asyncio.fixture(scope="function")
# async def project_bulk_factory(customer_factory: Callable, project_factory: Callable):
#     async def project_bulk_creation(
#         size: int,
#         customer_id: Optional[UUID4] = None,
#         **kwargs,
#     ):
#         if customer_id is None:
#             customer = await customer_factory()
#             customer_id = customer.id

#         projects = await asyncio.gather(
#             *[project_factory(customer_id=customer_id, **kwargs) for _ in range(size)]
#         )
#         return projects

#     return project_bulk_creation


# @pytest_asyncio.fixture(scope="function")
# async def search_group_factory(
#     project_factory: Callable, db_session, type: Optional[SearchTypes] = None
# ):
#     async def create_search_group(
#         project_id: Optional[UUID4] = None,
#         **kwargs,
#     ):
#         if project_id is None:
#             project = await project_factory()
#             project_id = project.id
#         kwargs["project"] = project_id

#         if type is not None:
#             kwargs["type"] = type

#         search_data = SearchGroupFactory(**kwargs)
#         query = sa.insert(SearchGroup).values(**search_data.dict())
#         await db_session.execute(query)

#         query = sa.select(SearchGroup).filter_by(id=search_data.id)
#         result = await db_session.execute(query)
#         return result.scalar_one()

#     return create_search_group


# @pytest_asyncio.fixture(scope="function")
# async def search_group_bulk_factory(project_factory: Callable, search_group_factory: Callable):
#     async def search_group_bulk_creation(
#         size: int,
#         project_id: Optional[UUID4] = None,
#         **kwargs,
#     ):
#         if project_id is None:
#             project = await project_factory()
#             project_id = project.id

#         search_groups = await asyncio.gather(
#             *[search_group_factory(project_id=project_id, **kwargs) for _ in range(size)]
#         )
#         return search_groups

#     return search_group_bulk_creation


# @pytest_asyncio.fixture(scope="function")
# async def search_item_factory(search_group_factory: Callable, db_session):
#     async def create_search_item(
#         group_id: Optional[UUID4] = None,
#         project_id: Optional[UUID4] = None,
#         **kwargs,
#     ):
#         if group_id is None:
#             group: SearchGroup = await search_group_factory(project_id=project_id)
#             group_id = group.id
#         else:
#             search_group_entity_service = SearchGroupEntityService(session=db_session)
#             group = await search_group_entity_service.select_one(id=group_id)

#         topic_data = TopicPayloadCreateSchemaFactory(project_id=group.project).dict(
#             convert_uuid_to_str=True
#         )
#         kwargs.setdefault("topic_data", topic_data)

#         search_data = SearchItemFactory(group=group_id, **kwargs)
#         query = sa.insert(SearchItem).values(**search_data.dict())
#         await db_session.execute(query)

#         query = sa.select(SearchItem).filter_by(id=search_data.id)
#         result = await db_session.execute(query)
#         return result.scalar_one()

#     return create_search_item


# @pytest_asyncio.fixture(scope="function")
# async def search_item_bulk_factory(project_factory: Callable, search_item_factory: Callable):
#     async def search_item_bulk_creation(
#         size: int,
#         project_id: Optional[UUID4] = None,
#         **kwargs,
#     ):
#         if project_id is None:
#             project = await project_factory()
#             project_id = project.id

#         search_items = await asyncio.gather(
#             *[search_item_factory(project_id=project_id, **kwargs) for _ in range(size)]
#         )
#         return search_items

#     return search_item_bulk_creation


# @pytest_asyncio.fixture(scope="function")
# async def search_item_history_factory(search_item_factory: Callable, db_session):
#     async def create_search_item_history(
#         search_item_id: Optional[UUID4] = None,
#         group_id: Optional[UUID4] = None,
#         project_id: Optional[UUID4] = None,
#         **kwargs,
#     ):
#         if search_item_id is None:
#             search_item = await search_item_factory(group_id=group_id, project_id=project_id)
#             search_item_id = search_item.id

#         search_data = SearchItemHistoryFactory(search=search_item_id, **kwargs)
#         query = sa.insert(SearchItemHistory).values(**search_data.dict())
#         await db_session.execute(query)

#         query = sa.select(SearchItemHistory).filter_by(id=search_data.id)
#         result = await db_session.execute(query)
#         return result.scalar_one()

#     return create_search_item_history


# @pytest_asyncio.fixture(scope="function")
# async def project_role_factory(project_factory: Callable, user_factory: Callable, db_session):
#     async def create_project_role(
#         role: ProjectRolesEnum = ProjectRolesEnum.VIEWER,
#         project_id: Optional[UUID4] = None,
#         user_id: Optional[UUID4] = None,
#         customer_id: Optional[UUID4] = None,
#     ):
#         if not project_id:
#             project_id = (await project_factory(customer_id=customer_id)).id

#         if not user_id:
#             user_id = (await user_factory(customer_id=customer_id)).id

#         project_role_data = ProjectRoleFactory(user=user_id, project=project_id, role=role)
#         await db_session.execute(sa.insert(ProjectRole).values(**project_role_data.dict()))

#         result = await db_session.execute(sa.select(ProjectRole).filter_by(id=project_role_data.id))
#         return result.scalar_one()

#     return create_project_role


# @pytest_asyncio.fixture(scope="function")
# async def customer_role_factory(customer_factory: Callable, user_factory: Callable, db_session):
#     async def create_customer_role(
#         role: CustomerRolesEnum = CustomerRolesEnum.CUSTOMER_ADMIN,
#         user_id: Optional[UUID4] = None,
#         customer_id: Optional[UUID4] = None,
#     ):
#         if not customer_id:
#             customer_id = (await customer_factory()).id

#         if not user_id:
#             user_id = (await user_factory(customer_id=customer_id)).id

#         customer_role_data = CustomerRoleFactory(user=user_id, customer=customer_id, role=role)

#         await db_session.execute(sa.insert(CustomerRole).values(**customer_role_data.dict()))

#         query = sa.select(CustomerRole).filter_by(id=customer_role_data.id)
#         result = await db_session.execute(query)
#         return result.scalar_one()

#     return create_customer_role


# @pytest_asyncio.fixture(scope="function")
# async def notification_factory(customer_factory: Callable, user_factory: Callable, db_session):
#     async def create_notification(
#         search_item_ids: Optional[list[Union[str, UUID4, uuid.UUID]]] = None,
#         customer_id: Optional[Union[str, UUID4, uuid.UUID]] = None,
#         created_by: Optional[Union[str, UUID4, uuid.UUID]] = None,
#         type: NotificationTypeEnum = NotificationTypeEnum.GLOBAL,
#         **kwargs,
#     ):
#         if not customer_id:
#             customer_id = (await customer_factory()).id

#         if not created_by:
#             created_by = (await user_factory(customer_id=customer_id)).id

#         notification_data = NotificationFactory(
#             created_by=created_by, customer_id=customer_id, type=type, **kwargs
#         )

#         await db_session.execute(sa.insert(Notification).values(**notification_data.dict()))

#         query = sa.select(Notification).filter_by(id=notification_data.id)
#         result = await db_session.execute(query)
#         if search_item_ids:
#             await db_session.execute(
#                 sa.insert(NotificationSearchAssociation).values(
#                     [
#                         dict(notification_id=notification_data.id, search_item_id=search_item_id)
#                         for search_item_id in search_item_ids
#                     ]
#                 )
#             )

#         return result.scalar_one()

#     return create_notification


# @pytest_asyncio.fixture(scope="function")
# async def notification_subscription_factory(
#     user_factory: Callable, notification_factory: Callable, db_session
# ):
#     async def create_notification_subscription(
#         notification_id: Optional[UUID4] = None,
#         user_id: Optional[UUID4] = None,
#         notification_email=None,
#         **kwargs,
#     ):
#         if not notification_id:
#             notification_id = (await notification_factory()).id

#         if not user_id and not notification_email:
#             user_id = (await user_factory()).id

#         notification_data = NotificationSubscriptionFactory(
#             user_id=user_id,
#             notification_id=notification_id,
#             notification_email=notification_email,
#             **kwargs,
#         )

#         await db_session.execute(
#             sa.insert(NotificationSubscription).values(**notification_data.dict())
#         )

#         query = sa.select(NotificationSubscription).filter_by(id=notification_data.id)
#         result = await db_session.execute(query)

#         return result.scalar_one()

#     return create_notification_subscription


# @pytest_asyncio.fixture(scope="function")
# async def request_auth_data(user_factory: Callable, db_session):
#     async def create_request_auth_data(user_id=None, session=None):
#         if user_id is None:
#             user_id = (await user_factory()).id
#         from core.entity_service import UserEntityService

#         user = (await UserEntityService(session=db_session).select_with_roles(id=user_id))[0]
#         return RequestAuthData(user=user, session=str(session or uuid.uuid4()))

#     return create_request_auth_data
