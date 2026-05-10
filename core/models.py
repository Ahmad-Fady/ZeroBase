from django.db import models
from django.utils import timezone
from datetime import timedelta

def one_month_hence():
    return timezone.now().date() + timedelta(days=30)


class InternshipOffer(models.Model):
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    # contact_info = models.TextField(max_length=1024)
    city = models.ForeignKey('accounts.City', on_delete=models.PROTECT)
    location = models.ForeignKey('accounts.Location', on_delete=models.CASCADE)
    offer_creation_date = models.DateField(auto_now_add=True)
    offer_end_date = models.DateField(default=one_month_hence())
