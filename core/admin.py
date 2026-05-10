from django.contrib import admin
from .models import InternshipOffer
from .forms import InternshipOfferForm

# @admin.register(InternshipOffer)
class InternshipOfferAdmin(admin.ModelAdmin):
    form = InternshipOfferForm # This ensures the clean() method runs in Admin too!

# Register your models here.
admin.site.register(InternshipOffer, InternshipOfferAdmin)
