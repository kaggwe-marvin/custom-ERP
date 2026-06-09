from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from apps.iam.models import Document, EnterpriseUser


@admin.register(EnterpriseUser)
class EnterpriseUserAdmin(UserAdmin):
    """Custom control panel tracking corporate roles and geographic data."""

    list_display = (
        "username",
        "email",
        "job_title",
        "department",
        "region",
        "is_staff",
    )
    list_filter = ("job_title", "region", "department", "is_staff")
    fieldsets = UserAdmin.fieldsets + (  # type: ignore
        (
            "Corporate Meta Identity",
            {"fields": ("job_title", "department", "region")},
        ),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin panel displaying object ownership and isolation rules."""

    list_display = (
        "title",
        "owner",
        "classification_badge",
        "target_region",
        "is_isolated_to_owner",
    )
    list_filter = ("classification", "target_region", "is_isolated_to_owner")
    search_fields = ("title", "owner__username")

    @admin.display(description="Sensitivity Rating")
    def classification_badge(self, obj: Document) -> str:
        """Renders styled labels inside row lists based on classification fields."""
        if obj.classification == "CRITICAL":
            return format_html(
                '<span style="background: #FFE4E6; color: #9F1239; px: 8px; border-radius: 4px; font-weight: bold;">CRITICAL</span>'
            )
        return format_html(
            '<span style="background: #FEF3C7; color: #92400E; px: 8px; border-radius: 4px;">CONFIDENTIAL</span>'
        )
