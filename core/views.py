# core/views.py

from django.contrib import messages # <-- Already here, good!
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import Niche, GeneratedNewsletter
from .forms import NicheForm
from . import ai_service

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "core/signup.html"

@login_required
def home(request):
    if request.method == 'POST':
        form = NicheForm(request.POST)
        if form.is_valid():
            niche = form.save(commit=False)
            niche.user = request.user
            niche.save()
            messages.success(request, f"Niche '{niche.name}' added successfully!") # <-- Added success message
            return redirect('home')
        else:
            messages.error(request, "Failed to add niche. Please correct the errors below.") # <-- Added error message
            # If the form is invalid, it will re-render with errors
            # The message adds extra feedback.
    else:
        form = NicheForm()

    niches = Niche.objects.filter(user=request.user)
    return render(request, "core/home.html", {'form': form, 'niches': niches})

@login_required
def niche_detail(request, pk):
    niche = get_object_or_404(Niche, pk=pk, user=request.user)

    if request.method == 'POST':
        # Assuming ai_service.generate_newsletter_content takes niche.name directly
        content = ai_service.generate_newsletter_content(niche.name)
        if not content.startswith("Error:"):
            GeneratedNewsletter.objects.create(niche=niche, content=content)
            messages.success(request, f"Newsletter for '{niche.name}' successfully generated!") # <-- Added success message
        else:
            messages.error(request, f"Failed to generate newsletter: {content}") # <-- Added error message
        return redirect('niche_detail', pk=niche.pk) # Redirect to the same page to show message and new newsletter

    newsletters = niche.newsletters.all()
    return render(request, 'core/niche_detail.html', {'niche': niche, 'newsletters': newsletters})

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'core/landing.html')


