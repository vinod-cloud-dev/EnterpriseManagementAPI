class DomainError(Exception):
    """A business-rule violation safe to expose through the API."""

    status_code = 400

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
