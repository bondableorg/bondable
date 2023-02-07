from enum import Enum


class UserTypes(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    FACILITATOR = "facilitator"
    RESIDENT = "resident"
