"""
adjust_challenge URL Configuration

"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('campaigns/',include('cpi.urls')),
    path('admin/', admin.site.urls),
]
