import pytest
from decimal import Decimal
from apps.core_finance.services import LiveCurrencyService
from apps.core_finance.models import Account, AccountType, JournalEntry, LedgerLine
from apps.iam.models import EnterpriseUser, JobTitle


class TestMultiCurrencyEngine:

    def test_live_currency_service_api_extraction(self) -> None:
        """Validates that the live service fetches valid rate mappings with fallbacks."""
        rates = LiveCurrencyService.get_usd_rates()
        assert "USD" in rates
        assert "EUR" in rates
        assert isinstance(rates["USD"], Decimal)
        assert rates["USD"] == Decimal("1.000000")

    @pytest.mark.django_db
    def test_multi_currency_ledger_line_auto_normalization(self) -> None:
        """Verifies that ledger items calculate values in the base currency automatically."""
        user = EnterpriseUser.objects.create_user(
            username="forex_rep", job_title=JobTitle.FINANCE_MGR
        )
        cash = Account.objects.create(
            code="1011", name="Euro Account Cash", type=AccountType.ASSET
        )
        equity = Account.objects.create(
            code="3011", name="Foreign Capital", type=AccountType.EQUITY
        )

        entry = JournalEntry.objects.create(
            description="European Investment Injection", posted_by=user
        )

        # Post an entry in EUR using an explicit static conversion factor (1 EUR = 1.08 USD)
        rate = Decimal("1.080000")
        line1 = LedgerLine.objects.create(
            journal_entry=entry,
            account=cash,
            currency="EUR",
            exchange_rate=rate,
            debit=Decimal("10000.0000"),
        )
        line2 = LedgerLine.objects.create(
            journal_entry=entry,
            account=equity,
            currency="EUR",
            exchange_rate=rate,
            credit=Decimal("10000.0000"),
        )

        # Confirm calculations match base currency parameters (10,000 * 1.08 = 10,800 USD)
        assert line1.debit_base == Decimal("10800.0000")
        assert line2.credit_base == Decimal("10800.0000")

        # Verify that the general entry balance check runs successfully
        entry.post_to_ledger()
        assert entry.is_posted is True
