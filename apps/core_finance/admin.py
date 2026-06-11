from typing import Any
from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from apps.core_finance.models import Account, JournalEntry, LedgerLine


class LedgerLineFormSet(BaseInlineFormSet):
    """Enforces absolute double-entry balance alignment during browser interactions."""

    def clean(self) -> None:
        super().clean()
        total_debit = 0
        total_credit = 0
        active_lines = 0

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                total_debit += form.cleaned_data.get("debit", 0)
                total_credit += form.cleaned_data.get("credit", 0)
                active_lines += 1

        if active_lines > 0 and total_debit != total_credit:
            raise ValidationError(
                f"Imbalanced Ledger Entry: Total Debits ({total_debit}) must match Total Credits ({total_credit})."
            )


class LedgerLineInline(admin.TabularInline):
    """Nests tabular transaction splits directly inside the parent Journal view."""

    model = LedgerLine
    formset = LedgerLineFormSet
    extra = 2
    min_num = 2
    autocomplete_fields = ["account"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Tracks ledger account categorization parameters and identifiers."""

    list_display = ("code", "name", "type")
    list_filter = ("type",)
    search_fields = ("code", "name")


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    """Administration portal controlling automated transaction ledger posting processes."""

    list_display = ("timestamp", "description", "posted_by", "is_posted")
    list_filter = ("is_posted", "timestamp")
    search_fields = ("description", "posted_by__username")
    inlines = [LedgerLineInline]
    readonly_fields = ("is_posted",)
    actions = ["finalize_entries"]

    @admin.action(description="Finalize selected Journal Entries onto General Ledger")
    def finalize_entries(self, request: Any, queryset: Any) -> None:
        """Executes atomic ledger posting routines safely from the record table action dropdown."""
        success_count = 0
        for entry in queryset:
            try:
                entry.post_to_ledger()
                success_count += 1
            except ValidationError as error:
                self.message_user(
                    request, f"Error posting entry: {error.message}", level="ERROR"
                )

        if success_count > 0:
            self.message_user(
                request, f"Successfully finalized {success_count} ledger journal rows."
            )
