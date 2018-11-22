from django.apps import AppConfig


class CrawlerConfig(AppConfig):
    name = 'scrapy_ui.crawler'
    verbose_name = "Crawler"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
