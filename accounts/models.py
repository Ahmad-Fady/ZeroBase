from django.db import models
from django.core.exceptions import ValidationError

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Address(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.location.name}, {self.city.name}"

    def clean(self):
        if self.location.city_id != self.city:
            raise ValidationError("Location does not belong to the selected city")


class User(models.Model):
    # user_id = models.CompositePrimaryKey()
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    account_creation_date = models.CharField(max_length=100)
    # One-to-One because a User usually has only one primary address
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

class Company(models.Model):
    company_id = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    website_url = models.CharField(max_length=100)
    market_share = models.CharField(max_length=100)
    created_at = models.CharField(max_length=100)
    account_creation_date = models.CharField(max_length=100)
    # Foreign Key because a company can have multiple office addresses
    addresses = models.ManyToManyField(Address, related_name="companies")
