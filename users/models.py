import os
import time

from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.conf import settings


class CustomUser(AbstractUser):
    is_premium = models.BooleanField(default=False)
    auth0_id = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.pk} {self.username} {self.auth0_id}"


class AnonymousFiles(models.Model):
    text = models.TextField()
    audiofile = models.FileField(upload_to='audio_files', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.audiofile}"


@receiver(post_delete, sender=AnonymousFiles)
def delete_audiofile(sender, instance, **kwargs):
    if instance.audiofile:
        os.remove(instance.audiofile.path)


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
