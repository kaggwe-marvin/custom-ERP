import pytest
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

        # CEO has wildcard clearance
        assert ceo.has_baseline_capability("ledger.manage") is True
        # Finance manager can touch financials but not staff
        assert fin_mgr.has_baseline_capability("ledger.manage") is True
        assert fin_mgr.has_baseline_capability("staff.view") is False
        # Sales rep is locked out of accounting systems
        assert sales_rep.has_baseline_capability("ledger.manage") is False

    def test_abac_geographic_fencing_restrictions(self) -> None:
        """Validates that users cannot view documents outside their location scope."""
        owner = EnterpriseUser.objects.create_user(
            username="us_owner", job_title=JobTitle.SALES_REP, region="US"
        )
        foreign_user = EnterpriseUser.objects.create_user(
            username="eu_viewer", job_title=JobTitle.SALES_REP, region="EU"
        )

        # Mock baseline permission mappings manually for document scope
        for user in [owner, foreign_user]:
            user.ROLE_CAPABILITIES[JobTitle.SALES_REP].append("document.view")

        doc = Document.objects.create(
            title="US Market Pipeline Strategy",
            classification="CONFIDENTIAL",
            owner=owner,
            target_region="US",
        )

        # Owner has access, but the European rep gets intercepted by ABAC logic
        assert doc.permits_user(owner, "view") is True
        assert doc.permits_user(foreign_user, "view") is False

    def test_dashboard_view_status_code_and_context(self) -> None:
        """Ensures the IAM Control Panel renders cleanly with evaluation maps."""
        # Simple anonymous client test since view mocks session data
        from django.test import Client

        client = Client()
        url = reverse("apps_iam:dashboard")

        response = client.get(url)

        assert response.status_code == 200
        assert "user" in response.context
        assert "dataset" in response.context
