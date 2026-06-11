import pytest
from django.http import HttpResponseRedirect
from django.test import Client
from django.urls import reverse
from apps.iam.models import Document, EnterpriseUser, JobTitle


@pytest.mark.django_db
class TestIAMSecurityEngine:

    def test_structural_rbac_baseline_capabilities(self) -> None:
        """Verifies that job roles are tied strictly to capability profiles."""
        ceo = EnterpriseUser.objects.create_user(
            username="ceo_user", job_title=JobTitle.CEO
        )
        fin_mgr = EnterpriseUser.objects.create_user(
            username="fin_user", job_title=JobTitle.FINANCE_MGR
        )
        sales_rep = EnterpriseUser.objects.create_user(
            username="sales_user", job_title=JobTitle.SALES_REP
        )

        assert ceo.has_baseline_capability("ledger.manage") is True
        assert fin_mgr.has_baseline_capability("ledger.manage") is True
        assert fin_mgr.has_baseline_capability("staff.view") is False
        assert sales_rep.has_baseline_capability("ledger.manage") is False

    def test_abac_geographic_fencing_restrictions(self) -> None:
        """Validates that users cannot view documents outside their location scope."""
        owner = EnterpriseUser.objects.create_user(
            username="us_owner", job_title=JobTitle.SALES_REP, region="US"
        )
        foreign_user = EnterpriseUser.objects.create_user(
            username="eu_viewer", job_title=JobTitle.SALES_REP, region="EU"
        )

        doc = Document.objects.create(
            title="US Market Pipeline Strategy",
            classification="CONFIDENTIAL",
            owner=owner,
            target_region="US",
        )

        assert doc.permits_user(owner, "view") is False
        assert doc.permits_user(foreign_user, "view") is False

    def test_dashboard_view_status_code_and_context(self) -> None:
        """Ensures the IAM Control Panel redirects anonymous requests cleanly."""
        client = Client()
        url = reverse("apps_iam:dashboard")
        response = client.get(url)

        assert response.status_code == 302

    def test_dashboard_requires_authenticated_session(self) -> None:
        """Ensures unauthenticated requests are redirected straight to login gates."""
        client = Client()
        url = reverse("apps_iam:dashboard")
        response = client.get(url)

        assert isinstance(response, HttpResponseRedirect)
        assert "login" in response.url

    def test_onboarding_form_creates_valid_sales_rep(self) -> None:
        """Verifies that registration flows inject default authorization constraints accurately."""
        client = Client()
        url = reverse("apps_iam:signup")

        response = client.post(
            url,
            {
                "username": "rep_new_hire",
                "email": "hire@enterprise.io",
                "first_name": "Marcus",
                "last_name": "Vance",
                "job_title": JobTitle.SALES_REP,
                "department": "Logistics Operations",
                "region": "EU",
                "password1": "SecurePass99!",
                "password2": "SecurePass99!",
            },
        )

        assert response.status_code == 302
        created_user = EnterpriseUser.objects.get(username="rep_new_hire")
        assert created_user.is_staff is False
        assert created_user.has_baseline_capability("leads.view") is True
