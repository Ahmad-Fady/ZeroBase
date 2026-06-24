from django import forms
import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import InternshipOffer

class InternshipFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    company_name = django_filters.CharFilter(lookup_expr='icontains', label='Company Name')

    class Meta:
        model = InternshipOffer
        fields = ['city', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.layout = Layout(
            Row(
                Column('title', css_class='small form-group col-6'),
                Column('company_name', css_class='small form-group col-6'),
                css_class='row gx-2 gy-2',
            ),
            Row(
                Column('city', css_class='small form-group col-6'),
                Column('location', css_class='small form-class col-6'),
                css_class='row gx-2 gy-2',
            ),
            Row('description', css_class='small'),
            Submit('submit', 'Filter Results', css_class='btn btn-primary mt-3')
        )
