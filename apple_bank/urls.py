"""
URL configuration for apple_bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('secure-admin-portal/', admin.site.urls),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json')),
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/javascript')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', include('banking.urls')),
]


