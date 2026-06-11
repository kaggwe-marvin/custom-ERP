from django.urls import path
from apps.core_finance.views import FinancialReportDashboardView
from .views import PrintableInvoiceDetailView

app_name = "apps_finance"

urlpatterns = [
    path("reports/", FinancialReportDashboardView.as_view(), name="reports"),
    path(
        "invoice/<str:invoice_number>/print/",
        PrintableInvoiceDetailView.as_view(),
        name="invoice_print",
    ),
]
