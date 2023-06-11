from __future__ import annotations

import traceback

from django.conf import settings
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, status_code):
        super().__init__(detail, status_code)
        self.detail = detail
        self.status_code = status_code


class DataValidationError(ValidationError):
    pass


def custom_exception_handler(exc, context) -> Response | None:
    if isinstance(exc, ValidationError):
        exc = BaseCustomException(detail=exc.detail, status_code=exc.status_code)
    elif isinstance(exc, AssertionError):
        exc = BaseCustomException(detail=str(exc), status_code=400)
    elif not hasattr(exc, "detail"):
        exc = BaseCustomException(detail=str(exc), status_code=400)

    if hasattr(exc, "detail"):
        error_code: str = getattr(exc.detail, "code", "api_error")
    elif isinstance(exc.detail, list):
        error_code: str = exc.default_detail

    if settings.DEBUG:
        traceback.print_exc()

    error_message: str = str(exc.detail)
    data: dict = {"error_code": error_code, "error_message": error_message}
    return Response(data, status=exc.status_code)
