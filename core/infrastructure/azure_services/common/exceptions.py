class AWSClientException(Exception):
    """Base class for Statistic Exceptions."""


class AWSAuthException(AWSClientException):
    """Exception related to authentication errors."""
