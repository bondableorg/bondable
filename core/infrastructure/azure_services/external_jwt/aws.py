# from typing import Optional

# import aiohttp

# from core.infrastructure.azure_services.external_jwt.common.base import ExternalJWT
# from core.infrastructure.azure_services.external_jwt.common.exceptions import AWSExternalJWTException
# from core.logging import logger


# class AWSExternalJWT(ExternalJWT):
#     """Client to retrieve JTW token from aws side."""

#     def __init__(
#         self,
#         url,
#         key,
#         secret,
#     ):
#         self.url = url
#         self.key = key
#         self.secret = secret

#     async def get_token(self, payload: Optional[dict] = None):
#         """Create JWT external_jwt to interact with Relation Desk API on AWS side.
#         This external_jwt will be used by Front-end Application, to retrieve data from
#         """
#         data = {
#             "key": self.key,
#             "secret": self.secret,
#             "payload": payload,
#         }

#         async with aiohttp.request("POST", url=self.url, json=data) as response:
#             try:
#                 if response.status != 200:
#                     raise AWSExternalJWTException(
#                         f"AWSExternalJWT | get_token | not valid response status | "
#                         f"response.status = {response.status}"
#                     )
#                 response_data = await response.json()
#                 token = response_data["access_token"]
#             except Exception as e:
#                 logger.error(
#                     f"AWSExternalJWT | get_token | exception occurred, original error = {e}"
#                 )
#                 raise AWSExternalJWTException(str(e))

#         return token
