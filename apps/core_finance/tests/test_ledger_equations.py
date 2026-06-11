import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.iam.models import EnterpriseUser, JobTitle
from apps.core_finance.models import Account, AccountType, JournalEntry, LedgerLine


@pytest.mark.django_db
class TestFinancialLedgerEngine:

    def test_double_entry_imbalance_blocker(self) -> None:
        """Verifies that the balancing validation engine intercepts asynchronous entry streams."""
        user = EnterpriseUser.objects.create_user(
            username="finance_officer", job_title=JobTitle.FINANCE_MGR
        )

        cash = Account.objects.create(
            code="1010", name="Corporate Cash", type=AccountType.ASSET
        )
        equity = Account.objects.create(
            code="3010", name="Share Capital", type=AccountType.EQUITY
        )

        # Initialize an isolated journal shell context
        entry = JournalEntry.objects.create(
            description="Initial Funding Venture", posted_by=user
        )

        # Add an unbalanced line (Debit only)
        LedgerLine.objects.create(
            journal_entry=entry, account=cash, debit=Decimal("50000.0000")
        )

        # Attempting to finalize this entry must throw an explicit structural ValidationError
        with pytest.raises(ValidationError):
            entry.post_to_ledger()

        # Add the balancing transaction line item to resolve the validation check
        LedgerLine.objects.create(
            journal_entry=entry, account=equity, credit=Decimal("50000.0000")
        )

        # The ledger validation check should now pass cleanly
        entry.post_to_ledger()
        assert entry.is_posted is True
