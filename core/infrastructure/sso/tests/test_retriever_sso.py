# import mock
# import pytest

# from core.controllers.common.exceptions import UnauthorizedException
# from core.infrastructure.sso.common.schemas import RetrieverUserInfoResponse
# from core.infrastructure.sso.bondable import RetrieverSSO


# class TestRetrieverSSO:
#     TEST_CLASS = RetrieverSSO

#     @mock.patch("core.infrastructure.sso.retriever.aiohttp.client.ClientSession")
#     @pytest.mark.asyncio
#     async def test_fetch_success(self, session):
#         client = self.TEST_CLASS()
#         return_value = {}
#         session.get.return_value.__aenter__.return_value.status = 200
#         session.get.return_value.__aenter__.return_value.json = mock.AsyncMock(
#             return_value=return_value
#         )
#         result = await client.fetch(session=session, url="fake_url", session_id="session_id")
#         assert result == return_value

#     @mock.patch("core.infrastructure.sso.retriever.aiohttp.client.ClientSession")
#     @pytest.mark.asyncio
#     async def test_fetch_fail(self, session):
#         client = self.TEST_CLASS()
#         session.get.return_value.__aenter__.return_value.status = 400
#         with pytest.raises(UnauthorizedException):
#             await client.fetch(session=session, url="fake_url", session_id="session_id")

#     @pytest.mark.asyncio
#     async def test_get_user_info(self):
#         client = self.TEST_CLASS()
#         user_data = {
#             "account": {"id": 1},
#             "customer": {"id": 20000001, "name": "test_customer_name"},
#         }
#         client.fetch = mock.AsyncMock(return_value=user_data)
#         result = await client.get_user_info("test_session_id")
#         assert result == RetrieverUserInfoResponse(**user_data)
