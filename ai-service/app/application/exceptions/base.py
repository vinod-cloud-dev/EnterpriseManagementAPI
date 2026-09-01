class ApplicationError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ConversationAccessDeniedError(ApplicationError):
    def __init__(self) -> None:
        super().__init__(
            message="You do not have access to this conversation",
            status_code=403,
        )