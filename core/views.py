from django.shortcuts import render

from .models import *

def index(request):
    """The home page."""
    return render(request, "core/index.html")
