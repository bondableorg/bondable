from enum import Enum


class UserRolesEnum(str, Enum):
    ADMIN = "admin"
    ANALYSIS = "analysis"
    EDITOR = "editor"
    USER = "user"
