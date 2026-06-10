from django.contrib.auth import views as auth_views
from django.urls import path
from apps.iam.views import IAMDashboardView, EnterpriseSignUpView

app_name = "apps_iam"

urlpatterns = [
    path("", IAMDashboardView.as_view(), name="dashboard"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="iam/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", EnterpriseSignUpView.as_view(), name="signup"),
]
