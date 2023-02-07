from abc import ABC, abstractmethod


class BaseSSO(ABC):
    @abstractmethod
    def get_user_info(self, session_id: str):
        """Get external user info"""
