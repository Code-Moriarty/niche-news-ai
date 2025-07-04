from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy

from .models import Niche, GeneratedNewsletter
from .forms import NicheForm
from . import ai_service

from django.contrib.auth.forms import UserCreationForm

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
            return redirect('home')
    else:
        form = NicheForm()

    niches = Niche.objects.filter(user=request.user)
    return render(request, "core/home.html", {'form': form, 'niches': niches})


@login_required
def niche_detail(request, pk):
    niche = get_object_or_404(Niche, pk=pk, user=request.user)

    if request.method == 'POST':
        content = ai_service.generate_newsletter_content(niche.name)
        if not content.startswith("Error:"):
            GeneratedNewsletter.objects.create(niche=niche, content=content)
        return redirect('niche_detail', pk=niche.pk)

    newsletters = niche.newsletters.all()
    return render(request, 'core/niche_detail.html', {
        'niche': niche,
        'newsletters': newsletters
    })

