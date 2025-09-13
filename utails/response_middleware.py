import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework.response import Response as DRFResponse


class ResponseFormattingMiddleware:
    EXCLUDED_PATHS = [
        "/admin",  # Django admin
        "/api/schema",  # drf-spectacular schema
        "/api/schema/swagger-ui",  # Swagger UI
        "/api/schema/redoc",  # Redoc
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path: str = request.path
        if any(path.startswith(p) for p in self.EXCLUDED_PATHS):
            return self.get_response(request)

        response = self.get_response(request)

        if isinstance(response, (JsonResponse, DRFResponse)):
            return self.format_response(response)

        return response

    def format_response(self, response):
        status_code = response.status_code
        succeeded = 200 <= status_code < 400

        data = getattr(response, "data", None)
        if data is None:
            try:
                data = json.loads(response.content.decode("utf-8"))
            except Exception:
                data = response.content.decode("utf-8")

        safe_data = self.make_safe(data)

        message = None
        if isinstance(safe_data, dict) and "message" in safe_data:
            message = safe_data.pop("message")
        if not message:
            message = "Success" if succeeded else "Error"

        formatted = {
            "statusCode": status_code,
            "meta": None,
            "succeeded": succeeded,
            "message": message,
            "errors": None if succeeded else safe_data,
            "data": safe_data if succeeded else None,
        }

        return JsonResponse(
            formatted, status=status_code, safe=False, encoder=DjangoJSONEncoder
        )

    def make_safe(self, obj):
        if isinstance(obj, dict):
            return {k: self.make_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.make_safe(v) for v in obj]
        elif hasattr(obj, "__dict__"):
            return str(obj)
        return obj
