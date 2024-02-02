from django.conf import settings
from django.db import models


class AudioFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    text_file = models.FileField(upload_to='text_files', blank=True, null=True)
    filename = models.CharField(max_length=124, blank=True, null=True)
    audio_file = models.FileField(upload_to='audio_files', blank=True, null=True)
    audio_filename = models.CharField(max_length=124, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} > {self.user.username} > {self.filename}"