from django.apps import AppConfig


class IamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.iam"
    # This label maps the relational database identifier strings back to the apps_iam space
    label = "apps_iam"
