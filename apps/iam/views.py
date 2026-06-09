from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.iam.models import Document, EnterpriseUser, JobTitle


class IAMDashboardView(LoginRequiredMixin, TemplateView):
    """The enterprise access control view requiring real database session tokens."""

    template_name = "iam/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        active_user = self.request.user

        # Explicit type guard ensuring compliance with strict type rules
        assert isinstance(active_user, EnterpriseUser)

        # Safe programmatic extraction of name characters for UI fallback avatars
        first = getattr(active_user, "first_name", "E")[:1]
        last = getattr(active_user, "last_name", "P")[:1]
        active_user.initials = f"{first}{last}".upper()  # type: ignore

        # Context-aware query filtering: Evaluate permissions dynamically across documents
        all_documents = Document.objects.select_related("owner").all()

        dataset = []
        for doc in all_documents:
            dataset.append(
                {"document": doc, "has_access": doc.permits_user(active_user, "view")}
            )

        context["user"] = active_user
        context["dataset"] = dataset
        context["available_roles"] = JobTitle.choices
        return context
