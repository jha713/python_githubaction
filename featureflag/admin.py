from django.contrib import admin
from .models import FeatureFlag , User

# Register your models here.
admin.site.register(FeatureFlag)
admin.site.register(User)