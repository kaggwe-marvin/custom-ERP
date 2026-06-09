from typing import Any
from django.views.generic import TemplateView
from apps.iam.models import Document, EnterpriseUser, JobTitle


class IAMDashboardView(TemplateView):
    template_name = "iam/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Read persona selection from GET parameters to switch identities dynamically
        selected_role = self.request.GET.get("simulate_role", JobTitle.FINANCE_MGR)
        selected_region = self.request.GET.get("simulate_region", "EU")

        # Fallback safeguard against unsanitized arguments
        if selected_role not in JobTitle.values:
            selected_role = JobTitle.FINANCE_MGR

        # 1. Instantiate current identity based on UI controls
        active_user = EnterpriseUser(
            username=f"simulated_{selected_role.lower()}",
            first_name="Simulation",
            last_name="Persona",
            job_title=selected_role,
            department="Operations Cluster",
            region=selected_region,
        )
        active_user.initials = "SP"  # type: ignore

        # 2. Base structural references
        us_sales_rep = EnterpriseUser(username="sales_us", region="US")
        hq_cfo = EnterpriseUser(username="cfo_global", region="Global")

        # 3. Security protected document corpus
        sample_documents = [
            Document(
                title="Q2 European Tax Provisioning",
                classification="CONFIDENTIAL",
                owner=hq_cfo,
                target_region="EU",
            ),
            Document(
                title="US Market Pipeline Strategy",
                classification="CRITICAL",
                owner=us_sales_rep,
                target_region="US",
            ),
            Document(
                title="Global Restructuring Ledger",
                classification="CRITICAL",
                owner=hq_cfo,
                target_region="Global",
            ),
        ]

        # 4. Evaluate access rules dynamically
        dataset = []
        for doc in sample_documents:
            # Grant simulated viewing privileges to match baseline capabilities
            if not f"document.view" in active_user.ROLE_CAPABILITIES.get(
                active_user.job_title, []
            ):
                active_user.ROLE_CAPABILITIES.setdefault(
                    active_user.job_title, []
                ).append("document.view")

            dataset.append(
                {"document": doc, "has_access": doc.permits_user(active_user, "view")}
            )

        context["user"] = active_user
        context["dataset"] = dataset
        context["available_roles"] = JobTitle.choices
        return context
