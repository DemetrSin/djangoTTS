import os
from zipfile import ZipFile

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.custom_logger import Logger


class AudioFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    text_file = models.FileField(upload_to='text_files', blank=True, null=True)
    filename = models.CharField(max_length=124, blank=True, null=True)
    audiofile = models.FileField(upload_to='audio_files', blank=True, null=True)
    zipfile = models.FileField(upload_to='zip_files', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} > {self.user.username} > {self.filename}"

    @staticmethod
    def count_files(user):
        return AudioFile.objects.filter(user=user).count()


@receiver(pre_delete, sender=AudioFile)
def delete_files_on_audiofile_delete(sender, instance, **kwargs):
    try:
        if instance.text_file:
            os.remove(instance.text_file.path)
        if instance.audiofile:
            os.remove(instance.audiofile.path)
        if instance.zipfile:
            get_file_names_from_zip(instance.zipfile.path)
            os.remove(instance.zipfile.path)
    except Exception as e:
        Logger(level='error', msg=f'{e}').create_log()


class UserAction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=124, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


def get_file_names_from_zip(zipfile_path):
    with ZipFile(zipfile_path, 'r') as zipf:
        file_names = zipf.namelist()
        for file_name in file_names:
            os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
