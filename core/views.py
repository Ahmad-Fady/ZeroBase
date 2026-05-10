from django.views.generic import CreateView, ListView, DetailView
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
    template_name = "core/index.html"
    ordering = ['offer_creation_date'] 
    # This handles the "10 per page" logic automatically
    paginate_by = 10

