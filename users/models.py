from django.db import models
from django.contrib.auth.models import AbstractUser


class UserData(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # WICHTIG: Passwort wird später gehasht gespeichert
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

