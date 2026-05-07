from django.db import models
from accounts.models import Company, City, Location
# from django.core.exceptions import ValidationError


class InternshipOffer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    contact_info = models.TextField(max_length=1024)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
