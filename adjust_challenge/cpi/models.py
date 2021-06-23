from django.db import models
from rest_framework import serializers


class ADCampaigns(models.Model):
    date = models.DateField()
    channel = models.CharField(max_length=50)
    country = models.CharField(max_length=2)
    os = models.CharField(max_length=50)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    installs = models.IntegerField(default=0)
    spend = models.FloatField(default=0.0)
    revenue = models.FloatField(default=0.0)

    class Meta:
        ordering = ['date']


class ADCampSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADCampaigns
        fields = '__all__'
