from django.db import models

# Create your models here.
class Stock(models.Model):
    scriptid = models.CharField(max_length=100, null=False, blank=False, unique=True)
    exchange = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ['scriptid']

    def __str__(self):
        return self.scriptid


class Stock_price(models.Model):
    stock = models.ForeignKey(Stock, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField()
    closing_price = models.DecimalField('Closing Price', max_digits=16, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = (("stock", "date"),)

    def __str__(self):
        return (self.stock.scriptid + '-' + str(self.date))
