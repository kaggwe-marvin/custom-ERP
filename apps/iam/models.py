from django.contrib.auth.models import AbstractUser
from django.db import models


class JobTitle(models.TextChoices):
    CEO = "CEO", "Chief Executive Officer"
    FINANCE_MGR = "FINANCE_MGR", "Finance Manager"
    HR_SPECIALIST = "HR_SPECIALIST", "HR Specialist"
    SALES_REP = "SALES_REP", "Sales Representative"


class EnterpriseUser(AbstractUser):
    job_title: models.CharField = models.CharField(
        max_length=50, choices=JobTitle.choices, default=JobTitle.SALES_REP
    )
    department: models.CharField = models.CharField(max_length=100, db_index=True)
    region: models.CharField = models.CharField(max_length=50, default="Global")

    ROLE_CAPABILITIES: dict[str, list[str]] = {
        JobTitle.CEO: ["*"],
        JobTitle.FINANCE_MGR: ["financials.view", "financials.create", "ledger.manage"],
        JobTitle.HR_SPECIALIST: ["staff.view", "staff.manage"],
        JobTitle.SALES_REP: ["leads.view", "leads.create", "opportunities.view"],
    }

    def has_baseline_capability(self, capability: str) -> bool:
        allowed = self.ROLE_CAPABILITIES.get(self.job_title, [])
        return "*" in allowed or capability in allowed


class Document(models.Model):
    title: models.CharField = models.CharField(max_length=255)
    classification: models.CharField = models.CharField(
        max_length=50, default="CONFIDENTIAL"
    )
    owner: models.ForeignKey = models.ForeignKey(
        EnterpriseUser, on_delete=models.CASCADE
    )
    target_region: models.CharField = models.CharField(max_length=50, default="Global")
    is_isolated_to_owner: models.BooleanField = models.BooleanField(default=False)

    def permits_user(self, user: EnterpriseUser, context_action: str) -> bool:
        if not user.has_baseline_capability(f"document.{context_action}"):
            return False
        if self.owner == user:
            return True
        if self.is_isolated_to_owner and self.owner != user:
            return False
        if (
            self.target_region != "Global"
            and user.region != self.target_region
            and user.job_title != JobTitle.CEO
        ):
            return False
        return True
