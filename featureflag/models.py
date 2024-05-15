from django.db import models

# Create your models here.

class FeatureFlag(models.Model):
    name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=False)

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=200)