from django.urls import path
from apps.iam.views import IAMDashboardView

app_name = "iam"

urlpatterns = [
    path("", IAMDashboardView.as_view(), name="dashboard"),
]
