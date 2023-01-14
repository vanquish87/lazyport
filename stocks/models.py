from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    scriptid = models.CharField(max_length=100, null=False, blank=False, unique=True)
    exchange = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name