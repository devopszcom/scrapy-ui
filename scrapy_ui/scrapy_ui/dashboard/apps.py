from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'scrapy_ui.dashboard'
    verbose_name = "Dashboard"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
