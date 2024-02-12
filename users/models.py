from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_premium = models.BooleanField(default=False)
    auth0_id = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.pk} {self.username} {self.auth0_id}"


class AnonymousFiles(models.Model):
    text = models.TextField()
    audiofile = models.FileField(upload_to='audio_files', blank=True, null=True)
