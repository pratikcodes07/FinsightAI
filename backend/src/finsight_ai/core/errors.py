from __future__ import annotations


class FinSightError(Exception):
    def __init__(self, message: str, code: str = "finsight_error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class NotFoundError(FinSightError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message=message, code="not_found")


class ValidationError(FinSightError):
    def __init__(self, message: str = "Invalid request") -> None:
        super().__init__(message=message, code="validation_error")
