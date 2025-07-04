# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import Niche
from .forms import NicheForm

# Handles user registration
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")  # After sign up, go to login
    template_name = "core/signup.html"

# Home page that shows niche form and saved niches
@login_required
def home(request):
    if request.method == 'POST':
        form = NicheForm(request.POST)
        if form.is_valid():
            niche = form.save(commit=False)
            niche.user = request.user
            niche.save()
            return redirect('home')
    else:
        form = NicheForm()

    niches = Niche.objects.filter(user=request.user)
    return render(request, "core/home.html", {'form': form, 'niches': niches})
