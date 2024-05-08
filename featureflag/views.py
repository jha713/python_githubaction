from django.shortcuts import render
from .models import FeatureFlag
import requests
import yaml
import json
import os

def index(request):
    # Retrieve all feature flags from the database
    feature_flags = FeatureFlag.objects.all()
    return render(request, 'index.html', {'feature_flags': feature_flags})
