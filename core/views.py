# niche-news-ai/core/views.py

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST # NEW: Import this decorator
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView # NEW: Import for CustomLoginView (if used)


from .models import Niche, GeneratedNewsletter
from .forms import NicheForm
from . import ai_service

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "core/signup.html"

# NEW: Custom Login View (Assuming you are using this or a similar one for login)
# If you are using a different approach for login, you can remove this class.
class CustomLoginView(LoginView):
    template_name = 'registration/login.html' # Make sure this path points to your actual login template
    redirect_authenticated_user = True # Redirects logged-in users away from the login page

    def get_success_url(self):
        messages.success(self.request, "You have been successfully logged in!")
        return reverse_lazy('home') # Redirect to home page on successful login

@login_required
def home(request):
    if request.method == 'POST':
        form = NicheForm(request.POST)
        if form.is_valid():
            niche = form.save(commit=False)
            niche.user = request.user
            niche.save()
            messages.success(request, f"Niche '{niche.name}' added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Failed to add niche. Please correct the errors below.")
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
            messages.success(request, f"Newsletter for '{niche.name}' successfully generated!")
        else:
            messages.error(request, f"Failed to generate newsletter: {content}")
        return redirect('niche_detail', pk=niche.pk)

    newsletters = niche.newsletters.all()
    return render(request, 'core/niche_detail.html', {'niche': niche, 'newsletters': newsletters})

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'core/landing.html')

# --- Profile View ---
@login_required
def profile_view(request):
    """
    Renders the user profile page.
    """
    return render(request, 'core/profile.html')

# NEW: Delete Niche View (re-added)
@login_required
@require_POST # Ensure this view only accepts POST requests
def delete_niche(request, pk):
    niche = get_object_or_404(Niche, pk=pk, user=request.user) # Ensure user owns the niche
    niche_name = niche.name # Store name before deleting for the message
    niche.delete()
    messages.success(request, f"Niche '{niche_name}' and its newsletters have been successfully deleted.")
    return redirect('home')