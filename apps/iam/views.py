from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.iam.models import Document, EnterpriseUser, JobTitle
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


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


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.iam.models import EnterpriseUser, JobTitle


class EnterpriseUserCreationForm(UserCreationForm):
    """Custom instantiation form injecting corporate classification markers."""

    class Meta(UserCreationForm.Meta):
        model = EnterpriseUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "job_title",
            "department",
            "region",
        )


class EnterpriseSignUpView(CreateView):
    """Transactional creation point for onboarding operational user profiles."""

    model = EnterpriseUser
    form_class = EnterpriseUserCreationForm
    template_name = "iam/signup.html"
    success_url = reverse_lazy("apps_iam:login")

    def form_valid(self, form: Any) -> Any:
        # Enforce normal workspace standard privileges by default
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return super().form_valid(form)
