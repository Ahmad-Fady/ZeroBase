from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Q
from django.shortcuts import render
from .models import *
from .forms import InternshipOfferForm

class OfferCreationView(CreateView):
    model = InternshipOffer
    form_class = InternshipOfferForm
    template_name = "core/create-offer.html"
    # success_url = "/success/"

class ListRecentOffers(ListView):
    """The home page."""
    model = InternshipOffer
    context_object_name = "offers"
    template_name = "core/internships.html"
    ordering = ['offer_creation_date'] 
    # This handles the "10 per page" logic automatically
    paginate_by = 10


def index(request):
    """The home page."""
    return render(request, "core/index.html")

def internships(request):
    """The home page."""
    return render(request, "core/internships.html")

def jobs(request):
    """The home page."""
    return render(request, "core/jobs.html")

def learn(request):
    """The home page."""
    return render(request, "core/learn.html")




from django_filters.views import FilterView
from .filters import InternshipFilter

class InternshipFilteredListView(FilterView):
    model = InternshipOffer
    template_name = 'core/search_results.html'
    filterset_class = InternshipFilter
    context_object_name = 'offers'


# select * from offers where 
"""
cairo ekoba
cairo almaadi
cairo madinet_nasr
"""
