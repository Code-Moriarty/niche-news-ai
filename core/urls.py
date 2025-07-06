# core/urls.py
from django.urls import path
# from django.contrib.auth import views as auth_views # You can remove this import too
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),     # Public landing page for guests
    path("home/", views.home, name="home"),                # User dashboard with niches
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("niche/<int:pk>/", views.niche_detail, name="niche_detail"),   # Detail and AI generate page
    path('profile/', views.profile_view, name='profile'),
    path('niche/<int:pk>/delete/', views.delete_niche, name='delete_niche'),
]



