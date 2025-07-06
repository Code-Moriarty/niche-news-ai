# config/urls.py

"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin site
    path('admin/', admin.site.urls),

    # Include Django's built-in authentication URLs (for login, logout, password reset, etc.)
    # These URLs are typically prefixed with 'accounts/'
    path('accounts/', include('django.contrib.auth.urls')),

    # Include your core app's URLs at the root of the project
    # This means URLs defined in 'core.urls' will be accessible directly (e.g., /home/, /niche/<pk>/)
    path('', include('core.urls')),
]

