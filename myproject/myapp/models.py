from django.db import models

# Create your models here.
# myapp/models.py

from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
