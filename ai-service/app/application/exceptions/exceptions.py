class ApplicationError(Exception):
    """Base exception for application-level errors."""
    pass


class ConversationAccessDeniedError(ApplicationError):
    """Raised when a user tries to access another user's conversation."""
    pass