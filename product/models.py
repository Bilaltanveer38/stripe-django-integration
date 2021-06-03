from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    url = models.URLField(default='https://google.com')

    def __str__(self):
        return self.name

    def get_price(self):
        return self.price/100