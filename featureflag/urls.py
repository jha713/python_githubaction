from django.urls import path
from . import views

urlpatterns = [
    path('getFeatureFlagValue/', views.get_feature_flag_value, name='feature_flag'),
    path('userOperations/', views.user_operations, name='user_operations'),
    path('edit_delete_user/<int:user_id>/', views.edit_delete_user, name='edit_delete_user'),
    # Add other URL patterns here
]
