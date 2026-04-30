from django.db import models
from django.core.exceptions import ValidationError

class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='locations')

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Address(models.Model):
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    location = models.ForeignKey('Location', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.location.name}, {self.city.name}"

    def clean(self):
        if self.location.city != self.city:
            raise ValidationError("Location does not belong to the selected city")


class User(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField()
    password = models.CharField(max_length=150)
    # One-to-One because a User usually has only one primary address
    address = models.OneToOneField(Address, on_delete=models.PROTECT)

class Company(models.Model):
    company_name = models.CharField(max_length=50)
    description = models.CharField(max_length=1024, blank=True, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=150)
    website_url = models.URLField()
    market_share = models.BigIntegerField()
    company_created_at = models.DateField()
    # Foreign Key because a company can have multiple office addresses
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    location = models.ForeignKey('Location', on_delete=models.PROTECT)
    addresses = models.ManyToManyField(Address, related_name="companies")
