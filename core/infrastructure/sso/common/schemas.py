from typing import Optional

from pydantic import BaseModel, Field, validator


class RetrieverCustomerInfo(BaseModel):
    """Information About Customer, which user belongs to.
    As we don't require all info about company.

    Example:
    {
        "invoicePlace": {
            "name": "retno"
        },
        "companyName": "RelationDesk",
        "intercom": {
            "primaryContact": "supportnorge@retriever.no",
            "id": "123123",
            "type": "account"
        },
        "id": 20123123,
        "vismaId": null
    }
    """

    company_name: Optional[str] = Field(alias="companyName")
    id: Optional[int]

    class Config:
        allow_population_by_field_name = True


class RetrieverUserInfoAccountDetails(BaseModel):
    """Info about Retriever user account.

    Example:
    {
        "role": "admin",
        "id": 123123
    }
    """

    id: int
    role: Optional[str]


class RetrieverEmailLoginInfo(BaseModel):
    """Email login information.

    Example:
    {
        "description": "",
        "id": 123123,
        "email": "adminv@admin.com",
        "external_jwt": "igKqmMM_bCAYw5OElNd4B777QAsdvtDaPgJZL5jqpJBQFPyE"
    }
    """

    id: int
    email: str
    description: Optional[str]


class FullTimeZoneInfo(BaseModel):
    """Information about user's timezone.

    Example:
        {
            "momentData": "Europe/Oslo|+01:00 +02:00|-10 -20|
                0101010101010101010101010101010101010101010101010101010101010
                1010101010101010101010101010101010101010101010101010101010101
                0101|-2awM0 Qm0 W6o0 5pf0 WM0 1fA0 1cM0 1cM0 1cM0 1cM0 wJc0
                1fA0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1qM0 WM0
                zpc0 1a00 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1cM0 1cM0
                1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1cM0 1cM0
                1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1o00 11A0 1o00
                11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0
                1qM0 WM0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1qM0
                WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0
                1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0
                11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0
                1o00",
            "id": "Europe/Oslo"
        }
    """

    moment_data: Optional[str] = Field(alias="momentData")
    id: str

    class Config:
        allow_population_by_field_name = True


class RetrieverUserInfoResponse(BaseModel):
    """Data is a union of data from two services, because any service don't
    provide full required information.
    """

    country: Optional[str]
    access: Optional[dict]
    timezone: Optional[FullTimeZoneInfo]
    language: Optional[str]
    accountname: Optional[str]
    role: Optional[str] = Field(alias="accountRole")
    email_login: Optional[RetrieverEmailLoginInfo] = Field(alias="emailLogin")
    user_name: Optional[str] = Field(alias="userName", default="")
    listen_role: Optional[str]
    account: RetrieverUserInfoAccountDetails
    customer: RetrieverCustomerInfo

    class Config:
        allow_population_by_field_name = True


class EmailLoginSchema(BaseModel):
    """Information about User's Email Login account stored on Retriever SSO side."""
    email: str
    role: str
    uname: str


class CustomerAccountSchema(BaseModel):
    """Info about Customer Accounts on Retriever side"""
    email: Optional[str] = None
    username: str
    role: str
    language: str
    visible: Optional[bool]

    @validator("email")
    def normalize_email(cls, value):
        if isinstance(value, str):
            value.strip().lower()
        return value
