from django.shortcuts import render

from .models import *

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
