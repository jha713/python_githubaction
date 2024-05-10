from django.urls import path
from . import views

urlpatterns = [
    path('getFeatureFlagValue/', views.get_feature_flag_value, name='feature_flag'),
    # Add other URL patterns here
]
