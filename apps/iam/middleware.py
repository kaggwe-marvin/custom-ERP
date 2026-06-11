from typing import Any, Callable
from django.http import HttpRequest, HttpResponse
from apps.iam.models import SecurityAuditEvent, EnterpriseUser


class EnterpriseAuditMiddleware:
    """Intercepts incoming processing requests to write security audit entries."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:

        response = self.get_response(request)

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR", "0.0.0.0")

        user = request.user
        actor_user = user if isinstance(user, EnterpriseUser) else None

        action_type = f"HTTP_{request.method}"
        if request.path.startswith("/admin/"):
            action_type = f"ADMIN_{request.method}"

        SecurityAuditEvent.objects.create(
            actor=actor_user,
            action_type=action_type,
            resource_path=request.path,
            ip_address=ip_address,
            status_code=response.status_code,
            metadata={
                "get_params": dict(request.GET.items()),
                "user_agent": request.META.get("HTTP_USER_AGENT", "Unknown"),
            },
        )

        return response
