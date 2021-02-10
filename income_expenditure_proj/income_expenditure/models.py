from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    paon = models.CharField(max_length=80)
    saon = models.CharField(max_length=80, blank=True, default='')
    street = models.CharField(max_length=80)
    town_city = models.CharField(max_length=80)
    county = models.CharField(max_length=80)
    postcode = models.CharField(max_length=8)

    def __str__(self):
        return f"Address: <{self.paon}{', ' + self.saon if self.saon != '' else None} {self.street}, {self.postcode}>"


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
