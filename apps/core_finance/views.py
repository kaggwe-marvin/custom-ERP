from decimal import Decimal
from typing import Any, Dict, List
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from apps.core_finance.models import Account, AccountType, LedgerLine
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from apps.core_finance.models import Invoice


class FinancialReportDashboardView(LoginRequiredMixin, TemplateView):
    """Generates real-time financial dashboards with multi-currency tracking."""

    template_name = "core_finance/reports.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        accounts = Account.objects.all()
        trial_balance: List[Dict[str, Any]] = []

        total_debit_base = Decimal("0.0000")
        total_credit_base = Decimal("0.0000")

        assets: List[Dict[str, Any]] = []
        liabilities: List[Dict[str, Any]] = []
        equity: List[Dict[str, Any]] = []

        total_assets = Decimal("0.0000")
        total_liabilities = Decimal("0.0000")
        total_equity = Decimal("0.0000")

        for acct in accounts:

            lines = LedgerLine.objects.filter(
                account=acct, journal_entry__is_posted=True
            )

            if not lines.exists():
                continue

            currencies_involved = lines.values_list("currency", flat=True).distinct()

            for curr in currencies_involved:
                curr_lines = lines.filter(currency=curr)

                debits_orig = curr_lines.aggregate(Sum("debit"))[
                    "debit__sum"
                ] or Decimal("0.0000")
                credits_orig = curr_lines.aggregate(Sum("credit"))[
                    "credit__sum"
                ] or Decimal("0.0000")

                debits_base = curr_lines.aggregate(Sum("debit_base"))[
                    "debit_base__sum"
                ] or Decimal("0.0000")
                credits_base = curr_lines.aggregate(Sum("credit_base"))[
                    "credit_base__sum"
                ] or Decimal("0.0000")

                total_debit_base += debits_base
                total_credit_base += credits_base

                if acct.type == AccountType.ASSET:
                    net_asset = debits_base - credits_base
                    if net_asset > 0:
                        assets.append(
                            {
                                "name": acct.name,
                                "currency": curr,
                                "orig_bal": debits_orig - credits_orig,
                                "base_bal": net_asset,
                            }
                        )
                        total_assets += net_asset

                elif acct.type == AccountType.LIABILITY:
                    net_liab = credits_base - debits_base
                    if net_liab > 0:
                        liabilities.append(
                            {
                                "name": acct.name,
                                "currency": curr,
                                "orig_bal": credits_orig - debits_orig,
                                "base_bal": net_liab,
                            }
                        )
                        total_liabilities += net_liab

                elif acct.type == AccountType.EQUITY:
                    net_eq = credits_base - debits_base
                    if net_eq > 0:
                        equity.append(
                            {
                                "name": acct.name,
                                "currency": curr,
                                "orig_bal": credits_orig - debits_orig,
                                "base_bal": net_eq,
                            }
                        )
                        total_equity += net_eq

                trial_balance.append(
                    {
                        "code": acct.code,
                        "name": acct.name,
                        "currency": curr,
                        "debit_orig": debits_orig,
                        "credit_orig": credits_orig,
                        "debit_base": debits_base,
                        "credit_base": credits_base,
                    }
                )

        context.update(
            {
                "trial_balance": trial_balance,
                "total_debit_base": total_debit_base,
                "total_credit_base": total_credit_base,
                "assets": assets,
                "liabilities": liabilities,
                "equity": equity,
                "total_assets": total_assets,
                "total_liabilities": total_liabilities,
                "total_equity": total_equity,
                "total_liab_equity": total_liabilities + total_equity,
            }
        )
        return context


class PrintableInvoiceDetailView(LoginRequiredMixin, DetailView):
    """Generates standardized, cleanly printable HTML billing documents."""

    model = Invoice
    template_name = "core_finance/invoice_print.html"
    context_object_name = "invoice"

    def get_object(self, queryset: Any = None) -> Invoice:

        return get_object_or_404(
            Invoice, invoice_number=self.kwargs.get("invoice_number")
        )
