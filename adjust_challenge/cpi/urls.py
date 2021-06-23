from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ADCampaignList

# API endpoints
urlpatterns = format_suffix_patterns([
    path('cpi/',
        ADCampaignList.as_view(),
        name='ad-campaign'),

])