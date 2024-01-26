"""
URL configuration for locallibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
]
# Used include() to add paths from the catalog applications


urlpatterns += [
    path('catalog/', include('catalog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# this is used to redirect the home url to the application

urlpatterns += [
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
]
# Django does not support static files such as JS and CSS but we can use this function to
# allow the static files to be accessed by the views


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
