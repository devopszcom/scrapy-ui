from django.contrib import admin
from . import models


@admin.register(models.CrawlerNode)
class CrawlerNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'host', 'port')
