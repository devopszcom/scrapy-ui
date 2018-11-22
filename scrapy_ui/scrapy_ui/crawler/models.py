from django.db import models


class CrawlerNode(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=6800)

    def __str__(self):
        return "{} - {}".format(self.id, self.name)
