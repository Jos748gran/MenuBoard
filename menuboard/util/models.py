from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.user.username