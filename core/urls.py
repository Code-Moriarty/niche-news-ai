# core/urls.py
from django.urls import path
# from django.contrib.auth import views as auth_views # You can remove this import too
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),     # Public landing page for guests
    path("home/", views.home, name="home"),                # User dashboard with niches
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # Removed: path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    # Removed: path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("niche/<int:pk>/", views.niche_detail, name="niche_detail"),   # Detail and AI generate page
]



