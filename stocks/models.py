from django.db import models

# Create your models here.
class Stock(models.Model):
    scriptid = models.CharField(max_length=100, null=False, blank=False, unique=True)
    exchange = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.scriptid