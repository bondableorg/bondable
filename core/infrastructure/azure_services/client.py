# import hashlib
# import json
# from typing import Union, Optional, List
# from urllib.parse import urljoin

# import aiohttp
# from fastapi import status

# from core.controllers.common.exceptions import HandlerException
# from core.infrastructure.azure_services.common.base import BaseAggregationsClient
# from core.infrastructure.azure_services.common.exceptions import (
#     AWSAuthException,
#     AWSClientException,
# )
# from core.infrastructure.azure_services.external_jwt.aws import AWSExternalJWT
# from core.logging import logger


# AWS_API_AUTH_TOKEN = None


# class ASWServicesAPIClient(BaseAggregationsClient):
#     """AWS Aggregations API client"""

#     def __init__(
#         self,
#         base_url: str,
#         cache_header_name: str,
#         token_factory: AWSExternalJWT,
#         statistic_path: str,
#         matched_docs_stable_version: str,
#         matched_docs_latest_version: str,
#         matched_docs_export_path: str,
#         notification_scheduler_path: str,
#         retriever_admin_path: str,
#     ):
#         self.base_url = base_url
#         self.statistic_path = statistic_path
#         self.matched_docs_path_stable = f"matched-doc-search/{matched_docs_stable_version}/search"
#         self.matched_docs_path_latest = f"matched-doc-search/{matched_docs_latest_version}/search"
#         self.matched_docs_export_path = matched_docs_export_path
#         self.notification_scheduler_path = notification_scheduler_path
#         self.retriever_admin_path = retriever_admin_path
#         self.cache_header_name = cache_header_name
#         self.token_factory = token_factory

#     async def get_auth_header(self) -> dict:
#         global AWS_API_AUTH_TOKEN
#         if AWS_API_AUTH_TOKEN is None:
#             logger.debug("Fetching new token")
#             AWS_API_AUTH_TOKEN = await self.token_factory.get_token()
#         return {"Authorization": AWS_API_AUTH_TOKEN}

#     async def _perform_request(
#         self,
#         url: str,
#         method: str,
#         headers: dict,
#         log_auth_error: bool = False,
#         required_statuses: Optional[List[int]] = None,
#         **kwargs,
#     ) -> dict:
#         headers = headers | await self.get_auth_header()
#         if required_statuses is None:
#             required_statuses = [status.HTTP_200_OK]

#         log_extra_content = {
#             "url": url,
#             "method": method,
#             "headers": headers,
#             "kwargs": kwargs,
#             "required_statuses": required_statuses,
#         }

#         logger.debug(
#             f"{self.__class__.__name__}._perform_request | request data", extra=log_extra_content
#         )

#         async with aiohttp.request(
#             method.upper(),
#             url=url,
#             headers=headers,
#             connector=aiohttp.TCPConnector(ssl=False),
#             **kwargs,
#         ) as response:
#             if response.status in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):
#                 if log_auth_error:
#                     logger.error(
#                         f"{self.__class__.__name__}._perform_request | Not authorized",
#                         extra=log_extra_content | {"status": str(response.status)},
#                     )
#                 raise AWSAuthException(
#                     f"{self.__class__.__name__}._perform_request | Not authorized."
#                 )
#             elif response.status not in required_statuses:
#                 try:
#                     data = await response.json()
#                 except Exception:
#                     data = await response.text()
#                 logger.warning(
#                     f"{self.__class__.__name__}._perform request | Wrong response code",
#                     extra=log_extra_content
#                     | {
#                         "response_status": str(response.status),
#                         "response_text": data,
#                     },
#                 )
#                 raise HandlerException(status_code=response.status, detail=data)
#             else:
#                 data = await response.json()

#         logger.debug(
#             f"{self.__class__.__name__}._perform request | response data",
#             extra=log_extra_content | {"data": data, "response_status": str(response.status)},
#         )
#         return data

#     async def _transport(
#         self,
#         method: str,
#         url: str,
#         **kwargs,
#     ) -> dict:
#         """Aggregations API Transport layer.
#         Execute _perform_request method and run retry on Auth error.
#         """
#         global AWS_API_AUTH_TOKEN

#         headers = kwargs.pop("headers", {})

#         request_params = {
#             "url": url,
#             "method": method,
#             "headers": headers,
#             **kwargs,
#         }

#         try:
#             resp = await self._perform_request(**request_params)
#         except AWSAuthException:
#             AWS_API_AUTH_TOKEN = None
#             resp = await self._perform_request(
#                 **(request_params | {"log_auth_error": True})  # type:ignore
#             )
#         except aiohttp.ClientError as e:
#             logger.error(
#                 f"{self.__class__.__name__}._transport | exception = {e}",
#                 extra={
#                     "url": url,
#                     "method": method,
#                     "headers": headers,
#                     "kwargs": kwargs,
#                     "error": str(e),
#                 },
#             )
#             raise AWSClientException(str(e))

#         return resp

#     def get_cache_header(self, request_data: dict):
#         request_json_data = json.dumps(request_data, sort_keys=True, default=str)
#         cache_header_data = hashlib.md5(request_json_data.encode()).hexdigest()
#         return {self.cache_header_name: cache_header_data}

#     # Statistic API
#     async def fetch_statistic(self, request_data: dict):
#         headers = self.get_cache_header(request_data=request_data)
#         url = urljoin(self.base_url, self.statistic_path)
#         response_data = await self._transport(
#             method="POST",
#             url=url,
#             headers=headers,
#             json=request_data,
#         )
#         return response_data

#     # Documents Search API
#     async def fetch_documents(self, request_data: dict):
#         headers = self.get_cache_header(request_data=request_data)
#         url = urljoin(self.base_url, self.matched_docs_path_stable)
#         response_data = await self._transport(
#             method="POST", url=url, headers=headers, json=request_data
#         )
#         return response_data

#     async def fetch_documents_latest(self, request_data: dict):
#         headers = self.get_cache_header(request_data=request_data)
#         url = urljoin(self.base_url, self.matched_docs_path_latest)
#         response_data = await self._transport(
#             method="POST", url=url, headers=headers, json=request_data
#         )
#         return response_data

#     # Matched docs export
#     async def export_documents(self, request_data: dict):
#         url = urljoin(self.base_url, self.matched_docs_export_path)
#         response_data = await self._transport(method="POST", url=url, json=request_data)
#         return response_data

#     # Notification Scheduler
#     # todo: cleanup
#     async def fetch_notification_rules_for_customer(
#         self,
#         customer_id: str,
#     ) -> list[dict]:
#         notification_scheduler_base_url = urljoin(self.base_url, self.notification_scheduler_path)
#         url = urljoin(notification_scheduler_base_url, "search_rules")
#         params = {"customer_id": customer_id}
#         response_data = await self._transport(method="GET", url=url, params=params)
#         return response_data["values"]

#     async def create_notification_rule(self, request_data: dict) -> dict:
#         notification_scheduler_base_url = urljoin(self.base_url, self.notification_scheduler_path)
#         url = urljoin(notification_scheduler_base_url, "rule")
#         response_data = await self._transport(method="POST", url=url, json=request_data)
#         return response_data

#     async def update_notification_rule(self, rule_id: str, request_data: dict) -> dict:
#         notification_scheduler_base_url = urljoin(self.base_url, self.notification_scheduler_path)
#         url = urljoin(notification_scheduler_base_url, f"rule/{rule_id}")
#         response_data = await self._transport(method="PUT", url=url, json=request_data)
#         return response_data

#     async def delete_notification_rule(self, rule_id: str) -> None:
#         notification_scheduler_base_url = urljoin(self.base_url, self.notification_scheduler_path)
#         url = urljoin(notification_scheduler_base_url, f"rule/{rule_id}")
#         await self._transport(method="DELETE", url=url)
#         return

#     async def sync_notification_rules(self, request_data: dict) -> dict:
#         notification_scheduler_base_url = urljoin(self.base_url, self.notification_scheduler_path)
#         url = urljoin(notification_scheduler_base_url, "rules")
#         response_data = await self._transport(method="POST", url=url, json=request_data)
#         return response_data

#     # Some Retriver Admin

#     async def get_retriever_admin_customer(self, customer_id: Union[str, int]) -> Optional[dict]:
#         retriever_admin_path_base_url = urljoin(self.base_url, self.retriever_admin_path)
#         url = urljoin(retriever_admin_path_base_url, f"customer/{customer_id}")
#         response_data = await self._transport(
#             method="GET", url=url, required_statuses=[status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#         )
#         return response_data

#     async def get_retriever_admin_customer_accounts(self, customer_id: Union[str, int]):
#         """Get customer accounts from retriever database through retriever-admin service
#         based on AWS side.
#         """
#         retriever_admin_path_base_url = urljoin(self.base_url, self.retriever_admin_path)
#         url = urljoin(retriever_admin_path_base_url, f"customer/{customer_id}/accounts")
#         # create cache header based on customer_id
#         response_data = await self._transport(method="GET", url=url)
#         return response_data
