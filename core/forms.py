from django import forms
from .models import InternshipOffer

class InternshipOfferForm(forms.ModelForm):
    class Meta:
        model = InternshipOffer
        fields = ("company", "title", "description", "date", "city", "location", "offer_end_date")


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data is None:
            return None

        city = cleaned_data.get('city')
        location = cleaned_data.get('location')

        if city and location:
            if location.city != city:
                self.add_error('location', "The location is not in this city")
        return cleaned_data
