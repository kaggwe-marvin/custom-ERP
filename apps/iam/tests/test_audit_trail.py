import pytest
from django.test import Client
from django.urls import reverse
from apps.iam.models import SecurityAuditEvent, EnterpriseUser, JobTitle


@pytest.mark.django_db
class TestAuditTrailEngine:

    def test_middleware_automatically_logs_request(self) -> None:
        """Verifies that an unauthenticated page request triggers an audit record."""
        client = Client()
        url = reverse("apps_iam:dashboard")

        # Confirm the database log table is currently empty
        assert SecurityAuditEvent.objects.count() == 0

        # Requesting a protected path triggers a 302 redirect
        response = client.get(url)
        assert response.status_code == 302

        # Verify that an event was captured automatically by the middleware layer
        assert SecurityAuditEvent.objects.count() == 1
        event = SecurityAuditEvent.objects.first()
        assert event is not None
        assert event.action_type == "HTTP_GET"
        assert event.resource_path == url
        assert event.status_code == 302
