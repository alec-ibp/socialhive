from __future__ import annotations

from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, status_code, exc):
        super().__init__(detail, status_code)
        self.detail = detail
        self.status_code = status_code


def custom_exception_handler(exc, context) -> Response | None:
    if isinstance(exc, ValidationError):
        exc = BaseCustomException(detail=exc.detail, status_code=exc.status_code, exc=exc)
    
    if isinstance(exc.detail,list):
        error_code: str = exc.default_detail
    else:
        error_code: str = getattr(exc.detail, "code", "api_error")
    error_message: str = str(exc.detail)
    data: dict = {"error_code": error_code, "error_message": error_message}
    return Response(data, status=exc.status_code)