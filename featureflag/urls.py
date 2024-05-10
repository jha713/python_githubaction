from django.urls import path
from . import views

urlpatterns = [
    path('event_receiver/', views.event_receiver, name='event_receiver'),
    path('stop_continuous_polling/', views.stop_continuous_polling, name='stop_continuous_polling'),
]
