from http import HTTPStatus
from typing import Any

from rest_framework.views import Response, exception_handler


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom API exception handler"""
    # Call Rest framework's default exception handler first
    # to get the standard error response

    response = exception_handler(exc, context)
    if response is not None:
        http_code_to_message = {v.value: v.description for v in HTTPStatus}
        response.data["message"] = http_code_to_message[response.status_code]
    return response
