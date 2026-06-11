import uuid
from decimal import Decimal
from typing import Any
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.iam.models import EnterpriseUser


class AccountType(models.TextChoices):
    ASSET = "ASSET", "Asset (Debit Balance)"
    LIABILITY = "LIABILITY", "Liability (Credit Balance)"
    EQUITY = "EQUITY", "Equity (Credit Balance)"
    REVENUE = "REVENUE", "Revenue (Credit Balance)"
    EXPENSE = "EXPENSE", "Expense (Debit Balance)"


class Account(models.Model):
    """A financial account ledger track within the operational corporate framework."""

    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    code: models.CharField = models.CharField(max_length=20, unique=True, db_index=True)
    name: models.CharField = models.CharField(max_length=100)
    type: models.CharField = models.CharField(
        max_length=20, choices=AccountType.choices
    )

    def __str__(self) -> str:
        return f"{self.code} - {self.name} ({self.type})"


class JournalEntry(models.Model):
    """An atomic transaction context bundling multiple distinct entry lines."""

    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    timestamp: models.DateTimeField = models.DateTimeField(
        default=timezone.now, db_index=True
    )
    description: models.TextField = models.TextField()
    posted_by: models.ForeignKey = models.ForeignKey(
        EnterpriseUser, on_delete=models.PROTECT
    )
    is_posted: models.BooleanField = models.BooleanField(default=False)

    lines: models.Manager["LedgerLine"]

    class Meta:
        verbose_name_plural = "Journal Entries"

    def clean(self) -> None:
        """Enforces balanced double-entry accounting in the base currency (USD)."""
        if self.pk:
            lines_queryset = self.lines.all()
            if lines_queryset.exists():
                total_debits = sum(line.debit_base for line in lines_queryset)
                total_credits = sum(line.credit_base for line in lines_queryset)

                if abs(total_debits - total_credits) > Decimal("0.0001"):
                    raise ValidationError(
                        f"Imbalanced Base Equation: Base Debits ({total_debits}) must match Base Credits ({total_credits})."
                    )

    def post_to_ledger(self) -> None:
        """Locks the entry state atomically to prevent retroactive data tampering."""
        if self.is_posted:
            raise ValidationError("This Journal Entry has already been finalized.")

        with transaction.atomic():
            self.clean()
            self.is_posted = True
            self.save()


class LedgerLine(models.Model):
    """A distinct credit or debit allocation line with original and base values."""

    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    journal_entry: models.ForeignKey = models.ForeignKey(
        JournalEntry, on_delete=models.CASCADE, related_name="lines"
    )
    account: models.ForeignKey = models.ForeignKey(Account, on_delete=models.PROTECT)

    currency: models.CharField = models.CharField(max_length=3, default="USD")
    exchange_rate: models.DecimalField = models.DecimalField(
        max_digits=12, decimal_places=6, default=Decimal("1.000000")
    )

    debit: models.DecimalField = models.DecimalField(
        max_digits=18, decimal_places=4, default=Decimal("0.0000")
    )
    credit: models.DecimalField = models.DecimalField(
        max_digits=18, decimal_places=4, default=Decimal("0.0000")
    )

    debit_base: models.DecimalField = models.DecimalField(
        max_digits=18, decimal_places=4, default=Decimal("0.0000")
    )
    credit_base: models.DecimalField = models.DecimalField(
        max_digits=18, decimal_places=4, default=Decimal("0.0000")
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Automatically calculates values in the base currency using strict decimal math."""
        self.debit_base = (self.debit * self.exchange_rate).quantize(Decimal("0.0001"))
        self.credit_base = (self.credit * self.exchange_rate).quantize(
            Decimal("0.0001")
        )
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.debit < 0 or self.credit < 0:
            raise ValidationError(
                "Financial transaction values cannot be negative numbers."
            )
        if self.debit > 0 and self.credit > 0:
            raise ValidationError(
                "A single line cannot allocate both Debit and Credit splits."
            )
        if self.debit == 0 and self.credit == 0:
            raise ValidationError(
                "Transaction lines must contain a monetary value specification."
            )
        if self.exchange_rate <= 0:
            raise ValidationError("Exchange rates must be positive numbers.")


class Customer(models.Model):
    """Enterprise client profile linked to accounts receivable tracking fields."""

    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    company_name: models.CharField = models.CharField(max_length=150, unique=True)
    billing_email: models.EmailField = models.EmailField()

    receivable_account: models.ForeignKey = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        limit_choices_to={"type": AccountType.ASSET},
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.company_name


class Invoice(models.Model):
    """Billing record tracking customer balances across original transaction currencies."""

    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    invoice_number: models.CharField = models.CharField(
        max_length=50, unique=True, db_index=True
    )

    customer: models.ForeignKey = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="invoices",
        null=True,
        blank=True,
    )
    date_issued: models.DateField = models.DateField(default=timezone.now)
    currency: models.CharField = models.CharField(max_length=3, default="USD")
    exchange_rate: models.DecimalField = models.DecimalField(
        max_digits=12, decimal_places=6, default=Decimal("1.000000")
    )
    is_sent: models.BooleanField = models.BooleanField(default=False)

    lines: models.Manager["InvoiceLine"]

    def __str__(self) -> str:

        comp_name = self.customer.company_name if self.customer else "UNASSIGNED"
        return f"INV-{self.invoice_number} // {comp_name}"

    @property
    def total_amount(self) -> Decimal:
        """Calculates total invoice volume in the original currency choice."""
        return Decimal(sum(line.total_price for line in self.lines.all()))

    @property
    def total_amount_base(self) -> Decimal:
        """Calculates total invoice volume normalized to USD base parameters."""
        return (self.total_amount * self.exchange_rate).quantize(Decimal("0.0001"))


class InvoiceLine(models.Model):
    """Granular billing row detailing individual goods or service items."""

    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    invoice: models.ForeignKey = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="lines", null=True, blank=True
    )
    description: models.CharField = models.CharField(max_length=255)
    quantity: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("1.00")
    )
    unit_price: models.DecimalField = models.DecimalField(
        max_digits=14, decimal_places=4, default=Decimal("0.0000")
    )

    @property
    def total_price(self) -> Decimal:
        return (self.quantity * self.unit_price).quantize(Decimal("0.0001"))
