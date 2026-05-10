# from django.shortcuts import render
from .admin import AddCompanyForm, AddStudentForm, User
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Create your views here.
class StudentSignUpView(CreateView):
    form_class = AddStudentForm
    success_url = reverse_lazy('login')
    template_name = "registration/student-signup.html"

class CompanySignUpView(CreateView):
    form_class = AddCompanyForm
    success_url = reverse_lazy('login')
    template_name = "registration/company-signup.html"

class CommonLoginView(CreateView):
    form_class = User
    success_url = reverse_lazy('login')
    template_name = "registration/login.html"

